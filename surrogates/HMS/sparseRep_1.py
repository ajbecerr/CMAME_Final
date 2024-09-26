import glob
# from matplotlib import collections as mc
from multiscale_new import *
import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error
import sys

maxs = int(sys.argv[1])
delta = float(sys.argv[2])
qoi = str(sys.argv[3])
fuel = str(sys.argv[4])
dropout = str(sys.argv[5])

print(maxs)
print(delta)
print(qoi)
print(fuel)
print(dropout)

# Data = np.load('../../ablateOutputs/all_domains.npy')
# domains = glob.glob('../../ablateOutputs/domainParaffin_*_B.npy')

# all_domains = []
# for domain in domains:
#     domain_i = np.load(domain)
#     i = int(domain.split('_')[1].split('.')[0])
#     E38_domain = np.array([[arr[i][3]] for j in range(len(domain_i))])
#     E53_domain = np.array([[arr[i][4]] for j in range(len(domain_i))])
#     E155_domain = np.array([[arr[i][2]] for j in range(len(domain_i))])
#     velFac_domain = np.array([[arr[i][5]] for j in range(len(domain_i))])
#     domain_i = np.hstack((domain_i, E38_domain, E53_domain, E155_domain, velFac_domain))
#     all_domains.append(domain_i)
    # np.save(domain, domain_i)

# if fuel == 'CH4':
#     arr = np.loadtxt('../../sampling/ablate_parameters_CH4.csv', delimiter=',', dtype=str)
#     boundaries = glob.glob('../../ablateOutputs/boundaryParaffin_*_B.npy')
    
#     # all_boundaries = []
#     # for boundary in boundaries:
#     #     boundary_i = np.load(boundary, allow_pickle=True)
#     #     i = int(boundary.split('_')[1].split('.')[0])
#     #     E38_boundary = np.array([[arr[i][3]] for j in range(len(boundary_i))])
#     #     b53_boundary = np.array([[arr[i][4]] for j in range(len(boundary_i))])
#     #     E155_boundary = np.array([[arr[i][2]] for j in range(len(boundary_i))])
#     #     velFac_boundary = np.array([[arr[i][5]] for j in range(len(boundary_i))])
#     #     boundary_i = np.hstack((boundary_i, E38_boundary, b53_boundary, E155_boundary, velFac_boundary))
#     #     all_boundaries.append(boundary_i)
#     #    # np.save(boundary, boundary_i)
# else:
#     arr = np.loadtxt('../../sampling/ablate_parameters_MMA.csv', delimiter=',', dtype=str)
#     boundaries = glob.glob('../../ablateOutputs/boundaryPMMA_*_B.npy')
    
#     all_boundaries = []
#     for boundary in boundaries:
#         boundary_i = np.load(boundary, allow_pickle=True)
#         i = int(boundary.split('_')[1].split('.')[0])
#         b249_boundary = np.array([[arr[i][3]] for j in range(len(boundary_i))])
#         E250_boundary = np.array([[arr[i][4]] for j in range(len(boundary_i))])
#         E1_boundary = np.array([[arr[i][2]] for j in range(len(boundary_i))])
#         E257_boundary = np.array([[arr[i][5]] for j in range(len(boundary_i))])
#         velFac_boundary = np.array([[arr[i][6]] for j in range(len(boundary_i))])
#         latent_boundary = np.array([[arr[i][7]] for j in range(len(boundary_i))])
#         boundary_i = np.hstack((boundary_i, E1_boundary, b249_boundary, E250_boundary, E257_boundary, velFac_boundary, latent_boundary))
#         all_boundaries.append(boundary_i)
#     #    # np.save(boundary, boundary_i)
    
# # domains = all_domains
# boundaries = all_boundaries
# # Data = np.vstack((domain for domain in domains))
# Data = np.vstack((boundary for boundary in boundaries))

# if qoi == 'rdot':
#     Data = np.hstack((Data[:, 2:], Data[:, 0:1])).astype(float)
#     print(Data)
# else:
#     Data = np.hstack((Data[:, 2:], Data[:, 1:2])).astype(float)
#     print(Data)
    
# max_cols = np.diag([1/max(Data[:, i]) for i in range(len(Data[0]))])
# Data = np.matmul(Data, max_cols)
# print(Data)

###

# Data = pd.read_csv('PMMAboundary_GASP_'+dropout+'_train.csv')
# # Data = Data.dropna()
# Data = Data.to_numpy()
Data = np.vstack([np.array(pd.read_csv('train_sample_'+str(i)+'.csv')) for i in range(1, 6)])
if qoi == 'rdot':
    Data = np.hstack((Data[:, 3:-1], Data[:, 1].reshape(-1, 1))).astype(float)
else:
    Data = np.hstack((Data[:, 3:-1], Data[:, 2].reshape(-1, 1))).astype(float)
max_cols = np.diag([1/max(Data[:, i]) for i in range(len(Data[0]))])
Data = np.matmul(Data, max_cols)
print(Data)
print(len(Data))

eps = epsilon_0(Data, maxs, delta)
delta = str(delta)
print(eps)

sparse1, Bs1, Cs1, f1, T1 = Multiscale_train(Data, eps, maxs)
np.save('sparse_'+'_'+delta+'_'+qoi+'_'+dropout+'.npy', sparse1)
np.save('Cs_'+'_'+delta+'_'+qoi+'_'+dropout+'.npy', Cs1)
np.save('T_'+'_'+delta+'_'+qoi+'_'+dropout+'.npy', T1)

scales = sorted(set(sparse1[:, -1]))
data3 = []
for ss in range(maxs+1):
    ind = np.where(sparse1[:, -1] <= ss)[0]
    Bs = Bs1[:, ind]
    # np.save('B_'+str(ss)+'_'+delta+'_'+qoi+'_'+dropout+'.npy', Bs)
    # np.save('B_'+str(ss)+'.npy', Bs)
    print(Bs)
    Cs = Cs1[ind]
    # np.save('C_'+str(ss)+'_'+delta+'_'+qoi+'_'+dropout+'.npy', Cs)
    # np.save('C_'+str(ss)+'.npy', Cs)
    print(Cs)
    proj = Bs.dot(Cs)
    mse = mean_squared_error(Data[:, -1], proj)
    data3.append([Bs.shape[1]/Bs.shape[0], mse])
data3 = np.array(data3)
np.save('MSE_'+delta+'_'+qoi+'_'+dropout+'.npy', data3)
print(data3)