# 🚦 TrafficVision – Traffic Violation & Accident Hotspot Analysis

## 📌 Overview

TrafficVision is a web-based analytics platform designed to help monitor traffic violations, record accident details, identify accident hotspots, and visualize traffic-related insights. The system enables administrators to manage traffic records efficiently while providing interactive dashboards and reports for better decision-making.

---

## ✨ Features

* 🔐 Secure Admin Login
* 🚗 Add and Manage Traffic Violations
* 🚑 Record Accident Details
* 📍 Accident Hotspot Analysis
* 📊 Interactive Dashboard with Charts
* 📈 Traffic Statistics and Reports
* 🗄️ PostgreSQL Database Integration
* 🎨 Responsive User Interface
* 🔍 Search and View Records
* 📄 Organized Data Management

---

## 🛠️ Tech Stack

### Frontend

* HTML5
* CSS3
* JavaScript
* Bootstrap

### Backend

* Python
* Flask

### Database

* PostgreSQL

### Data Visualization

* Chart.js

---

## 📂 Project Structure

```text
TrafficVision/
│
├── app.py
├── requirements.txt
├── static/
│   ├── css/
│   ├── js/
│   └── images/
│
├── templates/
│   ├── login.html
│   ├── dashboard.html
│   ├── add_violation.html
│   ├── view_violations.html
│   ├── add_accident.html
│   ├── view_accidents.html
│   ├── hotspots.html
│   └── reports.html
│
├── database/
│   ├── schema.sql
│   └── db_connection.py
│
└── README.md
```

---

## ⚙️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/TrafficVision.git
cd TrafficVision
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate the environment:

**Windows**

```bash
venv\Scripts\activate
```

**Linux / macOS**

```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure PostgreSQL

* Create a PostgreSQL database.
* Update the database credentials in your Flask configuration or database connection file.

### 5. Run the Application

```bash
python app.py
```

Open your browser and visit:

```text
http://127.0.0.1:5000
```

---

## 📊 Dashboard Features

The dashboard provides:

* Total Traffic Violations
* Total Accident Records
* High-Risk Locations
* Monthly Traffic Trends
* Violation Distribution
* Accident Severity Analysis
* Interactive Charts

---

## 📍 Accident Hotspot Analysis

The system identifies locations with a high number of reported accidents, helping authorities:

* Detect high-risk areas
* Improve road safety
* Plan preventive measures
* Support traffic management decisions

---

## 💾 Database Tables

* Admins
* Violations
* Accidents

---

## 📸 Screenshots

Add screenshots of the following pages:

* Login Page
* Dashboard
* Add Violation
* View Violations
* Add Accident
* Accident Hotspots
* Reports Page

---

## 🚀 Future Enhancements

* AI-based Accident Prediction
* Real-Time Traffic Monitoring
* GIS Map Integration
* Email Notifications
* PDF Report Generation
* Mobile Responsive Dashboard
* Machine Learning for Risk Prediction
* User Role Management

---

## 🎯 Learning Outcomes

This project demonstrates practical knowledge of:

* Full Stack Web Development
* Python Flask Framework
* PostgreSQL Database Design
* CRUD Operations
* Data Visualization
* Dashboard Development
* Traffic Data Analysis
* Responsive Web Design

---

## 📄 License

This project is developed for educational and portfolio purposes.
