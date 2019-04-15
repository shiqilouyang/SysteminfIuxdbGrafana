from influxdb import InfluxDBClient
from conf import ConfManagement

def __build_influxdb_json(id, measurement, value):
    model_json = [
        {
            "measurement": measurement,
            "tags":{
                "id": id
            },
            "fields":{
                "value": value
            }
        }
    ]
    return model_json

def record_parse_result(measurement,job_id,result):
    if not result:
        return
    result = __build_influxdb_json(job_id, measurement, str(result))
    # [{'fields': {'value': '117391360'}, 'measurement': 'cpu', 'tags': {'id': 1}}]
    print(result)
    Influx_Conn().set(result)


class Influx_Conn():
    def __init__(self):
        self.setting = ConfManagement("influxDB")
        self._client = InfluxDBClient(
            host=self.setting.get_ini('influx_host'),
            port=self.setting.get_ini('influx_port'),
            username=self.setting.get_ini("username"),
            password=self.setting.get_ini('password'),
            database=self.setting.get_ini("database")
        )

    def get(self, sql, default=None, version=None, **kwargs):
        return self._client.query(sql, **kwargs)

    def set(self, json, default=None, version=None, **kwargs):
        return self._client.write_points(json, **kwargs)

    def delete_series(self, measurement=None, tags=None):
        return self._client.delete_series(measurement=measurement, tags=tags)
