from abc import ABCMeta
from influxdb import InfluxDBClient
from six import add_metaclass
from conf import ConfManagement


@add_metaclass(ABCMeta)
class InfluxdbOperation():
    def __init__(self):
        self.setting =ConfManagement("influxDB")
        self.client = InfluxDBClient(
            host=self.setting.get_ini('influx_host'),
            port=self.setting.get_ini('influx_port'),
            username=self.setting.get_ini("username"),
            password=self.setting.get_ini('password'),
        )
        self.dbname = self.setting.get_ini('influx_database')

    def state_forwards(self, app_label, state):
        pass

class CreateInfluxdbDatabase(InfluxdbOperation):
    reversible = True

    def database_forwards(self):
        self.client.create_database(self.dbname)

    def database_backwards(self, app_label, schema_editor, from_state, to_state):
        self.client.drop_database(self.dbname)

    def describe(self):
        return 'Create influxdb database {0}'.format(self.dbname)


class CreateInfluxdbRetentionPolicy(InfluxdbOperation):
    reversible = True

    def __init__(self, name, duration, replication, default=False):
        super(CreateInfluxdbRetentionPolicy, self).__init__()
        self.name = name
        self.duration = duration
        self.replication = replication
        self.default = default

    def database_forwards(self):
        self.client.create_retention_policy(
            name=self.name,
            duration=self.duration,
            replication=self.replication,
            database=self.dbname,
            default=self.default
        )

    def database_backwards(self, app_label, schema_editor, from_state, to_state):
        self.client.drop_retention_policy(
            name=self.name,
            database=self.dbname
        )

    def describe(self):
        return 'Create influxdb retention policy {0}.{1}'.format(self.dbname, self.name)


class CreateInfluxdbContinuousQuery(InfluxdbOperation):
    reversible = True

    def __init__(self, name, interval, src_policy, dst_policy, regex='.*'):
        super(CreateInfluxdbContinuousQuery, self).__init__()
        self.name = name
        self.interval = interval
        self.src_policy = src_policy
        self.dst_policy = dst_policy
        self.regex = regex

    def database_forwards(self, app_label, schema_editor, from_state, to_state):
        self.client.query(
            'CREATE CONTINUOUS QUERY {0.name} ON {0.dbname} '
            'BEGIN '
            'SELECT last(value) as value '
            'INTO "{0.dst_policy}".:MEASUREMENT '
            'FROM "{0.src_policy}"./{0.regex}/ '
            'GROUP BY time({0.interval}),* '
            'END'.format(self)
        )

    def database_backwards(self, app_label, schema_editor, from_state, to_state):
        self.client.query(
            'DROP CONTINUOUS QUERY {0}'.format(self.name)
        )

    def describe(self):
        return 'Create influxdb continuous query {0}.{1}'.format(self.dbname, self.name)


class CreatePreferenceData():
    reversible = True

    def __init__(self, name, value):
        from datetime import datetime
        self.name = name
        self.value = value
        self.create_time = datetime.now()
        self.modify_time = self.create_time

    def state_forwards(self, app_label, state):
        pass

    def database_forwards(self, app_label, schema_editor, from_state, to_state):
        schema_editor.execute("INSERT INTO cluster_preference (NAME,VALUE,CREATE_TIME,MODIFY_TIME) VALUES"
                              " ('{0}','{1}','{2}','{3}');".format(self.name, self.value, self.create_time,
                                                                   self.modify_time))

    def database_backwards(self, app_label, schema_editor, from_state, to_state):
        schema_editor.execute('DROP TABLE cluster_preference;')

    def describe(self):
        return "Creates  a Preference data: name is {}, value is {}.".format(self.name, self.value)
