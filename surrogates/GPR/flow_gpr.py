# -*- coding: utf-8 -*-
"""
Created on Thu Aug 26 00:03:51 2021

@author: George
"""
import numpy as np
from matplotlib import pyplot as plt
import sklearn.gaussian_process as gp
import pandas as pd


domain9 = np.load('domain9.npy')
domain10 = np.load('domain10.npy')
domain11 = np.load('domain11.npy')
domain12 = np.load('domain12.npy')
domain13 = np.load('domain13.npy')
domain14 = np.load('domain14.npy')
domain15 = np.load('domain15.npy')
domain16 = np.load('domain16.npy')

domain9[:,2] = domain9[:,2]
domain10[:,2] = domain10[:,2]
domain11[:,2] = domain11[:,2]
domain12[:,2] = domain12[:,2]
domain13[:,2] = domain13[:,2]
domain14[:,2] = domain14[:,2]
domain15[:,2] = domain15[:,2]
domain16[:,2] = domain16[:,2]

domain9 = domain9[1:]
domain10 = domain10[1:]
domain11 = domain11[1:]
domain12 = domain12[1:]
domain13 = domain13[1:]
domain14 = domain14[1:]
domain15 = domain15[1:]
domain16 = domain16[1:]

domain = np.vstack([domain9,domain10,domain11,domain12,domain13,domain14,domain15,domain16])

# #Simplots
# fig, axs = plt.subplots(1, 2)
# axs[0].scatter(k,dfgpr[:,11], marker = 'x', color='k')
# axs[0].set_xlabel('N')
# axs[0].set_ylabel('Pinch-off volume (m^3)')
# axs[1].scatter(k, dfgpr[:,12], marker = 'x', color='r')
# axs[1].set_xlabel('N')
# axs[1].set_ylabel('Pinch-off time (s)')
# plt.subplots_adjust(left=0.1,
#                     bottom=0.1, 
#                     right=0.9, 
#                     top=0.9, 
#                     wspace=0.4, 
#                     hspace=0.4)
# plt.show()

from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import WhiteKernel, DotProduct, RBF
import matplotlib.pyplot as plt
import numpy as np


# Create kernel and define GPR
from sklearn.gaussian_process.kernels import ConstantKernel
kernel = 1.0 * RBF(1.0)
random_state = 0
gpr = GaussianProcessRegressor(kernel=kernel, random_state=random_state, alpha = 0.1, normalize_y=True)


x_train = np.delete(domain, 1, axis=1)
y_train_temp = domain[:, 1]

x_train_scaled = np.zeros((np.size(x_train, 0) , np.size(x_train, 1)))

x_train_scaled[:,0] = (x_train[:,0]-np.mean(x_train[:,0]))/np.std(x_train[:,0])
x_train_scaled[:,1] = (x_train[:,1]-np.mean(x_train[:,1]))/np.std(x_train[:,1])
x_train_scaled[:,2] = (x_train[:,2]-np.mean(x_train[:,2]))/np.std(x_train[:,2])


tempgpr = gpr.fit(x_train_scaled, y_train_temp)

predict_attrain = tempgpr.predict(x_train_scaled, return_std=False)

mse = np.vstack((y_train_temp,predict_attrain)).T

total_mse = 0
for i in range(0,np.size(mse,0)):
    lol = (mse[i,0] - mse[i,1])**2
    
    total_mse = total_mse + lol
# Create test data

import random

x_test_t = np.linspace(0,1200,100)
x_test_E = np.linspace(3.2,3.658,100)
x_test_G = np.linspace(5,50,100)

x_test = np.array(np.meshgrid(x_test_t, x_test_E, x_test_G)).T.reshape(-1,3)

x_test_scaled = np.zeros((np.size(x_test, 0) , np.size(x_test, 1)))


x_test_scaled[:,0] = (x_test[:,0]-np.mean(x_train[:,0]))/np.std(x_train[:,0])
x_test_scaled[:,1] = (x_test[:,1]-np.mean(x_train[:,1]))/np.std(x_train[:,1])
x_test_scaled[:,2] = (x_test[:,2]-np.mean(x_train[:,2]))/np.std(x_train[:,2])



y_hat_T, y_sigma_T = tempgpr.predict(x_test_scaled, return_std=True)



y_hat_T = y_hat_T[...,None]
y_sigma_T = y_sigma_T[...,None]

df_T_pred  = np.concatenate((x_test, y_hat_T,y_sigma_T), axis=1)

np.save('preds.npy',df_T_pred)


mean_yhat_T_t = np.zeros(100)
mean_ysigma_T_t = np.zeros(100)

for i in range(0,np.size(x_test_t,0)):
  mean_yhat_T_t[i] = np.mean(df_T_pred[df_T_pred[:,0] == x_test_t[i], 3])
  mean_ysigma_T_t[i] = np.mean(df_T_pred[df_T_pred[:,0] == x_test_t[i], 4])
  
#t ~ T plot



plt.figure()
plt.plot(x_train[:,0], y_train_temp, 'r.', markersize=10, label='Observations')
plt.plot(x_test_t, mean_yhat_T_t, 'b-', label='Mean Prediction')
plt.fill(np.concatenate([x_test_t, x_test_t[::-1]]),
         np.concatenate([mean_yhat_T_t - 1.9600 * mean_ysigma_T_t,
                        (mean_yhat_T_t + 1.9600 * mean_ysigma_T_t)[::-1]]),
         alpha=.5, fc='b', ec='None', label='95% confidence interval')
plt.xlabel('Timestep from ignition $(-)$')
plt.ylabel('Temperature at location above slab $(K)$')
plt.legend(loc='upper right')
plt.savefig('t_vs_T_plot.png',dpi=100)


#E ~ T plot
mean_yhat_T_E = np.zeros(100)
mean_ysigma_T_E = np.zeros(100)

for i in range(0,np.size(x_test_E,0)):
  mean_yhat_T_E[i] = np.mean(df_T_pred[df_T_pred[:,1] == x_test_E[i], 3])
  mean_ysigma_T_E[i] = np.mean(df_T_pred[df_T_pred[:,1] == x_test_E[i], 4])

plt.figure()
plt.plot(x_train[:,1], y_train_temp, 'r.', markersize=10, label='Observations')
plt.plot(x_test_E, mean_yhat_T_E, 'b-', label='Mean Prediction')
plt.fill(np.concatenate([x_test_E, x_test_E[::-1]]),
         np.concatenate([mean_yhat_T_E - 1.9600 * mean_ysigma_T_E,
                        (mean_yhat_T_E + 1.9600 * mean_ysigma_T_E)[::-1]]),
         alpha=.5, fc='b', ec='None', label='95% confidence interval')
plt.xlabel('Activation Energy $E_{155} x 10^4 (cal/mol)$')
plt.ylabel('Temperature at location above slab $(K)$')
plt.legend(loc='upper right')
plt.savefig('E_vs_T_plot.png',dpi=100)

#E ~ T plot
mean_yhat_T_G = np.zeros(100)
mean_ysigma_T_G = np.zeros(100)

for i in range(0,np.size(x_test_G,0)):
  mean_yhat_T_G[i] = np.mean(df_T_pred[df_T_pred[:,2] == x_test_G[i], 3])
  mean_ysigma_T_G[i] = np.mean(df_T_pred[df_T_pred[:,2] == x_test_G[i], 4])

plt.figure()
plt.plot(x_train[:,2], y_train_temp, 'r.', markersize=10, label='Observations')
plt.plot(x_test_G, mean_yhat_T_G, 'b-', label='Mean Prediction')
plt.fill(np.concatenate([x_test_G, x_test_G[::-1]]),
         np.concatenate([mean_yhat_T_G - 1.9600 * mean_ysigma_T_G,
                        (mean_yhat_T_G + 1.9600 * mean_ysigma_T_G)[::-1]]),
         alpha=.5, fc='b', ec='None', label='95% confidence interval')
plt.xlabel('Oxidizer flux $(\frac{kg}{m^2 s)$')
plt.ylabel('Temperature at location above slab $(K)$')
plt.legend(loc='upper right')
plt.savefig('E_vs_T_plot.png',dpi=100)


#Temp pdf MCM

#Assume uniform inputs t, E, G
Nsims = 50000


G = np.random.uniform(5, 50, Nsims)

E = np.random.uniform(3.2,3.658, Nsims)


t = np.random.uniform(0,1200, Nsims)

ensembles = np.column_stack([t, E, G])


ensembles_scaled = np.zeros((np.size(ensembles, 0), np.size(ensembles, 1)))


ensembles_scaled[:,0] = (ensembles[:,0]-np.mean(ensembles[:,0]))/np.std(ensembles[:,0])
ensembles_scaled[:,1] = (ensembles[:,1]-np.mean(ensembles[:,1]))/np.std(ensembles[:,1])
ensembles_scaled[:,2] = (ensembles[:,2]-np.mean(ensembles[:,2]))/np.std(ensembles[:,2])

y_hat_T, y_sigma_T = tempgpr.predict(ensembles_scaled, return_std=True)


import seaborn as sns

figure = plt.figure()
sns.kdeplot(y_hat_T, color = '#0504aa', shade = True)
#sns.kdeplot(y_sigma_vol, color = 'grey', shade = True)
plt.xlabel(r'$T_{68,18}$', fontsize = 18 )
plt.ylabel('Probability Density', fontsize = 18 )
plt.savefig('pdf.png',dpi=100)
#plt.legend(ncol = 2, bbox_to_anchor=(0.15, -0.25), loc='upper left', borderaxespad=0, labels=['Pinch-off volume'], fontsize = 12)


# # #T ~ vol plot

# # plt.figure()
# # plt.plot(x_train[:,0], y_train_vol, 'r.', markersize=10, label='Observations')
# # plt.plot(x_test_T, y_hat_vol, 'b-', label='Mean Prediction')
# # plt.fill(np.concatenate([x_test_T, x_test_T[::-1]]),
# #          np.concatenate([y_hat_vol - 1.9600 * y_sigma_vol,
# #                         (y_hat_vol + 1.9600 * y_sigma_vol)[::-1]]),
# #          alpha=.5, fc='b', ec='None', label='95% confidence interval')
# # plt.xlabel('Temperature $(^{o}C)$')
# # plt.ylabel('Pinch-off volume $()$')
# # #plt.ylim(np.min(y_hat_vol), np.max(y_hat_vol))
# # #plt.xticks(np.arange(min(x_test_T), max(x_test_T)+1, 1.0))
# # plt.legend(loc='upper right')


# # #just G
# # x_train_G = x_train[:,2]
# # x_train_G = x_train_G.reshape(-1, 1)
# # volgpr = gpr.fit(x_train_G, y_train_vol)
# # x_test_G = x_test[:,2]
# # x_test_G = x_test_G.reshape(-1,1)

# # y_hat_vol, y_sigma_vol = volgpr.predict(x_test_G, return_std=True)

# # #just lambda
# # x_train_l = x_train[:,1]
# # x_train_l = x_train_l.reshape(-1, 1)
# # volgpr = gpr.fit(x_train_l, y_train_vol)
# # x_test_l = x_test[:,1]
# # x_test_l = x_test_l.reshape(-1,1)
# # y_hat_vol, y_sigma_vol = volgpr.predict(x_test_l, return_std=True)

# # #TG
# # x_train_TG = x_train[:,[0,2]]
# # volgpr = gpr.fit(x_train_TG, y_train_vol)
# # x_test_TG = x_test[:,[0,2]]

# # y_hat_vol, y_sigma_vol = volgpr.predict(x_test_TG, return_std=True)


# # #all
# # volgpr = gpr.fit(x_train, y_train_vol)

# # y_hat_vol, y_sigma_vol = volgpr.predict(x_test, return_std=True)


# # def normalize_2d(matrix):
# #     norm = np.linalg.norm(matrix)
# #     matrix = matrix/norm  # normalized matrix
# #     return matrix

# # #T and G
# # x_test_TG = normalize_2d(x_test_TG)
# # x_train_TG = normalize_2d(x_train_TG)
# # volgpr = gpr.fit(x_train_TG, y_train_vol)
# # y_hat_vol, y_sigma_vol = volgpr.predict(x_test_TG, return_std=True)


# # #all
# # x_test = normalize_2d(x_test)
# # x_train = normalize_2d(x_train)
# # volgpr = gpr.fit(x_train, y_train_vol)
# # y_hat_vol, y_sigma_vol = volgpr.predict(x_test, return_std=True)

