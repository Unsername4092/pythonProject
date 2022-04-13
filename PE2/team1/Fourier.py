import xml.etree.ElementTree as elemTree
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import r2_score
data = elemTree.parse('LION1.xml')
root = data.getroot()
# Wavelength-Transmission graph
L = []                      # Empty list for saving wavelength
for n in root.iter('L'):    # Save the each wavelength data in the list
    L.append(list(map(float, n.text.split(','))))
del L[2][-1]
IL = []                     # Empty list for saving Measured transmission
for m in root.iter('IL'):   # Save the each transmission data in the list
    IL.append(list(map(float, m.text.split(','))))
del IL[2][-1]
wls = []                    # Empty list for saving Voltage value
for l in root.iter('WavelengthSweep'):   # Saves the voltage value to be used as a label.
    wls.append('DC = {}'.format(l.attrib['DCBias']))
wls[-1]='Reference' # Set the last label as reference.
r=0
plt.plot(L[r],IL[r])
plt.show()
# 데이터를 이용해 푸리에 급수를 그리기.


r=0
plt.plot(L[r], IL[r], label="Original Data")
wn = 4
L = 2*np.pi
FuData = np.zeros((wn + 1, len(L[r])))  # 각 wave의 데이터
def int_c(x, y):  # A0를 계산한다
    area = np.trapz(y=y, x=x)
    return area
A0 = (1 / L) * int_c(L[r], IL[r])
for n in range(1, wn + 1):
    kn = 2 * np.pi * n / L
    def int_a(x, y):
        in_int = y * np.sin(2 * np.pi * n * x / L)
        area = np.trapz(y=in_int, x=x)
        return area


    An = (2 / L) * int_a(L[r], IL[r])


    def int_b(x, y):
        in_int = y * np.cos(2 * np.pi * n * x / L)
        area = np.trapz(y=in_int, x=x)
        return area


    Bn = (2 / L) * int_b(L[r], IL[r])
    fs = An * np.sin(kn * L[r]) + Bn * np.cos(kn * L[r])
    if n == 1:
        FuSum = A0 + fs
        FuData[0, :] = A0
        FuData[1, :] = fs
    else:
        FuSum = FuSum + fs  # [x + y for x, y in zip(FuSum,fs)]
        FuData[n, :] = fs
# 각 wave number의 그래프를 그린다.
for i in range(1, wn + 1):
    plt.plot(L[r], A0 + FuData[i, :], label="wave number %d" % (i))

# 각 wave number의 합의 그래프를 그린다.
plt.plot(L[r], FuSum,label = "Sum of all wave number")

# 범례를 표기한다.
plt.legend(loc="upper right",framealpha=0,fontsize=10)

plt.show() # 화면에서 바로 볼 때 사용



print(len(IL[r]),r)
sum = 0                        # sum 함수가 float 에서는 사용이 안되기때문에 직접해준다.
for s in L[r]:                 # s - sum
    sum = sum + s
    mean = sum / len(L[r])
    M = []
    for c in range(len(L[r])):     # c - L[r] count
            lr=L[r]
            M.append(lr[c] - mean)         # 왜 평균값을 뺌으로써 fitting 이 잘되는걸까?
    pf = np.polyfit(M, IL[r], 40)
    ILP = np.polyval(pf, M)
    plt.plot(L[r], ILP, label='polyfit {}'.format(r))
    T_r2 = r2_score(IL[r], ILP)
print(T_r2)


