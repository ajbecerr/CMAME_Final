import glob
import h5py
import numpy as np
import sys

def compute_cell_centers(cells, vertices, dimensions=-1):
    # create a new np array based upon the dim
    number_cells = len(cells)
    vertices_dim = len(vertices[0])
    if dimensions < 0:
        dimensions = vertices_dim

    coords = np.zeros((number_cells, dimensions))

    # march over each cell
    for c in range(len(coords)):
        cell_vertices = [vertices[cells[c][i]] for i in range(dimensions)] # vertices.take(cells[c], axis=0)

        # take the average
        cell_center = np.sum(cell_vertices, axis=0)
        cell_center = cell_center / len(cell_vertices)

        # put back
        coords[c, 0:vertices_dim] = cell_center

    # if this is one d, flatten
    if dimensions == 1:
        coords = coords[:, 0]

    return coords

if str(sys.argv[1]) == 'pmma':
    domainFiles = glob.glob('../ablateInputs/slabs/_2dSlabPMMA_'+str(sys.argv[2])+'/domain/*.hdf5')
    # boundaryFiles = glob.glob('../ablateInputs/slabs/_2dSlabPMMA_'+str(sys.argv[2])+'/slabboundary/*.hdf5')
    boundaryMonitorFiles = glob.glob('../ablateInputs/slabs/_2dSlabPMMA_'+str(sys.argv[2])+'/slabboundary_monitor/*.hdf5')
    flowfield_mixfracFiles = glob.glob('../ablateInputs/slabs/_2dSlabParaffin_'+str(sys.argv[2])+'/flowField_mixtureFraction/*.hdf5')
else:
    domainFiles = glob.glob('../ablateInputs/slabs/_2dSlabParaffin_'+str(sys.argv[2])+'/domain/*.hdf5')
    # boundaryFiles = glob.glob('../ablateInputs/slabs/_2dSlabParaffin_'+str(sys.argv[2])+'/slabboundary/*.hdf5')
    boundaryMonitorFiles = glob.glob('../ablateInputs/slabs/_2dSlabParaffin_'+str(sys.argv[2])+'/slabboundary_monitor/*.hdf5')
    flowfield_mixfracFiles = glob.glob('../ablateInputs/slabs/_2dSlabParaffin_'+str(sys.argv[2])+'/flowField_mixtureFraction/*.hdf5')

# domainF0 = h5py.File(domainFiles[0], 'r')
# domainCells = list(domainF0['viz/topology/cells'])
# domainVertices = list(domainF0['geometry/vertices'])
# domain_cell_centers = compute_cell_centers(domainCells, domainVertices)

# boundaryF0 = h5py.File(boundaryMonitorFiles[0], 'r')
# boundaryCells = list(boundaryF0['viz/topology/cells'])
# boundaryVertices = list(boundaryF0['geometry/vertices'])
# boundary_cell_centers = compute_cell_centers(boundaryCells, boundaryVertices)

flowfield_mixfracF0 = h5py.File(flowfield_mixfracFiles[0], 'r')
flowfield_mixfracCells = list(flowfield_mixfracF0['viz/topology/cells'])
flowfield_mixfracVertices = list(flowfield_mixfracF0['geometry/vertices'])
flowfield_mixfrac_cell_centers = compute_cell_centers(flowfield_mixfracCells, flowfield_mixfracVertices)

# domain = np.array([0, 0, 0, 0, 0])
# for file in domainFiles:
#     f = h5py.File(file, 'r')
#     Temps = list(f['cell_fields/aux_temperature'][0])
#     Vels = list(f['cell_fields/aux_velocity'][0])
#     Times = [f['time'][0][0] for i in range(len(domain_cell_centers))]
#     domain_ij = np.hstack((np.array(list(zip(Times, Temps, Vels)), dtype='object'), domain_cell_centers))
#     domain = np.vstack((domain, domain_ij))
# domain = domain[1:]

# boundary = np.array([0, 0, 0, 0, 0])
# for file in boundaryMonitorFiles:
#     # print(file)
#     f = h5py.File(file, 'r')
#     # print(list(f['time']))
#     # print(list(f['cell_fields/slabboundary_monitor']))
#     Rdots = list(f['cell_fields/slabboundary_monitor_regressionRate'][0])
#     Qtots = list(np.array(f['cell_fields/slabboundary_monitor_conduction'][0]) + np.array(f['cell_fields/slabboundary_monitor_extraRad'][0]) + np.array(f['cell_fields/slabboundary_monitor_radiation'][0]))
#     Times = [f['time'][0][0] for i in range(len(boundary_cell_centers))]
#     boundary_ij = np.hstack((np.array(list(zip(Times, Rdots, Qtots))), boundary_cell_centers))    
#     boundary = np.vstack((boundary, boundary_ij))
# boundary = boundary[1:]

flowfield_Zmix = np.array([0 for i in range(4)])
for file in flowfield_mixfracFiles:
    f = h5py.File(file, 'r')
    Times = np.array([f['time'][0][0] for i in range(len(flowfield_mixfrac_cell_centers))]).reshape(-1, 1)
    flowfield_Zmix_ij = np.hstack((Times, f['cell_fields/monitor_zMix'][0].reshape(-1, 1), flowfield_mixfrac_cell_centers))
    flowfield_Zmix = np.vstack((flowfield_Zmix, flowfield_Zmix_ij))
flowfield_Zmix = flowfield_Zmix[1:]

if str(sys.argv[1]) == 'pmma':
    # np.save('../ablateOutputs/domainPMMA_'+str(sys.argv[2])+'.npy', domain)
    # print(domain)
    # np.save('../ablateOutputs/boundaryPMMA_'+str(sys.argv[2])+'.npy', boundary)
    # print(boundary)
    np.save('../ablateOutputs/flowfield_Zmix_PMMA_'+str(sys.argv[2])+'.npy', flowfield_Zmix)
    print(flowfield_Zmix)
# else:
#     np.save('../ablateOutputs/domainParaffin_'+str(sys.argv[2])+'.npy', domain)
#     print(domain)
#     np.save('../ablateOutputs/boundaryParaffin_'+str(sys.argv[2])+'.npy', boundary)
#     print(boundary)
