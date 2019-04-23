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
