"""
Tyler Moon
02/14/2025
Assignment 7.2
"""
import mysql.connector
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Database connection
db = mysql.connector.connect(
    host=os.getenv("HOST"),
    user=os.getenv("USER"),
    password=os.getenv("PASSWORD"),
    database=os.getenv("DATABASE")
)

cursor = db.cursor()

# Query 1: Display studio records
print("\n-- DISPLAYING Studio RECORDS --")
cursor.execute("SELECT studio_id, studio_name FROM studio")
studios = cursor.fetchall()
for studio_id, studio_name in studios:
    print(f"Studio ID: {studio_id}")
    print(f"Studio Name: {studio_name}\n")

# Query 2: Display genre records
print("-- DISPLAYING Genre RECORDS --")
cursor.execute("SELECT genre_id, genre_name FROM genre")
genres = cursor.fetchall()
for genre_id, genre_name in genres:
    print(f"Genre ID: {genre_id}")
    print(f"Genre Name: {genre_name}\n")

# Query 3: Display short film records (runtime < 120 minutes)
print("-- DISPLAYING Short Film RECORDS --")
cursor.execute("SELECT film_name, film_runtime FROM film WHERE film_runtime < 120")
short_movies = cursor.fetchall()
for film_name, film_runtime in short_movies:
    print(f"Film Name: {film_name}")
    print(f"Runtime: {film_runtime}\n")

# Query 4: Display films sorted by director
print("-- DISPLAYING Director RECORDS in Order --")
cursor.execute("SELECT film_name, film_director FROM film ORDER BY film_director")
films_by_director = cursor.fetchall()
for film_name, film_director in films_by_director:
    print(f"Film Name: {film_name}")
    print(f"Director: {film_director}\n")

# Close the connection
cursor.close()
db.close()
