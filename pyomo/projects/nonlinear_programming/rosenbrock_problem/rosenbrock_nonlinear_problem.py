# A Pyomo model for the Rosenbrock problem
# Example of Non-linear Problem (NLP) optimization (finding mininum value)

import pyomo.environ as pyo

model = pyo.ConcreteModel()
model.x = pyo.Var(initialize=1.5)
model.y = pyo.Var(initialize=1.5)

def rosenbrock(model):
	return (1.0 - model.x)**2 + 100.0 * (model.y - model.x**2)**2

model.obj = pyo.Objective(rule=rosenbrock, sense=pyo.minimize)

status = pyo.SolverFactory('ipopt').solve(model)
pyo.assert_optimal_termination(status)
model.pprint()