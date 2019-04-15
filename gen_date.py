from utils.MessageQueueCache import MessageQueueCache

from conf import ConfManagement
from utils.safe_linux import OSUtil

if __name__ == '__main__':
    confmessage = ConfManagement()
    data = confmessage.get_json()
    ms= MessageQueueCache()
    for item in data.get("spark-sql"):
        ms.put(item)
    for i in ms.q:
        path_gen_data = confmessage.get_ini("gen_data_scala")
        with open(path_gen_data, 'r') as f:
            lines = f.readlines()
        with open(path_gen_data, 'w') as f1:
            for line in lines:
                if "val scale = 2662" in line:
                    line = line.replace("val scale = 2662","val scale = %d"%i.get("datasize"))
                f1.write(line)

        path_hive_server = confmessage.get_ini("hive_server")
        with open(path_hive_server, 'r') as f:
            lines = f.readlines()
        with open(path_hive_server, 'w') as f1:
            for line in lines:
                if "offHeap.enabled=false" in line:
                    line = line.replace("offHeap.enabled=false",\
                                 "offHeap.enabled=%s"%i.get("offHeap-enabled"))
                if "cache.medium.type=AEP" in line:
                    line = line.replace("cache.medium.type=AEP",\
                                 "cache.medium.type=%s"%i.get("type"))
                f1.write(line)

        path_run_data_sh = confmessage.get_ini("run_gen_data_sh")
        with open(path_run_data_sh, 'r') as f:
            lines = f.readlines()
        with open(path_run_data_sh, 'w') as f1:
            for line in lines:
                if "offHeap.enabled=false" in line:
                    line = line.replace("offHeap.enabled=false",\
                                 "offHeap.enabled=%s"%i.get("offHeap-enabled"))
                f1.write(line)

        path_run_beeline_sh = confmessage.get_ini("run_beeline_sh")
        with open(path_run_beeline_sh, 'r') as f:
            lines = f.readlines()
        with open(path_run_beeline_sh, 'w') as f1:
            for line in lines:
                if "database_name = 'tpcds2662'" in line:
                    line = line.replace("database_name = 'tpcds2662'",\
                                 "database_name = 'tpcds%d'"%i.get("datasize"))
                f1.write(line)

        OSUtil.run_linux(path_run_data_sh)
        OSUtil.run_linux(path_hive_server)
        OSUtil.run_linux(path_run_beeline_sh)