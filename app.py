from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = "jatin_secret_key"

# Predefined users with balance and history
users = {
    "jatin": {"balance": 10000, "history": []},
    "ronak": {"balance": 12000, "history": []},
    "ankush": {"balance": 9500, "history": []},
    "simran": {"balance": 8700, "history": []},
    "deepak": {"balance": 10500, "history": []},
    "reetu": {"balance": 11200, "history": []}
}

# -------------------- HOME --------------------
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    name = request.form['username'].lower()
    if name in users:
        session['name'] = name
        session['balance'] = users[name]['balance']
        return redirect(url_for('dashboard'))
    else:
        return render_template('index.html', error="❌ Invalid name! Please try again.")

# -------------------- DASHBOARD --------------------
@app.route('/dashboard')
def dashboard():
    if 'name' not in session:
        return redirect(url_for('home'))
    return render_template('dashboard.html', name=session['name'], balance=session['balance'])

# -------------------- CREDIT --------------------
@app.route('/credit', methods=['GET', 'POST'])
def credit():
    if 'name' not in session:
        return redirect(url_for('home'))
    if request.method == 'POST':
        amount = int(request.form['amount'])
        session['balance'] += amount
        users[session['name']]['balance'] = session['balance']
        users[session['name']]['history'].append(f"💰 Credited ₹{amount}")
        flash(f"✅ ₹{amount} credited successfully!", "success")
        return redirect(url_for('dashboard'))
    return render_template('credit.html', name=session['name'], balance=session['balance'])

# -------------------- DEBIT --------------------
@app.route('/debit', methods=['GET', 'POST'])
def debit():
    if 'name' not in session:
        return redirect(url_for('home'))
    if request.method == 'POST':
        amount = int(request.form['amount'])
        if session['balance'] >= amount:
            session['balance'] -= amount
            users[session['name']]['balance'] = session['balance']
            users[session['name']]['history'].append(f"💸 Debited ₹{amount}")
            flash(f"💸 ₹{amount} debited successfully!", "success")
            return redirect(url_for('dashboard'))
        else:
            return render_template('debit.html', name=session['name'], balance=session['balance'], error="❌ Insufficient Balance!")
    return render_template('debit.html', name=session['name'], balance=session['balance'])

# -------------------- TRANSFER --------------------
@app.route('/transfer', methods=['GET', 'POST'])
def transfer():
    if 'name' not in session:
        return redirect(url_for('home'))
    if request.method == 'POST':
        recipient = request.form['recipient'].lower()
        amount = int(request.form['amount'])
        if recipient not in users:
            return render_template('transfer.html', name=session['name'], balance=session['balance'], error="❌ Recipient does not exist!")
        if recipient == session['name']:
            return render_template('transfer.html', name=session['name'], balance=session['balance'], error="❌ Cannot transfer to yourself!")
        if amount > session['balance']:
            return render_template('transfer.html', name=session['name'], balance=session['balance'], error="❌ Insufficient balance!")

        # Deduct from sender
        session['balance'] -= amount
        users[session['name']]['balance'] = session['balance']
        users[session['name']]['history'].append(f"🔁 Transferred ₹{amount} to {recipient}")

        # Add to recipient
        users[recipient]['balance'] += amount
        users[recipient]['history'].append(f"💰 Received ₹{amount} from {session['name']}")

        flash(f"✅ ₹{amount} transferred to {recipient} successfully!", "success")
        return redirect(url_for('dashboard'))

    return render_template('transfer.html', name=session['name'], balance=session['balance'], users=users.keys())

# -------------------- CHECK BALANCE --------------------
@app.route('/balance')
def balance():
    if 'name' not in session:
        return redirect(url_for('home'))
    return render_template('balance.html', name=session['name'], balance=session['balance'])

# -------------------- TRANSACTION HISTORY --------------------
@app.route('/history')
def history():
    if 'name' not in session:
        return redirect(url_for('home'))
    transaction_history = users[session['name']]['history']
    return render_template('history.html', name=session['name'], balance=session['balance'], history=transaction_history)

# -------------------- LOGOUT --------------------
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

# -------------------- RUN APP --------------------
if __name__ == '__main__':
    app.run(debug=True)
