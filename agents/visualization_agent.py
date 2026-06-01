def suggest_chart(rows):

    # ==========================
    # No Data
    # ==========================

    if not rows:
        return {
            "chart_type": "table"
        }

    columns = list(rows[0].keys())

    # ==========================
    # Single KPI
    # ==========================

    if len(columns) == 1:

        return {
            "chart_type": "kpi",
            "value_column": columns[0]
        }

    # ==========================
    # Two Columns
    # ==========================

    if len(columns) == 2:

        x_col = columns[0]
        y_col = columns[1]

        x_lower = x_col.lower()
        y_lower = y_col.lower()

        # ----------------------
        # Time Series → Line
        # ----------------------

        if any(
            keyword in x_lower
            for keyword in [
                "date",
                "day",
                "month",
                "year",
                "time"
            ]
        ):
            return {
                "chart_type": "line",
                "x_axis": x_col,
                "y_axis": y_col
            }

        # ----------------------
        # Category Distribution → Pie
        # ----------------------

        if any(
            keyword in x_lower
            for keyword in [
                "region",
                "department",
                "category",
                "status",
                "segment",
                "type"
            ]
        ):
            return {
                "chart_type": "pie",
                "label_column": x_col,
                "value_column": y_col
            }

        # ----------------------
        # Revenue/Product Metrics → Bar
        # ----------------------

        if any(
            keyword in y_lower
            for keyword in [
                "revenue",
                "sales",
                "profit",
                "amount",
                "count",
                "total"
            ]
        ):
            return {
                "chart_type": "bar",
                "x_axis": x_col,
                "y_axis": y_col
            }

        # ----------------------
        # Default Bar
        # ----------------------

        return {
            "chart_type": "bar",
            "x_axis": x_col,
            "y_axis": y_col
        }

    # ==========================
    # Three or More Columns
    # ==========================

    if len(columns) >= 3:

        numeric_columns = []

        for col in columns:

            value = rows[0].get(col)

            if isinstance(value, (int, float)):
                numeric_columns.append(col)

        # Scatter Plot
        if len(numeric_columns) >= 2:

            return {
                "chart_type": "scatter",
                "x_axis": numeric_columns[0],
                "y_axis": numeric_columns[1]
            }

    # ==========================
    # Fallback
    # ==========================

    return {
        "chart_type": "table"
    }