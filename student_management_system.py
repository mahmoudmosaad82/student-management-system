
import tkinter as tk
import psycopg2

# Create the main window
root = tk.Tk()
root.title("Student Management System")
root.config(bg="#2D3A45")

# Get the screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Set the width and height of the form
form_width = 300
form_height = 150

# Calculate the x and y coordinates for the form to be centered on the screen
#x = (screen_width // 2) - (form_width // 2)
#y = (screen_height // 2) - (form_height // 2)

# Set the geometry of the form to be centered on the screen
#root.geometry(f"{form_width}x{form_height}+{x}+{y}")
root.geometry("800x600")

# Create the form frame with a gray background
form = tk.Frame(root, bg="#3A4750")
form.place(relx=0.5, rely=0.5, anchor="center")

# Create a label for the student ID
id_label = tk.Label(form, text="Student ID:", anchor="w", bg="#3A4750",fg='white')
id_label.grid(row=0, column=0)

# Create an entry field for the student ID
id_entry = tk.Entry(form)
id_entry.grid(row=0, column=1)

# Create a label to display the student details
details_label = tk.Label(form, text="", bg="#3A4750")
details_label.grid(row=1, column=0, columnspan=2)


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
        # Create a string to display the student details
        details_text = "Name: {}\nProgram: {} ({})\n\nCourses:".format(student_data[1], student_data[2], student_data[3])

        # Get all courses and grades for the student from the database
        cur.execute('SELECT * FROM grades WHERE id=%s', (student_id,))
        course_data = cur.fetchall()

        for course in course_data:
            details_text += "\n{}: {}".format(course[1], course[2])

        details_text += "\n\nGPA: {}".format(student_data[4])

        # Update the label with the student details
        details_label.config(text=details_text, anchor="w", bg="#3A4750", fg="white")

    else:
        # Show an error message if the student ID is not found in the database
        details_label.config(text="Student ID not found", bg="#3A4750", fg="white")

    # Close the cursor and connection
    cur.close()
    conn.close()

# Create a button to show the student details
show_button = tk.Button(form, text="Show Details", command=show_details)
show_button.grid(row=2, column=0, columnspan=2)

# Start the main event loop
root.mainloop()
