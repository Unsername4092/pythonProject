import xml.etree.ElementTree as elemTree
import matplotlib.pyplot as plt
import numpy as np
data = elemTree.parse('LION1.xml')
root = data.getroot()
# I-V graph
V = []                          # Empty list for saving voltage value
for v in root.iter('Voltage'):  # Save each voltage value in the list.
    V.extend(list(map(float, v.text.split(','))))
I = []                          # Empty list for saving current value
for i in root.iter('Current'):  # Save the each current value in the list.
    I.extend(list(map(float, i.text.split(','))))
plt.figure(1, [7, 5])                                # Set the size and number of the graph window.
plt.title('I-V analysis', fontsize=18, fontweight='bold')   # Graph title
plt.xlabel('Voltage (V)', fontsize=13)                # title of x-axis
plt.ylabel('Current (A)', fontsize=13)                # title of y-axis
plt.yscale('log')                                     # Determine the yscale
plt.plot(V, np.abs(I), 'r.-', markersize=8)           # Plot the Voltage and Current values.
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
wls[-1]='Reference'         # Set the last label as reference.
plt.figure(2, [7, 5])       # Set the size and number of the graph window.
plt.title('Transmission spectra - as measured', fontsize=18, fontweight='bold') # Graph title
plt.xlabel('Wavelength (nm)', fontsize=13)              # Title of x-axis
plt.ylabel('Measured transmission (dBm)', fontsize=13)  # Title of y-axis
for r in range(len(L)):                                 # Plot the value and set the label for each graph
    plt.plot(L[r], IL[r], label=wls[r])
plt.legend(loc='best', ncol=2)                          # Sets the space for showing labels.
plt.show()                                              # Show the graphs
