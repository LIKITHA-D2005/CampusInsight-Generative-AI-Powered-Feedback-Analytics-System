import streamlit as st
import pandas as pd
import plotly.express as px

from fpdf import FPDF

from database import engine
from database import SessionLocal

from models import Base
from models import Feedback

from sentiment import analyze_sentiment

from analytics import (
    generate_ai_insight,
    generate_recommendation,
    detect_common_issues,
    generate_chat_reply
)

# ======================================================
# DATABASE
# ======================================================

Base.metadata.create_all(bind=engine)

# ======================================================
# PAGE CONFIG
# ======================================================

st.set_page_config(

    page_title="AI College Feedback System",

    layout="wide"
)

# ======================================================
# TITLE
# ======================================================

st.title("🎓 AI-Powered College Feedback System")

# ======================================================
# LOGIN
# ======================================================

role = st.sidebar.selectbox(

    "Login As",

    [
        "Student",
        "Admin"
    ]
)

admin_access = False

if role == "Admin":

    password = st.sidebar.text_input(

        "Enter Admin Password",

        type="password"
    )

    if password:

        if password == "admin123":

            admin_access = True

        else:

            st.sidebar.error(
                "Incorrect Password"
            )

# ======================================================
# STUDENT SECTION
# ======================================================

if role == "Student":

    st.subheader("Student Feedback Form")

    # ---------------- STUDENT DETAILS ----------------

    usn = st.text_input("Enter USN")

    department = st.selectbox(

        "Select Department",

        [
            "CSE",
            "ISE",
            "ECE",
            "EEE",
            "MECH",
            "CIVIL",
            "AIML",
            "AS"
        ]
    )

    year = st.selectbox(

        "Select Year",

        [
            "1st Year",
            "2nd Year",
            "3rd Year",
            "4th Year"
        ]
    )

    # ---------------- FEEDBACK TYPE ----------------

    feedback_type = st.selectbox(

        "Select Feedback Type",

        [
            "Teacher Feedback",
            "Facilities Feedback",
            "Events Feedback",
            "Club Activities",
            "Placement Support"
        ]
    )

    teacher_name = ""

    subject = ""

    # ---------------- TEACHER DETAILS ----------------

    if feedback_type == "Teacher Feedback":

        teacher_name = st.selectbox(

            "Select Teacher",

            [
                "Dr. Sharma",
                "Prof. Rao",
                "Dr. Mehta",
                "Prof. Kumar"
            ]
        )

        subject = st.selectbox(

            "Select Subject",

            [
                "Machine Learning",
                "DBMS",
                "Operating Systems",
                "Computer Networks"
            ]
        )

    # ---------------- QUESTIONS ----------------

    st.subheader("Rate the Following")

    questions = []

    if feedback_type == "Teacher Feedback":

        questions = [

            "Teaching Quality",

            "Subject Knowledge",

            "Communication Skills",

            "Doubt Clarification",

            "Student Interaction"
        ]

    elif feedback_type == "Facilities Feedback":

        questions = [

            "WiFi Quality",

            "Lab Facilities",

            "Classroom Environment",

            "Library Resources",

            "Campus Cleanliness"
        ]

    elif feedback_type == "Events Feedback":

        questions = [

            "Event Organization",

            "Technical Exposure",

            "Participation Opportunities",

            "Speaker Sessions",

            "Overall Experience"
        ]

    elif feedback_type == "Club Activities":

        questions = [

            "Club Engagement",

            "Learning Opportunities",

            "Team Collaboration",

            "Activity Quality",

            "Overall Club Experience"
        ]

    elif feedback_type == "Placement Support":

        questions = [

            "Mock Interviews",

            "Resume Guidance",

            "Company Opportunities",

            "Training Sessions",

            "Placement Preparation"
        ]

    # ---------------- RATINGS ----------------

    ratings = []

    for question in questions:

        rating = st.slider(

            question,

            1,

            5,

            3
        )

        ratings.append(rating)

    overall_rating = sum(ratings) / len(ratings)

    st.write(
        f"### Overall Rating: {overall_rating:.1f}/5"
    )

    rating1 = ratings[0]
    rating2 = ratings[1]
    rating3 = ratings[2]
    rating4 = ratings[3]
    rating5 = ratings[4]

    # ---------------- FEEDBACK ----------------

    feedback_text = st.text_area(

        "Additional Feedback (Max 500 characters)",

        max_chars=500
    )

    # ---------------- SUBMIT ----------------

    if st.button("Submit Feedback"):

        sentiment = analyze_sentiment(
            feedback_text
        )

        db = SessionLocal()

        new_feedback = Feedback(

            usn=usn,

            department=department,

            year=year,

            feedback_type=feedback_type,

            teacher_name=teacher_name,

            subject=subject,

            rating1=rating1,

            rating2=rating2,

            rating3=rating3,

            rating4=rating4,

            rating5=rating5,

            overall_rating=overall_rating,

            feedback_text=feedback_text,

            sentiment=sentiment
        )

        db.add(new_feedback)

        db.commit()

        st.success(
            "Feedback submitted successfully!"
        )

        # ---------------- GEMINI REPLY ----------------

        if overall_rating >= 4:

            st.success(
        "Thank you for your valuable feedback!"
        )

        elif overall_rating >= 3:

            st.info(
        "Thank you. We will look into your feedback."
         )

        else:

            st.warning(
        "Thank you for your honest feedback. "
        "We will work on improvements."
    )

# ======================================================
# ADMIN SECTION
# ======================================================

if role == "Admin" and admin_access:

    st.title("📊 AI Analytics Dashboard")

    db = SessionLocal()

    feedback_data = db.query(Feedback).all()

    if feedback_data:

        data = []

        for item in feedback_data:

            data.append({

                "Teacher": item.teacher_name,

                "Department": item.department,

                "Feedback Type": item.feedback_type,

                "Overall Rating": item.overall_rating,

                "Sentiment": item.sentiment,

                "Feedback Text": item.feedback_text
            })

        df = pd.DataFrame(data)

        # ---------------- FILTER ----------------

        dashboard_filter = st.selectbox(

            "Select Dashboard Type",

            [
                "Teacher Feedback",
                "Facilities Feedback",
                "Events Feedback",
                "Club Activities",
                "Placement Support"
            ]
        )

        filtered_df = df[
            df["Feedback Type"] == dashboard_filter
        ]

        # ---------------- METRICS ----------------

        col1, col2, col3 = st.columns(3)

        avg_rating = round(

            filtered_df["Overall Rating"].mean(),

            2
        )

        total_feedbacks = len(filtered_df)

        positive_count = len(

            filtered_df[
                filtered_df["Sentiment"] == "Positive"
            ]
        )

        with col1:

            st.metric(
                "Average Rating",
                avg_rating
            )

        with col2:

            st.metric(
                "Total Feedbacks",
                total_feedbacks
            )

        with col3:

            st.metric(
                "Positive Feedbacks",
                positive_count
            )

        # ---------------- TABLE ----------------

        if dashboard_filter != "Teacher Feedback":

            st.subheader("Feedback Records")

            st.dataframe(filtered_df)

        # ---------------- CSV DOWNLOAD ----------------

        csv = filtered_df.to_csv(index=False)

        st.download_button(

            label="📥 Download Feedback Report CSV",

            data=csv,

            file_name="feedback_report.csv",

            mime="text/csv"
        )

        # ---------------- PDF REPORT ----------------

        if st.button("Generate PDF Report"):

            pdf = FPDF()

            pdf.add_page()

            pdf.set_font(
                "Arial",
                size=12
            )

            pdf.cell(

                200,

                10,

                txt="College Feedback Analytics Report",

                ln=True,

                align='C'
            )

            pdf.ln(10)

            pdf.cell(

                200,

                10,

                txt=f"Dashboard Type: {dashboard_filter}",

                ln=True
            )

            pdf.cell(

                200,

                10,

                txt=f"Average Rating: {avg_rating}",

                ln=True
            )

            pdf.cell(

                200,

                10,

                txt=f"Total Feedbacks: {total_feedbacks}",

                ln=True
            )

            pdf.output("feedback_report.pdf")

            with open(

                "feedback_report.pdf",

                "rb"

            ) as file:

                st.download_button(

                    label="📄 Download PDF Report",

                    data=file,

                    file_name="feedback_report.pdf",

                    mime="application/pdf"
                )

        # ======================================================
        # TEACHER ANALYTICS
        # ======================================================

        if dashboard_filter == "Teacher Feedback":

            st.subheader("Teacher Analytics")

            # ---------------- DEPARTMENT FILTER ----------------

            department_list = filtered_df[
                "Department"
            ].dropna().unique()

            selected_department = st.selectbox(

                "Select Department",

                department_list
            )

            dept_filtered_df = filtered_df[

                filtered_df["Department"]
                == selected_department
            ]

            # ---------------- TEACHER FILTER ----------------

            teacher_list = dept_filtered_df[
                "Teacher"
            ].dropna().unique()

            selected_teacher = st.selectbox(

                "Select Teacher",

                teacher_list
            )

            teacher_df = dept_filtered_df[

                dept_filtered_df["Teacher"]
                == selected_teacher
            ]

            # ---------------- METRICS ----------------

            total_teacher_feedbacks = len(
                teacher_df
            )

            teacher_avg_rating = round(

                teacher_df[
                    "Overall Rating"
                ].mean(),

                2
            )

            positive_reviews = len(

                teacher_df[
                    teacher_df["Sentiment"]
                    == "Positive"
                ]
            )

            col1, col2, col3 = st.columns(3)

            with col1:

                st.metric(

                    "Total Feedbacks",

                    total_teacher_feedbacks
                )

            with col2:

                st.metric(

                    "Average Rating",

                    teacher_avg_rating
                )

            with col3:

                st.metric(

                    "Positive Reviews",

                    positive_reviews
                )

            # ---------------- FEEDBACK TEXTS ----------------

            st.subheader("Student Feedbacks")

            for feedback in teacher_df[
                "Feedback Text"
            ]:

                st.info(feedback)

            # ---------------- RATING GRAPH ----------------

            st.subheader("Rating Distribution")

            fig_rating = px.histogram(

                teacher_df,

                x="Overall Rating",

                nbins=5,

                title=f"{selected_teacher} Rating Distribution"
            )

            st.plotly_chart(fig_rating)

            # ---------------- SENTIMENT GRAPH ----------------

            sentiment_count = teacher_df[
                "Sentiment"
            ].value_counts().reset_index()

            sentiment_count.columns = [
                "Sentiment",
                "Count"
            ]

            st.subheader("Sentiment Analysis")

            fig_sentiment = px.pie(

                sentiment_count,

                names="Sentiment",

                values="Count",

                title=f"{selected_teacher} Sentiment Distribution"
            )

            st.plotly_chart(fig_sentiment)

            # ---------------- AI PERFORMANCE SUMMARY ----------------

            st.subheader("Performance Summary")

            summary_prompt = f"""

            Analyze this faculty performance.

            Teacher:
            {selected_teacher}

            Department:
            {selected_department}

            Average Rating:
            {teacher_avg_rating}

            Generate a short professional summary.
            """

            ai_summary = generate_ai_insight(

                teacher_avg_rating,

                selected_teacher
            )

            st.success(ai_summary)

            # ---------------- PERFORMANCE STATUS ----------------

            if teacher_avg_rating >= 4:

                st.success(
                    "Excellent Faculty Performance"
                )

            elif teacher_avg_rating >= 3:

                st.warning(
                    "Average Faculty Performance"
                )

            else:

                st.error(
                    "Faculty Performance Needs Improvement"
                )
        # ======================================================
        # NON-TEACHER ANALYTICS
        # ======================================================

        else:

            st.subheader("Overall Feedback Analysis")

            # ---------------- SENTIMENT PIE ----------------

            sentiment_count = filtered_df[
                "Sentiment"
            ].value_counts().reset_index()

            sentiment_count.columns = [
                "Sentiment",
                "Count"
            ]

            fig_sentiment = px.pie(

                sentiment_count,

                names="Sentiment",

                values="Count",

                title="Positive vs Negative Reviews"
            )

            st.plotly_chart(fig_sentiment)

            # ---------------- RATING DISTRIBUTION ----------------

            st.subheader("Rating Distribution")

            fig_rating = px.histogram(

                filtered_df,

                x="Overall Rating",

                nbins=5,

                title="Feedback Rating Distribution"
            )

            st.plotly_chart(fig_rating)

            # ---------------- AI SUMMARY ----------------

            positive_reviews = len(

                filtered_df[
                    filtered_df["Overall Rating"] >= 3.5
                ]
            )

            negative_reviews = len(

                filtered_df[
                    filtered_df["Overall Rating"] < 3.5
                ]
            )

            if positive_reviews > negative_reviews:

                st.success(

                    "Overall student satisfaction "
                    "appears positive for this category."
                )

            else:

                st.warning(

                    "Students appear dissatisfied "
                    "in this category. Improvements "
                    "may be required."
                )

        # ======================================================
        # DEPARTMENT ANALYTICS
        # ======================================================

        dept_avg = filtered_df.groupby(

            "Department"

        )["Overall Rating"].mean().reset_index()

        st.subheader("Department-wise Ratings")

        fig_dept = px.bar(

            dept_avg,

            x="Department",

            y="Overall Rating",

            color="Overall Rating",

            title="Department Performance"
        )

        st.plotly_chart(fig_dept)

        # ======================================================
        # AI INSIGHTS
        # ======================================================

        st.subheader("AI Insights")

        average_score = filtered_df[
            "Overall Rating"
        ].mean()

        insight = generate_ai_insight(

            average_score,

            dashboard_filter
        )

        st.info(insight)

        # ======================================================
        # AI RECOMMENDATIONS
        # ======================================================

        st.subheader("AI Recommendations")

        feedback_texts = filtered_df[
            "Feedback Text"
        ].dropna().tolist()

        for text in feedback_texts[:1]:

            recommendation = generate_recommendation(
                text
            )

            st.info(recommendation)

        # ======================================================
        # COMMON ISSUES
        # ======================================================

        st.subheader("Common Issues Detection")

        feedback_list = filtered_df[
            "Feedback Text"
        ].dropna().tolist()

        common_issue = detect_common_issues(
            feedback_list
        )

        st.warning(common_issue)

    else:

        st.info(
            "No feedback data available yet."
        )