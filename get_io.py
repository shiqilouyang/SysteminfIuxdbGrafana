import re
def bylineread(fimename):
    with open(fimename, 'r',encoding="utf-8") as f:
        line = f.readline()
        while line:
            yield line
            line = f.readline()


def get_w_r():
    list_w = []
    list_r = []
    for i in bylineread('io_message.log'):
        list_w_r = re.findall(' \d+\.\d+ ', i)[1:]
        if len(list_w_r) != 0:
            list_r.append(float(list_w_r[0]))
            list_w.append(float(list_w_r[1]))
    return '%.2f'%(sum(list_r)/5), '%.2f'%(sum(list_w)/5)



def get_AEP_Use():
    use_aep = []
    for i in bylineread('df-h.log'):
        if i.startswith("/dev/pmem"):
            use_aep.append(str(int(re.findall(' \d+', i)[1].strip())/1024) + "G") \
                if "M" in i \
                else use_aep.append(re.findall(' \d+', i)[1].strip() + "G")
    return float(use_aep[0][:-1]) + float(use_aep[1][:-1])