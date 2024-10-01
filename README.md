# Microservices: a Password Management System

This project implements a secure, scalable password management system using a microservices architecture. It provides users with a centralized platform to store, manage, and access their passwords while ensuring robust authentication and authorization mechanisms.

## Requirements

- Docker and Docker Compose for containerization and local development
- Python 3.12 or later
- Flask web framework
- Flask-SQLAlchemy for ORM
- Werkzeug for utilities (including password hashing)
- SQLite for local development (easily adaptable to PostgreSQL for production)

## > Authentication Service
Responsible for user registration, login, and token-based authentication.
## > Password Management Service
Handles CRUD operations for password entries, ensuring only authorized users can access specific passwords.


## Getting Started

### 1. Clone the Repository
```bash
git clone <repository-url>
cd <repository-name>
```
### 2. Database Setup:
The application uses SQLite for development. You can initialize the database by running:
```bash
python3 create_db.py
```
#### Switching to PostgreSQL:
To switch to PostgreSQL, modify the docker-compose.yml file to uncomment and configure the database services.

### 3. Build and Run the Services
To build and run the microservices using Docker Compose, execute the following command:
```bash
docker-compose up --build
```
This command will build the Docker images and start the services defined in the docker-compose.yml file.

### 4. Access the Services
- Authentication Service: http://localhost:5001

- Password Service: http://localhost:5002


## Contributing
This project provides a solid foundation for a secure, scalable password management system. It can be extended and enhanced to meet specific organizational needs or to add more advanced features in the future.

Feel free to submit pull requests or create issues for enhancements and bug fixes. 🪲

## Acknowledgments
Docker Documentation: [Docker](https://docs.docker.com)

Flask Documentation: [Flask](https://flask.palletsprojects.com/en/3.0.x/installation/)

SQLAlchemy Documentation: [SQLAlchemy](https://docs.sqlalchemy.org/en/20/)


# Enjoy this little project <3
