'''
Created on Feb 17, 2015

@author: umwilm
'''

import Image
import numpy as np

if __name__ == '__main__':
    pass

a = np.ones([100,100], dtype=np.byte)
print a.shape

i = Image.fromarray(a.astype(np.byte))
#i.show()
i2 = i.resize((80,120), Image.NEAREST)
#i2.show()
a2 = np.array(i2).astype(np.byte)
print a2.shape
