import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
import os

API_BASE = os.getenv(
    "API_URL",
    "http://localhost:8000"
)

API_BASE = "http://localhost:8000"

# ==================================
# Page Config
# ==================================

st.set_page_config(
    page_title="AI SQL Assistant",
    page_icon="🤖",
    layout="wide"
)

st.title("AI SQL Assistant")
st.caption("Ask business questions in natural language")

# ==================================
# Initialize Session State (MUST be first)
# ==================================

if "token" not in st.session_state:
    st.session_state.token = None

if "username" not in st.session_state:
    st.session_state.username = None

if "result" not in st.session_state:
    st.session_state.result = None

# ==================================
# Login Screen
# ==================================

if st.session_state.token is None:

    st.subheader("Login")

    username = st.text_input("Username")

    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button("Login"):

        try:

            response = requests.post(
                f"{API_BASE}/login",
                json={
                    "username": username,
                    "password": password
                },
                timeout=15
            )

            response.raise_for_status()

            data = response.json()

            st.session_state.token = data["token"]
            st.session_state.username = data["username"]

            st.success(f"Welcome {data['username']}")
            st.rerun()

        except requests.exceptions.HTTPError as e:
            try:
                detail = e.response.json().get("detail", str(e))
            except Exception:
                detail = str(e)
            st.error(f"Login Failed: {detail}")

        except Exception as e:
            st.error(f"Login Failed: {e}")

    st.stop()

# ==================================
# Sidebar (authenticated)
# ==================================

st.sidebar.title("Navigation")
st.sidebar.success(
    f"Logged in as {st.session_state.username}"
)

if st.sidebar.button("Logout"):
    st.session_state.token = None
    st.session_state.username = None
    st.session_state.result = None
    st.rerun()

show_history = st.sidebar.button("Load Report History")
show_analytics = st.sidebar.button("Analytics Dashboard")

token = st.session_state.token

# ==================================
# Analytics Dashboard
# ==================================

if show_analytics:

    try:

        summary_response = requests.get(
            f"{API_BASE}/analytics-summary",
            params={"token": token},
            timeout=15
        )

        advanced_response = requests.get(
            f"{API_BASE}/analytics-advanced",
            params={"token": token},
            timeout=15
        )

        summary_response.raise_for_status()
        advanced_response.raise_for_status()

        summary = summary_response.json()
        advanced = advanced_response.json()

        st.header("Analytics Dashboard")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Total Queries", summary["total_queries"])

        with col2:
            st.metric("Successful", summary["successful_queries"])

        with col3:
            st.metric("Failed", summary["failed_queries"])

        col4, col5, col6 = st.columns(3)

        with col4:
            st.metric("Avg Time (ms)", summary["avg_execution_time_ms"])

        with col5:
            st.metric("Fastest Query", advanced["fastest_query_ms"])

        with col6:
            st.metric("Slowest Query", advanced["slowest_query_ms"])

        st.divider()

        st.subheader("Most Asked Questions")

        top_questions_df = pd.DataFrame(advanced["top_questions"])

        if not top_questions_df.empty:

            st.dataframe(
                top_questions_df,
                use_container_width=True
            )

            st.subheader("Top Questions Chart")

            fig, ax = plt.subplots(figsize=(8, 4))
            ax.bar(
                top_questions_df["question"],
                top_questions_df["count"]
            )
            ax.set_ylabel("Count")
            ax.set_title("Most Asked Questions")
            plt.xticks(rotation=45, ha="right")
            st.pyplot(fig)
        else:
            st.info("No analytics data yet. Run some queries first.")

    except Exception as e:
        st.error(f"Analytics Error: {e}")

# ==================================
# Report History
# ==================================

if show_history:

    try:

        response = requests.get(
            f"{API_BASE}/report-history",
            params={"token": token},
            timeout=15
        )
        response.raise_for_status()

        history_data = response.json()

        st.subheader("Report History")

        history_df = pd.DataFrame(history_data["reports"])

        if not history_df.empty:
            st.dataframe(history_df, use_container_width=True)
        else:
            st.info("No reports saved yet.")

        st.markdown("### Download Latest Reports")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.link_button(
                "Download CSV",
                f"{API_BASE}/download-report?report_type=csv"
            )

        with col2:
            st.link_button(
                "Download Excel",
                f"{API_BASE}/download-report?report_type=excel"
            )

        with col3:
            st.link_button(
                "Download PDF",
                f"{API_BASE}/download-report?report_type=pdf"
            )

    except Exception as e:
        st.error(f"History Error: {e}")

# ==================================
# Query Input
# ==================================

question = st.text_input(
    "Ask a question",
    placeholder="Show total revenue by region"
)

run_query = st.button("Run Query")

if run_query:

    if not question:
        st.warning("Please enter a question.")
        st.stop()

    try:

        with st.spinner("Generating SQL and executing query..."):
            response = requests.get(
                f"{API_BASE}/query",
                params={
                    "question": question,
                    "token": token
                },
                timeout=60
            )
            response.raise_for_status()
            st.session_state.result = response.json()
            result = st.session_state.result

        st.subheader("Generated SQL")
        st.code(result["generated_sql"], language="sql")

        col1, col2 = st.columns(2)

        with col1:
            st.metric("Rows Returned", result["row_count"])

        with col2:
            st.metric("Chart Type", result["chart"]["chart_type"])

        st.subheader("Results")

        df = pd.DataFrame(result["rows"])
        st.dataframe(df, use_container_width=True)

        st.subheader("Visualization & Insights")

        col_chart, col_insights = st.columns([3, 1])

        with col_chart:

            st.markdown("### Visualization")

            backend_chart = result["chart"].get("chart_type", "bar")

            chart_option = st.selectbox(
                "Choose Chart Type",
                ["Auto", "Pie", "Bar", "Line", "Scatter"]
            )

            selected_chart = (
                backend_chart.lower()
                if chart_option == "Auto"
                else chart_option.lower()
            )

            try:
                if len(df.columns) >= 2 and not df.empty:

                    x_data = df.iloc[:, 0]
                    y_data = df.iloc[:, 1]

                    fig, ax = plt.subplots(figsize=(6, 4))

                    if selected_chart == "pie":
                        ax.pie(y_data, labels=x_data, autopct="%1.1f%%")
                        ax.set_title("Pie Chart")

                    elif selected_chart == "bar":
                        ax.bar(x_data, y_data)
                        ax.set_xlabel(df.columns[0])
                        ax.set_ylabel(df.columns[1])
                        ax.set_title("Bar Chart")
                        plt.xticks(rotation=45, ha="right")

                    elif selected_chart == "line":
                        ax.plot(x_data, y_data, marker="o")
                        ax.set_xlabel(df.columns[0])
                        ax.set_ylabel(df.columns[1])
                        ax.set_title("Line Chart")
                        plt.xticks(rotation=45, ha="right")

                    elif selected_chart == "scatter":
                        ax.scatter(range(len(y_data)), y_data)
                        ax.set_xticks(range(len(x_data)))
                        ax.set_xticklabels(x_data, rotation=45)
                        ax.set_xlabel(df.columns[0])
                        ax.set_ylabel(df.columns[1])
                        ax.set_title("Scatter Chart")

                    else:
                        st.info("No suitable visualization available.")

                    st.pyplot(fig, use_container_width=False)

                elif len(df.columns) == 1 and not df.empty:
                    st.metric(df.columns[0], df.iloc[0][df.columns[0]])

                else:
                    st.info("No data available for visualization.")

            except Exception as e:
                st.warning(f"Chart Error: {e}")

        with col_insights:

            st.markdown("### AI Insights")

            if "insights" in result and result["insights"]:
                for insight in result["insights"]:
                    st.success(insight)
            else:
                st.info("No insights available")

    except requests.exceptions.HTTPError as e:
        try:
            detail = e.response.json().get("detail", str(e))
        except Exception:
            detail = str(e)
        st.error(f"API Error: {detail}")

    except requests.exceptions.RequestException as e:
        st.error(f"Network Error: {str(e)}")

    except Exception as e:
        st.error(f"Error: {str(e)}")

else:
    st.info("Enter a question and click 'Run Query' to get started")
