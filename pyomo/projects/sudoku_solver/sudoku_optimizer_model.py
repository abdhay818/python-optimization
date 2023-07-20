# Sudoku Puzzle Solver using Pyomo Optimization Model

# Programmer : Muhamad Abdul Hay
# Reference  : "Pyomo - Optimization Modeling in Python" book
# 20 July 2023

import pyomo.environ as pyo 

# Create Python dict data structure for mapping sudoku 9 rows x 9 cols
# Define subsquare 3x3 inside 9x9 square
subsq_to_row_col = dict()

subsq_to_row_col[1] = [(i,j) for i in range (1,4) for j in range(1,4)]
#print(subsq_to_row_col[1])

subsq_to_row_col[2] = [(i,j) for i in range (1,4) for j in range (4,7)]
#print(subsq_to_row_col[2])

subsq_to_row_col[3] = [(i,j) for i in range (1,4) for j in range (7,10)]
#print(subsq_to_row_col[3])

subsq_to_row_col[4] = [(i,j) for i in range(4,7) for j in range(1,4)]
#print(subsq_to_row_col[4])

subsq_to_row_col[5] = [(i,j) for i in range(4,7) for j in range(4,7)]
#print(subsq_to_row_col[5])

subsq_to_row_col[6] = [(i,j) for i in range(4,7) for j in range(7,10)]
#print(subsq_to_row_col[6])

subsq_to_row_col[7] = [(i,j) for i in range (7,10) for j in range(1,4)]
#print(subsq_to_row_col[7])

subsq_to_row_col[8] = [(i,j) for i in range (7,10) for j in range (4,7)]
#print(subsq_to_row_col[8])

subsq_to_row_col[9] = [(i,j) for i in range (7,10) for j in range (7,10)]
#print(subsq_to_row_col[9])

# Print Sudoku 9x9 cells in (i,j) to verify the cell index
for i in range (1,10):
	# for j in range(1, 10):
	print(subsq_to_row_col[i]);

# Pyomo optimization model
def create_sudoku_model(board):
	model = pyo.ConcreteModel();

	# Store the starting board for the model
	model.board = board

	# Create sets for rows, cols, and squares [1..9]
	model.ROWS = pyo.RangeSet(1,9)
	model.COLS = pyo.RangeSet(1,9)
	model.SUBSQUARES = pyo.RangeSet(1,9)
	model.VALUES = pyo.RangeSet(1,9)

	# Create the binary variables to define the values
	model.y = pyo.Var(model.ROWS, model.COLS, model.VALUES, within=pyo.Binary)

	# Fix variables based on the current board
	for (r,c,v) in board:
		model.y[r,c,v,].fix(1)

	
	# Create the objective - this is a feasibility problem
	# we can just make it a constant
	model.obj = pyo.Objective(expr=1.0)

	# Sudoku Rules / Constrains list
	# Exactly one unique number in each row [1...9]
	def _RowCon(model, r, v):
		return sum(model.y[r,c,v] for c in model.COLS) ==1
	model.RowCon = pyo.Constraint(model.ROWS, model.VALUES, rule=_RowCon)

	# Exactly one number [1..9] for each column 
	def _ColCon(model, c, v):
		return sum(model.y[r,c,v] for r in model.ROWS) == 1
	model.ColCon = pyo.Constraint(model.COLS, model.VALUES, rule=_ColCon)

	# Exactly one number [1..9] for each subsquare
	def _SqCon(model, s, v):
		return sum(model.y[r,c,v] for (r,c) in subsq_to_row_col[s]) == 1
	model.SqCon = pyo.Constraint(model.SUBSQUARES, model.VALUES, rule=_SqCon)

	# Rule for one number for each cell [1..9]
	def _ValueCon(model, r, c):
		return sum(model.y[r,c,v] for v in model.VALUES) == 1
	model.ValueCon = pyo.Constraint(model.ROWS, model.COLS, rule=_ValueCon)

	return model


# To add new integer cut to the model
def add_integer_cut(model):
	if not hasattr(model, "IntegerCuts"):
		model.IntegerCuts = pyo.ConstraintList()

		cut_expr = 0.0
		for r in model.ROWS:
			for c in model.COLS:
				for v in model.VALUES:
					if not model.y[r,c,v].fixed:
						if pyo.value(model.y[r,c,v]) >= 0.5:
							cut_expr += (1.0 - model.y[r,c,v])
						else:
							cut_expr += model.y[r,c,v]
	model.IntegerCuts.add(cut_expr >= 1)

# Print current Sudoku solution stored in the model
def print_sudoku_solution(model):
	for r in model.ROWS:
		print(' '.join(str(v) for c in model.COLS for v in model.VALUES
		if pyo.value(model.y[r,c,v]) >= 0.5))






