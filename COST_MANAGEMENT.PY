from typing import Union, Dict
from decimal import Decimal

class Cost:
    """
    Represents an individual cost component in supply chain management,
    tracking the financial expenditure on production and delivery.
    """
    
    def __init__(self, name: str, value: Union[str, int, Decimal, float]) -> None:
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Invalid cost name. Must be a non-empty string.")
        if not isinstance(value, (str, int, float, Decimal)):
            raise TypeError("Invalid cost value. Must be a number or string convertible to Decimal.")
        
        self.__name: str = name.strip()
        self.__value: Decimal = Decimal(value)
        
        if self.__value < 0:
            raise ValueError("Cost value cannot be negative.")
    
    def __repr__(self) -> str:
        return f"<Cost: {self.__name}, Value: {self.__value}>"
    
    @property
    def name(self) -> str:
        return self.__name
    
    @property
    def value(self) -> Decimal:
        return self.__value

class Costs:
    """
    Manages multiple cost components within a storage center or product lifecycle.
    Provides methods to add, retrieve, and calculate total costs.
    """
    
    def __init__(self) -> None:
        self.__costs: Dict[str, Cost] = {}
    
    def __repr__(self) -> str:
        return f"<Costs: Total = {self.total}>"
    
    def add(self, cost: Cost) -> None:
        """Adds a new cost component."""
        if not isinstance(cost, Cost):
            raise TypeError("Expected an instance of Cost.")
        self.__costs[cost.name] = cost
    
    def get(self, name: str) -> Cost:
        """Retrieves a cost by name. Returns a default cost if not found."""
        return self.__costs.get(name, Cost(name, 0))
    
    @property
    def total(self) -> Decimal:
        """Calculates the total cost of all components."""
        return sum(cost.value for cost in self.__costs.values())
