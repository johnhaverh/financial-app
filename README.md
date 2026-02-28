# Financial App API

Modern RESTful API built with **FastAPI** for managing financial accounts, transactions, deposits, withdrawals, and transfers. Includes basic JWT authentication.

## Project Status (February 2026)
- **Phase 1: Modern Python Backend** 
  - Clean folder structure (`app/api`, `app/core`, `app/models`, `app/schemas`, `app/services`, etc.)
  - Data models using Python dataclasses
  - In-memory CRUD operations for accounts and transactions
  - Unit tests with pytest
  - FastAPI implementation with Pydantic validation
  - Basic JWT authentication (login endpoint + protected routes)
  - Professional API documentation (Swagger tags, descriptions, response models)

Next steps:  
- PostgreSQL integration, advanced SQL queries, Docker, logging, deployment

## Features
- Account creation with initial balance
- Deposit, withdraw, and transfer operations
- Transaction history tracking
- JWT-based authentication (Bearer token)
- Input validation and custom exceptions
- Interactive API documentation (Swagger UI & ReDoc)

## Installation

1. Clone the repository:
   
    ```bash
    git clone https://github.com/johnhaverh/financial-app.git
    cd financial-app

2. Create and activate a virtual environment:
    
    ```bash
    python -m venv .venv

    # Windows
    .venv\Scripts\activate

    # macOS / Linux
    source .venv/bin/activate

3. Install dependencies:

    ```bash
    pip install -r requirements.txt

## Runnign the API

1. Start the development server:
   
    ```bash
    uvicorn app.main:app --reload
    
    Once running, access:

        Swagger UI (interactive docs): http://127.0.0.1:8000/docs
        ReDoc (alternative docs): http://127.0.0.1:8000/redoc

## Authentication (JWT)

    Login Endpoint

        POST /token
        Form data:
            username: johndoe
            password: secret123

        Response example:
        
        ```JSON
        {
            "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
            "token_type": "bearer"
        }

    Use the token in headers for protected endpoints:
    
    ```text
    Authorization: Bearer <your_token_here>
    
    Test inactive user (should fail with 400):

        username: alice
        password: wonderland456

## Main Endpoints

<img src="https://github.com/johnhaverh/financial-app/blob/main/app/assets/endpoints.png" width="300" />


## Current Architecture

<img src="https://github.com/johnhaverh/financial-app/blob/main/app/assets/diagram.png" width="300" />

## Contributing
Feel free to open issues or pull requests. Suggestions for improvements (e.g., adding real database, Docker, tests coverage) are welcome!