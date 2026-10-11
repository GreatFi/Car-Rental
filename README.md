# Car Rental System

A Django car rental website with guest, registered user, and admin features.

## Setup

You need **Python** and **Git** installed.

**1. Clone the project**

```bash
git clone <repo-url>
cd <repo-folder>
```

Go into the folder that contains `manage.py`.

**2. Switch to your own branch**

```bash
git checkout <your-branch-name>
```

**3. Create a virtual environment**

```bash
python -m venv venv
```

**4. Activate it**

Windows:
```bash
venv\Scripts\activate
```

Mac/Linux:
```bash
source venv/bin/activate
```

You should see `(venv)` at the start of the terminal line.

**5. Install the packages**

```bash
pip install -r requirements.txt
```

**6. (Optional) Create your `.env` file**

Add your django secret key to it.

**7. Set up the database**

```bash
python manage.py migrate
```

**8. Create an admin account**

```bash
python manage.py createsuperuser
```

**9. Run the project**

```bash
python manage.py runserver
```

Open http://127.0.0.1:8000/ in your browser.
