from fastapi import FastAPI
import mysql.connector
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()

# Allow requests from frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv('DB_HOST', 'mysql'),
        user=os.getenv('DB_USER', 'root'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME', 'counter_db')
    )

@app.get("/increment")
def increment_counter():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE counter SET count = count + 1 WHERE id = 1;")
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Counter incremented"}

@app.get("/get")
def get_counter():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT count FROM counter WHERE id = 1;")
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return {"count": result[0]}
