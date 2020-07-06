import numpy as np
import matplotlib.pyplot as plt

def phaseCorr(a, b):
    corr = np.fft.fftn(a)*np.conjugate(np.fft.fftn(b))
    pc = corr/np.absolute(corr)
    return np.fft.fftshift(np.fft.ifftn(pc)).real

#1d example
t = np.arange(0,100)
a = np.sin(2*np.pi*t/20)
b = np.sin(2*np.pi*t/20+5)

plt.plot(t,a)
plt.plot(t,b)
plt.show()

center_x = a.shape[0]/2

corr = phaseCorr(a,b)
x = np.where(corr==np.max(corr))
x = x[0]

print('x shift:',center_x-x)

#2d example
a = np.array([[0,0,0,0],[0,1,0,0],[0,0,0,0],[0,0,0,0]])
b = np.array([[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,1,0]])

center_x = a.shape[0]/2
center_y = a.shape[1]/2

corr = phaseCorr(a,b)
x,y = np.where(corr==np.max(corr))
x,y = x[0],y[0]

print('a:')
print(a)
plt.imshow(a)
plt.grid()
plt.show()


print('b:')
print(b)
plt.imshow(b)
plt.grid()
plt.show()
print()
print('phase shift of `a` relative to `b`')
print('x shift:',center_x-x,'y shift:',center_y-y)
