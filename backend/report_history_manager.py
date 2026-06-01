import json
import os
from datetime import datetime


class ReportHistoryManager:

    def __init__(self):

        self.history_file = "report_history.json"

        # Create history file if it doesn't exist
        if not os.path.exists(self.history_file):

            with open(
                self.history_file,
                "w"
            ) as file:

                json.dump([], file)

    def save_report(
        self,
        question,
        csv_path,
        excel_path,
        pdf_path
    ):

        # Load existing history
        with open(
            self.history_file,
            "r"
        ) as file:

            reports = json.load(file)

        # Create new report entry
        report = {
            "report_id": len(reports) + 1,
            "question": question,
            "csv": csv_path,
            "excel": excel_path,
            "pdf": pdf_path,
            "created_at": str(datetime.now())
        }

        # Add to history
        reports.append(report)

        # Save back to file
        with open(
            self.history_file,
            "w"
        ) as file:

            json.dump(
                reports,
                file,
                indent=4
            )

        return report

    def get_history(self):

        with open(
            self.history_file,
            "r"
        ) as file:

            return json.load(file)