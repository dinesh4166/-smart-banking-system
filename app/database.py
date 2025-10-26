import os
import pymysql
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "3306"))
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "prac")

def get_connection():
    return pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME, cursorclass=pymysql.cursors.DictCursor, autocommit=True)

def init_db():
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(f"""CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(100) NOT NULL UNIQUE,
                password VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            ) ENGINE=InnoDB;""")
            cur.execute(f"""CREATE TABLE IF NOT EXISTS kyc_documents (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                document_type VARCHAR(50),
                document_number VARCHAR(100),
                status ENUM('PENDING','VERIFIED') DEFAULT 'PENDING',
                uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            ) ENGINE=InnoDB;""")
    finally:
        conn.close()
