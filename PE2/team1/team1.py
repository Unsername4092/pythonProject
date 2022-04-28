import xml.etree.ElementTree as elemTree
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import r2_score
import pandas as pd
from lmfit.models import ExpressionModel
data = elemTree.parse('LION1.xml')
root = data.getroot()
# I-V graph
V = []                          # Empty list for saving voltage value
for v in root.iter('Voltage'):  # Save each voltage value in the list.
    V.extend(list(map(float, v.text.split(','))))
I = []                          # Empty list for saving current value
for i in root.iter('Current'):  # Save the each current value in the list.
    I.extend(list(map(float, i.text.split(','))))
plt.figure(1, [18, 8])
plt.subplot(2, 3, 1)                               # Set the size and number of the graph window.
plt.title('I-V analysis', fontsize=18, fontweight='bold')   # Graph title
plt.xlabel('Voltage (V)', fontsize=13)                # title of x-axis
plt.ylabel('Current (A)', fontsize=13)                # title of y-axis
plt.yscale('log')                                     # Determine the y-scale
plt.yticks([10**i for i in range(-1,-11,-1)])       # y축의 간격을 설정
plt.scatter(V, np.exp(np.log(np.abs(I))))           # Plot the Voltage and Current values.
# Regression
p = np.polyfit(V, np.abs(I), 12)       # 다항식계수 구하기
y = np.polyval(p, V)                  # fitting 한 값 데이터
r2 = r2_score(np.abs(I), y)             # 결정계수
print(r2)
plt.plot(V, y, color='y', label='R squared {}'.format(r2))
print(I,V)

plt.legend(loc='lower left', ncol=2)
# Wavelength-Transmission graph
L = []                      # Empty list for saving wavelength
for n in root.iter('L'):    # Save the each wavelength data in the list
    L.append(list(map(float, n.text.split(','))))
del L[2][-1]                # 6066번째 데이터 제거
IL = []                     # Empty list for saving Measured transmission
for m in root.iter('IL'):   # Save the each transmission data in the list
    IL.append(list(map(float, m.text.split(','))))
del IL[2][-1]
wls = []                    # Empty list for saving Voltage value
for l in root.iter('WavelengthSweep'):   # Saves the voltage value to be used as a label.
    wls.append('DC = {}'.format(l.attrib['DCBias']))
wls[-1] = 'Reference'         # Set the last label as reference.
pr = np.polyfit(L[-1], IL[-1], 6)   # L IL 그래프 다항식계수구하기
yr = np.polyval(pr, L[-1])         # fitting 된 IL 데이터
r2_r = r2_score(IL[-1], yr)           # 결정계수
for sp in range(2, 5):         # sp - subplot
    plt.subplot(2, 3, sp)       # Set the size and number of the graph window.
    plt.title('Transmission spectra - as measured', fontsize=18, fontweight='bold')   # Graph title
    plt.xlabel('Wavelength (nm)', fontsize=13)              # Title of x-axis
    plt.ylabel('Measured transmission (dBm)', fontsize=13)  # Title of y-axis
    if sp == 2:                        # 두번째 subplot 에는 reference 와 fitting 값의 그래프를 그린다.
        plt.plot(L[-1], IL[-1], color='C6')
        plt.plot(L[-1], yr, color='black', linestyle='dashed', label='R squared = {}'.format(r2_r))
    if sp == 3:                        # 세번째 subplot 에는 기존 그래프에 fitting 된 reference 값을 빼준다.
        for r in range(len(L)-1):
            plt.plot(L[r], IL[r]-yr, label=wls[r])
    if sp == 4:                        # 네번째 subplot 에는 raw data 그래프를 그린다.
        for r in range(len(L)):
            plt.plot(L[r], IL[r], label=wls[r])
    plt.legend(loc='lower left', ncol=2)
plt.tight_layout()
plt.savefig('graph')
#plt.show()                                              # Show the graphs
TestSiteInfo=root.find('TestSiteInfo')
dict={'Lot':[],'Wafer':[],'Mask':[],'TestSite':[],'Name':[],'Date':[],'Operator':[],'DieColumn':[],'DieRow':[],'AnalysisWavelength (nm)':[],'Rsq of Ref. spectrum (6th)':[] ,'Max transmission of Ref. spec. (dB)':[]}
ref=IL[-1]
print(type(yr),type(ref))
AlignWavelength=next(root.iter('AlignWavelength'))
Modulator=next(root.iter('Modulator'))
for i in range(len(L)):
    dict['Lot'].append(TestSiteInfo.attrib['Batch'])
    dict['Wafer'].append(TestSiteInfo.attrib['Wafer'])
    dict['Mask'].append(TestSiteInfo.attrib['Maskset'])
    dict['TestSite'].append(TestSiteInfo.attrib['TestSite'])
    dict['Name'].append(Modulator.attrib['Name'])
    dict['Date'].append(root.attrib['CreationDate'])
    dict['Operator'].append(root.attrib['Operator'])
    dict['AnalysisWavelength (nm)'].append(AlignWavelength.text)
    dict['Max transmission of Ref. spec. (dB)'].append(min(IL[i]-yr))

    #dict['Rsq of Ref. spectrum (6th)'].append(r2_score(IL[i]-ref,IL[i]-yr))



print(pd.DataFrame(dict))
