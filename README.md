# 🎓 Student Performance Dashboard

![Python](https://img.shields.io/badge/Python-blue?logo=python)
![Pandas](https://img.shields.io/badge/Pandas-150458?logo=pandas)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-11557c)

[![Live Demo](https://img.shields.io/badge/🚀%20Live%20Demo-Open-green?style=for-the-badge)](https://student-performance-dashboard-kn3aqxvfy3dgmarj9lx4yz.streamlit.app/)

A dynamic and interactive Student Performance Analytics Dashboard built using Python, Pandas, Streamlit, and Matplotlib.

## 🚀 Live Demo

https://student-performance-dashboard-kn3aqxvfy3dgmarj9lx4yz.streamlit.app/

## 📸 Screenshots

### Dashboard Overview

![Dashboard Overview](screenshots/dashboard-overview.png)

### Risk Analysis

![Risk Analysis](screenshots/risk-analysis.png)

### Charts and Analytics

![Charts](screenshots/charts.png)

## 📌 Project Overview

This dashboard helps analyze student academic performance through interactive visualizations, ranking, risk analysis, filtering, and personalized recommendations.

Users can upload a CSV file containing student records and instantly view insights about student performance.

## ✨ Features

- Upload CSV datasets
- Automatic numeric subject detection
- Student search functionality
- Duplicate student name handling
- Student ranking system
- Top performer identification
- Student risk analysis
- Performance recommendations
- Subject-wise average calculation
- Minimum total marks filtering
- Interactive student tables
- Bar chart visualization
- Pie chart visualization
- Download processed reports

## 🛠 Technologies Used

- Python
- Pandas
- Streamlit
- Matplotlib
- Git
- GitHub
- Streamlit Community Cloud

## 📊 Dashboard Modules

### Student Data

Displays student records with calculated totals and rankings.

### Student Search

Search students by name and view filtered results.

### Student Details

Shows:

- Total Marks
- Average Marks
- Attendance
- Class Rank

### Performance Recommendation

Provides recommendations based on the student's weakest subject.

### Top Performer

Identifies the student with the highest total marks.

### Student Risk Analysis

Classifies students into:

- Safe
- Needs Attention
- High Risk

### Student Filtering

Allows users to filter students using the minimum total marks slider.

### Visualizations

- Subject Average Comparison (Bar Chart)
- Average Distribution (Pie Chart)

### Report Export

Download processed student data as a CSV file.

## 📂 Dataset Requirements

The uploaded CSV file **must contain a `Name` column**.

The `Name` column is required to identify and select students.

Example:

```csv
Name,Maths,Science,English,Attendance
Rahul,85,90,88,95
Kiran,92,91,95,98
Arjun,75,82,85,90
```

If the CSV does not contain a `Name` column, the dashboard will display an error and will not process the dataset.

## 🔢 Subject Column Handling

The dashboard automatically detects subject columns that contain numeric marks.

For example:

```csv
Name,Maths,Maths 2,Science,English
Arjun,80,85,90,78
Meena,92,88,94,91
Rahul,45,55,60,50
```

The numeric subject columns are used for performance calculations.

If a subject column contains non-numeric values, that column is removed from subject-based numerical analysis.

For example:

```csv
Name,Maths,Science,English
Rahul,85,90,Good
Kiran,92,91,Excellent
Arjun,75,82,Average
```

Here, `English` contains non-numeric values, so it is not used for:

- Total Marks
- Average Marks
- Rankings
- Subject Averages
- Risk Analysis
- Recommendations
- Charts

## 📝 Missing Marks

If marks are missing from a numeric subject column, the missing values are filled with `0`.

The dashboard also displays a notification informing the user that missing marks have been filled with zero.

## 👥 Duplicate Student Names

The dashboard supports students with duplicate names.

For example:

- Arjun (1)
- Arjun (2)
- Meena
- Rahul

This allows each student to be selected and analyzed separately even when multiple students have the same name.

## 🧮 Automatic Calculations

### Total Marks

Total marks are calculated using the selected numeric subject columns.

```text
Total Marks = Sum of Subject Marks
```

### Average Marks

```text
Average Marks = Total Marks / Number of Selected Subjects
```

### Ranking

Students are ranked according to their total marks.

### Subject Average

The dashboard calculates the average marks for each selected subject.

## 🔄 Dynamic Subject Selection

Users can select the subject columns they want to analyze.

Changing the selected subjects dynamically updates the relevant:

- Total Marks
- Average Marks
- Recommendations
- Subject comparisons
- Charts

## 🎚️ Minimum Marks Filter

The dashboard provides a minimum total marks slider.

Students whose total marks are below the selected minimum value are filtered out.

The slider can be moved across the available total-mark range, including minimum and maximum values.

## 📊 Example Dashboard Workflow

```text
Upload CSV
     ↓
Check Name Column
     ↓
Detect Numeric Subject Columns
     ↓
Handle Missing / Invalid Data
     ↓
Calculate Total & Average Marks
     ↓
Calculate Rankings
     ↓
Search / Select Students
     ↓
Generate Recommendations
     ↓
Perform Risk Analysis
     ↓
Display Charts & Analytics
     ↓
Download Processed CSV
```

## 📂 Project Structure

```text
student-performance-dashboard/
│
├── app.py
├── dataset.csv
├── fdataset.csv
├── requirements.txt
├── README.md
├── LICENSE
│
└── screenshots/
    ├── dashboard-overview.png
    ├── risk-analysis.png
    └── charts.png
```

## 🖥️ Installation

Clone the repository:

```bash
git clone https://github.com/Srishanth-45/student-performance-dashboard.git
cd student-performance-dashboard
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
streamlit run app.py
```

## 🌐 Deployment

The application is deployed using Streamlit Community Cloud.

Live application:

https://student-performance-dashboard-kn3aqxvfy3dgmarj9lx4yz.streamlit.app/

## 👨‍💻 Author

Srishanth Samala

GitHub: https://github.com/Srishanth-45

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
