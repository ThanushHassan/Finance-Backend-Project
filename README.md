# Finance Data Processing & Access Control Backend

This repository contains a robust Flask-based backend system designed for a financial dashboard. The project demonstrates advanced API design, Role-Based Access Control (RBAC), and efficient database management.

# 🚀 Quick Start

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/ThanushHassan/Finance-Backend-Project.git](https://github.com/ThanushHassan/Finance-Backend-Project.git)
   cd finance_assignment

# Set up the virtual environment:

# Bash
python -m venv venv
.\venv\Scripts\activate  # On Windows
pip install -r requirements.txt

# Run the application:

# Bash
python app.py

.

# Backend Design & Architectural Decisions
In this implementation, I focused on three key technical choices to ensure the system is scalable and secure:

1. Role-Based Access Control (RBAC) via Decorator Pattern
I implemented a custom @role_required decorator to manage user permissions (Admin, Analyst, Viewer).

Logical Thinking: Instead of repeating permission checks inside every function, the decorator acts as a reusable middleware.

Benefit: This keeps the business logic clean and ensures that security policies are applied consistently across the entire API.

2. Database-Level Aggregation for Performance
For the Dashboard Summary (Total Income, Expenses, and Balance), I used SQLAlchemy's func.sum to perform calculations directly within the database.

Logical Thinking: Calculating totals in Python requires loading all records into memory, which is inefficient. Offloading this to the SQL engine is significantly faster.

Benefit: The application remains highly responsive even as the dataset grows to thousands of transactions.

3. Input Validation & Data Integrity
The backend utilizes structured try-except blocks to handle transaction inputs.

Logical Thinking: I implemented validation to catch non-numeric inputs for transaction amounts before they reach the database.

Benefit: By returning a 400 Bad Request status code, the system prevents database corruption and provides clear feedback to the frontend.

# Project Structure
Plaintext
finance_assignment/
├── app.py             # Flask Application Entry Point
├── models.py          # SQLAlchemy Database Models
├── auth.py            # RBAC Middleware & Decorators
├── requirements.txt   # Project Dependencies
├── .gitignore         # Version Control Exclusions
└── README.md          # Technical Documentation

### **Final Step to update GitHub:**
1. Save the file in VS Code.
2. Run these three commands in your terminal:
   ```powershell
   git add README.md
   git commit -m "Update README with professional documentation"
   git push origin main
