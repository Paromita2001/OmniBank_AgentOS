

# import streamlit as st
# import pandas as pd
# import matplotlib.pyplot as plt
# from datetime import datetime
# import re
# import calendar

# from graph.builder import app_graph
# from interface.tts import speak_text
# from services.auth_service import authenticate_user
# from db.banking_db import get_transactions_by_time


# # =============================
# # PAGE CONFIG
# # =============================
# st.set_page_config(
#     page_title="OmniBank Agent OS",
#     page_icon="🏦",
#     layout="centered"
# )

# st.title("🏦 OmniBank Agent OS")
# st.caption("AI-Powered Banking Assistant")


# # =============================
# # MONTH MAP (Jan–Dec Support)
# # =============================
# MONTH_MAP = {
#     "january":1, "february":2, "march":3, "april":4,
#     "may":5, "june":6, "july":7, "august":8,
#     "september":9, "october":10, "november":11, "december":12,
#     "jan":1, "feb":2, "mar":3, "apr":4,
#     "jun":6, "jul":7, "aug":8,
#     "sep":9, "oct":10, "nov":11, "dec":12
# }


# # =============================
# # SESSION INIT
# # =============================
# if "user_id" not in st.session_state:
#     st.session_state.user_id = None

# if "chat_history" not in st.session_state:
#     st.session_state.chat_history = []

# if "graph_data" not in st.session_state:
#     st.session_state.graph_data = None


# # =============================
# # LOGIN PAGE
# # =============================
# def show_login():

#     st.subheader("🔐 Secure Login")

#     email = st.text_input("Email")
#     phone = st.text_input("Phone Number")

#     if st.button("Login"):
#         user_id = authenticate_user(email, phone)

#         if user_id:
#             st.session_state.user_id = user_id
#             st.success("Login Successful!")
#             st.rerun()
#         else:
#             st.error("Invalid Email or Phone")


# # =============================
# # MAIN APP
# # =============================
# def show_main_app():

#     st.success(f"Logged in as User ID: {st.session_state.user_id}")

#     if st.button("Logout"):
#         st.session_state.user_id = None
#         st.session_state.chat_history = []
#         st.session_state.graph_data = None
#         st.rerun()

#     st.divider()

#     st.subheader("💬 Ask OmniBank")

#     with st.form("chat_form", clear_on_submit=True):
#         user_query = st.text_input("Type your request")
#         submitted = st.form_submit_button("Send")

#         if submitted and user_query.strip():
#             process_user_input(user_query)

#     if st.session_state.graph_data is not None:
#         show_graph(st.session_state.graph_data)

#     st.divider()

#     st.subheader("📜 Conversation")

#     for role, message in st.session_state.chat_history:
#         if role == "You":
#             st.markdown(f"**🧑 You:** {message}")
#         else:
#             st.markdown(f"**🤖 OmniBank:** {message}")


# # =============================
# # PROCESS USER INPUT
# # =============================
# def process_user_input(text: str):

#     try:
#         response = app_graph.invoke({
#             "user_id": st.session_state.user_id,
#             "user_query": text
#         })

#         if isinstance(response, dict):
#             final_response = response.get("result", str(response))
#         else:
#             final_response = str(response)

#         # Remove "on None"
#         if " on None" in final_response:
#             final_response = final_response.replace(" on None", "")

#         lower_query = text.lower()

#         # if "month wise" in lower_query or "monthly" in lower_query:
#         #     prepare_monthly_trend(lower_query)

#         # elif "spend" in lower_query or "spent" in lower_query or "compare" in lower_query:
#         #     prepare_spending_graph(lower_query)
#         # Only trigger trend if user clearly asks for trend
#         if "trend" in lower_query or "month wise trend" in lower_query:
#             prepare_monthly_trend(lower_query)

#         elif "spend" in lower_query or "spent" in lower_query or "compare" in lower_query:
#             prepare_spending_graph(lower_query)
            
#         else:
#             st.session_state.graph_data = None

#     except Exception as e:
#         final_response = f"⚠️ System Error: {e}"
#         st.session_state.graph_data = None

#     st.session_state.chat_history.append(("You", text))
#     st.session_state.chat_history.append(("Assistant", final_response))

#     speak_text(final_response)


# # =============================
# # PREPARE SPENDING GRAPH
# # =============================
# def prepare_spending_graph(query_text):

#     selected_month = None
#     selected_year = datetime.now().year

#     for name, number in MONTH_MAP.items():
#         if name in query_text:
#             selected_month = number
#             break

#     year_match = re.search(r"\b(20\d{2})\b", query_text)
#     if year_match:
#         selected_year = int(year_match.group(1))

#     if selected_month:
#         start_date = datetime(selected_year, selected_month, 1)

#         if selected_month == 12:
#             end_date = datetime(selected_year + 1, 1, 1) - pd.Timedelta(seconds=1)
#         else:
#             end_date = datetime(selected_year, selected_month + 1, 1) - pd.Timedelta(seconds=1)
#     else:
#         today = datetime.now()
#         start_date = today.replace(day=1)
#         end_date = today

#     tx = get_transactions_by_time(
#         st.session_state.user_id,
#         start_date.strftime("%Y-%m-%d 00:00:00"),
#         end_date.strftime("%Y-%m-%d 23:59:59")
#     )

#     df = pd.DataFrame(tx, columns=["desc","amount","category","date"])

#     if df.empty:
#         st.session_state.graph_data = None
#         return

#     df["amount"] = df["amount"].astype(float)

#     # Dynamic category detection
#     categories = df["category"].str.lower().unique()
#     selected_category = None

#     for cat in categories:
#         if cat in query_text:
#             selected_category = cat
#             break

#     if selected_category:
#         df = df[df["category"].str.lower() == selected_category]

#     grouped = df.groupby("category")["amount"].sum()

#     st.session_state.graph_data = grouped


# # =============================
# # MONTHLY TREND
# # =============================
# def prepare_monthly_trend(query_text):

#     tx = get_transactions_by_time(
#         st.session_state.user_id,
#         "2020-01-01 00:00:00",
#         datetime.now().strftime("%Y-%m-%d 23:59:59")
#     )

#     df = pd.DataFrame(tx, columns=["desc","amount","category","date"])

#     if df.empty:
#         st.session_state.graph_data = None
#         return

#     df["amount"] = df["amount"].astype(float)
#     df["date"] = pd.to_datetime(df["date"])
#     df["month"] = df["date"].dt.to_period("M")

#     categories = df["category"].str.lower().unique()
#     selected_category = None

#     for cat in categories:
#         if cat in query_text:
#             selected_category = cat
#             break

#     if selected_category:
#         df = df[df["category"].str.lower() == selected_category]

#     monthly = df.groupby("month")["amount"].sum()

#     st.session_state.graph_data = monthly


# # =============================
# # SHOW GRAPH
# # =============================


# import plotly.graph_objects as go

# def show_graph(data):

#     if data is None or len(data) == 0:
#         st.info("No data available.")
#         return

#     st.subheader("📊 Spending Analytics")

#     # -------------------------
#     # CASE 1 : Single category
#     # -------------------------
#     if isinstance(data, pd.Series) and len(data) == 1:

#         category = data.index[0]
#         amount = data.values[0]

#         fig = go.Figure()

#         fig.add_trace(go.Indicator(
#             mode="number+delta",
#             value=amount,
#             title={"text": f"{category.title()} Spending"},
#             number={'prefix': "₹"},
#         ))

#         fig.update_layout(
#             template="plotly_dark",
#             height=250
#         )

#         st.plotly_chart(fig, use_container_width=True)

#     # -------------------------
#     # CASE 2 : Multiple categories
#     # -------------------------
#     elif isinstance(data, pd.Series):

#         fig = go.Figure()

#         fig.add_trace(go.Bar(
#             x=data.index,
#             y=data.values,
#             marker_color="#38bdf8",
#             text=data.values,
#             textposition="outside"
#         ))

#         fig.update_layout(
#             template="plotly_dark",
#             title="Spending Overview",
#             xaxis_title="Category",
#             yaxis_title="Amount",
#             height=350
#         )

#         st.plotly_chart(fig, use_container_width=True)

#     # -------------------------
#     # CASE 3 : Comparison
#     # -------------------------
#     elif isinstance(data, pd.DataFrame):

#         fig = go.Figure()

#         fig.add_trace(go.Bar(
#             x=data.index,
#             y=data["This Month"],
#             name="This Month"
#         ))

#         fig.add_trace(go.Bar(
#             x=data.index,
#             y=data["Last Month"],
#             name="Last Month"
#         ))

#         fig.update_layout(
#             template="plotly_dark",
#             barmode="group",
#             title="Monthly Spending Comparison",
#             height=350
#         )

#         st.plotly_chart(fig, use_container_width=True)
# # =============================
# # ROUTER
# # =============================
# if st.session_state.user_id is None:
#     show_login()
# else:
#     show_main_app()



import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go

from graph.builder import app_graph
from interface.tts import speak_text
from services.auth_service import authenticate_user
from db.banking_db import get_transactions_by_time


from pathlib import Path
from db.banking_db import (
    create_tables,
    insert_users,
    insert_accounts,
    insert_beneficiaries,
    insert_transactions,
    create_otp_table
)
from db.reminder_db import create_reminder_table
from services.reminder_scheduler import start_scheduler

DB_PATH = Path(__file__).parent.parent / "db" / "bank.db"

# ✅ CREATE DB ONLY IF NOT EXISTS
if not DB_PATH.exists():
    create_tables()
    create_otp_table()
    create_reminder_table()

    insert_users()
    insert_accounts()
    insert_beneficiaries()
    insert_transactions()

# ✅ START SCHEDULER ONLY ONCE
import streamlit as st
if "scheduler_started" not in st.session_state:
    start_scheduler()
    st.session_state.scheduler_started = True

# --------------------------------
# PAGE CONFIG
# --------------------------------
st.set_page_config(
    page_title="OmniBank Agent OS",
    page_icon="🏦",
    layout="wide"
)

st.title("🏦 OmniBank Agent OS")
st.caption("AI-Powered Banking Assistant")


# --------------------------------
# SESSION STATE
# --------------------------------
if "user_id" not in st.session_state:
    st.session_state.user_id = None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "graph_data" not in st.session_state:
    st.session_state.graph_data = None

if "graph_type" not in st.session_state:
    st.session_state.graph_type = None


# --------------------------------
# LOGIN
# --------------------------------
def show_login():

    st.subheader("🔐 Secure Login")

    email = st.text_input("Email")
    phone = st.text_input("Phone Number")

    if st.button("Login"):

        user_id = authenticate_user(email, phone)

        if user_id:
            st.session_state.user_id = user_id
            st.success("Login Successful")
            st.rerun()
        else:
            st.error("Invalid credentials")


# --------------------------------
# MAIN APP
# --------------------------------
def show_main_app():

    st.success(f"Logged in as User ID: {st.session_state.user_id}")

    if st.button("Logout"):
        st.session_state.user_id = None
        st.session_state.chat_history = []
        st.session_state.graph_data = None
        st.rerun()

    st.divider()

    col_chat, col_dashboard = st.columns([2,1])

    # -----------------------------
    # CHAT
    # -----------------------------
    with col_chat:

        st.subheader("💬 Ask OmniBank")

        with st.form("chat_form", clear_on_submit=True):

            user_query = st.text_input("Type your request")
            submitted = st.form_submit_button("Send")

            if submitted and user_query.strip():
                process_user_input(user_query)
    

    # -----------------------------
    # DASHBOARD
    # -----------------------------
    with col_dashboard:

        if st.session_state.graph_data is not None:
            show_dashboard(st.session_state.graph_data)


    st.divider()

    st.subheader("🧾 Conversation")

    for role, message in st.session_state.chat_history:

        if role == "You":
            st.markdown(f"🧑 **You:** {message}")
        else:
            st.markdown(f"🤖 **OmniBank:** {message}")

    # # -----------------------------
    # # DASHBOARD
    # # -----------------------------
    # with col_dashboard:

    #     if st.session_state.graph_data is not None:
    #         show_dashboard(st.session_state.graph_data)


# --------------------------------
# PROCESS USER QUERY
# --------------------------------

def process_user_input(text):

    try:

        response = app_graph.invoke({
            "user_id": st.session_state.user_id,
            "user_query": text
        })

        if isinstance(response, dict):

            final_response = response.get("result", str(response))

            intent = response.get("intent")
            entities = response.get("entities", {})

            # -----------------------------
            # EXTRACT VARIABLES (FIX)
            # -----------------------------
            category = entities.get("category")
            timeframe = entities.get("timeframe")

            # -----------------------------
            # CLEAN CATEGORY
            # -----------------------------
            invalid_categories = [
                "spending categories",
                "categories",
                "spending",
                "my spending",
                "all categories"
            ]

            if category and category.lower() in invalid_categories:
                category = None

            # -----------------------------
            # DEFAULT TIMEFRAME
            # -----------------------------
            if not timeframe:
                timeframe = "this_month"

            # -----------------------------
            # CLEAN RESPONSE TEXT
            # -----------------------------
            if "Timeframe not supported yet" in final_response:
                final_response = "Here is your spending analysis."

            if category is None:
                final_response = final_response.replace("on None", "")
                final_response = final_response.replace("None", "")

            if timeframe == "this_month":
                final_response = final_response.replace("this_month", "this month")

            if timeframe == "last_month":
                final_response = final_response.replace("last_month", "last month")

        else:

            final_response = str(response)
            intent = None
            category = None
            timeframe = None

        # -----------------------------
        # GRAPH LOGIC (FIXED CLEAN)
        # -----------------------------
        if intent == "analytics":

            query = text.lower()

            # -------- TREND --------
            if "trend" in query:

                prepare_graph_data(category, timeframe)

                st.session_state.graph_data = {
                    "type": "trend"
                }

            # -------- COMPARE --------
            elif "compare" in query or "vs" in query:

                prepare_graph_data(None, "compare")

            # -------- NORMAL DASHBOARD --------
            else:

                prepare_graph_data(category, timeframe)

        else:

            st.session_state.graph_data = None
            st.session_state.graph_trend = None

    except Exception as e:

        final_response = f"⚠️ Error: {e}"
        st.session_state.graph_data = None
        st.session_state.graph_trend = None

    # -----------------------------
    # SAVE CHAT
    # -----------------------------
    st.session_state.chat_history.append(("You", text))
    st.session_state.chat_history.append(("Assistant", final_response))

    # -----------------------------
    # SPEAK RESPONSE
    # -----------------------------
    speak_text(final_response)


# def process_user_input(text):

#     try:

#         response = app_graph.invoke({
#             "user_id": st.session_state.user_id,
#             "user_query": text
#         })

#         if isinstance(response, dict):

#             final_response = response.get("result", str(response))



#             # Fix unsupported timeframe message
#             if "Timeframe not supported yet" in final_response:
#                 final_response = "Here is your spending comparison."
            
            
#             intent = response.get("intent")
#             entities = response.get("entities", {})

#             category = entities.get("category")
#             timeframe = entities.get("timeframe")

#             # -----------------------------
#             # FIX "None during timeframe"
#             # -----------------------------
#             if category is None:

#                 final_response = final_response.replace("on None", "")
#                 #final_response = final_response.replace("None", "")
#                 if "on None" in final_response:
#                     final_response = final_response.replace("on None", "")
            
#             # make timeframe human readable
#             if timeframe == "this_month":
#                 final_response = final_response.replace("this_month", "this month")

#             if timeframe == "last_month":
#                 final_response = final_response.replace("last_month", "last month")

#         else:

#             final_response = str(response)
#             intent = None
#             entities = {}

#         # -----------------------------
#         # GRAPH LOGIC
#         # -----------------------------
#         if intent == "analytics":

#             category = entities.get("category")
#             timeframe = entities.get("timeframe")

#             prepare_graph_data(category, timeframe)

#         else:
#             st.session_state.graph_data = None

#     except Exception as e:

#         final_response = f"⚠️ Error: {e}"
#         st.session_state.graph_data = None

#     # -----------------------------
#     # SAVE CHAT
#     # -----------------------------
#     st.session_state.chat_history.append(("You", text))
#     st.session_state.chat_history.append(("Assistant", final_response))

#     # -----------------------------
#     # SPEAK RESPONSE
#     # -----------------------------
#     speak_text(final_response)



def prepare_graph_data(category=None, timeframe=None):

    today = datetime.now()

    # -----------------------------
    # MONTH RANGE
    # -----------------------------
    start_this_month = today.replace(day=1)
    end_this_month = today

    first_day_this_month = today.replace(day=1)
    last_day_last_month = first_day_this_month - pd.Timedelta(days=1)
    start_last_month = last_day_last_month.replace(day=1)

    # -----------------------------
    # FETCH DATA
    # -----------------------------
    this_month_tx = get_transactions_by_time(
        st.session_state.user_id,
        start_this_month.strftime("%Y-%m-%d 00:00:00"),
        end_this_month.strftime("%Y-%m-%d 23:59:59")
    )

    last_month_tx = get_transactions_by_time(
        st.session_state.user_id,
        start_last_month.strftime("%Y-%m-%d 00:00:00"),
        last_day_last_month.strftime("%Y-%m-%d 23:59:59")
    )

    df_this = pd.DataFrame(this_month_tx, columns=["desc","amount","category","date"])
    df_last = pd.DataFrame(last_month_tx, columns=["desc","amount","category","date"])

    if df_this.empty and df_last.empty:
        st.session_state.graph_data = None
        st.session_state.graph_trend = None
        return

    # -----------------------------
    # DATA CLEAN
    # -----------------------------
    if not df_this.empty:
        df_this["amount"] = df_this["amount"].astype(float)

    if not df_last.empty:
        df_last["amount"] = df_last["amount"].astype(float)
    
    # -----------------------------
    # CATEGORY COMPARISON (NEW)
    # -----------------------------
    if timeframe == "compare":

        this_group = df_this.groupby("category")["amount"].sum().reset_index()
        last_group = df_last.groupby("category")["amount"].sum().reset_index()

        merged = pd.merge(
            this_group,
            last_group,
            on="category",
            how="outer",
            suffixes=(" This Month", " Last Month")
        ).fillna(0)

        merged.columns = ["category", "This Month", "Last Month"]

        st.session_state.graph_data = {
            "type": "category_compare",
            "data": merged
        }

        return
    # -----------------------------
    # CATEGORY FILTER
    # -----------------------------
    if category and category.strip() != "":

        this_val = df_this[
            df_this["category"].str.lower().fillna("") == category.lower()
        ]["amount"].sum()

        last_val = df_last[
            df_last["category"].str.lower().fillna("") == category.lower()
        ]["amount"].sum()

        data = pd.DataFrame({
            "Month": ["Last Month", "This Month"],
            "Amount": [last_val, this_val]
        })

        st.session_state.graph_data = {
            "type": "category_single",
            "data": data
        }

    else:

        # FULL CATEGORY DASHBOARD
        this_group = df_this.groupby("category")["amount"].sum().reset_index()

        st.session_state.graph_data = {
            "type": "category_all",
            "data": this_group,
            "df_this": df_this,
            "df_last": df_last
        }

    # -----------------------------
    # MONTHLY TREND
    # -----------------------------
    df_all = pd.concat([df_this, df_last], ignore_index=True)

    if not df_all.empty:

        df_all["date"] = pd.to_datetime(df_all["date"])
        
        # Create month period
        df_all["month"] = df_all["date"].dt.to_period("M")

        # Group monthly spending
        monthly = (
            df_all.groupby("month")["amount"]
            .sum()
            .reset_index()
            .sort_values("month")
        )

        # Convert to string for plotting
        monthly["month"] = monthly["month"].astype(str)

        st.session_state.graph_trend = monthly

    else:
        st.session_state.graph_trend = None

# --------------------------------
# PREPARE DATA
# --------------------------------
# def prepare_graph_data(category=None, timeframe=None):

#     today = datetime.now()

#     start_this_month = today.replace(day=1)
#     end_this_month = today

#     first_day_this_month = today.replace(day=1)
#     last_day_last_month = first_day_this_month - pd.Timedelta(days=1)
#     start_last_month = last_day_last_month.replace(day=1)

#     this_month_tx = get_transactions_by_time(
#         st.session_state.user_id,
#         start_this_month.strftime("%Y-%m-%d 00:00:00"),
#         end_this_month.strftime("%Y-%m-%d 23:59:59")
#     )

#     last_month_tx = get_transactions_by_time(
#         st.session_state.user_id,
#         start_last_month.strftime("%Y-%m-%d 00:00:00"),
#         last_day_last_month.strftime("%Y-%m-%d 23:59:59")
#     )

#     df_this = pd.DataFrame(this_month_tx, columns=["desc","amount","category","date"])
#     df_last = pd.DataFrame(last_month_tx, columns=["desc","amount","category","date"])

#     if df_this.empty:
#         st.session_state.graph_data = None
#         return

#     df_this["amount"] = df_this["amount"].astype(float)
#     df_last["amount"] = df_last["amount"].astype(float)

#     # category filter
#     if category:

#         # this_val = df_this[df_this["category"] == category]["amount"].sum()
#         # last_val = df_last[df_last["category"] == category]["amount"].sum()
        

#         this_val = df_this[df_this["category"].str.lower() == category.lower()]["amount"].sum()
#         last_val = df_last[df_last["category"].str.lower() == category.lower()]["amount"].sum()
        
#         data = pd.DataFrame({
#             "Month": ["Last Month", "This Month"],
#             "Amount": [last_val, this_val]
#         })

#         st.session_state.graph_data = {
#             "type":"category_single",
#             "data":data
#         }

#         return

#     # full categories
#     this_group = df_this.groupby("category")["amount"].sum().reset_index()

#     st.session_state.graph_data = {
#         "type":"category_all",
#         "data":this_group,
#         "df_this":df_this,
#         "df_last":df_last
#     }


# 



# --------------------------------
# DASHBOARD
# --------------------------------
# def show_dashboard(graph_data):

#     data_type = graph_data["type"]

#     if data_type == "category_single":

#         df = graph_data["data"]

#         fig = px.bar(
#             df,
#             x="Month",
#             y="Amount",
#             color="Month",
#             template="plotly_dark"
#         )

#         st.plotly_chart(fig, use_container_width=True)


#     if data_type == "category_all":

#         df = graph_data["data"]

#         st.subheader("📊 Spending Dashboard")

#         # cards
#         total = df["amount"].sum()

#         #st.metric("💰 Total Spending", f"₹{total:.0f}")
#         col1, col2 = st.columns(2)

#         col1.metric("💰 Total Spending", f"₹{total:.0f}")
#         col2.metric("🧾 Categories", len(df))


#         # donut
#         fig1 = px.pie(
#             df,
#             names="category",
#             values="amount",
#             hole=0.5,
#             template="plotly_dark"
#         )

#         st.plotly_chart(fig1, use_container_width=True)

#         # bar chart
#         fig2 = px.bar(
#             df,
#             x="category",
#             y="amount",
#             color="category",
#             template="plotly_dark"
#         )

#         st.plotly_chart(fig2, use_container_width=True)


# def show_dashboard(graph_data):

#     data_type = graph_data["type"]

#     # -----------------------------
#     # CATEGORY SINGLE (Food example)
#     # -----------------------------
#     if data_type == "category_single":

#         df = graph_data["data"]

#         fig = px.bar(
#             df,
#             x="Month",
#             y="Amount",
#             color="Month",
#             template="plotly_dark",
#             text="Amount"
#         )

#         fig.update_layout(
#             title="Category Spending Comparison",
#             xaxis_title="Month",
#             yaxis_title="Amount"
#         )

#         st.plotly_chart(fig, use_container_width=True)


#     # -----------------------------
#     # CATEGORY COMPARISON
#     # -----------------------------
#     elif data_type == "category_compare":

#         df = graph_data["data"]

#         fig = px.bar(
#             df,
#             x="category",
#             y=["This Month", "Last Month"],
#             barmode="group",
#             template="plotly_dark",
#             title="Category Comparison (This Month vs Last Month)"
#         )

#         st.plotly_chart(fig, use_container_width=True)


#     # -----------------------------
#     # FULL DASHBOARD
#     # -----------------------------
#     elif data_type == "category_all":

#         df = graph_data["data"]

#         st.subheader("📊 Spending Dashboard")

#         # -----------------------------
#         # CARDS
#         # -----------------------------
#         total = df["amount"].sum()

#         col1, col2 = st.columns(2)

#         col1.metric("💰 Total Spending", f"₹{total:.0f}")
#         col2.metric("🧾 Categories", len(df))


#         # -----------------------------
#         # DONUT CHART
#         # -----------------------------
#         fig1 = px.pie(
#             df,
#             names="category",
#             values="amount",
#             hole=0.55,
#             template="plotly_dark",
#             title="Category Distribution"
#         )

#         st.plotly_chart(fig1, use_container_width=True)


#         # -----------------------------
#         # BAR CHART
#         # -----------------------------
#         fig2 = px.bar(
#             df,
#             x="category",
#             y="amount",
#             color="category",
#             template="plotly_dark",
#             title="Category Spending"
#         )

#         st.plotly_chart(fig2, use_container_width=True)


#         # -----------------------------
#         # TREND GRAPH (optional)
#         # -----------------------------
#         # if "trend" in graph_data:
#         #     trend = graph_data["trend"]

#         if "graph_trend" in st.session_state and st.session_state.graph_trend is not None:

#             trend = st.session_state.graph_trend.copy()

#             # Ensure month is string for plotly
#             trend["month"] = trend["month"].astype(str)

#             st.subheader("📈 Monthly Spending Trend")

#             fig3 = px.line(
#                 trend,
#                 x="month",
#                 y="amount",
#                 markers=True,
#                 template="plotly_dark"
#             )

#             fig3.update_layout(
#                 xaxis_title="Month",
#                 yaxis_title="Amount Spent",
#                 hovermode="x unified"
#             )

#             st.plotly_chart(fig3, use_container_width=True)


def show_dashboard(graph_data):

    data_type = graph_data.get("type")

    # -----------------------------
    # TREND ONLY
    # -----------------------------
    if data_type == "trend":

        if st.session_state.graph_trend is None:
            st.info("No trend data available.")
            return

        trend = st.session_state.graph_trend.copy()
        trend["month"] = trend["month"].astype(str)

        st.subheader("📈 Monthly Spending Trend")

        fig = px.line(
            trend,
            x="month",
            y="amount",
            markers=True,
            template="plotly_dark"
        )

        fig.update_layout(
            xaxis_title="Month",
            yaxis_title="Amount Spent",
            hovermode="x unified"
        )

        st.plotly_chart(fig, use_container_width=True)

        return


    # -----------------------------
    # CATEGORY SINGLE
    # -----------------------------
    if data_type == "category_single":

        df = graph_data["data"]

        fig = px.bar(
            df,
            x="Month",
            y="Amount",
            color="Month",
            template="plotly_dark",
            text="Amount"
        )

        fig.update_layout(
            title="Category Spending Comparison",
            xaxis_title="Month",
            yaxis_title="Amount"
        )

        st.plotly_chart(fig, use_container_width=True)

        return


    # -----------------------------
    # CATEGORY COMPARISON
    # -----------------------------
    if data_type == "category_compare":

        df = graph_data["data"]

        st.subheader("📊 Category Comparison")

        fig = px.bar(
            df,
            x="category",
            y=["This Month", "Last Month"],
            barmode="group",
            template="plotly_dark"
        )

        st.plotly_chart(fig, use_container_width=True)

        return


    # -----------------------------
    # FULL DASHBOARD
    # -----------------------------
    if data_type == "category_all":

        df = graph_data["data"]

        st.subheader("📊 Spending Dashboard")

        # -----------------------------
        # TOTAL CARDS
        # -----------------------------
        total = df["amount"].sum()

        col1, col2 = st.columns(2)

        col1.metric("💰 Total Spending", f"₹{total:.0f}")
        col2.metric("🧾 Categories", len(df))


        # -----------------------------
        # % CHANGE VS LAST MONTH
        # -----------------------------
        if "df_last" in graph_data and "df_this" in graph_data:

            last_total = graph_data["df_last"]["amount"].sum()
            this_total = graph_data["df_this"]["amount"].sum()

            change = 0

            if last_total > 0:
                change = ((this_total - last_total) / last_total) * 100

            st.metric("📉 Change vs Last Month", f"{change:.1f}%")

            if change > 20:
                st.warning("⚠️ Your spending increased significantly compared to last month.")

            elif change < -20:
                st.success("📉 Great! Your spending decreased compared to last month.")


        # -----------------------------
        # DONUT CHART
        # -----------------------------
        fig1 = px.pie(
            df,
            names="category",
            values="amount",
            hole=0.55,
            template="plotly_dark",
            title="Category Distribution"
        )

        st.plotly_chart(fig1, use_container_width=True)


        # -----------------------------
        # CATEGORY BAR
        # -----------------------------
        fig2 = px.bar(
            df,
            x="category",
            y="amount",
            color="category",
            template="plotly_dark",
            title="Category Spending"
        )

        st.plotly_chart(fig2, use_container_width=True)


        # -----------------------------
        # MONTHLY TREND
        # -----------------------------
        if st.session_state.graph_trend is not None:

            trend = st.session_state.graph_trend.copy()
            trend["month"] = trend["month"].astype(str)

            st.subheader("📈 Monthly Spending Trend")

            fig3 = px.line(
                trend,
                x="month",
                y="amount",
                markers=True,
                template="plotly_dark"
            )

            fig3.update_layout(
                xaxis_title="Month",
                yaxis_title="Amount Spent",
                hovermode="x unified"
            )

            st.plotly_chart(fig3, use_container_width=True)


        # -----------------------------
        # AI SAVING SUGGESTION
        # -----------------------------
        top_category = df.sort_values("amount", ascending=False).iloc[0]

        st.info(
            f"💡 You spent the most on **{top_category['category']}** "
            f"(₹{top_category['amount']:.0f}). "
            f"Reducing this category could help save money."
        )


        # -----------------------------
        # NEXT MONTH PREDICTION
        # -----------------------------
        if "df_this" in graph_data:

            avg_daily = graph_data["df_this"]["amount"].mean()
            prediction = avg_daily * 30

            st.info(
                f"📈 Estimated next month spending: **₹{prediction:.0f}**"
            )

# --------------------------------
# ROUTER
# --------------------------------
if st.session_state.user_id is None:
    show_login()
else:
    show_main_app()