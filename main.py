from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from typing import Any
import time
from pydantic import validator
from sqlalchemy import create_engine, Column, Integer, Float, Text
from sqlalchemy.orm import sessionmaker, declarative_base
import json

# Database Setup

DATABASE_URL = "sqlite:///./logs.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

class APILog(Base):
    __tablename__ = "api_logs"

    id = Column(Integer, primary_key=True, index=True)
    request_data = Column(Text)
    response_data = Column(Text)
    execution_time_ms = Column(Float)

Base.metadata.create_all(bind=engine)

# FastAPI App

app = FastAPI()

class MatrixInput(BaseModel):
    matrix: List[List[Any]]

    @validator("matrix")
    def check_integers(cls, v):
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



# Largest Rectangle Function

def largest_rectangle(matrix: List[List[int]]) -> tuple:
    if not matrix:
        return ([], 0)

    n, m = len(matrix), len(matrix[0])

    unique_numbers = set()
    for row in matrix:
        unique_numbers.update(row)

    def largest_histogram_area(heights):
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


# API Endpoint

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
