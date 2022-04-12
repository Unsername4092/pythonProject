import xml.etree.ElementTree as elemTree
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import r2_score
data = elemTree.parse('LION1.xml')
root = data.getroot()
# I-V graph
V = []                          # Empty list for saving voltage value
for v in root.iter('Voltage'):  # Save each voltage value in the list.
    V.extend(list(map(float, v.text.split(','))))
I = []                          # Empty list for saving current value
for i in root.iter('Current'):  # Save the each current value in the list.
    I.extend(list(map(float, i.text.split(','))))
plt.subplot(2,2,1)                               # Set the size and number of the graph window.
plt.title('I-V analysis', fontsize=18, fontweight='bold')   # Graph title
plt.xlabel('Voltage (V)', fontsize=13)                # title of x-axis
plt.ylabel('Current (A)', fontsize=13)                # title of y-axis
plt.yscale('log')                                     # Determine the yscale
plt.plot(V,np.exp(np.log(np.abs(I))), 'r.-', markersize=8)           # Plot the Voltage and Current values.
# 회귀선
p = np.polyfit(V,np.abs(I),12)
y = np.polyval(p,V)
plt.plot(V,y)
r2=r2_score(np.abs(I),y)
print(r2)
# Wavelength-Transmission graph
L = []                      # Empty list for saving wavelength
for n in root.iter('L'):    # Save the each wavelength data in the list
    L.append(list(map(float, n.text.split(','))))
IL = []                     # Empty list for saving Measured transmission
for m in root.iter('IL'):   # Save the each transmission data in the list
    IL.append(list(map(float, m.text.split(','))))
wls = []                    # Empty list for saving Voltage value
for l in root.iter('WavelengthSweep'):   # Saves the voltage value to be used as a label.
    wls.append('DC = {}'.format(l.attrib['DCBias']))
wls[-1]='Reference' # Set the last label as reference.
for sp in range(2,5):
    plt.subplot(2,2,sp)       # Set the size and number of the graph window.
    plt.title('Transmission spectra - as measured', fontsize=18, fontweight='bold') # Graph title
    plt.xlabel('Wavelength (nm)', fontsize=13)              # Title of x-axis
    plt.ylabel('Measured transmission (dBm)', fontsize=13)  # Title of y-axis
    if sp == 2:
        for r in range(len(L)):
            plt.plot(L[r], IL[r], label=wls[r])
    if sp==3:
        r=-1
        plt.plot(L[r], IL[r], label=wls[r])
        sum = 0
        for s in L[r]:
            sum = sum + s
        mean = sum / len(L[r])
        M = []
        for c in L[r]:
            M.append(c - mean)
        pf = np.polyfit(M, IL[r], 25)
        ILP = np.polyval(pf, M)
        plt.plot(L[r], ILP, label='polyfit {}'.format(r))
        T_r2 = r2_score(IL[r], ILP)
        print(T_r2)
    if sp == 4:
        for r in range(len(L)-1):
            sum = 0
            for s in L[r]:
                sum = sum + s
            mean = sum / len(L[r])
            M = []
            for c in L[r]:
                M.append(c - mean)
            pf = np.polyfit(M, IL[r], 40)
            ILP = np.polyval(pf, M)
            plt.plot(L[r], ILP, label='polyfit {}'.format(r))
            T_r2 = r2_score(IL[r], ILP)
            print(T_r2)
plt.legend(loc='best', ncol=2)                          # Sets the space for showing labels.
plt.tight_layout()
plt.show()                                              # Show the graphs