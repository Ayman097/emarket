# Ecommerce API with Django Framework

This repository contains the source code for an Ecommerce API built using the Django Framework in Python. The API is designed to handle various aspects of an online store, including accounts, orders, products, and utilities. The project structure is organized into separate modules for clarity and maintainability.

## Project Structure

- **account**: Module for handling user accounts and authentication.
- **emarket**: Main module for the Ecommerce API, includes core functionality.
- **order**: Module for managing and processing orders.
- **product**: Module for handling products and their details.
- **utils**: Utility module containing helper functions and common functionalities.
- **db.sqlite3**: SQLite database file containing sample data for testing.
- **manage.py**: Django management script for various project tasks.

## Getting Started

1. Clone the repository to your local machine:

   ```bash
   git clone https://github.com/your-username/ecommerce-api.git
   ```

2. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Apply the database migrations:

   ```bash
   python manage.py migrate
   ```

4. Run the development server:

   ```bash
   python manage.py runserver
   ```

   The API will be accessible at http://localhost:8000/.

## Contributing

If you'd like to contribute to the project, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix: `git checkout -b feature-name`.
3. Make your changes and commit them: `git commit -m 'Add new feature'`.
4. Push the changes to your fork: `git push origin feature-name`.
5. Create a pull request on the main repository.

Please make sure to follow the existing coding style and add appropriate tests for your changes.

