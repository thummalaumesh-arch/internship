# Student Task & Productivity Manager

> A modern, dark-themed Python desktop application that helps students organize, prioritize, track, and export their academic and personal tasks — powered by SQLite, CustomTkinter, and Matplotlib.

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)](https://www.python.org/)
[![GUI](https://img.shields.io/badge/GUI-CustomTkinter-blueviolet)](https://github.com/TomSchimansky/CustomTkinter)
[![Database](https://img.shields.io/badge/Storage-SQLite-lightgrey?logo=sqlite)](https://sqlite.org/)
[![License](https://img.shields.io/badge/License-Educational-green)]()
[![Status](https://img.shields.io/badge/Status-Working-success)]()

---

## Overview

**Student Task & Productivity Manager** is a fully-featured Python desktop productivity application built with a clean, modular package architecture. It gives students a modern dark-mode GUI to manage tasks end-to-end — from creation through analytics and export.

The app runs locally with **no internet connection required** and persists all data in a lightweight SQLite database.

---

## Features

### 📊 Dashboard
- At-a-glance statistics: Total, Completed, Pending, Overdue, Completion Rate
- Upcoming tasks list (next 7 pending tasks)
- Interactive calendar widget

### ✓ Task Manager
- Add, edit, and delete tasks
- Toggle tasks between **Pending** and **Completed**
- Filter by status, priority, and category
- Full-text search across title, description, and category
- Scrollable task table with sortable columns

### 📈 Analytics
- Pie chart: Task completion ratio
- Bar chart: High-priority, overdue, and completed task counts
- Powered by Matplotlib embedded directly in the GUI

### 📤 Export
- Export filtered task lists to **CSV** (via Pandas)
- Export professional **PDF reports** (via ReportLab) with styled table headers

### 🎨 UI/UX
- Dark / Light / System appearance modes
- CustomTkinter modern widget set
- Responsive layout — minimum window size enforced

---

## Technologies Used

| Technology        | Purpose                                    |
| ----------------- | ------------------------------------------ |
| Python 3.10+      | Core programming language                  |
| CustomTkinter     | Modern dark-mode GUI framework             |
| Tkinter / ttk     | Base widgets (Treeview, dialogs)           |
| tkcalendar        | Date picker and calendar widget            |
| SQLite3           | Local persistent task database             |
| Matplotlib        | Embedded analytics charts                  |
| Pandas            | CSV data export                            |
| ReportLab         | PDF report generation                      |

---

## Project Structure

```
Student_task_productivity_manager/
│
├── __init__.py          # Package marker
├── __main__.py          # Entry point for `python -m` execution
├── gui.py               # Main application window + all UI views
├── database.py          # SQLite database layer (CRUD + queries)
├── services.py          # Business logic, validation, CSV/PDF export
├── requirements.txt     # Python dependencies
└── README.md
```

> Data and logs are stored **outside** the package folder (sibling `data/` and `logs/` directories) and are excluded from version control via `.gitignore`.

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/thummalaumesh-arch/internship.git
cd internship
```

### 2. (Recommended) Create a Virtual Environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux / macOS
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Running the Application

From the **parent directory** of the package (i.e., one level above `Student_task_productivity_manager/`):

```bash
# Recommended — runs as a package module
python -m Student_task_productivity_manager

# Alternative — run directly
python Student_task_productivity_manager/gui.py
```

---

## How to Use

| Action            | How                                                             |
| ----------------- | --------------------------------------------------------------- |
| **Add Task**      | Click `+ Add Task` → fill in title, category, priority, deadline, description → Save |
| **Edit Task**     | Select a row in Task Manager → click `✎ Edit`                  |
| **Complete Task** | Select a row → click `✓ Complete / Reopen` (toggles status)    |
| **Delete Task**   | Select a row → click `🗑 Delete` → confirm                      |
| **Filter**        | Use the Status / Priority / Category dropdowns                  |
| **Search**        | Type in the search box → click Search                           |
| **Export CSV**    | Task Manager → `Export CSV` → choose save location             |
| **Export PDF**    | Task Manager → `Export PDF` → choose save location             |
| **Analytics**     | Click `📈 Analytics` in the sidebar                             |
| **Theme**         | Use the Appearance dropdown at the bottom of the sidebar        |

---

## Application Architecture

```
gui.py  ──imports──▶  database.py   (SQLite CRUD)
        ──imports──▶  services.py   (Validation + Export)
```

- **`Database`** — context-manager-based connection handling; creates tables on first run
- **`TaskService`** — stateless validation and task normalization
- **`export_csv` / `export_pdf`** — standalone export functions using Pandas and ReportLab
- **`TaskManagerApp`** — main `ctk.CTk` window; view switching via `show_dashboard / show_tasks / show_analytics`
- **`TaskDialog`** — modal `ctk.CTkToplevel` for add/edit workflows

---

## Data Storage

All task data is stored in a local SQLite file at:

```
../data/tasks.db   (relative to the package; never committed to git)
```

Schema:

```sql
CREATE TABLE tasks (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    title        TEXT NOT NULL,
    description  TEXT DEFAULT '',
    category     TEXT DEFAULT 'General',
    priority     TEXT NOT NULL DEFAULT 'Medium',
    deadline     TEXT NOT NULL,
    status       TEXT NOT NULL DEFAULT 'Pending',
    created_at   TEXT NOT NULL,
    completed_at TEXT
);
```

---

## Learning Outcomes

- Python package structure and relative imports
- Object-Oriented Programming (classes, inheritance, static methods)
- SQLite3 with context managers and parameterized queries
- GUI development with CustomTkinter and Tkinter ttk
- Embedded Matplotlib charts in Tkinter windows
- Data export with Pandas (CSV) and ReportLab (PDF)
- Exception handling and input validation
- Application logging with Python's `logging` module

---

## Future Improvements

- Desktop notifications for upcoming deadlines
- Recurring task support
- Cloud sync (Firebase / Supabase)
- User profiles and multi-user support
- AI-powered priority suggestions
- Mobile companion app

---

## Developer

**Umesh Thummala**  
Python Developer Intern | B.Tech CSE  

---

## License

This project was developed for educational and internship demonstration purposes.

---

<p align="center">Built with ❤️ using Python & CustomTkinter</p>
