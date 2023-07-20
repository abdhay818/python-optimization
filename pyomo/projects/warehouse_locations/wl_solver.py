# Solve an instance of the Warehouse Location problem

import pyomo.environ as pyo
from warehouse_location_optimization_model import create_warehouse_model

# Create sample data
N = ['Bangsar', 'Sentul', 'Rawang'] # Candidate warehouse locations
M = ['Gombak', 'Kajang', 'Serdang', 'Damansara'] # Customer locations

# Delivery cost from warehouse to customer, d[n,m] : cost
d = {
	 ('Bangsar', 'Gombak') : 250, \
	 ('Bangsar', 'Kajang') : 1606, \
	 ('Bangsar', 'Serdang') : 1550, \
	 ('Bangsar', 'Damansara') : 530, \
	 ('Sentul', 'Gombak') : 300, \
	 ('Sentul', 'Kajang') : 1792, \
	 ('Sentul', 'Serdang') : 1531, \
	 ('Sentul', 'Damansara') : 567, \
	 ('Rawang', 'Gombak') : 285, \
	 ('Rawang', 'Kajang') : 2322, \
	 ('Rawang', 'Serdang') : 1324, \
	 ('Rawang', 'Damansara') : 1236 }

P = 2 # Number of warehouse

# Create the Pyomo model
model = create_warehouse_model(N, M, d, P)

# Create the solver interface and solve the math model
solver = pyo.SolverFactory('glpk')

## Loop over values for mutable parameter P
for n in range (1,5):
	model.P = n
	result = solver.solve(model)
	pyo.assert_optimal_termination(result)
	print('# of warehouse:', n, ', delivery cost:', pyo.value(model.obj))
	print(model.y.pprint())

# Print the optimal warehouse locations
# model.y.pprint()

# print(pyo.value(model.obj))