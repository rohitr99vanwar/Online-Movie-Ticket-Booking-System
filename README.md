# 🎬 Movie Ticket Booking System

A full-stack web application for booking movie tickets with seat selection, show timings, and PDF ticket generation.

---

## 🚀 Features

* User Registration & Login
* Dynamic Movie Selection
* Seat Booking System
* Show Timing Selection
* Booking History
* PDF Ticket Generation
* Admin can Add Movies
* Seat Availability (Booked/Available)

---

## 🛠️ Tech Stack

* Frontend: HTML, CSS, JavaScript
* Backend: Python (Flask)
* Database: SQLite
* PDF: ReportLab

---

## 📂 Project Structure

```
ticket_booking/
│
├── app.py
├── requirements.txt
├── movies.db (auto-created)
├── ticket.pdf (generated)
│
├── templates/
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── history.html
│
├── static/
│   ├── style.css
│   ├── script.js
```

---

## ⚙️ Installation

### 1. Clone Repository

```
git clone https://github.com/YOUR_USERNAME/movie-ticket-booking.git
cd movie-ticket-booking
```

### 2. Create Virtual Environment

```
python -m venv venv
venv\Scripts\activate   (Windows)
```

### 3. Install Requirements

```
pip install -r requirements.txt
```

### 4. Run Project

```
python app.py
```

---

## 🌐 Open in Browser

```
http://127.0.0.1:5000
```

---

## 🔐 Default Flow

1. Register User
2. Login
3. Select Movie & Timing
4. Choose Seat
5. Book Ticket
6. Download PDF Ticket

---

## 💡 Notes

* Database auto-created on first run
* Delete `movies.db` if facing issues
* Admin can add new movies

---

## 📌 Author

👨‍💻 Rohit Revanwar

---

## ⭐ Future Improvements

* Online Payment Integration
* QR Code in Ticket
* Movie Posters UI
* Deployment on Cloud

---
