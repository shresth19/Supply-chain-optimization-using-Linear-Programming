import math
from abc import ABC, abstractmethod
from typing import Union, Dict
from decimal import Decimal

from COST_MANAGEMENT import Cost, Costs

class Product(ABC):
    """
    Represents a product in the supply chain, transitioning from raw materials to finished goods,
    distributed through various channels.
    """

    def __init__(
        self,
        name: str,
        price: Union[str, int, float, Decimal] = 0,
        demand: Union[str, int, float, Decimal] = 0,
        lead_time: Union[str, int, float, Decimal] = 0,
        inventory: Union[str, int, float, Decimal] = 0,
    ) -> None:
        self.name: str = self._validate_string(name, "Product name")
        self.inventory: Decimal = self._validate_decimal(inventory, "Inventory")
        self.demand: Decimal = self._validate_decimal(demand, "Demand")
        self.lead_time: Decimal = self._validate_decimal(lead_time, "Lead time")
        self.price: Decimal = self._validate_decimal(price, "Price")
        self.storage_costs: Costs = Costs()

    def __repr__(self) -> str:
        return f'<Product: {self.name} - Inventory: {self.inventory}>'

    @staticmethod
    def _validate_string(value: str, field_name: str) -> str:
        if not value or not isinstance(value, str):
            raise ValueError(f"Invalid {field_name}: {value}")
        return value

    @staticmethod
    def _validate_decimal(value: Union[str, int, float, Decimal], field_name: str) -> Decimal:
        try:
            decimal_value = Decimal(value)
            if decimal_value < 0:
                raise ValueError(f"{field_name} cannot be negative: {value}")
            return decimal_value
        except Exception:
            raise ValueError(f"Invalid {field_name}: {value}")

    @property
    def total_storage_cost(self) -> Decimal:
        return self.storage_costs.total

    @property
    @abstractmethod
    def total_variable_cost(self) -> Decimal:
        pass

    @property
    def optimum_inventory_level(self) -> Decimal:
        """
        Calculates the Economic Order Quantity (EOQ) for optimal inventory management.
        EOQ Formula: Q = sqrt(2 * D * K / h)
        """
        if not self.demand or not self.total_storage_cost or not self.total_variable_cost:
            raise RuntimeError("All values must be positive for EOQ calculation.")
        return Decimal(math.sqrt(2 * self.demand * self.total_variable_cost / self.total_storage_cost))

class ProducedProduct(Product):
    """ A Product manufactured by the company. """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.production_costs: Costs = Costs()

    @property
    def total_variable_cost(self) -> Decimal:
        return self.production_costs.total

class PurchasedProduct(Product):
    """ A Product sourced from external suppliers. """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.purchase_costs: Costs = Costs()

    @property
    def total_variable_cost(self) -> Decimal:
        return self.purchase_costs.total

if __name__ == '__main__':
    from MONTE_CARLO_SIMULATION import MonteCarloSimulator

    def run_simulation(title: str, times: int, product: Product, cost_dict: Dict[str, Dict]):
        simulator = MonteCarloSimulator(title=title, runs=times)
        
        def main() -> Decimal:
            for cost_type, values in cost_dict.items():
                for cost_name, params in values.items():
                    getattr(product, cost_type).add(Cost(cost_name, simulator.normal(**params)))
            return product.total_variable_cost if isinstance(product, ProducedProduct) else product.total_storage_cost
        
        simulator.simulate(main)
        simulator.summary()

    produced_product = ProducedProduct(name='Product I', inventory=100)
    purchased_product = PurchasedProduct(name='Product II', inventory=100)

    production_costs = {
        'production_costs': {
            'Energy Costs': {'mean': 2, 'std': 1, 'upper': 5, 'lower': 0},
            'Labor Costs': {'mean': 7, 'std': 2, 'upper': 10, 'lower': 5},
        }
    }
    storage_costs = {
        'storage_costs': {
            'Warehousing': {'mean': 0.1, 'std': 0.1, 'upper': 0.5, 'lower': 0},
            'Utilities': {'mean': 0.1, 'std': 0.1, 'upper': 0.5, 'lower': 0},
            'Insurance': {'mean': 0.1, 'std': 0.1, 'upper': 0.5, 'lower': 0},
        }
    }

    run_simulation('Product Variable Cost', 10, produced_product, production_costs)
    run_simulation('Product Storage Cost', 10, purchased_product, storage_costs)
