# Summary: Flask Application Entrypoint
# Description:
# This file initializes the Flask application using create_app()
# and runs it in development mode when executed directly.

from app import create_app   

app = create_app()

# Run development server (not used in production; Gunicorn handles that)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
