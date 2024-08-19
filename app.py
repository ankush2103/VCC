from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_mysqldb import MySQL
import MySQLdb.cursors

app = Flask(__name__)

# MySQL configurations
app.config['MYSQL_HOST'] = '10.128.0.7'
app.config['MYSQL_USER'] = 'vmg23ai2007_user'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'mydb'

# Initialize MySQL
mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create_table/<table_name>')
def create_table(table_name):
    cursor = mysql.connection.cursor()

    if table_name == 'student':
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS student (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100),
                age INT,
                grade VARCHAR(10)
            )
        ''')
    elif table_name == 'teacher':
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS teacher (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100),
                subject VARCHAR(100),
                experience_years INT
            )
        ''')

    mysql.connection.commit()
    cursor.close()
    return f'Table {table_name} created successfully!'

@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        grade = request.form['grade']

        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO student (name, age, grade) VALUES (%s, %s, %s)', (name, age, grade))
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('index'))

    return render_template('add_student.html')

@app.route('/add_teacher', methods=['GET', 'POST'])
def add_teacher():
    if request.method == 'POST':
        name = request.form['name']
        subject = request.form['subject']
        experience_years = request.form['experience_years']

        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO teacher (name, subject, experience_years) VALUES (%s, %s, %s)', (name, subject, experience_years))
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('index'))

    return render_template('add_teacher.html')

@app.route('/view_table/<table_name>')
def view_table(table_name):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    if table_name == 'student':
        cursor.execute('SELECT * FROM student')
    elif table_name == 'teacher':
        cursor.execute('SELECT * FROM teacher')

    rows = cursor.fetchall()
    cursor.close()

    return render_template('view_table.html', table_name=table_name, rows=rows)

@app.route('/add_student_json', methods=['POST'])
def add_student_json():
    data = request.get_json()
    name = data['name']
    age = data['age']
    grade = data['grade']

    cursor = mysql.connection.cursor()
    cursor.execute('INSERT INTO student (name, age, grade) VALUES (%s, %s, %s)', (name, age, grade))
    mysql.connection.commit()
    cursor.close()
    
    return jsonify({'message': 'Student added successfully!'})

@app.route('/add_teacher_json', methods=['POST'])
def add_teacher_json():
    data = request.get_json()
    name = data['name']
    subject = data['subject']
    experience_years = data['experience_years']

    cursor = mysql.connection.cursor()
    cursor.execute('INSERT INTO teacher (name, subject, experience_years) VALUES (%s, %s, %s)', (name, subject, experience_years))
    mysql.connection.commit()
    cursor.close()
    
    return jsonify({'message': 'Teacher added successfully!'})

if __name__ == '__main__':
    app.run(debug=True)
