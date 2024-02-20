#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 12 10:06:26 2023

@author: george
"""

import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
import math
import glob


arr = np.loadtxt('./../../sampling/ablate_parameters_MMA.csv', delimiter=',', dtype=str)
domains = glob.glob('./../../ablateOutputs/boundaryPMMA_*_B.npy')

all_domains = []
for domain in domains:
    domain_i = np.load(domain)
    i = int(domain.split('_')[1].split('.')[0])
    E257_domain = np.array([[arr[i][3]] for j in range(len(domain_i))])
    E250_domain = np.array([[arr[i][4]] for j in range(len(domain_i))])
    E1_domain = np.array([[arr[i][2]] for j in range(len(domain_i))])
    b249_domain = np.array([[arr[i][5]] for j in range(len(domain_i))])
    lv_domain = np.array([[arr[i][6]] for j in range(len(domain_i))])
    velFac_domain = np.array([[arr[i][7]] for j in range(len(domain_i))])
    index_i = np.array([i for j in range(len(domain_i))])
    index_i = np.expand_dims(index_i, 1)
    domain_i = np.hstack((domain_i, E1_domain, E257_domain, E250_domain,b249_domain, lv_domain, velFac_domain, index_i))
    all_domains.append(domain_i)

domains = all_domains
Data = np.vstack(([domain for domain in domains]))


df = pd.DataFrame(data = Data, columns=(['rdot', 'qrad', 'x','y','E1','E257', 'E250', 'b249', 'lv', 'V','ID']))
df.ID = df.ID.astype(int)
df.to_csv('PMMAboundary_GASP.csv')

#Sample test
#Test IDs - 26 58 44 52 23 5 37 53 28 10 22 59
sample_test_idxs = [26, 58, 44, 52, 23, 5, 37, 53, 28, 10, 22, 59]
sample_test_df = df[df['ID'].isin(sample_test_idxs)] 

ix_ts = list(set(sample_test_idxs))
sample_train_idxs = [x for x in range(1,65,1) if x not in ix_ts]
sample_train_df = df[df['ID'].isin(sample_train_idxs)]

sample_test_df.to_csv('PMMAboundary_GASP_sample_test.csv')
sample_train_df.to_csv('PMMAboundary_GASP_sample_train.csv')

#Boundary test locations
#Test rows - 43 38 49 90 80 12 8 88 26 60 75 6 17 22 52 7 47 86
location_test_idxs = [43, 38, 49, 90, 80, 12, 8, 88, 26, 60, 75, 6, 17, 22, 52, 7, 47, 86]
# Calculate the maximum index in the DataFrame
max_index = df.index.max()
included_indices = set()
for index in location_test_idxs:
    included_indices.update(range(index, max_index + 1, index))
location_test_df = df[df.index.isin(included_indices)]

location_train_idxs = [x for x in range(np.size(df,0)) if x not in included_indices]
location_train_df = df.iloc[location_train_idxs]

location_train_df.to_csv('PMMAboundary_GASP_location_train.csv')
location_test_df.to_csv('PMMAboundary_GASP_location_test.csv')