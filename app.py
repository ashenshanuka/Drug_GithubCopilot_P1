from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
import MySQLdb.cursors

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# MySQL configurations
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1234'
app.config['MYSQL_DB'] = 'pharmacy_copilot_db'
app.config['MYSQL_HOST'] = 'localhost'

mysql = MySQL(app)

@app.route('/')
def index():
    search_query = request.args.get('search')
    conn = mysql.connection
    cursor = conn.cursor(MySQLdb.cursors.DictCursor)
    
    if search_query:
        cursor.execute("SELECT * FROM drugs WHERE name LIKE %s OR id LIKE %s", ('%' + search_query + '%', '%' + search_query + '%'))
    else:
        cursor.execute("SELECT * FROM drugs")
    
    data = cursor.fetchall()
    cursor.close()
    return render_template('index.html', drugs=data)

@app.route('/add', methods=['GET', 'POST'])
def add_drug():
    if request.method == 'POST':
        name = request.form['name']
        quantity = request.form['quantity']
        price = request.form['price']
        expiration_date = request.form['expiration_date']
        
        if name and quantity and price and expiration_date:
            conn = mysql.connection
            cursor = conn.cursor()
            cursor.execute("INSERT INTO drugs (name, quantity, price, expiration_date) VALUES (%s, %s, %s, %s)", (name, quantity, price, expiration_date))
            conn.commit()
            flash('Drug Added Successfully')
            return redirect(url_for('index'))
        else:
            flash('Please fill out all fields')
            return redirect(url_for('add_drug'))
    return render_template('add_drug.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_drug(id):
    conn = mysql.connection
    cursor = conn.cursor(MySQLdb.cursors.DictCursor)
    
    if request.method == 'POST':
        name = request.form['name']
        quantity = request.form['quantity']
        price = request.form['price']
        expiration_date = request.form['expiration_date']
        
        cursor.execute("""
            UPDATE drugs
            SET name=%s, quantity=%s, price=%s, expiration_date=%s
            WHERE id=%s
        """, (name, quantity, price, expiration_date, id))
        conn.commit()
        flash('Drug Updated Successfully')
        return redirect(url_for('index'))
    
    cursor.execute("SELECT * FROM drugs WHERE id=%s", (id,))
    data = cursor.fetchone()
    cursor.close()
    return render_template('edit_drug.html', drug=data)

@app.route('/delete/<int:id>', methods=['GET'])
def delete_drug(id):
    conn = mysql.connection
    cursor = conn.cursor()
    cursor.execute("DELETE FROM drugs WHERE id=%s", (id,))
    conn.commit()
    flash('Drug Deleted Successfully')
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)