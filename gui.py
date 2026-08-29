import tkinter as tk

from tkinter import ttk

from tkinter import messagebox

from tkinter import filedialog

from datetime import datetime

import customtkinter as ctk

from tkcalendar import DateEntry

import matplotlib.pyplot as plt

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg
)

from .database import Database

from .services import (
    TaskService,
    export_csv,
    export_pdf
)


ctk.set_appearance_mode("dark")

ctk.set_default_color_theme("blue")


class TaskDialog(ctk.CTkToplevel):

    def __init__(
        self,
        parent,
        on_save,
        task=None
    ):

        super().__init__(parent)

        self.on_save = on_save

        self.task = task

        self.title(
            "Edit Task"
            if task
            else "Add Task"
        )

        self.geometry(
            "520x560"
        )

        self.resizable(
            False,
            False
        )

        self.transient(parent)

        self.grab_set()

        self.grid_columnconfigure(
            1,
            weight=1
        )

        title = (
            "Edit Task"
            if task
            else "Add New Task"
        )

        ctk.CTkLabel(

            self,

            text=title,

            font=ctk.CTkFont(
                size=24,
                weight="bold"
            )

        ).grid(

            row=0,

            column=0,

            columnspan=2,

            padx=25,

            pady=(25, 20)

        )

        self.title_var = tk.StringVar(

            value=(
                task["title"]
                if task
                else ""
            )

        )

        self.category_var = tk.StringVar(

            value=(
                task["category"]
                if task
                else "General"
            )

        )

        self.priority_var = tk.StringVar(

            value=(
                task["priority"]
                if task
                else "Medium"
            )

        )

        self.create_entry(
            "Task Title",
            self.title_var,
            1
        )

        self.create_entry(
            "Category",
            self.category_var,
            2
        )

        ctk.CTkLabel(
            self,
            text="Priority"
        ).grid(
            row=3,
            column=0,
            sticky="w",
            padx=25,
            pady=10
        )

        ctk.CTkComboBox(

            self,

            variable=self.priority_var,

            values=list(
                TaskService.PRIORITIES
            ),

            width=280

        ).grid(

            row=3,

            column=1,

            padx=25,

            pady=10,

            sticky="ew"

        )

        ctk.CTkLabel(
            self,
            text="Deadline"
        ).grid(
            row=4,
            column=0,
            sticky="w",
            padx=25,
            pady=10
        )

        self.deadline = DateEntry(

            self,

            width=25,

            date_pattern="yyyy-mm-dd",

            borderwidth=2

        )

        self.deadline.grid(

            row=4,

            column=1,

            padx=25,

            pady=10,

            sticky="w"

        )

        if task:

            self.deadline.set_date(

                datetime.strptime(
                    task["deadline"],
                    "%Y-%m-%d"
                )

            )

        ctk.CTkLabel(
            self,
            text="Description"
        ).grid(
            row=5,
            column=0,
            sticky="nw",
            padx=25,
            pady=10
        )

        self.description = ctk.CTkTextbox(

            self,

            width=280,

            height=130

        )

        self.description.grid(

            row=5,

            column=1,

            padx=25,

            pady=10,

            sticky="ew"

        )

        if task:

            self.description.insert(

                "1.0",

                task["description"]

            )

        ctk.CTkButton(

            self,

            text="Save Task",

            command=self.save,

            height=40,

            font=ctk.CTkFont(
                weight="bold"
            )

        ).grid(

            row=6,

            column=0,

            columnspan=2,

            padx=25,

            pady=25,

            sticky="ew"

        )

    def create_entry(
        self,
        label,
        variable,
        row
    ):

        ctk.CTkLabel(
            self,
            text=label
        ).grid(
            row=row,
            column=0,
            sticky="w",
            padx=25,
            pady=10
        )

        ctk.CTkEntry(

            self,

            textvariable=variable,

            width=280

        ).grid(

            row=row,

            column=1,

            padx=25,

            pady=10,

            sticky="ew"

        )

    def save(self):

        try:

            task = TaskService.normalize_task(

                self.title_var.get(),

                self.description.get(
                    "1.0",
                    "end"
                ).strip(),

                self.category_var.get(),

                self.priority_var.get(),

                self.deadline.get_date()
                .strftime("%Y-%m-%d")

            )

            task_id = (
                self.task["id"]
                if self.task
                else None
            )

            self.on_save(
                task,
                task_id
            )

            self.destroy()

        except ValueError as exc:

            messagebox.showerror(
                "Validation Error",
                str(exc),
                parent=self
            )


class TaskManagerApp(ctk.CTk):

    def __init__(self):

        super().__init__()

        self.db = Database()

        self.title(
            "Student Task & Productivity Manager"
        )

        self.geometry(
            "1250x760"
        )

        self.minsize(
            1050,
            650
        )

        self.search_var = tk.StringVar()

        self.status_var = tk.StringVar(
            value="All"
        )

        self.priority_var = tk.StringVar(
            value="All"
        )

        self.category_var = tk.StringVar(
            value="All"
        )

        self.build_layout()

        self.show_dashboard()

    def build_layout(self):

        self.grid_columnconfigure(
            1,
            weight=1
        )

        self.grid_rowconfigure(
            0,
            weight=1
        )

        self.sidebar = ctk.CTkFrame(

            self,

            width=220,

            corner_radius=0

        )

        self.sidebar.grid(

            row=0,

            column=0,

            sticky="nsew"

        )

        self.sidebar.grid_propagate(
            False
        )

        ctk.CTkLabel(

            self.sidebar,

            text="STUDENT\nPRODUCTIVITY",

            font=ctk.CTkFont(
                size=22,
                weight="bold"
            )

        ).pack(

            pady=(35, 35)

        )

        buttons = [

            (
                "📊 Dashboard",
                self.show_dashboard
            ),

            (
                "✓ Task Manager",
                self.show_tasks
            ),

            (
                "📈 Analytics",
                self.show_analytics
            )

        ]

        for text, command in buttons:

            ctk.CTkButton(

                self.sidebar,

                text=text,

                command=command,

                height=42,

                anchor="w",

                fg_color="transparent"

            ).pack(

                fill="x",

                padx=15,

                pady=5

            )

        ctk.CTkLabel(

            self.sidebar,

            text="Appearance"

        ).pack(

            side="bottom",

            pady=(0, 5)

        )

        ctk.CTkOptionMenu(

            self.sidebar,

            values=[
                "Dark",
                "Light",
                "System"
            ],

            command=ctk.set_appearance_mode

        ).pack(

            side="bottom",

            padx=25,

            pady=(0, 20),

            fill="x"

        )

        self.content = ctk.CTkFrame(

            self,

            corner_radius=0,

            fg_color="transparent"

        )

        self.content.grid(

            row=0,

            column=1,

            sticky="nsew",

            padx=20,

            pady=20

        )

        self.content.grid_rowconfigure(
            1,
            weight=1
        )

        self.content.grid_columnconfigure(
            0,
            weight=1
        )

        self.header = ctk.CTkFrame(

            self.content,

            fg_color="transparent"

        )

        self.header.grid(

            row=0,

            column=0,

            sticky="ew",

            pady=(0, 15)

        )

        self.header.grid_columnconfigure(
            0,
            weight=1
        )

        self.page_title = ctk.CTkLabel(

            self.header,

            text="Dashboard",

            font=ctk.CTkFont(
                size=28,
                weight="bold"
            )

        )

        self.page_title.grid(

            row=0,

            column=0,

            sticky="w"

        )

        ctk.CTkButton(

            self.header,

            text="+ Add Task",

            command=self.open_add_dialog,

            width=130,

            height=38

        ).grid(

            row=0,

            column=1,

            padx=5

        )

        self.body = ctk.CTkFrame(

            self.content,

            fg_color="transparent"

        )

        self.body.grid(

            row=1,

            column=0,

            sticky="nsew"

        )

        self.body.grid_columnconfigure(
            0,
            weight=1
        )

        self.body.grid_rowconfigure(
            1,
            weight=1
        )

    def clear_body(self):

        for widget in self.body.winfo_children():

            widget.destroy()

    def show_dashboard(self):

        self.page_title.configure(
            text="Dashboard"
        )

        self.clear_body()

        stats = self.db.get_statistics()

        cards = [

            (
                "Total Tasks",
                stats["total"]
            ),

            (
                "Completed",
                stats["completed"]
            ),

            (
                "Pending",
                stats["pending"]
            ),

            (
                "Overdue",
                stats["overdue"]
            ),

            (
                "Completion Rate",
                f'{stats["rate"]:.0f}%'
            )

        ]

        card_frame = ctk.CTkFrame(

            self.body,

            fg_color="transparent"

        )

        card_frame.grid(

            row=0,

            column=0,

            sticky="ew",

            pady=(0, 15)

        )

        for i, (label, value) in enumerate(cards):

            card_frame.grid_columnconfigure(
                i,
                weight=1
            )

            card = ctk.CTkFrame(
                card_frame,
                height=115
            )

            card.grid(

                row=0,

                column=i,

                padx=5,

                sticky="ew"

            )

            ctk.CTkLabel(

                card,

                text=label,

                font=ctk.CTkFont(
                    size=13
                )

            ).pack(
                pady=(20, 5)
            )

            ctk.CTkLabel(

                card,

                text=str(value),

                font=ctk.CTkFont(
                    size=28,
                    weight="bold"
                )

            ).pack()

        lower = ctk.CTkFrame(
            self.body
        )

        lower.grid(

            row=1,

            column=0,

            sticky="nsew"

        )

        lower.grid_columnconfigure(
            0,
            weight=1
        )

        lower.grid_columnconfigure(
            1,
            weight=1
        )

        lower.grid_rowconfigure(
            0,
            weight=1
        )

        upcoming = ctk.CTkFrame(
            lower
        )

        upcoming.grid(

            row=0,

            column=0,

            sticky="nsew",

            padx=(0, 8)

        )

        ctk.CTkLabel(

            upcoming,

            text="Upcoming Tasks",

            font=ctk.CTkFont(
                size=18,
                weight="bold"
            )

        ).pack(

            anchor="w",

            padx=18,

            pady=18

        )

        rows = self.db.get_tasks(
            status="Pending"
        )[:7]

        if not rows:

            ctk.CTkLabel(

                upcoming,

                text="No pending tasks. Great job!"

            ).pack(
                pady=30
            )

        for row in rows:

            text = (

                f'• {row["title"]}'

                f' | {row["deadline"]}'

                f' | {row["priority"]}'

            )

            ctk.CTkLabel(

                upcoming,

                text=text,

                anchor="w"

            ).pack(

                fill="x",

                padx=18,

                pady=7

            )

        calendar_box = ctk.CTkFrame(
            lower
        )

        calendar_box.grid(

            row=0,

            column=1,

            sticky="nsew",

            padx=(8, 0)

        )

        ctk.CTkLabel(

            calendar_box,

            text="Calendar",

            font=ctk.CTkFont(
                size=18,
                weight="bold"
            )

        ).pack(

            anchor="w",

            padx=18,

            pady=18

        )

        calendar = DateEntry(

            calendar_box,

            date_pattern="yyyy-mm-dd"

        )

        calendar.pack(
            padx=20,
            pady=10
        )

        ctk.CTkLabel(

            calendar_box,

            text="Select a date to review your schedule.",

            wraplength=250

        ).pack(
            pady=10
        )

    def show_tasks(self):

        self.page_title.configure(
            text="Task Manager"
        )

        self.clear_body()

        controls = ctk.CTkFrame(
            self.body
        )

        controls.grid(

            row=0,

            column=0,

            sticky="ew",

            pady=(0, 12)

        )

        controls.grid_columnconfigure(
            0,
            weight=1
        )

        ctk.CTkEntry(

            controls,

            textvariable=self.search_var,

            placeholder_text="Search tasks..."

        ).grid(

            row=0,

            column=0,

            padx=8,

            pady=10,

            sticky="ew"

        )

        ctk.CTkOptionMenu(

            controls,

            variable=self.status_var,

            values=[
                "All",
                "Pending",
                "Completed"
            ],

            command=lambda _: self.load_tasks()

        ).grid(

            row=0,

            column=1,

            padx=5

        )

        ctk.CTkOptionMenu(

            controls,

            variable=self.priority_var,

            values=[
                "All",
                "High",
                "Medium",
                "Low"
            ],

            command=lambda _: self.load_tasks()

        ).grid(

            row=0,

            column=2,

            padx=5

        )

        categories = (
            ["All"]
            + self.db.get_categories()
        )

        ctk.CTkOptionMenu(

            controls,

            variable=self.category_var,

            values=categories,

            command=lambda _: self.load_tasks()

        ).grid(

            row=0,

            column=3,

            padx=5

        )

        ctk.CTkButton(

            controls,

            text="Search",

            width=90,

            command=self.load_tasks

        ).grid(

            row=0,

            column=4,

            padx=8

        )

        table_frame = ctk.CTkFrame(
            self.body
        )

        table_frame.grid(

            row=1,

            column=0,

            sticky="nsew"

        )

        columns = (

            "id",
            "title",
            "category",
            "priority",
            "deadline",
            "status"

        )

        self.tree = ttk.Treeview(

            table_frame,

            columns=columns,

            show="headings"

        )

        headings = {

            "id": "ID",

            "title": "Task",

            "category": "Category",

            "priority": "Priority",

            "deadline": "Deadline",

            "status": "Status"

        }

        widths = {

            "id": 50,

            "title": 300,

            "category": 130,

            "priority": 90,

            "deadline": 110,

            "status": 100

        }

        for column in columns:

            self.tree.heading(

                column,

                text=headings[column]

            )

            self.tree.column(

                column,

                width=widths[column],

                anchor="center"

            )

        self.tree.pack(

            side="left",

            fill="both",

            expand=True,

            padx=10,

            pady=10

        )

        scrollbar = ttk.Scrollbar(

            table_frame,

            orient="vertical",

            command=self.tree.yview

        )

        scrollbar.pack(

            side="right",

            fill="y",

            pady=10

        )

        self.tree.configure(

            yscrollcommand=scrollbar.set

        )

        actions = ctk.CTkFrame(

            self.body,

            fg_color="transparent"

        )

        actions.grid(

            row=2,

            column=0,

            sticky="ew",

            pady=(10, 0)

        )

        buttons = [

            (
                "✓ Complete / Reopen",
                self.toggle_selected
            ),

            (
                "✎ Edit",
                self.edit_selected
            ),

            (
                "🗑 Delete",
                self.delete_selected
            ),

            (
                "Export CSV",
                self.export_csv
            ),

            (
                "Export PDF",
                self.export_pdf
            )

        ]

        for i, (text, command) in enumerate(buttons):

            ctk.CTkButton(

                actions,

                text=text,

                command=command,

                height=38

            ).grid(

                row=0,

                column=i,

                padx=5,

                sticky="ew"

            )

            actions.grid_columnconfigure(
                i,
                weight=1
            )

        self.load_tasks()

    def load_tasks(self):

        if not hasattr(
            self,
            "tree"
        ):

            return

        for item in self.tree.get_children():

            self.tree.delete(item)

        rows = self.db.get_tasks(

            self.search_var.get().strip(),

            self.status_var.get(),

            self.priority_var.get(),

            self.category_var.get()

        )

        for row in rows:

            self.tree.insert(

                "",

                "end",

                values=(

                    row["id"],

                    row["title"],

                    row["category"],

                    row["priority"],

                    row["deadline"],

                    row["status"]

                )

            )

    def selected_id(self):

        if not hasattr(
            self,
            "tree"
        ):

            return None

        selection = self.tree.selection()

        if not selection:

            messagebox.showwarning(

                "Select Task",

                "Please select a task first."

            )

            return None

        return int(

            self.tree.item(

                selection[0],

                "values"

            )[0]

        )

    def open_add_dialog(self):

        TaskDialog(
            self,
            self.save_task
        )

    def save_task(
        self,
        task,
        task_id=None
    ):

        try:

            if task_id:

                self.db.update_task(
                    task_id,
                    task
                )

                messagebox.showinfo(

                    "Success",

                    "Task updated successfully."

                )

            else:

                self.db.add_task(task)

                messagebox.showinfo(

                    "Success",

                    "Task added successfully."

                )

            self.show_tasks()

        except Exception as exc:

            messagebox.showerror(

                "Database Error",

                str(exc)

            )

    def edit_selected(self):

        task_id = self.selected_id()

        if task_id is None:

            return

        task = self.db.get_task(
            task_id
        )

        if task:

            TaskDialog(

                self,

                self.save_task,

                task

            )

    def delete_selected(self):

        task_id = self.selected_id()

        if task_id is None:

            return

        confirmed = messagebox.askyesno(

            "Confirm Delete",

            "Delete the selected task permanently?"

        )

        if confirmed:

            self.db.delete_task(
                task_id
            )

            self.show_tasks()

    def toggle_selected(self):

        task_id = self.selected_id()

        if task_id is None:

            return

        task = self.db.get_task(
            task_id
        )

        completed = (
            task["status"]
            != "Completed"
        )

        self.db.set_status(

            task_id,

            completed

        )

        self.load_tasks()

    def export_csv(self):

        rows = self.db.get_tasks(

            self.search_var.get().strip(),

            self.status_var.get(),

            self.priority_var.get(),

            self.category_var.get()

        )

        path = filedialog.asksaveasfilename(

            defaultextension=".csv",

            filetypes=[
                ("CSV file", "*.csv")
            ]

        )

        if not path:

            return

        try:

            export_csv(
                rows,
                path
            )

            messagebox.showinfo(

                "Export Complete",

                "CSV report created successfully."

            )

        except Exception as exc:

            messagebox.showerror(

                "Export Error",

                str(exc)

            )

    def export_pdf(self):

        rows = self.db.get_tasks(

            self.search_var.get().strip(),

            self.status_var.get(),

            self.priority_var.get(),

            self.category_var.get()

        )

        path = filedialog.asksaveasfilename(

            defaultextension=".pdf",

            filetypes=[
                ("PDF file", "*.pdf")
            ]

        )

        if not path:

            return

        try:

            export_pdf(
                rows,
                path
            )

            messagebox.showinfo(

                "Export Complete",

                "PDF report created successfully."

            )

        except Exception as exc:

            messagebox.showerror(

                "Export Error",

                str(exc)

            )

    def show_analytics(self):

        self.page_title.configure(

            text="Productivity Analytics"

        )

        self.clear_body()

        rows = self.db.get_tasks()

        stats = self.db.get_statistics()

        panel = ctk.CTkFrame(
            self.body
        )

        panel.grid(

            row=0,

            column=0,

            sticky="nsew"

        )

        self.body.grid_rowconfigure(

            0,

            weight=1

        )

        if not rows:

            ctk.CTkLabel(

                panel,

                text=(
                    "Add some tasks "
                    "to see productivity analytics."
                ),

                font=ctk.CTkFont(
                    size=18
                )

            ).pack(
                pady=100
            )

            return

        completed = stats["completed"]

        pending = stats["pending"]

        high = stats["high"]

        overdue = stats["overdue"]

        figure = plt.Figure(

            figsize=(9, 5.5),

            dpi=100

        )

        chart1 = figure.add_subplot(121)

        chart1.pie(

            [
                completed,
                pending
            ],

            labels=[
                "Completed",
                "Pending"
            ],

            autopct="%1.0f%%",

            startangle=90

        )

        chart1.set_title(
            "Task Completion"
        )

        chart2 = figure.add_subplot(122)

        chart2.bar(

            [
                "High Priority",
                "Overdue",
                "Completed"
            ],

            [
                high,
                overdue,
                completed
            ]

        )

        chart2.set_title(
            "Productivity Indicators"
        )

        chart2.set_ylabel(
            "Tasks"
        )

        canvas = FigureCanvasTkAgg(

            figure,

            master=panel

        )

        canvas.draw()

        canvas.get_tk_widget().pack(

            fill="both",

            expand=True,

            padx=20,

            pady=20

        )
