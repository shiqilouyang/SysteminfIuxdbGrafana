import re
def bylineread(fimename):
    with open(fimename, 'r',encoding="utf-8") as f:
        line = f.readline()
        while line:
            yield line
            line = f.readline()


def get_w_r():
    list_r = list_w = []
    for i in bylineread('io_message.log'):
        list_w_r = re.findall(' \d+\.\d+ ', i)[1:]
        if len(list_w_r) != 0:
            list_r.append(float(list_w_r[0]))
            list_w.append(float(list_w_r[1]))
    return '%.2f'%(sum(list_r)/5), '%.2f'%(sum(list_w)/5)