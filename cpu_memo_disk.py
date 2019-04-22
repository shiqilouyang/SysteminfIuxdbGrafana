import time
from abc import ABCMeta
from six import add_metaclass
import psutil
from get_io import get_w_r
from utils.safe_linux import OSUtil as os
from utils import record_parse_result
from utils.multipo_queque import Multipo_Queque
from utils.influx_used import CreateInfluxdbDatabase,CreateInfluxdbRetentionPolicy

@add_metaclass(ABCMeta)
class InfluxdbOperation(object):
    def __init__(self):
        self.q = Multipo_Queque()
        #self.ps = psutil.virtual_memory()
        self.queque = None
        self.list = list()
        self.measurement_cpu = "cpu"
        self.measurement_memory = "memory"
        self.measurement_io_read = "io_read"
        self.measurement_io_write = "io_write"
        self.measurement_io_wait = "io_wait"       
 
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
            # p1 = psutil.disk_io_counters()
            # p1_read_pre = p1.read_bytes/1024/1024
            # p1_write_end = p1.write_bytes/1024/1024
            # p1_read_time = p1.read_time/1000
            # p1_write_time = p1.write_time/1000
            # p2 = psutil.disk_io_counters()
            # p2_read_pre = p2.read_bytes/1024/1024
            # p2_write_end = p2.write_bytes/1024/1024
            # p2_read_time = p2.read_time/1000
            # p2_write_time = p2.write_time
            # if p2_read_time - p1_read_time == 0:
            #     io_read = 0
            # else:
            #     io_read = (p2_read_pre-p1_read_pre)/(p2_read_time-p1_read_time)
            # if p2_write_time-p1_write_time ==0:
            #     io_write=0
            # else:
            #     io_write = (p2_write_end-p1_write_end)/(p2_write_time-p1_write_time)

            os.run_linux("iostat -d 1 1 > io_message.log")
            io_read, io_write = get_w_r()
            self.num += 1
            (data, self.list, self.queque) = self.q.run('%.2f' % (psutil.cpu_times_percent(interval=None, percpu=False).user))
            record_parse_result(self.measurement_cpu, self.num, data)
            (data, self.list, self.queque) = self.q.run('%.2f'% (psutil.virtual_memory().used/1024/1024/1024))
            record_parse_result(self.measurement_memory, self.num, data)
            (data, self.list, self.queque) = self.q.run(io_read)
            record_parse_result(self.measurement_io_read, self.num, data)
            (data, self.list, self.queque) = self.q.run(io_write)
            record_parse_result(self.measurement_io_write, self.num, data)
            (data, self.list, self.queque) = self.q.run(
                '%.2f' % (psutil.cpu_times_percent(interval=None, percpu=False).iowait)
            )
            record_parse_result(self.measurement_io_wait, self.num, data)

if __name__ == '__main__':
    c = GetMessage()
    print(c.gen_message())
