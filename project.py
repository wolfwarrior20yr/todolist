import datetime
import json
import sqlite3
import tkinter as tk
from tkinter import messagebox
from plyer import notification  # Install plyer using: pip install plyer

# Create a SQLite database and table
conn = sqlite3.connect('tasks.db')
c = conn.cursor()
c.execute('''
          CREATE TABLE IF NOT EXISTS tasks (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              task TEXT NOT NULL,
              due_date TEXT,
              completed BOOLEAN
          )
          ''')
conn.commit()

# Global variable to store tasks
tasks = []


def add_task():
    task = input("Enter a task: ")
    due_date = input("Enter due date (YYYY-MM-DD) or leave blank: ")
    tasks.append({"task": task, "due_date": due_date if due_date else None, "completed": False})
    print("Task added successfully!")


def view_tasks():
    if not tasks:
        print("No tasks to display.")
    else:
        for i, task in enumerate(tasks):
            print(f"{i + 1}. {task['task']} - Due: {task['due_date'] if task['due_date'] else 'None'}")


def mark_complete():
    view_tasks()
    task_index = int(input("Enter the number of the task to mark as complete: ")) - 1
    if 0 <= task_index < len(tasks):
        tasks[task_index]["completed"] = True
        print("Task marked as complete!")
    else:
        print("Invalid task number.")


def delete_task():
    view_tasks()
    task_index = int(input("Enter the number of the task to delete: ")) - 1
    if 0 <= task_index < len(tasks):
        del tasks[task_index]
        print("Task deleted successfully!")
    else:
        print("Invalid task number.")


def save_tasks():
    with open("tasks.json", "w") as file:
        json.dump(tasks, file)
    print("Tasks saved successfully!")


def load_tasks():
    global tasks
    try:
        with open("tasks.json", "r") as file:
            tasks = json.load(file)
        print("Tasks loaded successfully!")
    except FileNotFoundError:
        print("No saved tasks found.")


def show_notification(task):
    notification.notify(
        title='Task Reminder',
        message=f"Don't forget to complete task: {task}",
        app_name='To-Do List'
    )


def add_task_gui():
    task = entry_task.get()
    due_date = entry_due_date.get()
    tasks.append({"task": task, "due_date": due_date if due_date else None, "completed": False})
    listbox_tasks.insert(tk.END, f"{task} - Due: {due_date if due_date else 'None'}")
    show_notification(task)  # Notify user when a new task is added
    entry_task.delete(0, tk.END)
    entry_due_date.delete(0, tk.END)


def view_tasks_gui():
    listbox_tasks.delete(0, tk.END)
    for i, task in enumerate(tasks):
        listbox_tasks.insert(tk.END, f"{i + 1}. {task['task']} - Due: {task['due_date'] if task['due_date'] else 'None'}")


def mark_complete_gui():
    selected_task = listbox_tasks.curselection()
    if selected_task:
        task_index = selected_task[0]
        tasks[task_index]["completed"] = True
        show_notification(tasks[task_index]['task'] + ' is marked as complete!')
        view_tasks_gui()
    else:
        messagebox.showwarning("Warning", "Select a task to mark as complete.")


def delete_task_gui():
    selected_task = listbox_tasks.curselection()
    if selected_task:
        task_index = selected_task[0]
        del tasks[task_index]
        show_notification('Task deleted successfully!')
        view_tasks_gui()
    else:
        messagebox.showwarning("Warning", "Select a task to delete.")


# Create the main window
window = tk.Tk()
window.title("To-Do List")

# Create GUI components
label_task = tk.Label(window, text="Task:")
entry_task = tk.Entry(window)
label_due_date = tk.Label(window, text="Due Date (YYYY-MM-DD):")
entry_due_date = tk.Entry(window)
button_add_task = tk.Button(window, text="Add Task", command=add_task_gui)
listbox_tasks = tk.Listbox(window)
button_view_tasks = tk.Button(window, text="View Tasks", command=view_tasks_gui)
button_mark_complete = tk.Button(window, text="Mark as Complete", command=mark_complete_gui)
button_delete_task = tk.Button(window, text="Delete Task", command=delete_task_gui)

# Place GUI components on the window
label_task.grid(row=0, column=0)
entry_task.grid(row=0, column=1)
label_due_date.grid(row=1, column=0)
entry_due_date.grid(row=1, column=1)
button_add_task.grid(row=2, column=0, columnspan=2, pady=10)
listbox_tasks.grid(row=3, column=0, columnspan=2, rowspan=5, pady=10)
button_view_tasks.grid(row=8, column=0, columnspan=2, pady=10)
button_mark_complete.grid(row=9, column=0, pady=10)
button_delete_task.grid(row=9, column=1, pady=10)

# Load tasks from the database
c.execute('SELECT * FROM tasks')
rows = c.fetchall()
for row in rows:
    tasks.append({
        "task": row[1],
        "due_date": row[2] if row[2] else None,
        "completed": row[3]
    })

# Display the GUI
window.mainloop()

# Save tasks to the database before exiting
for task in tasks:
    c.execute('''
              INSERT INTO tasks (task, due_date, completed)
              VALUES (?, ?, ?)
              ''', (task["task"], task["due_date"], task["completed"]))

conn.commit()
conn.close()
