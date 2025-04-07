# 🚀 BoringLaunch Clone - Automated Startup Submission

## **📌 Project Overview**
This project is a **custom alternative to BoringLaunch**, designed for personal use. The goal is to **automate the submission of startup details** to multiple platforms. Since some platforms provide APIs while others do not, this project will use a **hybrid approach**:

✅ **For platforms with APIs:** Use **FastAPI + requests** to submit data directly.
✅ **For platforms without APIs:** Use **Selenium** to fill and submit forms automatically.

The system will extract platform details from an **Excel sheet**, categorize them based on API availability, and submit startup information accordingly.

---

## **🛠️ Tech Stack**
### **Backend:**
- **FastAPI** (for handling API-based submissions)
- **Python Requests** (to communicate with platforms via API)
- **Selenium** (for automating web submissions when APIs are unavailable)

### **Frontend:**
- **React.js** (for the UI)
- **Tailwind CSS** (for styling)

### **Database:**
- **Supabase** (preferred for easy setup & API integration)

### **Automation & Deployment:**
- **Celery + Redis** (for task queuing if needed)
- **Docker** (for containerization)
- **Cursor.sh** (as the development environment)

---

## **🔄 Workflow**
1. **User uploads an Excel sheet** with platform details.
2. **Categorization of platforms:**
   - Platforms with APIs → Handled by FastAPI.
   - Platforms without APIs → Handled by Selenium.
3. **User inputs startup details** (name, description, website, etc.).
4. **Automated submission process begins:**
   - API-based platforms receive data via FastAPI.
   - Non-API platforms get automated form submissions via Selenium.
5. **Results are logged and stored** for tracking submission status.

---

## **📌 Key Features**
- **Automated startup submission** across multiple platforms.
- **Excel-based platform categorization** for API and non-API sites.
- **React-based dashboard** to monitor submission status.
- **Error handling & logging** for failed submissions.
- **Database storage** of submitted startups.

---

## **🚀 Next Steps**
1. **Develop script for categorizing platforms from Excel.**
2. **Implement FastAPI for API-based submissions.**
3. **Build Selenium automation for non-API platforms.**
4. **Develop the React frontend for user interaction.**
5. **Integrate Supabase for storing submission history.**
6. **Optimize and deploy the system.**

---

## ** project structure**


boringlaunch-clone/
│── backend/                   # Backend folder (FastAPI & Selenium)
│   │── main.py                # FastAPI app entry point
│   │── requirements.txt        # Backend dependencies
│   │── config.py               # Configuration settings (API keys, DB URL)
│   │── database.py             # Supabase/MongoDB connection
│   │── models.py               # Database models (if using an ORM)
│   │── services/               # Business logic (submission, logging)
│   │   │── api_submit.py       # Handles API-based submissions
│   │   │── selenium_submit.py  # Handles Selenium-based submissions
│   │   │── excel_parser.py     # Parses Excel sheet to categorize platforms
│   │   │── logger.py           # Logs successful and failed submissions
│   │── routers/                # FastAPI routes
│   │   │── submissions.py      # API endpoints for startup submission
│   │── tests/                  # Backend testing
│   │   │── test_api.py         # Unit tests for API submission
│   │   │── test_selenium.py    # Unit tests for Selenium automation
│
│── frontend/                   # Frontend folder (React)
│   │── public/                 # Static assets
│   │── src/                    # React source code
│   │   │── components/         # Reusable UI components
│   │   │   │── Dashboard.js    # Dashboard UI
│   │   │   │── Form.js         # Form to input startup details
│   │   │── pages/              # Main pages
│   │   │   │── Home.js         # Home page
│   │   │   │── Submissions.js  # Displays submission status
│   │   │── services/           # API calls to backend
│   │   │   │── submissionAPI.js # Calls backend FastAPI endpoints
│   │   │── App.js              # Main React app
│   │   │── index.js            # Entry point
│   │── package.json            # Frontend dependencies
│   │── tailwind.config.js      # Tailwind CSS config
│
│── scripts/                    # Utility scripts
│   │── setup.py                # Initializes project (DB, dependencies)
│   │── run_tests.py            # Runs all tests
│
│── .env                        # Environment variables
│── docker-compose.yml          # Docker setup
│── README.md                   # Project documentation
│── project_overview.md         # Instructions for Cursor.ai



This document should guide Cursor.ai in assisting with the project. Let's automate startup submissions efficiently! 🚀

