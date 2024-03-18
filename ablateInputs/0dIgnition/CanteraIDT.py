import pandas as pd
import numpy as np

import time

import cantera as ct

print(f"Runnning Cantera version: {ct.__version__}")

import matplotlib.pyplot as plt

plt.rcParams["axes.labelsize"] = 18
plt.rcParams["xtick.labelsize"] = 12
plt.rcParams["ytick.labelsize"] = 12
plt.rcParams["figure.autolayout"] = True
plt.rcParams["figure.dpi"] = 120

plt.style.use("ggplot")

gas = ct.Solution("MMA_temp.yaml")

# Define the reactor temperature and pressure
reactor_temperature = 1200  # Kelvin
reactor_pressure = 1013250  # Pascals

gas.TP = reactor_temperature, reactor_pressure

# Define the fuel, oxidizer and set the stoichiometry
gas.set_equivalence_ratio(phi=1.0, fuel="MMA(1)", oxidizer={"O2(2)": 1.0, "Ar": 3.76})

# Create a batch reactor object and add it to a reactor network
# In this example, the batch reactor will be the only reactor
# in the network
r = ct.IdealGasReactor(contents=gas, name="Batch Reactor")
reactor_network = ct.ReactorNet([r])

# use the above list to create a DataFrame
time_history = ct.SolutionArray(gas, extra="t")

def ignition_delay(states, species):
    """
    This function computes the ignition delay from the occurence of the
    peak in species' concentration.
    """
    i_ign = states(species).Y.argmax()
    return states.t[i_ign]
    
reference_species = "OH(6)"

# Tic
t0 = time.time()

# This is a starting estimate. If you do not get an ignition within this time, increase it
estimated_ignition_delay_time = 0.1
t = 0

counter = 1
while t < estimated_ignition_delay_time:
    t = reactor_network.step()
    if not counter % 10:
        # We will save only every 10th value. Otherwise, this takes too long
        # Note that the species concentrations are mass fractions
        time_history.append(r.thermo.state, t=t)
    counter += 1

# We will use the 'oh' species to compute the ignition delay
tau = ignition_delay(time_history, reference_species)

# Toc
t1 = time.time()

print(f"Computed Ignition Delay: {tau:.3e} seconds. Took {t1-t0:3.2f}s to compute")

# If you want to save all the data - molefractions, temperature, pressure, etc
# uncomment the next line
# time_history.to_csv("time_history.csv")
predictFile = open('ignitionDelay134.txt', "w")
predictFile.write(str(tau))
predictFile.close()

# plt.figure()
# plt.plot(time_history.t, time_history(reference_species).Y, "-o")
# plt.xlabel("Time (s)")
# plt.ylabel("$Y_{OH}$")

# plt.xlim([0, 0.05])
# plt.arrow(
#     0,
#     0.008,
#     tau,
#     0,
#     width=0.0001,
#     head_width=0.0005,
#     head_length=0.001,
#     length_includes_head=True,
#     color="r",
#     shape="full",
# )
# plt.annotate(
#     r"$Ignition Delay: \tau_{ign}$", xy=(0, 0), xytext=(0.01, 0.0082), fontsize=16
# );