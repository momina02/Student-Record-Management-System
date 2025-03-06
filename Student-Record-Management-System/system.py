from flask import Flask, request, jsonify, render_template
import mysql.connector
import os

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="sms"
)


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/add_student', methods=['POST'])
def add_student():
    if request.method == 'POST':
        student_id = request.form['student-id']
        student_name = request.form['student-name']
        student_degree = request.form['student-degree']
        student_year = request.form['student-year']
        student_course = request.form['student-course']

        cursor = db.cursor()
        query = "INSERT INTO students (student_id, student_name, student_degree, student_year, student_course) VALUES (%s, %s, %s, %s, %s)"
        values = (student_id, student_name, student_degree, student_year, student_course)

        cursor.execute(query, values)
        db.commit()
        cursor.close()

        return "Student added successfully"


@app.route('/update_student', methods=['POST'])
def update_student():
    if request.method == 'POST':
        student_id = request.form['student-id']
        new_student_name = request.form['new-student-name']

        cursor = db.cursor()
        query = "UPDATE students SET student_name = %s WHERE student_id = %s"
        values = (new_student_name, student_id)

        cursor.execute(query, values)
        db.commit()
        cursor.close()

        return "Student updated successfully"


@app.route('/delete_student', methods=['POST'])
def delete_student():
    if request.method == 'POST':
        student_id = request.form['student-id']
        cursor = db.cursor()
        query = "DELETE FROM students WHERE student_id = %s"
        values = (student_id,)

        cursor.execute(query, values)
        db.commit()
        cursor.close()

        return "Student deleted successfully"


# @app.route('/filter_students', methods=['POST'])
# def filter_students():
#     if request.method == 'POST':
#         student_degree = request.form['student-degree']

#         # Use dictionary cursor for column names
#         cursor = db.cursor(dictionary=True)
#         query = "SELECT * FROM students WHERE student_degree = %s"
#         values = (student_degree,)

#         cursor.execute(query, values)
#         results = cursor.fetchall()
#         cursor.close()

#         response_data = []
#         for row in results:
#             row_data = {}
#             for column_name, value in row.items():
#                 row_data[column_name] = value
#             response_data.append(row_data)

#         return jsonify(response_data)

@app.route('/filter_students', methods=['GET'])
def filter_students():
    if request.method == 'GET':
        student_degree = request.args.get('student-degree')
        student_course = request.args.get('student-course')

        cursor = db.cursor(dictionary=True)
        query = "SELECT * FROM students WHERE student_degree = %s AND student_course = %s"
        values = (student_degree, student_course)

        cursor.execute(query, values)
        results = cursor.fetchall()
        cursor.close()

        return render_template('index.html', filter_results=results)



if __name__ == '__main__':
    app.run(debug=True)
