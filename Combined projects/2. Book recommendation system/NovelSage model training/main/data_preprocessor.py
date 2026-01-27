import pandas as pd
from config import Config

class DataPreprocessor:
    
    def __init__(self, books, users, ratings):
        self.books = books
        self.users = users
        self.ratings = ratings
        self.ratings_with_books = None
        self.final_rating = None
        self.books_content = None
    
    def filter_active_users(self):
        """Filter users with more than MIN_USER_RATINGS ratings"""
        user_ratings_count = self.ratings['user_id'].value_counts()
        active_users = user_ratings_count[user_ratings_count > Config.MIN_USER_RATINGS].index
        self.ratings = self.ratings[self.ratings['user_id'].isin(active_users)]
        print(f"Filtered to {len(active_users)} active users")
        return self
    
    def merge_ratings_with_books(self):
        """Merge ratings with books data"""
        self.ratings_with_books = self.ratings.merge(self.books, on="ISBN")
        print(f"Merged data shape: {self.ratings_with_books.shape}")
        return self
    
    def filter_popular_books(self):
        """Filter books with at least MIN_BOOK_RATINGS ratings"""
        book_ratings_count = self.ratings_with_books.groupby('title')['rating'].count().reset_index()
        book_ratings_count.rename(columns={'rating': 'num_ratings'}, inplace=True)
        
        self.final_rating = self.ratings_with_books.merge(book_ratings_count, on='title')
        self.final_rating = self.final_rating[self.final_rating['num_ratings'] >= Config.MIN_BOOK_RATINGS]
        self.final_rating.drop_duplicates(['user_id', 'title'], inplace=True)
        
        print(f"Final rating data shape: {self.final_rating.shape}")
        return self
    
    def prepare_content_features(self):
        """Prepare content-based features"""
        self.books_content = self.books.drop_duplicates('title')
        self.books_content = self.books_content[self.books_content['title'].isin(self.final_rating['title'])]
        
        self.books_content['content_features'] = (
            self.books_content['title'] + ' ' + 
            self.books_content['author'] + ' ' + 
            self.books_content['publisher'].fillna('') + ' ' +
            self.books_content['year'].astype(str)
        )
        
        print(f"Books content shape: {self.books_content.shape}")
        return self
    
    def get_processed_data(self):
        """Return all processed data"""
        return {
            'books': self.books,
            'users': self.users,
            'ratings': self.ratings,
            'final_rating': self.final_rating,
            'books_content': self.books_content
        }