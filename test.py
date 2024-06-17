import numpy as np
import matplotlib.pyplot as plt

Fs = 100
f = 5
sample = 100
x = np.arange(sample)
y = np.sin(2 * np.pi * f * x / Fs)
plt.plot(x, y)
plt.xlabel('Sample (n)')
plt.ylabel('y')
plt.show()

Y = np.fft.fftshift(np.fft.fft(y))
f = np.arange(-Fs/2, Fs/2, Fs/sample)

Y_mag = np.abs(Y) 
Y_phase = np.angle(Y)

plt.subplot(1, 2, 1)
plt.plot(f, Y_mag, '.-')
plt.xlabel('Frequency')
plt.ylabel('Magnitude')

x_value = 5
y_value = 50

plt.annotate(f'({x_value}, {y_value:.2f})', 
             xy=(x_value, y_value), 
             xytext=(x_value+1, y_value+0.5))

plt.subplot(1, 2, 2)
plt.plot(f, Y_phase, '.-')
plt.xlabel('Frequency')
plt.ylabel('Phase')
plt.show()