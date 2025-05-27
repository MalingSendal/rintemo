#main.py

from app import create_app

app = create_app()  # This uses the app factory defined in app/__init__.py

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
