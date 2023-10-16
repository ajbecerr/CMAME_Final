import glob
# from matplotlib import collections as mc
from multiscale_new import *
import numpy as np
from sklearn.metrics import mean_squared_error
import sys

# Data = np.load('../../ablateOutputs/all_domains.npy')

arr = np.loadtxt('../../sampling/ablate_parameters.csv', delimiter=',', dtype=str)
# domains = glob.glob('../../ablateOutputs/domainParaffin_*_B.npy')
boundaries = glob.glob('../../ablateOutputs/boundaryParaffin_*_B.npy')

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
#    # np.save(domain, domain_i)

all_boundaries = []
for boundary in boundaries:
    boundary_i = np.load(boundary)
    i = int(boundary.split('_')[1].split('.')[0])
    E38_boundary = np.array([[arr[i][3]] for j in range(len(boundary_i))])
    E53_boundary = np.array([[arr[i][4]] for j in range(len(boundary_i))])
    E155_boundary = np.array([[arr[i][2]] for j in range(len(boundary_i))])
    velFac_boundary = np.array([[arr[i][5]] for j in range(len(boundary_i))])
    boundary_i = np.hstack((boundary_i, E38_boundary, E53_boundary, E155_boundary, velFac_boundary))
    all_boundaries.append(boundary_i)
#    # np.save(boundary, boundary_i)

# domains = glob.glob('../../ablateOutputs/domain_*.npy')
# domains = all_domains
boundaries = all_boundaries
# Data = np.vstack((domain for domain in domains))
Data = np.vstack((boundary for boundary in boundaries))
Data = np.hstack((Data[:, 2:], Data[:, 1:2])).astype(float)
print(Data)

maxs = int(sys.argv[1])
delta = float(sys.argv[2])

###

eps = epsilon_0(Data, maxs, delta)
print(eps)

sparse1, Bs1, Cs1, f1, T1, meanerror1 = KfoldCV(Data, 2, eps, maxs)

scales = sorted(set(sparse1[:, -1]))
data3 = []
for ss in range(maxs+1):
    ind = np.where(sparse1[:, -1] <= ss)[0]
    Bs = Bs1[:, ind]
    np.save('B_'+str(ss)+'.npy', Bs)
    print(Bs)
    Cs = Cs1[ind]
    np.save('C_'+str(ss)+'.npy', Cs)
    print(Cs)
    proj = Bs.dot(Cs)
    mse = mean_squared_error(Data[:, -1], proj)
    data3.append([Bs.shape[1]/Bs.shape[0], mse])
data3 = np.array(data3)
np.save('MSE.npy', data3)
print(data3)