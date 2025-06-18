# Supply-chain-optimization-using-Linear-Programming

This project aims to minimize total supply chain costs (production, storage, transportation) using **Linear Programming** with Python and PuLP.

## 🔧 Tools Used
- Python
- PuLP library

## 📌 Objective
Minimize:
- Production Cost  
- Storage Cost  
- Transportation Cost

## 🔍 Key Components
- **Decision Variables**: Quantities produced, stored, transported  
- **Constraints**: Capacity limits, demand fulfillment, non-negativity  
- **Objective Function**: Total Cost = Production + Storage + Transport Costs

## 🗂 Files
- `lp_model.py`: LP formulation
- `data/`: Input CSVs for cost, demand, capacity
- `run_optimization.py`: Runs the model

## 🚀 How to Run
```bash
pip install -r requirements.txt
python run_optimization.py
