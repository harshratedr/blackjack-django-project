# 🎲 Blackjack Django Project

A fully functional Blackjack game built with Django. Features include user authentication, a betting system, credit tracking, and a leaderboard.

---

## 🛠️ Setup Guide

Follow these steps to set up and run the project on your local machine.

### 1. Prerequisites
Ensure you have the following installed:
- Python 3.8 or higher
- pip (Python package manager)
- Git (optional, for cloning the repository)

### 2. Clone the Repository
If you have Git installed, clone the repository:
```bash
git clone https://github.com/harshratedr/blackjack-django-project.git
cd blackjack-django

If you don’t have Git, download the project as a ZIP file and extract it.
3. Set Up a Virtual Environment

Create a virtual environment to isolate dependencies:
bash
Copy

python -m venv venv

Activate the virtual environment:

    On Windows:
    bash
    Copy

    venv\Scripts\activate

    On macOS/Linux:
    bash
    Copy

    source venv/bin/activate

4. Install Dependencies

Install the required Python packages:
bash
Copy

pip install -r requirements.txt

5. Set Up the Database

Run migrations to set up the database:
bash
Copy

python manage.py migrate

6. Create a Superuser

Create an admin account to access the Django admin panel:
bash
Copy

python manage.py createsuperuser

Follow the prompts to set up your username, email, and password.
7. Run the Development Server

Start the Django development server:
bash
Copy

python manage.py runserver

Open your browser and go to:
Copy

http://127.0.0.1:8000/

8. Access the Admin Panel

To access the Django admin panel, go to:
Copy

http://127.0.0.1:8000/admin/

Log in with the superuser credentials you created earlier.
🚀 Features

    User Authentication: Register, log in, and log out.

    Betting System: Place bets and track your credits.

    Leaderboard: View the top players.

    User Stats: Track your wins, losses, and transaction history.

    Daily Login Bonus: Earn credits for logging in daily.

📂 Project Structure
Copy

blackjack_project/
├── blackjack/                      # Django app
│   ├── migrations/                 # Database migrations
│   ├── templates/                  # HTML templates
│   ├── __init__.py
│   ├── admin.py                    # Admin configuration
│   ├── apps.py                     # App configuration
│   ├── forms.py                    # Forms for registration and login
│   ├── models.py                   # Database models
│   ├── tests.py                    # Unit tests
│   ├── urls.py                     # App-specific URLs
│   ├── views.py                    # App logic and views
│   └── game_logic.py               # Game logic (OOP-based)
├── blackjack_project/              # Project settings folder
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py                 # Project settings
│   ├── urls.py                     # Main project URLs
│   └── wsgi.py
├── manage.py                       # Django management script
└── db.sqlite3                      # SQLite database

🛠️ Customization

    Change Starting Credits: Modify the credits field in the PlayerProfile model (models.py).

    Daily Bonus Amount: Update the bonus amount in the game view (views.py).

    UI Styling: Edit the Bootstrap classes in the templates (templates/blackjack/).

📝 License

This project is licensed under the MIT License. See the LICENSE file for details.
🙏 Credits

    Developed by Harsh Nagwanshi

    Inspired by classic Blackjack games.