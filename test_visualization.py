from agents.visualization_agent import suggest_chart

rows = [
    {
        "region_name": "East",
        "total_revenue": 20549018.79
    },
    {
        "region_name": "West",
        "total_revenue": 10504415.07
    }
]

result = suggest_chart(rows)

print(result)