import tkinter as tk
import psycopg2

# Create the main window
root = tk.Tk()
root.title("Student Management System")

# Create a label for the student ID
id_label = tk.Label(root, text="Student ID:")
id_label.grid(row=0, column=0)

# Create an entry field for the student ID
id_entry = tk.Entry(root)
id_entry.grid(row=0, column=1)

def show_details():
    # Get the student ID from the entry field
    student_id = id_entry.get()

    # Connect to the database
    conn = psycopg2.connect(
        host="localhost",
        port="5432",
        database="db",
        user="postgres",
        # password="mypassword"
    )

    # Create a cursor object
    cur = conn.cursor()

    # Get the student details from the database
    cur.execute('SELECT * FROM students WHERE id=%s', (student_id,))
    student_data = cur.fetchone()

    if student_data is not None:
        # Create a new window to display the student details
        details_window = tk.Toplevel()
        details_window.title("Student Details")

        # Create labels to display the student details
        name_label = tk.Label(details_window, text="Name: " + student_data[1])
        name_label.pack()
        program_label = tk.Label(details_window, text="Program: " + str(student_data[2]) + " (" + str(student_data[3] )+ ")")

        
        program_label.pack()

        # Get all courses and grades for the student from the database
        cur.execute('SELECT * FROM grades WHERE id=%s', (student_id,))
        course_data = cur.fetchall()

        # Create a label to display the courses and grades
        courses_label = tk.Label(details_window, text="Courses:")
        courses_label.pack()

        for course in course_data:
            course_label = tk.Label(details_window, text=course[1] + ": " + str(course[2]))
            course_label.pack()

        gpa_label = tk.Label(details_window, text="GPA: " + str(student_data[4]))
        gpa_label.pack()

    else:
        # Show an error message if the student ID is not found in the database
        error_label = tk.Label(root, text="Student ID not found")
        error_label.grid(row=2, column=0, columnspan=2)

    # Close the cursor and connection
    cur.close()
    conn.close()



# Create a button to show the student details
show_button = tk.Button(root, text="Show Details", command=show_details)
show_button.grid(row=1, column=0, columnspan=2)

# Start the main event loop
root.mainloop()
