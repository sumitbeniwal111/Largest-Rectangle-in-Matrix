from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from typing import Any
import time
from pydantic import validator
from sqlalchemy import create_engine, Column, Integer, Float, Text
from sqlalchemy.orm import sessionmaker, declarative_base
import json

"""
Database Setup
Creates a SQLite database file (logs.db) and
prepares a table that store request, response and execution time
"""

DATABASE_URL = "sqlite:///./logs.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

class APILog(Base):
    """
    Database table 
    Columns:
    - request_data: input matrix
    - response_data: output
    - execution_time_ms: time taken by API to compute
    """
    __tablename__ = "api_logs"

    id = Column(Integer, primary_key=True, index=True)
    request_data = Column(Text)
    response_data = Column(Text)
    execution_time_ms = Column(Float)

Base.metadata.create_all(bind=engine)


"""
FastAPI App Initialization
"""
app = FastAPI()

class MatrixInput(BaseModel):
    """
    Validates input matrix
    - matrix is not empty
    - rows are equal length
    - rows are not empty
    - all values are integers
    """
    matrix: List[List[Any]]

    @validator("matrix")
    def validate_matrix(cls, v):
        if len(v) == 0:
            raise ValueError("Matrix cannot be empty.")

        row_length = len(v[0])
        if row_length == 0:
            raise ValueError("Matrix rows cannot be empty.")
    
        for r, row in enumerate(v):
            if len(row) != row_length:
                raise ValueError(f"Row {r} has different length. Matrix must be rectangular.")

            for value in row:
                if not isinstance(value, int):
                    raise ValueError("Matrix must contain only integers.")
        return v



"""
largest_rectangle Function take input a 2D matrix
return Output (list of numbers with max area, maximum area)
Working:
- For each number in the matrix:
      Build histogram heights row by row
      Use stack method to find largest rectangle
- Keep track of max area found
- If multiple numbers have same area → return all
"""

def largest_rectangle(matrix: List[List[int]]) -> tuple:
    if not matrix:
        return ([], 0)

    n, m = len(matrix), len(matrix[0])

    unique_numbers = set()
    for row in matrix:
        unique_numbers.update(row)

    def largest_histogram_area(heights):
        """
        Input is list of heights
        Output largest rectangle area for that histogram
        """
        stack = []
        max_area = 0
        heights.append(0)

        for i, h in enumerate(heights):
            while stack and heights[stack[-1]] > h:
                height = heights[stack.pop()]
                width = i if not stack else (i - stack[-1] - 1)
                max_area = max(max_area, height * width)
            stack.append(i)

        heights.pop()
        return max_area

    max_area = 0
    best_numbers = []  # store all numbers with max area

    for num in unique_numbers:
        heights = [0] * m

        for i in range(n):
            for j in range(m):
                if matrix[i][j] == num:
                    heights[j] += 1
                else:
                    heights[j] = 0

            area = largest_histogram_area(heights)

            # If a new bigger area is found
            if area > max_area:
                max_area = area
                best_numbers = [num]

            # If an equal area is found
            elif area == max_area and area > 0:
                if num not in best_numbers:
                    best_numbers.append(num)

    return (best_numbers, max_area)


"""
API Endpoint: POST /largest-rectangle
Take input matrix in JSON format
return output numbers with largest rectangle and area
Working:
- Start timer
- Run largest_rectangle()
- Save request + response + time in DB
- Return result
"""
@app.get("/")
def home():
    return {"message": "API is running. Go to /docs for documentation."}

@app.post("/largest-rectangle")
def get_largest_rectangle(data: MatrixInput):
    start = time.perf_counter()

    number, area = largest_rectangle(data.matrix)

    result = {"number": number, "area": area}

    end = time.perf_counter()
    execution_time = (end - start) * 1000

    # Save log to DB
    db = SessionLocal()
    log_entry = APILog(
        request_data=json.dumps(data.dict()),
        response_data=json.dumps(result),
        execution_time_ms=execution_time
    )
    db.add(log_entry)
    db.commit()
    db.close()

    return result

