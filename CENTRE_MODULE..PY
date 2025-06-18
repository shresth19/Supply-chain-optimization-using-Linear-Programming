from decimal import Decimal 
from COST_MANAGEMENT import Cost, Costs

class Center:
    def __init__(self, name: str, address: str):
        self.name = name
        self.address = address
        self.costs = []

    def add_cost(self, cost: Cost):
        """Adds a fixed cost to the cost center."""
        self.costs.append(cost)

    @property
    def total_fixed_cost(self) -> Decimal:
        """Calculates the total fixed cost of the center."""
        return sum(cost.value for cost in self.costs)

    def simulate_fixed_cost(self, simulator):
        """Simulates different fixed cost scenarios for better forecasting."""
        simulated_costs = [simulator.normal(mean=cost.value, std=cost.value * 0.1, upper=cost.value * 1.5, lower=cost.value * 0.5) for cost in self.costs]
        return sum(simulated_costs)

    def __repr__(self):
        return f"Center(Name: {self.name}, Address: {self.address}, Total Fixed Cost: {self.total_fixed_cost})"
