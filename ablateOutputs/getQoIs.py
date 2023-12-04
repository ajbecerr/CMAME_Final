import glob
import numpy as np

# domains = glob.glob('domain*.npy')

# for domain in domains:
    # domain_i = np.load(domain, allow_pickle=True)
    # i = int(domain.split('_')[1].split('.')[0])

    # QoIs = []
    # for j in range(3216):
        # mask_j_k = np.array([k % 3216 == j for k in range(len(domain_i))])
        # domain_i_j_k = domain_i[mask_j_k, :]
        # Tmean = sum(domain_i_j_k[:, 1])/len(domain_i_j_k[:, 1])
        # Vmean = sum(domain_i_j_k[:, 2])/len(domain_i_j_k[:, 2])
        # QoIs.append(np.array([Tmean, Vmean, domain_i[j, -2], domain_i[j, -1]]))

    # print(np.array(QoIs))
    # np.save(domain.split('_')[0]+'_'+str(i)+'_B.npy', np.array(QoIs))

boundaries = glob.glob('boundary*.npy')

for boundary in boundaries:
    boundary_i = np.load(boundary, allow_pickle=True)
    i = int(boundary.split('_')[1].split('.')[0])

    QoIs = []
    for j in range(92):
        mask_j_k = np.array([k % 92 == j for k in range(len(boundary_i))])
        boundary_i_j_k = boundary_i[mask_j_k, :]
        Rdotmean = sum(boundary_i_j_k[:, 1])/len(boundary_i_j_k[:, 1])
        Qtotmean = sum(boundary_i_j_k[:, 2])/len(boundary_i_j_k[:, 2])
        QoIs.append(np.array([Rdotmean, Qtotmean, boundary_i[j, -2], boundary_i[j, -1]]))

    print(np.array(QoIs))
    np.save(boundary.split('_')[0]+'_'+str(i)+'_B.npy', np.array(QoIs))
