import pickle
from pathlib import Path
from config import Config
from collaborative_model import CollaborativeFilteringModel
from content_model import ContentBasedModel
from hybrid_model import HybridRecommendationModel

class ModelManager:
    """Manage model saving and loading operations"""
    
    def __init__(self):
        Config.MODELS_DIR.mkdir(exist_ok=True)
    
    def save_models(self, cf_model, cb_model, processed_data):
        """Save all models and processed data"""
        try:
            print("Saving models and processed data...")
            
            model_files = {
                'cf_model.pkl': cf_model,
                'cb_model.pkl': cb_model,
                'book_pivot.pkl': cf_model.book_pivot,
                'tfidf_vectorizer.pkl': cb_model.tfidf,
                'content_sim_matrix.pkl': cb_model.content_sim_matrix,
                'title_to_idx.pkl': cb_model.title_to_idx,
                'books_content.pkl': processed_data['books_content'],
                'final_rating.pkl': processed_data['final_rating'],
                'books_data.pkl': processed_data['books']
            }
            
            for filename, data in model_files.items():
                with open(Config.MODELS_DIR / filename, 'wb') as f:
                    pickle.dump(data, f)
                print(f"Saved: {filename}")
            
            print(f"All models saved successfully to: {Config.MODELS_DIR}")
            return True
            
        except Exception as e:
            print(f"Error saving models: {e}")
            return False
    
    def load_models(self):
        """Load all models and data"""
        try:
            print("Loading models and processed data...")
            
            # Check if all required files exist
            required_files = [
                'cf_model.pkl', 'cb_model.pkl', 'books_content.pkl',
                'final_rating.pkl', 'books_data.pkl'
            ]
            
            for filename in required_files:
                if not (Config.MODELS_DIR / filename).exists():
                    print(f"Required file not found: {filename}")
                    return None
            
            # Load models
            with open(Config.MODELS_DIR / 'cf_model.pkl', 'rb') as f:
                cf_model = pickle.load(f)
            
            with open(Config.MODELS_DIR / 'cb_model.pkl', 'rb') as f:
                cb_model = pickle.load(f)
            
            # Load processed data
            with open(Config.MODELS_DIR / 'books_content.pkl', 'rb') as f:
                books_content = pickle.load(f)
            
            with open(Config.MODELS_DIR / 'final_rating.pkl', 'rb') as f:
                final_rating = pickle.load(f)
            
            with open(Config.MODELS_DIR / 'books_data.pkl', 'rb') as f:
                books = pickle.load(f)
            
            # Create hybrid model
            hybrid_model = HybridRecommendationModel(cf_model, cb_model)
            
            print(f"All models loaded successfully from: {Config.MODELS_DIR}")
            
            return {
                'cf_model': cf_model,
                'cb_model': cb_model,
                'hybrid_model': hybrid_model,
                'books_content': books_content,
                'final_rating': final_rating,
                'books': books
            }
            
        except Exception as e:
            print(f"Error loading models: {e}")
            return None
    
    def models_exist(self):
        """Check if trained models exist"""
        required_files = [
            'cf_model.pkl', 'cb_model.pkl', 'books_content.pkl',
            'final_rating.pkl', 'books_data.pkl'
        ]
        
        return all((Config.MODELS_DIR / filename).exists() for filename in required_files)