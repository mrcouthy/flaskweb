# Flask Enterprise Web Application

A Flask-based web application featuring user authentication, authorization, blueprints, and a side navigation menu.

## Getting Started

### Prerequisites

- Python 3.x

### Setup

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd <repository_directory>
    ```

2.  **Create a virtual environment:**
    ```bash
    python -m venv venv
    ```
    Activate the virtual environment:
    -   On macOS and Linux:
        ```bash
        source venv/bin/activate
        ```
    -   On Windows:
        ```bash
        venv\\Scripts\\activate
        ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Running the Application

1.  **Run the Flask development server:**
    ```bash
    python app.py
    ```
    The application will be accessible at `http://127.0.0.1:5000/`.

2.  **Default Admin User:**
    On the first run, a default admin user is created with the following credentials:
    -   **Username:** `admin`
    -   **Password:** `admin`

    It is highly recommended to change these credentials after your first login.

## Running Tests

To run the automated tests for the application:

1.  Ensure all development dependencies (including test libraries like `pytest`) are installed from `requirements.txt`.
2.  Navigate to the root directory of the project.
3.  Run the tests using pytest:
    ```bash
    pytest
    ```
    Or, to be more specific:
    ```bash
    pytest tests/
    ```

This will discover and run all tests located in the `tests` directory.
