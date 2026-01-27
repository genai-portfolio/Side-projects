from pathlib import Path

class Config:
    
    # Paths
    # BASE_DIR = Path(__file__).parent.absolute()
    BASE_DIR = Path(__file__).parent.parent.absolute()
    DATA_DIR = BASE_DIR / 'data'
    MODELS_DIR = BASE_DIR / 'models'
    
    # Data files
    BOOKS_FILE = 'BX-Books.csv'
    USERS_FILE = 'BX-Users.csv'
    RATINGS_FILE = 'BX-Book-Ratings.csv'
    
    # Model parameters
    MIN_USER_RATINGS = 200
    MIN_BOOK_RATINGS = 50
    TFIDF_MAX_FEATURES = 10000
    
    # Recommendation parameters
    DEFAULT_TOP_N = 10
    HYBRID_CF_WEIGHT = 0.6
    HYBRID_CB_WEIGHT = 0.4
    
    # Image settings
    DEFAULT_IMAGE_URL = "https://via.placeholder.com/150x220?text=No+Image"