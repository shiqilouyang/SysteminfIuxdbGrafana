import time
from abc import ABCMeta
from six import add_metaclass
import psutil
from utils import record_parse_result
from utils.multipo_queque import Multipo_Queque
from utils.influx_used import CreateInfluxdbDatabase,CreateInfluxdbRetentionPolicy


@add_metaclass(ABCMeta)
class InfluxdbOperation(object):
    def __init__(self):
        self.q = Multipo_Queque()
        self.ps = psutil.virtual_memory()
        self.queque = None
        self.list = list()
        self.measurement_cpu = "cpu"
        self.measurement_memory = "memory"
        self.measurement_io_read = "io_read"
        self.measurement_io_write = "io_write"

    def get_message(self, app_label, state):
        pass


class GetMessage(InfluxdbOperation):
    def __init__(self):
        super().__init__()
        self.database_operation = CreateInfluxdbDatabase()
        self.database_Policy = CreateInfluxdbRetentionPolicy(
            "2h-default", "2h", 1, True)
        self.num = 0

    def gen_message(self):
        self.database_operation.database_forwards()
        self.database_Policy.database_forwards()
        while True:
            time.sleep(1)
            self.num += 1
            (data, self.list, self.queque) = self.q.run(psutil.cpu_percent(0))
            record_parse_result(self.measurement_cpu, self.num, data)
            (data, self.list, self.queque) = self.q.run(self.ps.percent)
            record_parse_result(self.measurement_memory, self.num, data)

            (data, self.list, self.queque) = self.q.run(
                psutil.disk_io_counters().read_count
            )
            record_parse_result(self.measurement_io_read, self.num, data)
            (data, self.list, self.queque) = self.q.run(
                psutil.disk_io_counters().write_count
            )
            record_parse_result(self.measurement_io_write, self.num, data)


if __name__ == '__main__':
    c = GetMessage()
    print(c.gen_message())
