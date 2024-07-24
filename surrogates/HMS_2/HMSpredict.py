import glob
import h5py
from multiscale_new import *
import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error
import sys

E1 = float(sys.argv[1])
E257 = float(sys.argv[2])
E250 = float(sys.argv[3])
b249 = float(sys.argv[4])
Lv = float(sys.argv[5])
v = float(sys.argv[6])

train_files = glob.glob('PMMA*train.csv')

#['PMMAboundary_GASP_location_train.csv', 'PMMAboundary_GASP_sample_train.csv']

qoi = 'rdot' # 'rdot' or 'qtot'
j = 3 # 0, 1, 2, or 3
k = 1 # 1, or 2
# ss = 12

Data = pd.read_csv(train_files[j%2])
#Data = Data.dropna()
Data = np.array(Data.values)

if qoi == 'rdot':
    Data = np.hstack((Data[:, 3:-1], Data[:, 1].reshape(-1, 1))).astype(float)
else:
    Data = np.hstack((Data[:, 3:-1], Data[:, 2].reshape(-1, 1))).astype(float)
    
max_cols = np.diag([1/max(Data[:, i]) for i in range(len(Data[0]))])
Data = np.matmul(Data, max_cols)
#print(Data)
#print(len(Data))

Cs = glob.glob('Cs*.npy')
#print(Cs)
sparse = glob.glob('sparse*.npy')
#print(sparse)
T = glob.glob('T*.npy')
#print(T)

#['Cs__0.005_qtot_location.npy', 'Cs__0.005_qtot_sample.npy', 'Cs__0.005_rdot_location.npy', 'Cs__0.005_rdot_sample.npy']
#['sparse__0.005_qtot_location.npy', 'sparse__0.005_qtot_sample.npy', 'sparse__0.005_rdot_location.npy', 'sparse__0.005_rdot_sample.npy']
#['T__0.005_qtot_location.npy', 'T__0.005_qtot_sample.npy', 'T__0.005_rdot_location.npy', 'T__0.005_rdot_sample.npy']

Cs = np.load(Cs[j])
sparse = np.load(sparse[j])
T = np.load(T[j])

QoI = predict(np.matmul(np.array([[0.019031407, 0.001521122, E1, E257, E250, b249, Lv, v]]), max_cols[:-1, :-1]), sparse, T, Cs)

predictFile = open('predict.txt', "w")
predictFile.write(str(QoI[0]))
predictFile.close()