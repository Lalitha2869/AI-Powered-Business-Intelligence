from backend.report_history_manager import ReportHistoryManager

history = ReportHistoryManager()

history.save_report(
    question="Show revenue by region",
    csv_path="exports/report.csv",
    excel_path="exports/report.xlsx",
    pdf_path="exports/report.pdf"
)

print(
    history.get_history()
)