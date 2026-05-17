# 🍽️ EJUST Kitchen — Restaurant Ordering System

<div align="center">

[![Live Demo](https://img.shields.io/badge/🌐%20Live%20Demo-amr510.pythonanywhere.com-brightgreen?style=for-the-badge)](https://amr510.pythonanywhere.com/)
[![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-Backend-black?style=for-the-badge&logo=flask)](https://flask.palletsprojects.com/)
[![SQLite](https://img.shields.io/badge/SQLite-Database-003B57?style=for-the-badge&logo=sqlite)](https://sqlite.org)
[![Pytest](https://img.shields.io/badge/Tested%20with-Pytest%20%2B%20Playwright-orange?style=for-the-badge)](https://pytest.org)

**A comprehensive restaurant management and ordering system built with Flask — covering everything from online ordering and live order tracking to a real-time Kitchen Display System, table reservations, and QR-based waiter calling.**

### 🚀 [View Live Demo](https://amr510.pythonanywhere.com/)



</div>

---

## 📸 Screenshots

### 🏠 Home Page
<img width="1907" height="916" alt="image" src="https://github.com/user-attachments/assets/30690cc6-fa94-4a52-86d7-cc5b97f832e9" />


### 🍕 Menu — Filterable by Category
<img width="1897" height="909" alt="image" src="https://github.com/user-attachments/assets/e8e3814a-02a0-4cfb-8aee-d37960506c56" />


### 🪑 Table Reservation
<img width="1902" height="924" alt="image" src="https://github.com/user-attachments/assets/3e25cbf2-6729-4635-a9ba-603c57100e30" />

---

## ✨ Features

### 👤 Customer Features

- **Menu Browsing** — Explore the menu with category filters: Main, Side, Drink, Dessert
- **Shopping Cart** — Add items to a persistent cart and adjust quantities
- **Order Placement** — Place an order with customer name and address/table info
- **Real-Time Order Tracking** — Track status from *Preparing* → *Out for Delivery* → *Delivered*
- **Table Reservations** — Book a table by date, time slot, and party size
- **Waiter Calling** — Scan a QR code at a table to call a waiter directly from your device

### 🧑‍💼 Staff & Admin Features

- **Admin Dashboard** — View key metrics: total revenue, order counts, and top-selling items
- **Kitchen Display System (KDS)** — Real-time dashboard for kitchen staff to manage orders as they move through the cooking process
- **Order Management** — View the full order queue and update statuses
- **Reservation Management** — View upcoming reservations and update status (Confirmed, Seated, etc.)
- **Waiter Call Queue** — Staff-facing interface to see and resolve pending table calls
- **Menu Management** — Add menu items, edit details, and toggle availability
- **User Management** — Create new staff and admin accounts

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Backend** | Python, Flask, SQLAlchemy |
| **Database** | SQLite |
| **Frontend** | HTML, CSS, JavaScript, Jinja2 |
| **Unit & Integration Tests** | Pytest |
| **End-to-End Tests** | Playwright |
| **Hosting** | PythonAnywhere |

---

## 🚀 Local Setup

### Prerequisites

- Python 3.x
- Node.js (for E2E tests only)

### Installation

1. **Clone the repository**

```bash
git clone https://github.com/amr-mohsen-ali/restaurant-ordering-system.git
cd restaurant-ordering-system
```

2. **Create and activate a virtual environment**

```bash
# macOS / Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
.\venv\Scripts\activate
```

3. **Install Python dependencies**

```bash
pip install -r requirements.txt
```

4. **Run the application**

```bash
python app.py
```

Visit `http://127.0.0.1:5000` — the database and seed data are created automatically on first run.

---

## 🧪 Running Tests

The project includes unit, integration, and end-to-end tests.

**Python tests (Pytest)**

```bash
pytest
```

**End-to-End tests (Playwright)**

> Make sure the Flask app is running in a separate terminal first.

```bash
npm install
npx playwright test
```

---

## 📁 Project Structure

```
.
├── app.py                  # Application entry point
├── requirements.txt        # Python dependencies
├── package.json            # Node.js dependencies (Playwright)
├── src/
│   ├── __init__.py         # Flask application factory
│   ├── admin.py            # Admin dashboard & management blueprints
│   ├── auth.py             # User authentication & authorization
│   ├── cart.py             # Shopping cart functionality
│   ├── database.py         # SQLAlchemy models & database seeding
│   ├── kitchen.py          # Kitchen Display System (KDS)
│   ├── menu.py             # Menu browsing
│   ├── order.py            # Order placement & management
│   ├── reservations.py     # Table reservations
│   └── tracking.py         # Order tracking
├── static/                 # CSS, JS, images
├── templates/              # Jinja2 HTML templates
└── tests/
    ├── test_*.py           # Unit & integration tests
    └── e2e/                # Playwright end-to-end tests
```



---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

<div align="center">
⭐ If you found this project useful, please give it a star!
</div>
