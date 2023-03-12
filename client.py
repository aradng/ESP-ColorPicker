from zeroconf import Zeroconf
from time import sleep
import requests
import numpy as np

zeroconf = Zeroconf()
lut = [0,    1,    2,    3,    4,    5,    7,    9,    12,
15,    18,    22,    27,    32,    38,    44,    51,    58,
67,    76,    86,    96,    108,    120,    134,    148,    163,
180,    197,    216,    235,    255]

lut = []
LightLevel = 0
base = 0.0039215
while (LightLevel < 255):
    lut.append(int(LightLevel))
    LightLevel = base**4.0
    base += 0.0039215

INPUT_SIZE = 255       # Input integer size
OUTPUT_SIZE = 255      # Output integer size
INT_TYPE = 'const unsigned char'
TABLE_NAME = 'cie';

def cie1931(L):
    L = L*103.0
    if L <= 8:
        return (L/903.3)
    else:
        return ((L+16.0)/119.0)**3

x = range(0,int(INPUT_SIZE+1))
y = [round(cie1931(float(L)/INPUT_SIZE)*OUTPUT_SIZE) for L in x]
lut = []
for i,L in enumerate(y):
    lut.append(int(L))

lut = [0,    0,    1,    1,    2,    2,    3,    3,    4,    4,    4,    5,    5,    6,    6,    7,
    7,    8,    8,    8,    9,    9,   10,   10,   11,   11,   12,   12,   13,   13,   14,   15,
   15,   16,   17,   17,   18,   19,   19,   20,   21,   22,   22,   23,   24,   25,   26,   27,
   28,   29,   30,   31,   32,   33,   34,   35,   36,   37,   38,   39,   40,   42,   43,   44,
   45,   47,   48,   50,   51,   52,   54,   55,   57,   58,   60,   61,   63,   65,   66,   68,
   70,   71,   73,   75,   77,   79,   81,   83,   84,   86,   88,   90,   93,   95,   97,   99,
  101,  103,  106,  108,  110,  113,  115,  118,  120,  123,  125,  128,  130,  133,  136,  138,
  141,  144,  147,  149,  152,  155,  158,  161,  164,  167,  171,  174,  177,  180,  183,  187,
  190,  194,  197,  200,  204,  208,  211,  215,  218,  222,  226,  230,  234,  237,  241,  245,
  249,  254,  258,  262,  266,  270,  275,  279,  283,  288,  292,  297,  301,  306,  311,  315,
  320,  325,  330,  335,  340,  345,  350,  355,  360,  365,  370,  376,  381,  386,  392,  397,
  403,  408,  414,  420,  425,  431,  437,  443,  449,  455,  461,  467,  473,  480,  486,  492,
  499,  505,  512,  518,  525,  532,  538,  545,  552,  559,  566,  573,  580,  587,  594,  601,
  609,  616,  624,  631,  639,  646,  654,  662,  669,  677,  685,  693,  701,  709,  717,  726,
  734,  742,  751,  759,  768,  776,  785,  794,  802,  811,  820,  829,  838,  847,  857,  866,
  875,  885,  894,  903,  913,  923,  932,  942,  952,  962,  972,  982,  992, 1002, 1013, 1023,]

lut = [int(i/4) for i in lut]

def get_ip(name = 'ESP-ColorPicker', service = '_http._tcp.local.'):
    try:
        return zeroconf.get_service_info(service, f"{name}.{service}").parsed_addresses()
    except (AssertionError, AttributeError):
        return []
    except KeyboardInterrupt:
        raise KeyboardInterrupt

def set_rgb(ip , rgb):
    try:
        print(rgb)
        r = requests.get(f"http://{ip}/?r{rgb[0]}g{rgb[1]}b{rgb[2]}&", timeout=2)
        # print(r.elapsed.total_seconds()*1000)
    except KeyboardInterrupt:
        raise KeyboardInterrupt
    except:
        pass

while True:
    try:
        ip = get_ip()
        if not ip:
            continue
        ip = ip[0]
        print(f"found ESP at IP {ip}")
        print(f"running light show")
        rgb = [0,0,255]
        for i in range(3):
            set_rgb(ip , rgb)
            rgb.pop(0)
            rgb.append(0)
            sleep(1)
        rgb = [0,0,0]
        for j in range(3):
            for i in lut:
                rgb[j] = i
                set_rgb(ip, rgb)
            sleep(1)
        sleep(3)
    except KeyboardInterrupt:
        break

zeroconf.close()