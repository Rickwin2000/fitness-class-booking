# 🧘 Fitness Booking API

A simple Django REST API for managing and booking fitness classes.

---

## 🔧 Requirements

- Python 3.11+

---

## ⚙️ Setup & Run

```bash
# 1. Create and activate a virtual environment
python3.11 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Make and apply migrations
python manage.py makemigrations
python manage.py migrate

# 4. Seed sample data (make sure you have a custom command named 'seed_fitness_classes')
python manage.py seed_fitness_classes

# 5. Run the development server
python manage.py runserver

# 6. Run the test suite
pytest
