from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy # pyright: ignore[reportMissingImports]
from sqlalchemy import func # pyright: ignore[reportMissingImports]
from datetime import datetime
from functools import wraps

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///finance.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# --- MODELS ---
class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    type = db.Column(db.String(10), nullable=False) 
    category = db.Column(db.String(50), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    description = db.Column(db.String(200))

    def to_dict(self):
        return {
            "id": self.id, "amount": self.amount, "type": self.type,
            "category": self.category, "date": self.date.strftime("%Y-%m-%d"),
            "description": self.description
        }

# --- AUTH MIDDLEWARE ---
def role_required(allowed_roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user_role = request.headers.get('X-User-Role') 
            if not user_role:
                return jsonify({"error": "Missing X-User-Role header."}), 401
            if user_role not in allowed_roles:
                return jsonify({"error": f"Access denied for {user_role}"}), 403
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# --- ROUTES ---
@app.route('/api/records', methods=['POST'])
@role_required(['Admin'])
def add_record():
    data = request.json
    try:
        new_record = Transaction(
            amount=float(data['amount']),
            type=data['type'],
            category=data['category'],
            description=data.get('description', '')
        )
        db.session.add(new_record)
        db.session.commit()
        return jsonify({"message": "Record created", "id": new_record.id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/api/dashboard/summary', methods=['GET'])
@role_required(['Admin', 'Analyst', 'Viewer'])
def get_summary():
    summary = db.session.query(
        func.sum(Transaction.amount).filter(Transaction.type == 'Income').label('inc'),
        func.sum(Transaction.amount).filter(Transaction.type == 'Expense').label('exp')
    ).first()
    return jsonify({
        "total_income": summary.inc or 0,
        "total_expense": summary.exp or 0,
        "net_balance": (summary.inc or 0) - (summary.exp or 0)
    })

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)