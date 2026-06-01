import pandas as pd

from backend.report_exporter import ReportExporter

data = [
    {
        "region_name": "East",
        "revenue": 1000
    },
    {
        "region_name": "West",
        "revenue": 800
    }
]

df = pd.DataFrame(data)

exporter = ReportExporter()

csv_path = exporter.export_csv(df)

excel_path = exporter.export_excel(df)

pdf_path = exporter.export_pdf(
    question="Show revenue by region",
    sql="""
    SELECT region_name,
           SUM(revenue)
    FROM sales
    GROUP BY region_name
    """,
    rows=data,
    insights=[
        "East generated highest revenue",
        "West generated second highest revenue"
    ]
)

print("CSV:", csv_path)
print("Excel:", excel_path)
print("PDF:", pdf_path)