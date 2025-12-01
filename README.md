# Largest Rectangle in Matrix – FastAPI Service

**Quick Links:**  
- 🔗 [Features](#features)  
- 🔗 [My Approach](#my-approach)  
- 🔗 [API Endpoint](#api-endpoint)  
- 🔗 [How the Algorithm Works](#how-the-algorithm-works)  
- 🔗 [How to Run the Project](#how-to-run-the-project)  
- 🔗 [Database Logging](#database-logging)  
- 🔗 [Project Structure](#project-structure)  
- 🔗 [Sample Matrices](#sample-matrices)  
- 🔗 [Technologies Used](#technologies-used)  
- 🔗 [Author](#author)  

---

This project is a FastAPI-based service that finds the largest rectangle made from the same number inside a 2D matrix.  
Along with this, the API also stores every request, response, and execution time in a SQLite database.

---

## Features

- Finds the largest rectangle for each unique number.
- If multiple numbers have the same max area, all of them are returned.
- Works efficiently even for 100×100 matrices.
- Validates the input to make sure the matrix is rectangular and contains only integers.
- Logs all API calls into a SQLite database.

---

## My Approach

I broke the problem down into small parts so it becomes easier to handle.

1. First, I understood that a rectangle can only be formed when the same number is repeated in a block.

2. Instead of brute force, I used the “largest rectangle in histogram” technique.  
   I applied this method for every unique number in the matrix to find its maximum rectangle area.

3. If multiple numbers had the same area, I kept all of them.

4. Before running the algorithm, I added proper validation:
   - Matrix must not be empty  
   - All rows must be of the same length  
   - Rows must not be empty  
   - Every value must be an integer  

5. I built a FastAPI POST endpoint that accepts the matrix and returns the result.

6. I measured how long the computation takes using `time.perf_counter()`.

7. Every request and response is saved into `logs.db` using SQLAlchemy.  
   This helps in checking how the API behaves over time.

---

## API Endpoint

### POST `/largest-rectangle`

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

## How the Algorithm Works

1. For each unique number, I create a histogram for each row.
2. Using the stack-based histogram logic, I find the largest rectangle for that number.
3. I compare the results for all numbers.
4. All numbers that share the maximum area are returned.

Time complexity is:

```
O(U × R × C)
```

where U = unique numbers, R = rows, C = columns.

---

## How to Run the Project

### 1. Install dependencies

```
pip install -r requirements.txt
```

### 2. Start the FastAPI server

```
uvicorn main:app --reload
```

### 3. Open Swagger UI

```
http://127.0.0.1:8000/docs
```

You can test the API here.

---

## Database Logging

A file named `logs.db` is created automatically.

To see logs using VS Code, install:

* SQLTools
* SQLTools SQLite Driver

Then open the database and view entries.

Each log contains:

* request data
* response data
* execution time (ms)

---

## Project Structure

```
fastapi-largest-rectangle/
│── main.py
│── requirements.txt
│── README.md
│── logs.db   (auto-created)
```

---

## Sample Matrices

### Single Winner

```
[[1,1,1],
 [1,1,1]]
```

→ `{ "numbers": [1], "area": 6 }`

### Multiple Winners

```
[[1,1,2,2],
 [1,1,2,2]]
```

→ `{ "numbers": [1,2], "area": 4 }`

### Single Element

```
[[5]]
```

→ `{ "numbers": [5], "area": 1 }`

### Invalid Matrix

```
[[1,2], [3]]
```

→ Error: Matrix must be rectangular

---

## Technologies Used

* FastAPI
* Pydantic
* SQLAlchemy
* SQLite
* Uvicorn
* Python 3.8+

---

## Author

Sumit  
Backend Developer
