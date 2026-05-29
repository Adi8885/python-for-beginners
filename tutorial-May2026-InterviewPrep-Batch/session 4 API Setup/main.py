import os
import sqlite3
from fastapi import FastAPI, HTTPException, Query

app = FastAPI(
    title="IMDB Movie Ratings API",
    description="API to query ratings and voter turnout from the SQL IMDB Database.",
    version="1.0.0"
)

# Resolve path to the database dynamically (one level up from this directory)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "..", "imdb dataset", "Db-IMDB-SQL-Dataset.db")

def get_db_connection():
    """Helper function to get a connection and return rows as dictionaries."""
    if not os.path.exists(DB_PATH):
        raise HTTPException(
            status_code=500, 
            detail=f"Database file not found at: {DB_PATH}. Please verify the path."
        )
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Enables column access by name
    return conn

@app.get("/movies", tags=["Movies"])
def list_movies(
    min_rating: float = Query(0.0, ge=0.0, le=10.0, description="Minimum IMDB rating filter"),
    limit: int = Query(10, ge=1, le=100, description="Number of results to retrieve")
):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = """
        SELECT MID, title, year, rating, num_votes 
        FROM Movie 
        WHERE rating >= ? 
        LIMIT ?
    """
    cursor.execute(query, (min_rating, limit))
    rows = cursor.fetchall()
    conn.close()
    
    return [dict(row) for row in rows]

@app.get("/movies/{movie_id}", tags=["Movies"])
def get_movie_detail(movie_id: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = "SELECT MID, title, year, rating, num_votes FROM Movie WHERE MID = ?"
    cursor.execute(query, (movie_id,))
    row = cursor.fetchone()
    conn.close()
    
    if row is None:
        raise HTTPException(status_code=404, detail=f"Movie with ID '{movie_id}' not found")
        
    return dict(row)

@app.get("/movies/popular", tags=["Analytics"])
def get_most_popular_movies(limit: int = Query(5, ge=1, le=50)):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = """
        SELECT title, rating, num_votes 
        FROM Movie 
        ORDER BY num_votes DESC 
        LIMIT ?
    """
    cursor.execute(query, (limit,))
    rows = cursor.fetchall()
    conn.close()
    
    return [dict(row) for row in rows]

@app.get("/genres/{genre_name}/movies", tags=["Genres"])
def get_movies_by_genre(genre_name: str, limit: int = Query(5, ge=1, le=50)):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = """
        SELECT m.title, m.year, m.rating, g.Name AS genre
        FROM Movie m
        JOIN M_Genre mg ON m.MID = mg.MID
        JOIN Genre g ON mg.GID = g.GID
        WHERE g.Name LIKE ?
        ORDER BY m.rating DESC
        LIMIT ?
    """
    cursor.execute(query, (f"%{genre_name}%", limit))
    rows = cursor.fetchall()
    conn.close()
    
    if not rows:
        raise HTTPException(
            status_code=404, 
            detail=f"No movies found matching genre '{genre_name}'"
        )
        
    return [dict(row) for row in rows]
