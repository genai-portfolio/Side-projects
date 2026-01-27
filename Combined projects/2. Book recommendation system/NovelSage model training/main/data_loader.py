import pandas as pd
from pathlib import Path
from config import Config

class DataLoader:

    
    @staticmethod
    def load_books():
        """Load and preprocess books data"""
        try:
            books = pd.read_csv(
                Config.DATA_DIR / Config.BOOKS_FILE, 
                sep=';', 
                on_bad_lines='skip', 
                encoding='latin-1'
            )
            
            # Select and rename columns
            books = books[['ISBN', 'Book-Title', 'Book-Author', 'Year-Of-Publication', 'Publisher', 'Image-URL-L']]
            books.rename(columns={
                'Book-Title': 'title',
                'Book-Author': 'author',
                'Year-Of-Publication': 'year',
                'Publisher': 'publisher',
                'Image-URL-L': 'img_url'
            }, inplace=True)
            
            print(f"Books data loaded successfully. Shape: {books.shape}")
            return books
        
        except Exception as e:
            print(f"Error loading books data: {e}")
            return None
    
    @staticmethod
    def load_users():
        """Load and preprocess users data"""
        try:
            users = pd.read_csv(
                Config.DATA_DIR / Config.USERS_FILE, 
                sep=';', 
                on_bad_lines='skip', 
                encoding='latin-1'
            )
            
            users.rename(columns={
                'User-ID': 'user_id',
                'Location': 'location',
                'Age': 'age'
            }, inplace=True)
            
            print(f"Users data loaded successfully. Shape: {users.shape}")
            return users
        
        except Exception as e:
            print(f"Error loading users data: {e}")
            return None
    
    @staticmethod
    def load_ratings():
        """Load and preprocess ratings data"""
        try:
            ratings = pd.read_csv(
                Config.DATA_DIR / Config.RATINGS_FILE, 
                sep=';', 
                on_bad_lines='skip', 
                encoding='latin-1'
            )
            
            ratings.rename(columns={
                'User-ID': 'user_id',
                'Book-Rating': 'rating'
            }, inplace=True)
            
            print(f"Ratings data loaded successfully. Shape: {ratings.shape}")
            return ratings
        
        except Exception as e:
            print(f"Error loading ratings data: {e}")
            return None