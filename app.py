import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Student Dashboard", page_icon="📊", layout="wide")
# ------------------------Page Title --------------------------------------
st.title("Student Performance Dashboard")

# ------------------------File Upload--------------------------------------
uploaded_file = st.file_uploader("Upload Student CSV File",type=["csv"])

# -----------------------Check if file uploaded---------------------------
if uploaded_file is not None:

    # ------------------Read CSV-------------------------------------------
    try:
        df = pd.read_csv(uploaded_file)
        if df.empty:
            st.error("The uploaded CSV file is empty.")
            st.stop()
        if any(".1" in col or col.endswith(tuple([f".{i}" for i in range(1,10)])) for col in df.columns):
            st.error("Duplicate column names found in the CSV file. Please ensure all column names are unique.")
            st.stop()
    except Exception as e:
        st.error(f"Error reading CSV file: {e}")
        st.stop()
    # -----------------Handle missing numeric values-----------------------
    numeric_cols = df.select_dtypes(include='number').columns

    if df[numeric_cols].isnull().values.any():
        st.warning("Some marks were missing and have been filled with 0.")
        df[numeric_cols] = df[numeric_cols].fillna(0)

    # -----------------Check Name Column-----------------------
    if "Name" not in df.columns:
        st.error("Dataset must contain a 'Name' column.")
        st.stop()

    df["Name"] = df["Name"].fillna("Unknown")

    # -----------------Detect Numeric Columns-----------------------
    excluded_columns = ["Attendance", "StudentID"]
    numeric_columns = [
        col for col in df.select_dtypes(include='number').columns
        if col not in excluded_columns
    ]

    # ----------------- Check Numeric Columns-----------------------
    if len(numeric_columns) == 0:
        st.error("No numeric subject columns found.")
        st.stop()

    # ------------------Subject Selection---------------------------
    st.sidebar.header("Dashboard Controls")

    subject_columns = st.sidebar.multiselect("Select Subject Columns",numeric_columns,default=numeric_columns)

    if len(subject_columns) == 0:
        st.warning("Please select at least one subject column.")
        st.stop()

    # ----------------- Total Calculation--------------------------
    df["Total"] = df[subject_columns].sum(axis=1)

    df["Rank"] = (df["Total"].rank(method="dense", ascending=False).astype(int))

    # -----------------Show Dataset---------------------------------
    st.subheader("Student Data")
    columns_order = ["Name"] + subject_columns + ["Total", "Rank"]
    st.dataframe(df,use_container_width=True)

    # ----------------Search Student--------------------------------
    search_name = st.sidebar.text_input("Search Student")

    if search_name:
        search_results = df[df["Name"].str.contains(search_name,case=False,na=False)]
        if not search_results.empty:
            st.subheader("Search Results")
            st.dataframe(search_results,use_container_width=True)
        else:
            st.warning("No student found.")

    # ----------------Student Selector------------------------------
    st.subheader("Student Details")
    df["Display Name"] = df["Name"] + " (" + (df.groupby("Name").cumcount() + 1).astype(str) + ")"
    df.loc[~df["Name"].duplicated(keep=False), "Display Name"] = df["Name"]

    student_name_display = st.sidebar.selectbox("Select Student",df["Display Name"])

    selected_student = df[df["Display Name"] == student_name_display]
    student = selected_student.iloc[0]

    # --------------Student Metrics----------------------------------
    total_marks = student[subject_columns].sum()
    average_marks = student[subject_columns].mean()

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Marks",f"{total_marks:.0f}")
    with col2:
        st.metric("Average Marks",f"{average_marks:.2f}")
    with col3:
        if "Attendance" in df.columns:
            try:
                att_val = float(str(student["Attendance"]).replace("%", "").strip())
                st.metric("Attendance", f"{att_val:.0f}%")
            except (ValueError, TypeError):
                st.metric("Attendance", str(student["Attendance"]))
        else:
            st.metric("Attendance", "N/A")
    with col4:
        st.metric("Rank", f"{student['Rank']} / {len(df)}")
    # --------------Performance Recommendation------------------------
    st.subheader("Performance Recommendation")

    weakest_subject = student[subject_columns].idxmin()
    lowest_score = student[subject_columns].min()

    st.write(f"Weakest Subject: {weakest_subject}")
    st.write(f"Current Score: {lowest_score}")

    if lowest_score < 40:
        st.error(f"Focus heavily on {weakest_subject}. Immediate improvement needed.")
    elif lowest_score < 60:
        st.warning(f"Practice more in {weakest_subject}.")
    else:
        st.success(f"Excellent performance. {weakest_subject} is your lowest-scoring subject, but all subjects are strong.")

    st.divider()

    # ------------------------Average Marks------------------------------------
    st.subheader("Average Marks")

    averages = {}
    for column in subject_columns:
        averages[column] = round(df[column].mean(),2)

    avg_df = pd.DataFrame(averages.items(),columns=["Subject","Average"])

    st.dataframe(avg_df,use_container_width=True)

    #--------------- Filter Students-----------------------------------
    st.subheader("Filter Students")

    if df["Total"].min() == df["Total"].max():
        st.sidebar.info("Only one student — filter not available.")
        filtered_students = df
    else:
        min_marks = st.sidebar.slider(
            "Select Minimum Total Marks",
            int(df["Total"].min()),
            int(df["Total"].max()),
            int(df["Total"].min())
        )
        filtered_students = df[df["Total"] >= min_marks]

    st.dataframe(filtered_students.drop(columns=["Display Name"], errors="ignore"),use_container_width=True)

    # ----------------Top Performer--------------------------------------
    st.subheader("Top Performer")

    highest_marks = df["Total"].max()
    toppers = df[df["Total"] == highest_marks]
    st.write("Highest Marks:", highest_marks)

    st.dataframe(
        toppers[["Name", "Total"]],
        use_container_width=True
    )
    st.divider()

    # ----------------Weak Students---------------------------------------
    st.subheader("Student Risk Analysis")

    risk_df = df.copy()
    risk_df["Average"] = (risk_df[subject_columns].mean(axis=1).round(2))

    def classify_risk(avg):
        if avg < 40:   return "🔴 High Risk"
        elif avg < 60: return "🟡 Needs Attention"
        else:          return "🟢 Safe"

    risk_df["Risk Status"] = (risk_df["Average"].apply(classify_risk))

    # ----------------Weakest Subject--------------------------------------
    risk_df["Subject to Improve"] = (risk_df[subject_columns] .idxmin(axis=1))

    # -----------------Lowest Score-----------------------------------------
    risk_df["Lowest Score"] = (risk_df[subject_columns].min(axis=1))
    risk_df["Recommendation"] = risk_df.apply(
        lambda row:f"Focus on {row['Subject to Improve']}"
        if row["Risk Status"] != "🟢 Safe"
        else "Maintain current performance",
        axis=1
    )

    st.dataframe(
        risk_df[["Name","Average","Risk Status","Subject to Improve","Lowest Score","Recommendation"]],
        use_container_width=True
    )
    #------------------ Visualizations --------------------------------------
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Subject Average Comparison")
        subjects = list(averages.keys())
        average_values = list(averages.values())
        if sum(average_values) > 0:
            fig, ax = plt.subplots()
            ax.bar(subjects, average_values, color='steelblue', edgecolor='white')
            ax.set_ylabel("Average")
            ax.set_title("Average by Subject")
            ax.set_ylim(bottom=0)
            plt.xticks(rotation=45,ha="right")
            plt.tight_layout()
            st.pyplot(fig)
        else:
            st.warning("Cannot create bar chart because all values are zero.")
    with col2:
        st.subheader("Average Distribution")
        fig2, ax2 = plt.subplots()
        if sum(average_values) > 0:
            ax2.pie(average_values, labels=subjects, autopct="%1.1f%%")
            ax2.set_title("Subject Contribution")
            plt.tight_layout()
            st.pyplot(fig2)
        else:
            st.warning("Cannot create pie chart because all values are zero.")

    st.divider()

    #---------------- Download Report--------------------------------
    st.subheader("Download Report")
    csv = df.to_csv(index=False)
    st.download_button(
        label="Download Processed CSV",
        data=csv,
        file_name="processed_student_report.csv",
        mime="text/csv"
    )
else:
    st.info("Please upload a CSV file to continue.")