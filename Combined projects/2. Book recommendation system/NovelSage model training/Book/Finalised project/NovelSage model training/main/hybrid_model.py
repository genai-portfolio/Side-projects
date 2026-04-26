from config import Config

class HybridRecommendationModel:

    def __init__(self, cf_model, cb_model):
        self.cf_model = cf_model
        self.cb_model = cb_model
    
    def get_recommendations(self, book_title, books_content, books, 
                          cf_weight=Config.HYBRID_CF_WEIGHT, 
                          cb_weight=Config.HYBRID_CB_WEIGHT, 
                          top_n=Config.DEFAULT_TOP_N):
        """Generate hybrid recommendations"""
        try:
            print(f"Generating hybrid recommendations for: {book_title}")
            
            cf_recs = self.cf_model.get_recommendations(book_title, books_content, books, top_n*2)
            cb_recs = self.cb_model.get_recommendations(book_title, books_content, top_n*2)
            
            if not cf_recs and not cb_recs:
                print("No recommendations found from either model")
                return []
            
            combined_scores = {}
            
            # Add collaborative filtering scores
            for rec in cf_recs:
                combined_scores[rec['title']] = {
                    'data': rec,
                    'score': rec['score'] * cf_weight
                }
            
            # Add content-based scores
            for rec in cb_recs:
                if rec['title'] in combined_scores:
                    combined_scores[rec['title']]['score'] += rec['score'] * cb_weight
                else:
                    combined_scores[rec['title']] = {
                        'data': rec,
                        'score': rec['score'] * cb_weight
                    }
            
            # Sort by combined score
            sorted_recs = sorted(combined_scores.values(), key=lambda x: x['score'], reverse=True)
            
            # Prepare final recommendations
            final_recommendations = []
            for rec in sorted_recs[:top_n]:
                final_rec = rec['data'].copy()
                final_rec['score'] = float(rec['score'])
                final_rec['type'] = 'hybrid'
                final_recommendations.append(final_rec)
            
            print(f"Generated {len(final_recommendations)} hybrid recommendations")
            return final_recommendations
        
        except Exception as e:
            print(f"Error in hybrid recommendations: {e}")
            return []