import xml.etree.ElementTree as etree
import matplotlib.pyplot as plt
import numpy as np

xml = etree.parse('C:/Users/qrudg/PycharmProjects/pythonProject/PE2/team1/LION1.xml')  # xml 파일 불러오기
root = xml.getroot()

wls = []
for i in root.iter('WavelengthSweep'):
    wls.append(i.attrib['DCBias'])
print(wls)

a = 0
for i in root.iter('WavelengthSweep'):
    a = a+1
    if a != len(wls) :
        L = list(map(float, i[0].text.split(',')))
        IL = list(map(float, i[1].text.split(',')))
        site_key = list(i.attrib.keys())
        site_values = list(i.attrib.values())
        plt.plot(L, IL, label=('DCBias =' + site_values[1]))


    else:
        L = list(map(float, i[0].text.split(',')))
        IL = list(map(float, i[1].text.split(',')))
        plt.plot(L, IL, label=('reference'))

plt.legend(loc='best')
plt.show()