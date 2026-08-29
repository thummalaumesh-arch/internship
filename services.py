import logging

from datetime import datetime

from pathlib import Path

import pandas as pd

from reportlab.lib import colors

from reportlab.lib.pagesizes import A4

from reportlab.lib.styles import getSampleStyleSheet

from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer
)


BASE_DIR = Path(__file__).resolve().parent.parent

LOG_DIR = BASE_DIR / "logs"

LOG_DIR.mkdir(exist_ok=True)


logging.basicConfig(

    filename=LOG_DIR / "application.log",

    level=logging.INFO,

    format=(
        "%(asctime)s | "
        "%(levelname)s | "
        "%(message)s"
    )

)


logger = logging.getLogger(__name__)


class TaskService:

    """Business logic and validation."""

    PRIORITIES = (
        "Low",
        "Medium",
        "High"
    )

    @staticmethod
    def validate(
        title,
        deadline,
        priority
    ):

        title = title.strip()

        if not title:

            raise ValueError(
                "Task title is required."
            )

        if len(title) > 120:

            raise ValueError(
                "Task title must be 120 characters or fewer."
            )

        try:

            datetime.strptime(
                deadline,
                "%Y-%m-%d"
            )

        except ValueError as exc:

            raise ValueError(
                "Deadline must use YYYY-MM-DD format."
            ) from exc

        if priority not in TaskService.PRIORITIES:

            raise ValueError(
                "Invalid priority selected."
            )

        return title

    @staticmethod
    def normalize_task(
        title,
        description,
        category,
        priority,
        deadline
    ):

        title = TaskService.validate(
            title,
            deadline,
            priority
        )

        category = category.strip()

        if not category:

            category = "General"

        return {

            "title": title,

            "description": description.strip(),

            "category": category,

            "priority": priority,

            "deadline": deadline

        }


def export_csv(rows, path):

    data = [
        dict(row)
        for row in rows
    ]

    if not data:

        raise ValueError(
            "There are no tasks to export."
        )

    dataframe = pd.DataFrame(data)

    dataframe.to_csv(
        path,
        index=False
    )

    logger.info(
        "Exported %s tasks to CSV: %s",
        len(data),
        path
    )


def export_pdf(rows, path):

    data = [
        dict(row)
        for row in rows
    ]

    if not data:

        raise ValueError(
            "There are no tasks to export."
        )

    document = SimpleDocTemplate(
        path,
        pagesize=A4
    )

    styles = getSampleStyleSheet()

    story = [

        Paragraph(
            "Student Task & Productivity Report",
            styles["Title"]
        ),

        Spacer(1, 12),

        Paragraph(
            (
                f"Generated: "
                f"{datetime.now():%Y-%m-%d %H:%M}"
            ),
            styles["Normal"]
        ),

        Spacer(1, 12)

    ]

    table_data = [

        [
            "ID",
            "Task",
            "Category",
            "Priority",
            "Deadline",
            "Status"
        ]

    ]

    for row in data:

        table_data.append([

            str(row["id"]),

            row["title"][:28],

            row["category"][:15],

            row["priority"],

            row["deadline"],

            row["status"]

        ])

    table = Table(
        table_data,
        repeatRows=1
    )

    table.setStyle(
        TableStyle([

            (
                "BACKGROUND",
                (0, 0),
                (-1, 0),
                colors.HexColor("#263238")
            ),

            (
                "TEXTCOLOR",
                (0, 0),
                (-1, 0),
                colors.white
            ),

            (
                "GRID",
                (0, 0),
                (-1, -1),
                0.5,
                colors.grey
            ),

            (
                "FONTNAME",
                (0, 0),
                (-1, 0),
                "Helvetica-Bold"
            ),

            (
                "FONTSIZE",
                (0, 0),
                (-1, -1),
                8
            ),

            (
                "VALIGN",
                (0, 0),
                (-1, -1),
                "MIDDLE"
            )

        ])
    )

    story.append(table)

    document.build(story)

    logger.info(
        "Exported %s tasks to PDF: %s",
        len(data),
        path
    )