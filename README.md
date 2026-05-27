# 🎓 CampusInsight – Generative AI-Powered Feedback Analytics System

## 📌 Project Overview

CampusInsight is a Generative AI-powered feedback analytics system designed to collect, analyze, and visualize student feedback intelligently. The system uses NLP, sentiment analysis, AI-generated insights, and interactive dashboards to help institutions improve faculty performance, campus facilities, placements, and student experience.

---

# 🚀 Objective

The main objective of this project is to develop an intelligent feedback management system that:

- Collects structured student feedback digitally
- Performs AI-based sentiment analysis
- Generates intelligent insights and recommendations
- Detects common issues automatically
- Visualizes analytics through interactive dashboards
- Assists institutions in data-driven decision making

---

# ❗ Problem Statement

Traditional feedback systems in educational institutions are mostly manual and lack intelligent analysis capabilities. Challenges include:

- Manual feedback collection
- Difficult analysis of large datasets
- No sentiment understanding
- Lack of real-time insights
- No intelligent recommendation system
- Poor visualization of analytics

These limitations make it difficult for institutions to identify critical issues and improve overall student satisfaction.

---

# 💡 Proposed Solution

CampusInsight solves these problems by providing an AI-driven feedback analytics platform that:

- Digitally collects student feedback
- Stores data using SQLite database
- Uses NLP for sentiment analysis
- Integrates Gemini API for AI-generated insights and recommendations
- Detects common issues using text analysis
- Displays analytics using interactive visual dashboards

The system enables institutions to monitor faculty performance, facilities, placements, and student satisfaction effectively.

---

# 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core programming |
| Streamlit | Frontend & dashboard |
| SQLite | Database storage |
| SQLAlchemy | ORM database handling |
| Pandas | Data processing |
| Plotly | Interactive visualizations |
| NLP (TextBlob/VADER) | Sentiment analysis |
| Gemini API | Generative AI insights |
| FPDF | PDF report generation |

---

# ⚙️ Key Features

## 👨‍🎓 Student Module
- Student feedback form
- Department & year selection
- Teacher/facility/event feedback categories
- Dynamic rating system
- Text feedback submission

## 🤖 AI Features
- NLP-based sentiment analysis
- Gemini-powered AI insights
- AI-generated recommendations
- Common issue detection
- Intelligent feedback summarization

## 📊 Admin Dashboard
- Interactive analytics dashboard
- Department-wise analytics
- Teacher-wise analytics
- Sentiment visualization
- Rating distribution graphs
- Trend analysis

## 📄 Report Generation
- CSV report export
- PDF analytics report generation

## 🔐 Authentication
- Admin password protection
- Separate student/admin access

---

# 🧠 AI & NLP Workflow

1. Student submits feedback through the Streamlit interface  
2. Feedback data is stored in SQLite database  
3. NLP-based sentiment analysis processes the feedback text  
4. Gemini API generates AI insights and recommendations  
5. Common issues are detected using text analysis  
6. Analytics data is processed using Pandas  
7. Interactive charts and dashboards are generated using Plotly  
8. Admin dashboard displays insights, trends, and performance analytics  
9. Reports can be exported as CSV and PDF for institutional analysis
