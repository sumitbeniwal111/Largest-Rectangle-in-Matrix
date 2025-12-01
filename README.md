# Largest Rectangle in Matrix – FastAPI Service

This project implements a **FastAPI-based service** that finds the **largest rectangle formed by identical integers** inside a 2D matrix.  
It also logs every API request, response, and execution time into a **SQLite database** for analytics.

- [Largest Rectangle in Matrix – FastAPI Service](#largest-rectangle-in-matrix--fastapi-service)
  - [Features](#features)
    - [Core Functionalities](#core-functionalities)
    - [Input Validation](#input-validation)
    - [Logging (SQLite)](#logging-sqlite)
    - [Developer Friendly](#developer-friendly)
  - [API Endpoint](#api-endpoint)
    - [**POST** `/largest-rectangle`](#post-largest-rectangle)
    - [Request Body](#request-body)
    - [Successful Response](#successful-response)
    - [Example Error Response](#example-error-response)
  - [Algorithm Overview](#algorithm-overview)
  - [How to Run the Project](#how-to-run-the-project)
    - [1️⃣ Install dependencies](#1️⃣-install-dependencies)
    - [2️⃣ Start the FastAPI server](#2️⃣-start-the-fastapi-server)
    - [3️⃣ Open Swagger UI](#3️⃣-open-swagger-ui)
  - [Database Logging](#database-logging)
  - [Project Structure](#project-structure)
  - [Sample Test Matrices](#sample-test-matrices)
    - [🔹 Single Winner](#-single-winner)
    - [🔹 Multiple Winners](#-multiple-winners)
    - [🔹 Single Element](#-single-element)
    - [🔹 Non-Rectangular (Invalid)](#-non-rectangular-invalid)
  - [Technologies Used](#technologies-used)
  - [Author](#author)

## Features

### Core Functionalities

- Computes the **largest rectangle area** for each unique number in the matrix.
- If multiple numbers produce the **same maximum area**, _all_ such numbers are returned.
- Efficient algorithm using **histogram-based rectangle detection**.
- Handles matrices up to **100 × 100**.

### Input Validation

- Accepts only **integer-only matrices**.
- Ensures matrix is **non-empty**.
- Ensures matrix rows are **all equal length** (rectangular).
- Rejects invalid values with detailed error messages.

### Logging (SQLite)

Every API call logs:

- Request body
- Response JSON
- Execution time (ms)
- Stored in `logs.db` (auto-created)

### Developer Friendly

- Auto-generated Swagger UI
- Clean project structure

---

## API Endpoint

### **POST** `/largest-rectangle`

### Request Body

```json
{
  "matrix": [
    [1, 1, 2, 2],
    [1, 1, 2, 2]
  ]
}
```

### Successful Response

```json
{
  "numbers": [1, 2],
  "area": 4
}
```

### Example Error Response

Invalid non-integer value:

```json
{
  "detail": [
    {
      "loc": ["body", "matrix"],
      "msg": "Invalid value at row 1, column 2: Matrix must contain only integers.",
      "type": "value_error"
    }
  ]
}
```

---

## Algorithm Overview

For each unique number in the matrix:

1. Convert matrix to a **binary grid** (1 if cell matches number, else 0)
2. Build **histogram heights row-by-row**
3. Apply **largest rectangle in histogram** algorithm
4. Track:

   - max area
   - list of numbers producing max area

Time Complexity:

```
O(U × R × C)    (U = unique numbers, R = rows, C = columns)
```

Works comfortably for 100×100 grids.

---

## How to Run the Project

### 1️⃣ Install dependencies

```
pip install -r requirements.txt
```

### 2️⃣ Start the FastAPI server

```
uvicorn main:app --reload
```

### 3️⃣ Open Swagger UI

```
http://127.0.0.1:8000/docs
```

You can test the API directly in your browser.

---

## Database Logging

A SQLite database named **`logs.db`** is created automatically.

To view logs:

```bash
sqlite3 logs.db
```

Inside SQLite:

```sql
SELECT * FROM api_logs;
```

Each entry contains:

- `request_data`
- `response_data`
- `execution_time_ms`

---

## Project Structure

```
fastapi-largest-rectangle/
│── main.py
│── requirements.txt
│── README.md
│── logs.db               (auto-created)
```

---

## Sample Test Matrices

### 🔹 Single Winner

```
[[1,1,1],
 [1,1,1]]
```

→ `{ "numbers": [1], "area": 6 }`

### 🔹 Multiple Winners

```
[[1,1,2,2],
 [1,1,2,2]]
```

→ `{ "numbers": [1,2], "area": 4 }`

### 🔹 Single Element

```
[[5]]
```

→ `{ "numbers": [5], "area": 1 }`

### 🔹 Non-Rectangular (Invalid)

```
[[1,2], [3]]
```

→ Error: _Matrix must be rectangular_

---

## Technologies Used

- **FastAPI** (API framework)
- **Pydantic** (data validation)
- **SQLite** (logging DB)
- **SQLAlchemy** (ORM)
- **Uvicorn** (ASGI server)
- **Python 3.8+**

---

## Author

Sumit
FastAPI Backend Developer