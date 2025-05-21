# Group Backend Flask Project

## Overview

Group Backend is a RESTful API service built with Flask. It is designed to handle user authentication, role-based access control, and profile management for group applications. The project emphasizes modularity and scalability, making it easy to extend and maintain as your application grows.

## Features

- **User Authentication & Authorization:** Secure login system and role-based access features.
- **Profile Management:** Handles user details such as gender, age, location, and more.
- **Database Migrations:** Utilizes Alembic to manage schema changes seamlessly.
- **RESTful API Endpoints:** Provides endpoints that can easily integrate with a frontend or mobile app.
- **Configuration & Environment Variables:** Supports configurable settings for multiple environments.

## Technology Stack

- **Backend Framework:** [Flask](https://flask.palletsprojects.com/)
- **Database & ORM:** SQLAlchemy with Alembic for migrations
- **Python:** Version 3.8 or higher  
- **Other Dependencies:** See `requirements.txt` for a full list

## Setup & Installation

### Prerequisites

- Python 3.8+ installed locally
- pip (Python’s package manager)
- (Optional) Virtual Environment for dependency isolation

### Installation Steps

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/yourusername/group_backend.git
   cd group_backend
