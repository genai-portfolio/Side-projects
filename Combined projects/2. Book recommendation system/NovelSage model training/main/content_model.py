import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from config import Config

class ContentBasedModel:
    
    def __init__(self):
        self.tfidf = None
        self.content_sim_matrix = None
        self.title_to_idx = None
        self.is_trained = False
    
    def train(self, books_content):
        """Train the content-based model"""
        try:
            print("Training content-based model...")
            
            # TF-IDF Vectorizer
            self.tfidf = TfidfVectorizer(
                stop_words='english', 
                max_features=Config.TFIDF_MAX_FEATURES
            )
            
            tfidf_matrix = self.tfidf.fit_transform(books_content['content_features'])
            self.content_sim_matrix = cosine_similarity(tfidf_matrix)
            
            # Create title to index mapping
            self.title_to_idx = pd.Series(books_content.index, index=books_content['title'])
            self.title_to_idx.drop_duplicates(inplace=True)
            
            self.is_trained = True
            print("Content-based model trained successfully")
            
        except Exception as e:
            print(f"Error training content-based model: {e}")
            self.is_trained = False
    
    def get_recommendations(self, book_title, books_content, top_n=Config.DEFAULT_TOP_N):
        """Generate content-based recommendations"""
        if not self.is_trained:
            print("Model not trained yet")
            return []
        
        try:
            if book_title not in self.title_to_idx:
                print(f"Book '{book_title}' not found in content-based data")
                return []
                
            cb_idx = self.title_to_idx[book_title]
            sim_scores = list(enumerate(self.content_sim_matrix[cb_idx]))
            sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
            sim_scores = sim_scores[1:top_n+1]
            
            recommendations = []
            for i, score in sim_scores:
                title = books_content['title'].iloc[i]
                book_info = books_content[books_content['title'] == title].iloc[0]
                
                img_url = self._validate_image_url(book_info['img_url'])
                
                recommendations.append({
                    'title': title,
                    'author': book_info['author'],
                    'year': book_info['year'],
                    'publisher': book_info['publisher'],
                    'image_url': img_url,
                    'score': float(score),
                    'type': 'content'
                })
            
            return recommendations[:top_n]
        
        except Exception as e:
            print(f"Error in content recommendations: {e}")
            return []
    
    def _validate_image_url(self, img_url):
        """Validate and return proper image URL"""
        if not isinstance(img_url, str) or not img_url.startswith('http'):
            return Config.DEFAULT_IMAGE_URL
        return img_url