# 🌌 NexusERP - Premium Enterprise Suite

NexusERP is a unified, state-of-the-art Enterprise Resource Planning (ERP) suite designed to streamline business relations, manage scheduling, simplify task tracking, automate cloud file storage, and generate industry-grade PDFs for Quotations and Proforma Invoices. 

Built on a robust, asynchronous **FastAPI** backend and styled with a custom, sleek **modern glassmorphic frontend UI**, NexusERP comes fully integrated with **Google Workspace APIs** (Google Drive & Google Calendar).

---

## 🚀 Key Features Walkthrough

### 1. 🔐 Secure Authentication & Session Hub
*   **Role-Based Access**: Multi-user login profiles supporting default **Admin** (`admin1` / `admin123`) and **User** (`user1` / `user123`) authorization tiers.
*   **Security Architecture**: Secure session storage and custom JWT token handles ensuring that APIs are restricted to active, authenticated sessions.
*   **Aesthetics**: Sleek glassmorphism login screen with glowing mesh gradients and custom form micro-animations.

### 2. 📊 Live Interactive Dashboard
*   **Executive Intelligence**: Real-time counters showing Total Buyers, Total Manufacturers, Pending Tasks, and Scheduled Calendar Events.
*   **Performance Metrics**: Integrated charts and activity pipelines detailing current database entries and system health parameters.
*   **Quick Action Drawer**: Fast-navigation panels to jump directly to document generation, scheduler, or upload hub.

### 3. 💼 Buyer & Manufacturer CRM
*   **Comprehensive Profiles**: Track business name, GST identification, active payment terms, addresses, and multi-country defaults.
*   **Categorization**: Organizes manufacturers by primary product categories and filters buyers by geographical locations.
*   **Live Search & Pagination**: Full-text client search filter powered by dynamic, stateful database queries.

### 4. 📅 Integrated Google Calendar Scheduler
*   **OAuth 2.0 Integration**: Syncs seamlessly with Google Calendar using secure, client-consent flow.
*   **Type-Based Event Categories**: Color-coded scheduling for *Appointments*, *Meetings*, *Tasks*, and *Events*.
*   **Event Lifecycle Manager**: Add, view, edit status (Scheduled, Completed, Cancelled), set start/end durations, and configure custom locations.

### 5. 📋 Status-Driven Task Management Board
*   **Collaborative Tasks**: Assign tasks to administrators with custom deadlines and detailed markdown-capable descriptions.
*   **Task Statuses & Priorities**: Color-coded categorization by Status (*Pending*, *In Progress*, *Completed*) and Priority (*Low*, *Medium*, *High*).
*   **Deadlines & Alerts**: Dynamic highlighting of overdue tasks to keep projects and deliveries on time.

### 6. 📤 Drive-Powered Document Hub
*   **Dual Storage Sync**: Automatically uploads files to the local server storage and synchronizes them instantly onto your Google Drive.
*   **Structured Folder Auto-Creation**: Dynamically creates standard folder structures on Google Drive to match files.
*   **Interactive Explorer**: Interactive list of uploaded files, complete with metadata (size, upload timestamp, Google Drive ID).

### 7. 📄 Gold-Standard Quotation Generator
*   **Interactive Product Itemizer**: Dynamically add multiple products with HS Codes, rates, packaging, and descriptions.
*   **Formula Calculations**: Automatic on-the-fly math for unit rate totals, customizable percentage discounts, and final values.
*   **ReportLab PDF Generation**: Generates pixel-perfect, gold-and-navy themed professional PDF quotations ready for direct printing or client sharing.

### 8. 💸 Enterprise Proforma Invoice System
*   **Export Logistics**: Includes comprehensive cargo tracking inputs (Port of Loading, Port of Discharge, Mode of Shipment, Delivery Time).
*   **L/C & Payment Terms**: Supports custom advance payment vs Letter of Credit (L/C) percentage configurations.
*   **Declaration & Legal Standard**: Embeds international trade declarations of origin, amount-in-words translations, and stylized CEO signatures.

---

## 🛠️ Technology Stack

*   **Backend Framework**: FastAPI (Python 3.9+) - Ultra-fast, async-ready, auto-documented.
*   **Database Engine**: SQLAlchemy & SQLite - Lightweight and structured relational database.
*   **Google Workspace Integrations**: Google Calendar API & Google Drive API (v3) via Google OAuth client.
*   **PDF Generation**: ReportLab - Direct stream-to-buffer canvas rendering for custom formatting.
*   **Frontend Interface**: Modern HTML5, Vanilla CSS3 (Custom Glassmorphic Theme), and pure asynchronous Vanilla JavaScript.

---

## 📁 Repository Structure

```tree
NexusERP/
├── main.py                    # Application entry point & FastAPI setup
├── reset_database.py          # Database initializer and default admin creator
├── clear.py                   # Utility to clear temporary tokens & test logs
├── test.py                    # Test suite for verifying API functionalities
├── .gitignore                 # Safe workspace tracking exclusion rules
│
├── api/                       # API Business Logic Layer
│   └── routes/
│       ├── auth.py            # Login, Google OAuth initialization, & callback
│       ├── buyer.py           # CRUD operations for Buyers
│       ├── calendar.py        # Calendar synchronization and CRUD endpoints
│       ├── file_upload.py     # File uploading and Google Drive integration
│       ├── manufacturer.py    # CRUD operations for Manufacturers
│       ├── proforma_invoice.py# reportlab PDF generation for Invoices
│       ├── quotation.py       # reportlab PDF generation for Quotations
│       └── tasks.py           # CRUD operations for Admin Tasks
│
├── database/                  # SQLite Connection & Schemas
│   ├── connection.py          # SQLAlchemy engine and session initializer
│   └── models.py              # Relational models (Admin, Buyer, Manufacturer, Task, Event)
│
├── schemas/                   # Pydantic Schemas for Request/Response Validation
│   ├── auth.py, buyer.py, calendar.py, manufacturer.py, 
│   ├── proforma_invoice.py, quotation.py, task.py
│
├── utils/                     # Core Business Helper Scripts
│   ├── auth.py                # Password hashing and session token verification
│   ├── google_drive.py        # Google Drive API upload stream handler
│   └── storage.py             # Local storage system setup and uploads directory rules
│
└── static/                    # Premium Glassmorphic Frontend Client
    ├── index.html             # Sleek Login view
    ├── dashboard.html         # Live Admin Dashboard
    ├── buyers.html            # Buyers Relationship Panel
    ├── manufacturers.html     # Manufacturers relationship Panel
    ├── calendar.html          # Interactive Calendar view
    ├── tasks.html             # Tasks tracking board
    ├── uploads.html           # Google Drive Upload Hub
    ├── quotation.html         # Quotation generation tool
    ├── proforma_invoice.html  # Proforma Invoice generator
    ├── css/
    │   └── style.css          # Custom styling containing premium gradients & variables
    └── js/
        └── [api, auth, buyers, config, dashboard, manufacturers, tasks, theme, uploads].js
```

---

## ⚙️ Local Setup Guide

### 1. Prerequisites
Ensure you have Python (version 3.9 or higher) and Git installed on your system.

### 2. Setup Virtual Environment
Run the following commands inside the `NexusERP` directory:
```bash
# Create virtual environment
python -m venv venv

# Activate on Windows:
venv\Scripts\activate
# Activate on macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
NexusERP requires the following Python libraries. Install them via `pip`:
```bash
pip install fastapi uvicorn sqlalchemy reportlab google-api-python-client google-auth-httplib2 google-auth-oauthlib pydantic
```

### 4. Database Setup
Create and populate the database with demo users (`admin1` & `user1`):
```bash
python reset_database.py
```

### 5. Google Workspace Credentials (Optional)
To enable Google Calendar and Google Drive integrations:
1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a project, enable the **Google Calendar API** and **Google Drive API**.
3. Configure the OAuth Consent Screen and create **OAuth Client ID** credentials (Desktop Application).
4. Download the credentials as `credentials.json` and save it directly in the `NexusERP` root folder.
5. *(The application will automatically guide you through consent setup when you click "Connect Calendar" or "Upload to Drive" in the frontend)*.

---

## 🚀 Running the Server

Start the development server:
```bash
python main.py
```
Or use Uvicorn directly:
```bash
uvicorn main:app --port 8001 --reload
```

Open your browser and navigate to:
*   **Web Portal**: [http://127.0.0.1:8001](http://127.0.0.1:8001)
*   **Interactive API Docs**: [http://127.0.0.1:8001/docs](http://127.0.0.1:8001/docs)

---

### 🔑 Default Credentials
*   **Administrator**:
    *   *Username*: `admin1`
    *   *Password*: `admin123`
*   **Standard User**:
    *   *Username*: `user1`
    *   *Password*: `user123`

---
*Created with 💙 by Antigravity AI for NexusERP*
