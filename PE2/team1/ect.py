import xml.etree.ElementTree as elemTree
import matplotlib.pyplot as plt
import numpy as np
from numpy import exp
from sklearn.metrics import r2_score
from lmfit import Model
data = elemTree.parse('LION1.xml')
root = data.getroot()
V = []
for v in root.iter('Voltage'):
    V.extend(list(map(float, v.text.split(','))))
I = []
for i in root.iter('Current'):
    I.extend(list(map(float, i.text.split(','))))
    I = list(map(abs, I))

x = np.array(V[:])
y = np.array(I[:])
fit1 = np.polyfit(x, y, 12)
fit1 = np.poly1d(fit1)

def IV_fit(X, Is, Vt):
    return (Is * (exp(X/Vt) - 1))    #

model = Model(IV_fit)
result = model.fit(y, X=x, Is=10**-15, Vt=0.026)

def IVR(y):
    global yhat, ybar
    yhat = result.best_fit
    ybar = np.sum(y)/len(y)
    sse = np.sum((yhat - ybar) ** 2)
    sst = np.sum((y - ybar) ** 2)
    return sse/sst

# 결정계수 구하는 다른 방법
r2 = r2_score(I, result.best_fit)
print(r2)

plt.subplot(2, 2, 1)
plt.plot(V, I, 'b.', label='data', markersize=8)
plt.plot(x, result.best_fit, label='best_fit')
plt.plot(x, result.best_fit, 'r-', label='R-squared ={}'.format(IVR(y)))
plt.legend(loc = 'best')
#plt.yscale('log')
plt.title('I-V analysis', fontsize=18, fontweight='bold')
plt.xlabel('Voltage[V]', fontsize=13)
plt.ylabel('Current[A]', fontsize=13)
plt.show()
print(yhat-ybar)
print(ybar)
print(yhat)
print(I)