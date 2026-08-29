# Student Task & Productivity Manager

> A simple, user-friendly Python desktop application designed to help students organize, prioritize, track, and manage their academic and personal tasks efficiently.

[![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)](https://www.python.org/)
[![GUI](https://img.shields.io/badge/GUI-Tkinter-orange)](https://docs.python.org/3/library/tkinter.html)
[![Storage](https://img.shields.io/badge/Storage-Local%20JSON-green)](https://www.json.org/)
[![Status](https://img.shields.io/badge/Status-Completed-success)]()

---

## Overview

**Student Task & Productivity Manager** is a Python-based desktop productivity application developed to simplify everyday task management for students.

The application allows users to create tasks, assign priorities and deadlines, update existing tasks, mark tasks as completed, filter tasks, and export task information.

The project demonstrates practical implementation of:

* Python Programming
* Object-Oriented Programming (OOP)
* GUI Development
* File Handling
* JSON Data Storage
* Event-Driven Programming
* Task Management Logic

---

## Features

### Task Management

* Add new tasks
* Edit existing tasks
* Delete tasks
* Mark tasks as completed
* View all available tasks

### Priority Management

Tasks can be organized according to priority:

* High
* Medium
* Low

### Deadline Tracking

* Assign deadlines to tasks
* View upcoming tasks
* Identify overdue tasks

### Task Filtering

Filter tasks based on their current status:

* All Tasks
* Pending
* Completed

### Local Data Storage

Task information is stored locally using a JSON file, allowing the application to preserve data between sessions without requiring an external database.

### Data Export

Task information can be exported for backup or further analysis.

---

## Technologies Used

| Technology    | Purpose                       |
| ------------- | ----------------------------- |
| Python        | Core programming language     |
| Tkinter       | Graphical User Interface      |
| JSON          | Local data storage            |
| File Handling | Reading and writing task data |
| OOP           | Application architecture      |

---

## Project Structure

```text
Student-Task-Productivity-Manager/
│
├── main.py
├── requirements.txt
├── tasks.json
├── README.md
└── screenshots/
    └── application.png
```

> The exact files may vary depending on the final project implementation.

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR-USERNAME/student-task-productivity-manager.git
```

### 2. Enter the Project Directory

```bash
cd student-task-productivity-manager
```

### 3. Create a Virtual Environment

```bash
python3 -m venv venv
```

### 4. Activate the Virtual Environment

**Linux / macOS**

```bash
source venv/bin/activate
```

**Windows**

```bash
venv\Scripts\activate
```

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

### 6. Run the Application

```bash
python3 main.py
```

---

## Linux Tkinter Setup

If Tkinter is not installed on Ubuntu/Debian-based systems:

```bash
sudo apt update
sudo apt install python3-tk
```

Then run:

```bash
python3 main.py
```

---

## How to Use

### 1. Add a Task

Enter the required information such as:

* Task title
* Description
* Priority
* Deadline

Then click **Add Task**.

### 2. Edit a Task

Select an existing task and choose the **Edit** option to update its information.

### 3. Complete a Task

Select a task and mark it as **Completed** once the work is finished.

### 4. Delete a Task

Select an unwanted task and click **Delete**.

### 5. Filter Tasks

Use the filtering options to quickly view:

```text
All Tasks
Pending Tasks
Completed Tasks
```

### 6. Export Tasks

Use the export functionality to save task information for backup or future use.

---

## Application Workflow

```text
              ┌──────────────────┐
              │   Start Program  │
              └────────┬─────────┘
                       │
                       ▼
              ┌──────────────────┐
              │   Load Tasks     │
              │   from JSON      │
              └────────┬─────────┘
                       │
                       ▼
              ┌──────────────────┐
              │   Main Dashboard │
              └────────┬─────────┘
                       │
          ┌────────────┼────────────┐
          ▼            ▼            ▼
      Add Task      Edit Task    Delete Task
          │            │            │
          └────────────┼────────────┘
                       ▼
              ┌──────────────────┐
              │ Update Task Data │
              └────────┬─────────┘
                       │
                       ▼
              ┌──────────────────┐
              │ Save to JSON     │
              └────────┬─────────┘
                       │
                       ▼
              ┌──────────────────┐
              │ Continue / Exit  │
              └──────────────────┘
```

---

## Data Management

The application uses a local JSON file to store task information.

Example:

```json
{
    "title": "Complete Python Assignment",
    "priority": "High",
    "deadline": "2026-08-30",
    "status": "Pending"
}
```

This approach keeps the project lightweight and eliminates the need for a database server.

---

## Learning Outcomes

Through this project, the following concepts were practically implemented:

* Python fundamentals
* Object-Oriented Programming
* Classes and objects
* Functions and modules
* Exception handling
* GUI development with Tkinter
* JSON serialization and deserialization
* File handling
* Event-driven programming
* User input validation
* Application workflow design

---

## Future Improvements

The project can be extended with:

* Desktop task reminders
* Productivity statistics
* Task completion charts
* SQLite database integration
* Cloud synchronization
* User authentication
* Dark mode
* Mobile application
* AI-powered task prioritization
* Calendar integration

---

## Application Preview

Add screenshots of your application inside the `screenshots` folder and display them here:

```markdown
![Application Screenshot](screenshots/application.png)
```

---

## Project Status

**Status:** Completed

This project was developed as a Python internship project to demonstrate practical Python programming, GUI development, data management, and software development skills.

---

## Developer

**Parthu**

Python Developer Intern | B.Tech CSE (AI & ML)

---

## License

This project is created for educational and internship purposes.

---

<p align="center">
  Built with ❤️ using Python
</p>
