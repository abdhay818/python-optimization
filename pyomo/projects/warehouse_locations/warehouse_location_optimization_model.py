# Warehouse location problem
## 
##	This optimization problem is to find the locations for a set of warehouses that meet delivery demands while optimizing transportation costs. 
# 
# The goal is to determine the optimal warehouse locations that will minimize the total cost of product delivery. 
##

## Pyomo Concrete Model

import pyomo.environ as pyo

def create_warehouse_model(N, M, d, P):
	model = pyo.ConcreteModel(name="Warehouse Location")

	model.x = pyo.Var(N, M, bounds=(0,1))
	model.y = pyo.Var(N, within=pyo.Binary)
	model.P = pyo.Param(initialize=P, mutable=True)

	def obj_rule(mdl):
		return sum(d[n,m] * mdl.x[n,m] for n in N for m in M)
	model.obj = pyo.Objective(rule=obj_rule)

	def demand_rule(mdl, m):
		return sum(mdl.x[n,m] for n in N) == 1
	model.demand = pyo.Constraint(M, rule=demand_rule)

	def warehouse_active_rule(mdl, n, m):
		return mdl.x[n,m] <= mdl.y[n]
	model.warehouse_active = pyo.Constraint(N,M, rule=warehouse_active_rule)

	def num_warehouses_rule(mdl):
		return sum(mdl.y[n] for n in N) <= mdl.P
	model.num_warehouses = pyo.Constraint(rule=num_warehouses_rule)

	return model


