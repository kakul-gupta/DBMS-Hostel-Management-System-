from flask import Flask, render_template, request, redirect
from db_config import get_connection
from datetime import date

app = Flask(__name__)

# Home Page
@app.route('/')
def index():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()
    conn.close()
    return render_template('index.html', students=students)

# Add Student
@app.route('/add', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        name = request.form['name']
        room = request.form['room']
        dob = request.form['dob']
        dept = request.form['dept']
        address = request.form['address']

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO students (name, room_no, dob, department, address) VALUES (%s,%s,%s,%s,%s)",
            (name, room, dob, dept, address)
        )
        conn.commit()
        conn.close()
        return redirect('/')

    return render_template('add_student.html')

# Attendance
@app.route('/attendance', methods=['GET', 'POST'])
def attendance():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()

    if request.method == 'POST':
        for student in students:
            status = request.form.get(f"status_{student['id']}")

            if status:
                cursor.execute(
                    "INSERT INTO attendance (student_id, date, status) VALUES (%s, CURDATE(), %s)",
                    (student['id'], status)
                )

        conn.commit()

    conn.close()
    return render_template('attendance.html', students=students)

# DELETE STUDENT
@app.route('/delete/<int:id>')
def delete_student(id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM students WHERE id = %s", (id,))
    conn.commit()
    conn.close()
    return redirect('/')


# EDIT STUDENT (GET + POST)
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_student(id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        name = request.form['name']
        room = request.form['room']
        dept = request.form['dept']

        cursor.execute(
            "UPDATE students SET name=%s, room_no=%s, department=%s WHERE id=%s",
            (name, room, dept, id)
        )
        conn.commit()
        conn.close()
        return redirect('/')

    cursor.execute("SELECT * FROM students WHERE id=%s", (id,))
    student = cursor.fetchone()
    conn.close()

    return render_template('edit_student.html', student=student)

if __name__ == '__main__':
    app.run(debug=True)