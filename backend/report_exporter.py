import os
import pandas as pd

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import getSampleStyleSheet


class ReportExporter:

    def export_csv(self, dataframe):

        os.makedirs(
            "exports",
            exist_ok=True
        )

        file_path = "exports/report.csv"

        dataframe.to_csv(
            file_path,
            index=False
        )

        return file_path
    
    def export_pdf(
        self,
        question,
        sql,
        rows,
        insights
    ):
        os.makedirs(
            "exports",
            exist_ok=True
        )

        file_path = "exports/report.pdf"

        doc = SimpleDocTemplate(file_path)

        styles = getSampleStyleSheet()

        content = []

        content.append(
            Paragraph(
                "AI SQL Assistant Report",
                styles["Title"]
            )
        )

        content.append(
            Spacer(1, 12)
        )

        content.append(
            Paragraph(
                f"<b>Question:</b> {question}",
                styles["Normal"]
            )
        )

        content.append(
            Spacer(1, 12)
        )

        content.append(
            Paragraph(
                "<b>Generated SQL:</b>",
                styles["Heading2"]
            )
        )

        content.append(
            Paragraph(
                sql.replace("\n", "<br/>"),
                styles["Code"]
            )
        )

        content.append(
            Spacer(1, 12)
        )

        content.append(
            Paragraph(
                "<b>Results:</b>",
                styles["Heading2"]
            )
        )

        for row in rows[:20]:
            content.append(
                Paragraph(
                    str(row),
                    styles["Normal"]
                )
            )

        content.append(
            Spacer(1, 12)
        )

        content.append(
            Paragraph(
                "<b>Insights:</b>",
                styles["Heading2"]
            )
        )

        for insight in insights:
            content.append(
                Paragraph(
                    f"• {insight}",
                    styles["Normal"]
                )
            )

        doc.build(content)

        return file_path

    def export_excel(self, dataframe):

        os.makedirs(
            "exports",
            exist_ok=True
        )

        file_path = "exports/report.xlsx"

        dataframe.to_excel(
            file_path,
            index=False
        )

        return file_path