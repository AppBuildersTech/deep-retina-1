
# coding: utf-8

# In[1]:

import numpy as np
from os.path import expanduser, join
import os
import json
import theano
import pyret.filtertools as ft
from preprocessing import datagen, loadexpt
from utils import rolling_window, mksavedir
import h5py
from scipy.stats import pearsonr
import preprocessing

# make save directory
save_dir = mksavedir(prefix='Experiment STC')

# # Load white noise data

# In[2]:

whitenoise_train = loadexpt(0, 'whitenoise', 'train', 40, roll=False)


# In[5]:

import os
#f = h5py.File(os.path.join(preprocessing.datadirs['lane.local'], '15-10-07/whitenoise.h5'), 'r')
f = h5py.File(os.path.join(preprocessing.datadirs['lenna'], '15-10-07/whitenoise.h5'), 'r')


# In[6]:

spk = f['spikes/cell01']


# In[8]:

time = np.array(f['train/time'])
sta, tax = ft.getsta(time, whitenoise_train.X, spk, 35)


# In[11]:

Xcut = ft.cutout(whitenoise_train.X, idx=np.flipud(ft.filterpeak(sta)[1]), width=5)


# In[113]:

stc = np.zeros((35*11*11, 35*11*11))
for idx, s in enumerate(ft.getste(time, Xcut, spk, 35)):
    sr = s.astype('float').ravel()
    if sr.size == (35*11*11):
        stc += np.outer(sr, sr)
        
    if idx % 500 == 0:
        print('{}'.format(100.*idx/len(spk)))


# In[ ]:

stc_normalized = stc/len(spk)

# subtract cut out sta
sta_cutout = ft.cutout(sta, idx=np.flipud(ft.filterpeak(sta)[1]), width=5)
stc_normalized -= np.outer(sta_cutout.ravel(), sta_cutout.ravel())
#hist(np.diag(stc_normalized))

## SAVE RESULT ##
f = h5py.File(join(save_dir, 'full_stc_experiment_15_10_07.h5'), 'w')
f.create_dataset('stc', data=stc_normalized)
f.close()


# In[ ]:

#u,v = np.linalg.eigh(stc_normalized)


