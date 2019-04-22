listA = []
import re
def bylineread(fimename):
    with open(fimename) as f:
        line = f.readline()
        while line:
            yield line
            line = f.readline()

for i in bylineread('io_message'):
    list_w_r = re.findall(' \d+\.\d+ ', i)[1:]
    if len(list_w_r) !=0:
        listA.append(list_w_r)


print(listA)
'''
Linux 3.10.0-327.el7.x86_64 (sr585) 	2019年04月22日 	_x86_64_	(88 CPU)



Device:            tps    kB_read/s    kB_wrtn/s    kB_read    kB_wrtn

sda               1.59       310.44        77.66 2452475633  613554260

sdb               1.73       309.01        68.90 2441230765  544292872

sdc               1.76       302.18        69.03 2387286357  545344492

sdd               1.58       309.64        68.50 2446196097  541148548

sde               2.30         8.81        70.26   69613198  555024762

sdf               1.72       301.61        68.72 2382717901  542926216

dm-0              0.00         0.00         0.01       4179      44855
'''