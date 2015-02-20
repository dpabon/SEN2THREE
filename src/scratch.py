"""
Simple demo of a horizontal bar chart.
"""
import numpy as np
import pylab as plt

# Example data
classes = ('Sat','Dark','Soil','Snow','Veg','Water','LPC','MPC','HPC','Cirr','ClS')
x_pos = np.arange(len(classes))
performance = 100 * np.random.rand(len(classes))

plt.bar(x_pos, performance, align='center', alpha=0.4)
plt.xticks(x_pos, classes)
plt.ylabel('Percentage')
plt.title('Classification')

plt.show()
