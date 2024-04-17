# app.py

from flask import Flask, render_template, request

app = Flask(__name__)

expenses = []

def add_expense(amount, category, month):
    expenses.append({'amount': amount, 'category': category, 'month': month})

def find_index_of_dict_with_value(list_of_dicts, key, value):
    for index, item in enumerate(list_of_dicts):
        if item.get(key) == value:
            return index
    return None  # Return None if not found

def calculate_monthly_total(month):
    monthly_expenses = [expense['amount'] for expense in expenses if expense['month'] == month]
    return sum(monthly_expenses)

def calculate_monthly_category_totals():
    monthly_category_totals = {}
    for expense in expenses:
        month = expense['month']
        category = expense['category']
        if month in monthly_category_totals:
            if category in monthly_category_totals[month]:
                monthly_category_totals[month][category] += expense['amount']
            else:
                monthly_category_totals[month][category] = expense['amount']
        else:
            monthly_category_totals[month] = {category: expense['amount']}
    return monthly_category_totals

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_expense', methods=['POST'])
def add_expense_route():
    amount = float(request.form['amount'])
    category = request.form['category']
    month = request.form['month']
    add_expense(amount, category, month)
    return render_template('expense_added.html')


@app.route('/edit_expense', methods=['POST'])
def edit_expense_route():
    # Assuming you have a unique identifier for each expense, like an ID
    expense_id = request.form['expense_id']
    amount = float(request.form['amount'])
    category = request.form['category']
    month = request.form['month']
    
    # Assuming you have a function named edit_expense to handle the editing
    edit_expense(expense_id, amount, category, month)
    
    return render_template('expense_edited.html')

@app.route('/delete_expense', methods=['POST'])
def delete_expense_route():
    # Assuming you have a unique identifier for each expense, like an ID
    expense_id = request.form['expense_id']
    
    # Assuming you have a function named delete_expense to handle the deletion
    delete_expense(expense_id)
    
    return render_template('expense_deleted.html')

@app.route('/monthly_expenses')
def monthly_expenses():
    monthly_category_totals = calculate_monthly_category_totals()
    monthly_totals = {month: sum(category_totals.values()) for month, category_totals in monthly_category_totals.items()}
    return render_template('monthly_expenses.html', monthly_category_totals=monthly_category_totals, monthly_totals=monthly_totals)

if __name__ == '__main__':
    app.run(debug=True)
