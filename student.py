import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# Database Connection
conn = sqlite3.connect("students.db")
cursor = conn.cursor()

# Create Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    student_id INTEGER PRIMARY KEY,
    name TEXT,
    age INTEGER,
    gender TEXT,
    course TEXT,
    marks REAL
)
""")

conn.commit()


# Add Student
def add_student():
    try:
        student_id = int(input("Enter Student ID: "))
        name = input("Enter Name: ")
        age = int(input("Enter Age: "))
        gender = input("Enter Gender: ")
        course = input("Enter Course: ")
        marks = float(input("Enter Marks: "))

        cursor.execute(
            "INSERT INTO students VALUES (?, ?, ?, ?, ?, ?)",
            (student_id, name, age, gender, course, marks)
        )

        conn.commit()
        print("Student Added Successfully!")

    except sqlite3.IntegrityError:
        print("Student ID already exists!")
    except ValueError:
        print("Invalid input!")


# View Students
def view_students():
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()

    if len(students) == 0:
        print("No Records Found")
        return

    print("\n------ STUDENT RECORDS ------")

    for student in students:
        print(student)


# Search Student
def search_student():
    sid = int(input("Enter Student ID: "))

    cursor.execute(
        "SELECT * FROM students WHERE student_id = ?",
        (sid,)
    )

    student = cursor.fetchone()

    if student:
        print("\nStudent Found:")
        print(student)
    else:
        print("Student Not Found")


# Update Student
def update_student():
    sid = int(input("Enter Student ID: "))
    new_marks = float(input("Enter New Marks: "))

    cursor.execute(
        "UPDATE students SET marks = ? WHERE student_id = ?",
        (new_marks, sid)
    )

    conn.commit()

    if cursor.rowcount > 0:
        print("Student Updated Successfully!")
    else:
        print("Student Not Found")


# Delete Student
def delete_student():
    sid = int(input("Enter Student ID: "))

    cursor.execute(
        "DELETE FROM students WHERE student_id = ?",
        (sid,)
    )

    conn.commit()

    if cursor.rowcount > 0:
        print("Student Deleted Successfully!")
    else:
        print("Student Not Found")


# View Topper
def view_topper():
    cursor.execute("""
        SELECT *
        FROM students
        ORDER BY marks DESC
        LIMIT 1
    """)
    topper = cursor.fetchone()

    if topper:
        print("\nTopper Details:")
        print(topper)
    else:
        print("No Data Found")


# Export to Excel
def export_excel():
    df = pd.read_sql_query(
        "SELECT * FROM students",
        conn
    )

    df.to_excel(
        "students_report.xlsx",
        index=False
    )

    print("Excel File Created Successfully!")


# Bar Chart
def bar_chart():
    df = pd.read_sql_query(
        "SELECT name, marks FROM students",
        conn
    )

    if len(df) == 0:
        print("No Data Available")
        return

    plt.figure(figsize=(8, 5))
    plt.bar(df["name"], df["marks"])

    plt.title("Student Marks")
    plt.xlabel("Student Name")
    plt.ylabel("Marks")

    plt.savefig("marks_graph.png")
    plt.show()


# Pie Chart
def pie_chart():
    df = pd.read_sql_query(
        "SELECT name, marks FROM students",
        conn
    )

    if len(df) == 0:
        print("No Data Available")
        return

    plt.figure(figsize=(7, 7))

    plt.pie(
        df["marks"],
        labels=df["name"],
        autopct="%1.1f%%"
    )

    plt.title("Marks Distribution")

    plt.savefig("marks_pie_chart.png")
    plt.show()


# Main Menu
while True:

    print("\n========== STUDENT MANAGEMENT SYSTEM ==========")
    print("1. Add Student")
    print("2. View Students")
    print("3. Search Student")
    print("4. Update Student")
    print("5. Delete Student")
    print("6. View Topper")
    print("7. Export To Excel")
    print("8. Show Bar Chart")
    print("9. Show Pie Chart")
    print("10. Exit")
    choice = input("Enter Choice: ")

    if choice == "1":
        add_student()

    elif choice == "2":
        view_students()

    elif choice == "3":
        search_student()

    elif choice == "4":
        update_student()

    elif choice == "5":
        delete_student()

    elif choice == "6":
        view_topper()

    elif choice == "7":
        export_excel()

    elif choice == "8":
        bar_chart()

    elif choice == "9":
        pie_chart()

    elif choice == "10":
        print("Thank You")
        conn.close()
        break

    else:
        print("Invalid Choice")