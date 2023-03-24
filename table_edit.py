import tkinter as tk
from tkinter import ttk
import psycopg2

# Create the main window
root = tk.Tk()
root.title("Student Management System")
root.config(bg="#2D3A45")

# Set the width and height of the form
form_width = 800
form_height = 600

# Set the geometry of the form to be centered on the screen
root.geometry(f"{form_width}x{form_height}+100+100")

# Create the form frame with a gray background
form = tk.Frame(root, bg="#3A4750")
form.place(relx=0.5, rely=0.5, anchor="center")

# Create a label for the student ID
id_label = tk.Label(form, text="Student ID:", anchor="w", bg="#3A4750", fg='white')
id_label.grid(row=0, column=0)

# Create an entry field for the student ID
id_entry = tk.Entry(form)
id_entry.grid(row=0, column=1)

# Create a Treeview widget to display the student details
details_tree = ttk.Treeview(form, columns=("Program", "Year", "Course", "Grade", "GPA"))
details_tree.grid(row=1, column=0, columnspan=2)
details_tree.heading("#0", text="Name")
details_tree.heading("Program", text="Program")
details_tree.heading("Year", text="Year")
details_tree.heading("Course", text="Course")
details_tree.heading("Grade", text="Grade")
details_tree.heading("GPA", text="GPA")

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
        # Clear the existing data in the Treeview widget
        details_tree.delete(*details_tree.get_children())

        # Create a string to display the student details
        name = student_data[1]
        program = student_data[2]
        year = student_data[3]
        gpa = student_data[4]
        details_tree.insert("", tk.END, text=name, values=(program, year, "", "", gpa))

        # Get all courses and grades for the student from the database
        cur.execute('SELECT * FROM grades WHERE id=%s', (student_id,))
        course_data = cur.fetchall()

        for course in course_data:
            course_name = course[1]
            grade = course[2]
            details_tree.insert("", tk.END, text="", values=(program, year, course_name, grade, ""))

    else:
        # Show an error message if the student ID is not found in the database
        details_tree.delete(*details_tree.get_children())
        details_tree.insert("", tk.END, text="Student ID not found")

    # Close the cursor and connection
    cur.close()
    conn.close()

# Create a button to show the student details
show_button = tk.Button(form, text="Show Details", command=show_details)
show_button.grid(row=2, column=0, columnspan=2)

# Start the main event loop
root.mainloop()
