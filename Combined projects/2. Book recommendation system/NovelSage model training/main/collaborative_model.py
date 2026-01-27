import numpy as np
import pandas as pd
from sklearn.neighbors import NearestNeighbors
from scipy.sparse import csr_matrix
from config import Config

class CollaborativeFilteringModel:
    
    def __init__(self):
        self.model = None
        self.book_pivot = None
        self.is_trained = False
    
    def train(self, final_rating):
        """Train the collaborative filtering model"""
        try:
            print("Training collaborative filtering model...")
            
            # Create user-item matrix
            self.book_pivot = final_rating.pivot_table(
                index='title', 
                columns='user_id', 
                values='rating'
            ).fillna(0)
            
            book_sparse = csr_matrix(self.book_pivot.values)
            
            # Build KNN model
            self.model = NearestNeighbors(metric='cosine', algorithm='brute')
            self.model.fit(book_sparse)
            
            self.is_trained = True
            print("Collaborative filtering model trained successfully")
            
        except Exception as e:
            print(f"Error training collaborative filtering model: {e}")
            self.is_trained = False
    
    def get_recommendations(self, book_title, books_content, books, top_n=Config.DEFAULT_TOP_N):
        """Generate collaborative filtering recommendations"""
        if not self.is_trained:
            print("Model not trained yet")
            return []
        
        try:
            if book_title not in self.book_pivot.index:
                print(f"Book '{book_title}' not found in collaborative filtering data")
                return []
                
            book_idx = np.where(self.book_pivot.index == book_title)[0][0]
            distances, indices = self.model.kneighbors(
                self.book_pivot.iloc[book_idx, :].values.reshape(1, -1),
                n_neighbors=top_n+1
            )
            
            recommendations = []
            for i in range(1, len(indices.flatten())):
                title = self.book_pivot.index[indices.flatten()[i]]
                book_info = books_content[books_content['title'] == title]
                
                if book_info.empty:
                    book_info = books[books['title'] == title]
                    if book_info.empty:
                        continue
                
                book_info = book_info.iloc[0]
                img_url = self._validate_image_url(book_info['img_url'])
                
                recommendations.append({
                    'title': title,
                    'author': book_info['author'],
                    'year': book_info['year'],
                    'publisher': book_info['publisher'],
                    'image_url': img_url,
                    'score': float(1 - distances.flatten()[i]),
                    'type': 'collaborative'
                })
            
            return recommendations[:top_n]
        
        except Exception as e:
            print(f"Error in collaborative recommendations: {e}")
            return []
    
    def _validate_image_url(self, img_url):
        """Validate and return proper image URL"""
        if not isinstance(img_url, str) or not img_url.startswith('http'):
            return Config.DEFAULT_IMAGE_URL
        return img_url