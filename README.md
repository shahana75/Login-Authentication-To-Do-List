# SHAZAM 

A simple full-stack **Login + To-Do Web App** built using Flask.

##  About

This project allows users to create an account, log in securely, and manage their personal tasks. Each user gets their own dashboard with a working to-do list.

---

##  Features

* User login & auto signup
* Password hashing (secure storage)
* Session-based authentication
* Add tasks
* Mark tasks as complete
* Delete tasks

---

##  Tech Used

* Python (Flask)
* HTML, CSS
* JavaScript
* JSON (for storing users)

---

##  How to Run

```bash
git clone https://github.com/your-username/shazam.git
cd shazam
pip install flask
python app.py
```

Open: http://127.0.0.1:5000

---

##  Project Files

* `app.py` → Backend (Flask app)
* `login.html` → Login page
* `user_page.html` → Dashboard
* `notes.js` → To-do logic
* `users.json` → User data

---

##  Notes

* New users are created automatically on first login
* Passwords are stored in hashed format
* Data is not persistent for tasks (only users are saved)

---

##  Future Updates

* Save tasks per user
* Add database
* Improve UI
* Deploy online

---

##  Author

Shahana
