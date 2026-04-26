from data_loader import DataLoader
from data_preprocessor import DataPreprocessor
from collaborative_model import CollaborativeFilteringModel
from content_model import ContentBasedModel
from hybrid_model import HybridRecommendationModel
from model_manager import ModelManager
from config import Config

class RecommendationEngine:
    
    def __init__(self):
        self.cf_model = None
        self.cb_model = None
        self.hybrid_model = None
        self.processed_data = None
        self.model_manager = ModelManager()
        self.is_trained = False
    
    def train_models(self):
        """Train all recommendation models"""
        print("="*60)
        print("Starting model training...")
        print("="*60)
        
        # Load data
        print("\n1. Loading data...")
        books = DataLoader.load_books()
        users = DataLoader.load_users()
        ratings = DataLoader.load_ratings()
        
        if any(data is None for data in [books, users, ratings]):
            print("Failed to load data")
            return False
        
        # Preprocess data
        print("\n2. Preprocessing data...")
        preprocessor = DataPreprocessor(books, users, ratings)
        preprocessor.filter_active_users()
        preprocessor.merge_ratings_with_books()
        preprocessor.filter_popular_books()
        preprocessor.prepare_content_features()
        
        self.processed_data = preprocessor.get_processed_data()
        
        # Train collaborative filtering model
        print("\n3. Training collaborative filtering model...")
        self.cf_model = CollaborativeFilteringModel()
        self.cf_model.train(self.processed_data['final_rating'])
        
        # Train content-based model
        print("\n4. Training content-based model...")
        self.cb_model = ContentBasedModel()
        self.cb_model.train(self.processed_data['books_content'])
        
        # Create hybrid model
        print("\n5. Creating hybrid model...")
        self.hybrid_model = HybridRecommendationModel(self.cf_model, self.cb_model)
        
        # Save models
        print("\n6. Saving models...")
        if self.model_manager.save_models(self.cf_model, self.cb_model, self.processed_data):
            self.is_trained = True
            print("\n" + "="*60)
            print("Model training completed successfully!")
            print("="*60)
            return True
        else:
            print("Failed to save models")
            return False
    
    def load_trained_models(self):
        """Load pre-trained models"""
        print("Checking for existing trained models...")
        
        if not self.model_manager.models_exist():
            print("No trained models found")
            return False
        
        loaded_data = self.model_manager.load_models()
        
        if loaded_data:
            self.cf_model = loaded_data['cf_model']
            self.cb_model = loaded_data['cb_model']
            self.hybrid_model = loaded_data['hybrid_model']
            self.processed_data = {
                'books_content': loaded_data['books_content'],
                'final_rating': loaded_data['final_rating'],
                'books': loaded_data['books']
            }
            self.is_trained = True
            print("Models loaded successfully!")
            return True
        
        print("Failed to load models")
        return False
    
    def get_recommendations(self, book_title, method='hybrid', top_n=Config.DEFAULT_TOP_N):
        """Get recommendations using specified method"""
        if not self.is_trained:
            print("Models not trained or loaded. Please train or load models first.")
            return []
        
        if method == 'collaborative':
            return self.cf_model.get_recommendations(
                book_title, 
                self.processed_data['books_content'],
                self.processed_data['books'],
                top_n
            )
        elif method == 'content':
            return self.cb_model.get_recommendations(
                book_title,
                self.processed_data['books_content'],
                top_n
            )
        elif method == 'hybrid':
            return self.hybrid_model.get_recommendations(
                book_title,
                self.processed_data['books_content'],
                self.processed_data['books'],
                top_n=top_n
            )
        else:
            print("Invalid method. Use 'collaborative', 'content', or 'hybrid'")
            return []
    
    def get_available_books(self, limit=None):
        """Get list of all available books for recommendations"""
        if not self.is_trained:
            print("Models not trained or loaded")
            return []
        
        books = self.processed_data['books_content']['title'].unique().tolist()
        if limit:
            return books[:limit]
        return books
    
    def search_books(self, query, limit=10):
        """Search for books by title"""
        if not self.is_trained:
            print("Models not trained or loaded")
            return []
        
        books = self.processed_data['books_content']
        matching_books = books[books['title'].str.contains(query, case=False, na=False)]
        
        results = []
        for _, book in matching_books.head(limit).iterrows():
            results.append({
                'title': book['title'],
                'author': book['author'],
                'year': book['year'],
                'publisher': book['publisher']
            })
        
        return results
    
    def get_book_info(self, book_title):
        """Get detailed information about a specific book"""
        if not self.is_trained:
            return None
        
        book_info = self.processed_data['books_content'][
            self.processed_data['books_content']['title'] == book_title
        ]
        
        if book_info.empty:
            return None
        
        book = book_info.iloc[0]
        return {
            'title': book['title'],
            'author': book['author'],
            'year': book['year'],
            'publisher': book['publisher'],
            'image_url': book['img_url'] if isinstance(book['img_url'], str) and book['img_url'].startswith('http') else Config.DEFAULT_IMAGE_URL
        }