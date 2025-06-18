from pulp import LpProblem, LpVariable, lpSum, LpMinimize

# Define the Linear Programming problem
model = LpProblem(name="Supply_Chain_Optimization", sense=LpMinimize)

# Decision Variables
production = LpVariable("Production", lowBound=0, cat="Continuous")
storage = LpVariable("Storage", lowBound=0, cat="Continuous")
transport = LpVariable("Transport", lowBound=0, cat="Continuous")

# Cost Coefficients
cost_production = 50  # Cost per unit produced
cost_storage = 5      # Cost per unit stored
cost_transport = 10   # Cost per unit transported

# Objective Function: Minimize total supply chain cost
model += lpSum([
    cost_production * production,
    cost_storage * storage,
    cost_transport * transport
]), "Total_Cost"

# Constraints
model += production >= 500, "Minimum_Production"
model += storage >= 100, "Minimum_Storage"
model += transport >= 200, "Minimum_Transport"
model += production + storage >= transport, "Balance_Constraint"

# Solve the LP problem
model.solve()

# Print Results
print("\nOptimal Solution:")
print(f"Production: {production.varValue}")
print(f"Storage: {storage.varValue}")
print(f"Transport: {transport.varValue}")
print(f"Total Cost: {model.objective.value()}")
