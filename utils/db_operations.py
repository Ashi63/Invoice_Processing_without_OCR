import streamlit as st
import sqlite3

# Function to create a user table if it doesn't exist
def create_user_table():
    conn = sqlite3.connect('user_db.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            company_name TEXT NOT NULL,
            email TEXT NOT NULL,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Function to insert a new user
def insert_user(first_name, last_name, company_name, email, username, password):
    conn = sqlite3.connect('user_db.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO users (first_name, last_name, company_name, email, username, password)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (first_name, last_name, company_name, email, username, password))
    conn.commit()
    conn.close()

# Function to check if a user exists in the database
def check_user(username, password):
    conn = sqlite3.connect('user_db.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
    user = cursor.fetchone()
    conn.close()
    return user