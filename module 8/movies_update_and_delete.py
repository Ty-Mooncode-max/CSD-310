"""
Tyler Moon
02/15/2025
Assignment 8.2
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

# Function to display films
def show_films(cursor, title):
    print(f"-- {title} --")
    query = """
    SELECT film_name AS Name, film_director AS Director, 
           genre_name AS Genre, studio_name AS Studio
    FROM film
    INNER JOIN genre ON film.genre_id = genre.genre_id
    INNER JOIN studio ON film.studio_id = studio.studio_id;
    """
    cursor.execute(query)
    films = cursor.fetchall()

    for film in films:
        print(f"Film Name: {film[0]}\nDirector: {film[1]}\nGenre: {film[2]}\nStudio: {film[3]}\n")

# Display initial films
show_films(cursor, "DISPLAYING FILMS")

# Check if 'The Matrix' already exists before inserting
check_query = "SELECT film_name FROM film WHERE film_name = 'The Matrix';"
cursor.execute(check_query)

# Consume any unread result from the previous query (to avoid internal error)
cursor.fetchall()

# Check if "The Matrix" is already present
existing_film = cursor.fetchone()

if not existing_film:
    # Insert a new film (Ensure genre_id, studio_id, and runtime exist)
    insert_query = """
    INSERT INTO film (film_name, film_director, genre_id, studio_id, film_releaseDate, film_runtime) 
    VALUES (%s, %s, 
           (SELECT genre_id FROM genre WHERE genre_name = 'SciFi'), 
           (SELECT studio_id FROM studio WHERE studio_name = '20th Century Fox'),
           %s, %s);
    """
    new_film = ("The Matrix", "Lana Wachowski, Lilly Wachowski", "1999-03-31", 136)  # Adding film_runtime
    try:
        cursor.execute(insert_query, new_film)
        db.commit()
        print("Film 'The Matrix' inserted.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
else:
    print("The film 'The Matrix' already exists.")

# Display after insert (if inserted)
show_films(cursor, "DISPLAYING FILMS AFTER INSERT")

# Update 'Alien' to Horror
update_query = """
UPDATE film SET genre_id = (SELECT genre_id FROM genre WHERE genre_name = 'Horror') 
WHERE film_name = 'Alien';
"""
cursor.execute(update_query)
db.commit()

# Display after update
show_films(cursor, "DISPLAYING FILMS AFTER UPDATE - Changed Alien to Horror")

# Delete 'Gladiator'
delete_query = "DELETE FROM film WHERE film_name = 'Gladiator';"
cursor.execute(delete_query)
db.commit()

# Display after delete
show_films(cursor, "DISPLAYING FILMS AFTER DELETE")

# Close cursor and connection
cursor.close()
db.close()
