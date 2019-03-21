import importlib

Simulation = 'Simulation'
importlib.import_module(Simulation)

simulation = Simulation(10, 12)

print('Opening simulation window...')

simulation.start() 
