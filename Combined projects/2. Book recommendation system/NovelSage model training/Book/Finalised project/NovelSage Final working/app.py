import os
import pickle
import numpy as np
import pandas as pd
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, Response, stream_with_context, send_from_directory
import io
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import requests
from huggingface_hub import InferenceClient
from dotenv import load_dotenv
from scraper_utils import deep_search_for_book, create_pdf_from_text
from automated_downloader import download_book, batch_download_handpicked, get_safe_filename
import json

# Load environment variables
load_dotenv()

from models import db, User, Activity

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'NovelSageAI-Super-Secret-Key-2026')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///novelsage.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# --- Recommendation Logic (Adapted from original app.py) ---

def load_models():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    models_dir = os.path.join(base_dir, "models")
    
    models = {}
    files = {
        'cf_model': 'cf_model.pkl',
        'book_pivot': 'book_pivot.pkl',
        'tfidf': 'tfidf_vectorizer.pkl',
        'content_sim_matrix': 'content_sim_matrix.pkl',
        'title_to_idx': 'title_to_idx.pkl',
        'books_content': 'books_content.pkl',
        'final_rating': 'final_rating.pkl',
        'books': 'books_data.pkl'
    }

    for key, filename in files.items():
        file_path = os.path.join(models_dir, filename)
        if os.path.exists(file_path):
            with open(file_path, 'rb') as f:
                models[key] = pickle.load(f)
        else:
            print(f"Warning: model file {filename} not found.")
    
    return models

def load_handpicked_links():
    handpicked_path = os.path.join(os.path.dirname(__file__), "models", "handpicked_links.json")
    if os.path.exists(handpicked_path):
        with open(handpicked_path, 'r') as f:
            return json.load(f)
    return []

models_cache = load_models()
handpicked_links = load_handpicked_links()

# Load Full Catalog and Verified Books
def load_full_catalog():
    bx_books_path = r"c:\Users\gamer\Gul-Friend-Project\NovelSage model training\data\BX-Books.csv"
    verified_path = os.path.join(os.path.dirname(__file__), "models", "Verified-Books.csv")
    
    try:
        # Load main BX-Books catalog
        if os.path.exists(bx_books_path):
            print(f"Loading full catalog from {bx_books_path}...")
            # Use same robust reading logic from verify_links.py
            full_df = pd.read_csv(bx_books_path, sep=';', encoding='latin-1', quoting=3, on_bad_lines='skip', low_memory=False)
            
            # Clean column names and data
            full_df.columns = [c.strip('"') for c in full_df.columns]
            
            # Use Image-URL-M as the default image_url for consistency
            column_map = {
                'ISBN': 'ISBN',
                'Book-Title': 'title',
                'Book-Author': 'author',
                'Year-Of-Publication': 'year',
                'Image-URL-M': 'img_url'
            }
            
            # Keep only necessary columns and rename
            present_cols = [c for c in column_map.keys() if c in full_df.columns]
            full_df = full_df[present_cols].rename(columns={c: column_map[c] for c in present_cols})
            
            # Strip excessive quotes/whitespace from values
            for col in full_df.columns:
                if full_df[col].dtype == object:
                    full_df[col] = full_df[col].astype(str).str.strip('"').str.strip()
            
            # Now load and merge verified books
            if os.path.exists(verified_path):
                print(f"Merging verified links from {verified_path}...")
                verified_df = pd.read_csv(verified_path, on_bad_lines='skip')
                # Clean up ISBN and pdf_link columns
                verified_df['ISBN'] = verified_df['ISBN'].astype(str).str.strip('"').str.strip()
                
                # Merge into full catalog
                full_df = full_df.merge(verified_df[['ISBN', 'pdf_link']], on='ISBN', how='left')
                print(f"Verified links merged. Total rows: {len(full_df)}")
            
            # Update models_cache with this richer dataset
            models_cache['books_content'] = full_df
            return full_df
        else:
            print(f"Warning: {bx_books_path} not found. Using pickled subset.")
            return models_cache.get('books_content', pd.DataFrame())
    except Exception as e:
        print(f"Error loading full catalog: {e}")
        return models_cache.get('books_content', pd.DataFrame())

# Initialize the rich dataset
all_books_df = load_full_catalog()

def collaborative_recommendations(book_title, top_n=8):
    try:
        if book_title not in models_cache['book_pivot'].index:
            return []
        book_idx = np.where(models_cache['book_pivot'].index == book_title)[0][0]
        distances, indices = models_cache['cf_model'].kneighbors(
            models_cache['book_pivot'].iloc[book_idx, :].values.reshape(1, -1),
            n_neighbors=top_n+1)
        
        recs = []
        for i in range(1, len(indices.flatten())):
            title = models_cache['book_pivot'].index[indices.flatten()[i]]
            book_info = models_cache['books_content'][models_cache['books_content']['title'] == title]
            if book_info.empty: continue
            
            book_info = book_info.iloc[0]
            recs.append({
                'title': title, 'author': book_info['author'], 'year': book_info['year'],
                'image_url': book_info['img_url'], 'isbn': book_info['ISBN'], 
                'pdf_link': book_info.get('pdf_link') if not pd.isna(book_info.get('pdf_link')) else None,
                'score': (1 - distances.flatten()[i]), 'type': 'collaborative'
            })
        return recs[:top_n]
    except: return []

def content_recommendations(book_title, top_n=8):
    try:
        if book_title not in models_cache['title_to_idx']: return []
        idx = models_cache['title_to_idx'][book_title]
        sim_scores = sorted(list(enumerate(models_cache['content_sim_matrix'][idx])), key=lambda x: x[1], reverse=True)[1:top_n+1]
        
        recs = []
        for i, score in sim_scores:
            title = models_cache['books_content']['title'].iloc[i]
            book_info = models_cache['books_content'].iloc[i]
            recs.append({
                'title': title, 'author': book_info['author'], 'year': book_info['year'],
                'image_url': book_info['img_url'], 'isbn': book_info['ISBN'], 
                'pdf_link': book_info.get('pdf_link') if not pd.isna(book_info.get('pdf_link')) else None,
                'score': score, 'type': 'content'
            })
        return recs
    except: return []

def hybrid_recommendations(book_title, top_n=8):
    cf = collaborative_recommendations(book_title, top_n*2)
    cb = content_recommendations(book_title, top_n*2)
    combined = {r['title']: {'data': r, 'score': r['score'] * 0.6} for r in cf}
    for r in cb:
        if r['title'] in combined: combined[r['title']]['score'] += r['score'] * 0.4
        else: combined[r['title']] = {'data': r, 'score': r['score'] * 0.4}
    
    sorted_recs = sorted(combined.values(), key=lambda x: x['score'], reverse=True)
    return [r['data'] for r in sorted_recs[:top_n]]

def get_trending_books(top_n=10):
    try:
        # Based on rating count in final_rating.pkl
        titles = models_cache['final_rating'].groupby('title')['rating'].count().sort_values(ascending=False).head(top_n).index.tolist()
        trending = []
        for t in titles:
            info = models_cache['books_content'][models_cache['books_content']['title'] == t]
            if not info.empty:
                r = info.iloc[0]
                link = r.get('pdf_link')
                trending.append({
                    'title': t, 
                    'author': r['author'], 
                    'image_url': r['img_url'], 
                    'isbn': r['ISBN'],
                    'pdf_link': link if not pd.isna(link) else None
                })
        return trending
    except: return []

# --- Presentation Success Layer (Guaranteed Downloads) ---
PRESENTATION_ARSENAL = {
    # 1. System Success Test (The "Fluke" that will ALWAYS work)
    "System Test": "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf",
    
    # 2. Real Books with Multi-Source Backup
    "The Witching Hour": "https://vaccination.gov.ng/Resources/cTDDcn/278049/The%20Witching%20Hour%20Anne%20Rice.pdf",
    "Me Talk Pretty One Day": "https://ia600201.us.archive.org/1/items/metalkprettyoned00seda/metalkprettyoned00seda.pdf",
    "The Weight of Water": "https://archive.org/download/weightofwaterano00shre/weightofwaterano00shre.pdf",
    "The Fellowship of the Ring": "https://archive.org/download/the-fellowship-of-the-ring_202111/The%20Fellowship%20of%20the%20Ring.pdf",
    "The Alchemist": "https://archive.org/download/thealchemist_202102/The_Alchemist.pdf"
}

def discover_book_link(isbn, title):
    """Dynamic discovery logic from verify_links.py"""
    TIMEOUT = (5, 10)
    
    # 1. Try Google Books API
    try:
        gb_url = f"https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}"
        resp = requests.get(gb_url, timeout=TIMEOUT)
        data = resp.json()
        if 'items' in data:
            acc = data['items'][0].get('accessInfo', {})
            pdf_link = acc.get('pdf', {}).get('downloadLink')
            if pdf_link: return pdf_link
            if acc.get('accessViewStatus') in ['FULL', 'SAMPLE']:
                reader_link = acc.get('webReaderLink')
                if reader_link: return reader_link
    except: pass

    # 2. Try Open Library / Archive.org
    try:
        ol_url = f"https://openlibrary.org/api/volumes/brief/isbn/{isbn}.json"
        resp = requests.get(ol_url, timeout=TIMEOUT)
        data = resp.json()
        if data and str(isbn) in data:
            records = data[str(isbn)].get('records', {})
            for key in records:
                ia_id = records[key].get('data', {}).get('identifiers', {}).get('archive', [None])[0]
                if ia_id:
                    direct_pdf = f"https://archive.org/download/{ia_id}/{ia_id}.pdf"
                    try:
                        head = requests.head(direct_pdf, timeout=(3, 5), allow_redirects=True)
                        if head.status_code == 200: return direct_pdf
                    except: pass
                    return f"https://archive.org/details/{ia_id}"
    except: pass

    # 3. Last Resort: Deep Search Scraper (Selenium)
    try:
        print(f"APIs failed. Triggering Deep Search Scraper for {title}...")
        deep_result = deep_search_for_book(isbn, title)
        if deep_result:
            return deep_result # Return full dict
    except Exception as e:
        print(f"Scraper error: {e}")

    return None

def cache_new_link(isbn, title, link):
    """Append newly discovered link to the local catalog and file"""
    try:
        verified_path = os.path.join(os.path.dirname(__file__), "models", "Verified-Books.csv")
        
        # 1. Update in-memory DataFrame for immediate session use
        if 'books_content' in models_cache:
            idx = models_cache['books_content'].index[models_cache['books_content']['ISBN'] == isbn]
            if not idx.empty:
                models_cache['books_content'].at[idx[0], 'pdf_link'] = link
                print(f"Updated in-memory cache for {title}")
        
        # 2. Persist to file
        if os.path.exists(verified_path):
            existing_df = pd.read_csv(verified_path, nrows=0) # Just get columns
            
            # Create a dictionary with all columns from the file
            new_row_dict = {col: "" for col in existing_df.columns}
            new_row_dict['ISBN'] = isbn
            new_row_dict['Book-Title'] = title
            new_row_dict['pdf_link'] = link
            
            new_data = pd.DataFrame([new_row_dict])
            # Reorder columns to match existing file exactly
            new_data = new_data[existing_df.columns]
            
            new_data.to_csv(verified_path, mode='a', header=False, index=False)
            print(f"Successfully appended new link for {title} to {verified_path}")
    except Exception as e:
        print(f"Caching error: {e}")

# --- NovelBot Integration ---

hf_token = os.getenv('HUGGINGFACE_API_TOKEN')
client = InferenceClient(model="meta-llama/Llama-3.2-1B-Instruct", token=hf_token) if hf_token else None

@app.route('/chat', methods=['POST'])
def chat():
    if not client:
        return jsonify({'response': "Chatbot is offline. Please configure your Hugging Face API Token in the .env file."})
    
    user_msg = request.json.get('message', '')
    trending = [b['title'] for b in get_trending_books(5)]
    trending_str = ", ".join(trending)
    
    system_prompt = f"You are NovelSage AI (NovelBot), a helpful book expert. The current trending books are: {trending_str}. " \
                    f"When mentioning a book, ALWAYS use the format [BOOK:Book Title]. " \
                    f"When mentioning an author, ALWAYS make their name **bold**. " \
                    f"Keep answers professional, insightful, and formatted to be highly readable."
    
    try:
        response = ""
        for message in client.chat_completion(
            messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": user_msg}],
            max_tokens=200,
            stream=True,
        ):
            if message.choices and len(message.choices) > 0:
                content = message.choices[0].delta.content
                if content:
                    response += content
        return jsonify({'response': response.strip()})
    except Exception as e:
        return jsonify({'response': f"Error: {str(e)}"})

@app.route('/get_book_card/<path:title>')
def get_book_card(title):
    # Search in full catalog
    book_info = all_books_df[all_books_df['title'].str.contains(title, case=False, na=False)].head(1)
    if not book_info.empty:
        book = book_info.iloc[0]
        return jsonify({
            'title': book['title'],
            'author': book['author'],
            'image_url': book['img_url'] if not pd.isna(book['img_url']) else 'https://via.placeholder.com/150x220?text=No+Cover'
        })
    return jsonify({'error': 'Book not found'}), 404
@app.route('/get_summary/<path:book_title>')
def get_summary(book_title):
    # 1. Try NovelBot Neural Engine
    if client:
        try:
            prompt = f"You are a literary expert. Provide a concise summary (exactly 3 sentences) of the book: {book_title}."
            summary = ""
            for message in client.chat_completion(
                messages=[{"role": "user", "content": prompt}],
                max_tokens=150,
                stream=True,
            ):
                if message.choices and len(message.choices) > 0:
                    content = message.choices[0].delta.content
                    if content:
                        summary += content
            
            if summary.strip() and "I don't know" not in summary and "I'm sorry" not in summary:
                return jsonify({'summary': summary.strip()})
        except Exception as e:
            print(f"HF Summary Error: {e}")

    # 2. Fallback to Google Books API
    try:
        url = f"https://www.googleapis.com/books/v1/volumes?q=intitle:{requests.utils.quote(book_title)}"
        response = requests.get(url, timeout=(3, 5))
        data = response.json()
        if 'items' in data:
            description = data['items'][0].get('volumeInfo', {}).get('description', '')
            if description:
                # Truncate if too long or just use first 300 chars for "conciseness"
                sentences = description.split('.')[:3]
                concise_summary = '. '.join(sentences) + '.'
                return jsonify({'summary': concise_summary})
    except Exception as e:
        print(f"Google Books API Error: {e}")

    return jsonify({'summary': "Summary not available for this book."})

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def handle_book_delivery(direct_link, title, force_redirect=False):
    """Internal helper to stream or link to a discovered book"""
    if not direct_link:
        return None
        
    print(f"Handling delivery for: {direct_link} (Force Redirect: {force_redirect})")
    
    if force_redirect:
        return jsonify({'link': direct_link, 'type': 'online'})

    # If it's a direct file link, try to stream it
    if any(ext in direct_link.lower() for ext in ['.pdf', '.epub', '/download/']):
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
                'Referer': 'https://www.google.com/'
            }
            file_resp = requests.get(direct_link, stream=True, timeout=(5, 15), headers=headers, verify=False)
            
            if file_resp.status_code == 200:
                ext = 'pdf' if '.pdf' in direct_link.lower() else 'epub'
                safe_title = "".join([c for c in title if c.isalnum() or c in (' ', '_', '-')]).strip()
                filename = f"{safe_title}.{ext}"
                
                return Response(
                    stream_with_context(file_resp.iter_content(chunk_size=8192)),
                    content_type=file_resp.headers.get('content-type'),
                    headers={"Content-Disposition": f"attachment; filename=\"{filename}\""}
                )
        except Exception as e:
            print(f"Streaming failed, falling back to online link: {e}")
            
    # Default to returning the link for frontend to open in a new tab
    return jsonify({'link': direct_link, 'type': 'online'})

@app.route('/read_book/<isbn>/<path:title>')
@login_required
def read_book(isbn, title):
    try:
        print(f"--- READ REQUEST: {title} (ISBN: {isbn}) ---")
        
        # Check if the book exists locally in the downloads folder
        download_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "downloads")
        
        # We need to find the file regardless of extension (.pdf or .epub)
        found_file = None
        for ext in ['.pdf', '.epub']:
            safe_name = get_safe_filename(title, ext)
            test_path = os.path.join(download_dir, safe_name)
            if os.path.exists(test_path):
                found_file = safe_name
                break
        
        if found_file:
            print(f"Book found locally: {found_file}")
            # Instead of streaming, we tell the frontend to open the reader
            return jsonify({
                'status': 'available',
                'filename': found_file,
                'title': title
            })
        
        # If not found locally, check if it's a handpicked link we can download automatically
        for entry in handpicked_links:
            if entry['title'].lower() in title.lower() or title.lower() in entry['title'].lower():
                return jsonify({
                    'status': 'download_needed',
                    'message': "This book needs to be downloaded before you can read it.",
                    'is_handpicked': True,
                    'link': entry['link'],
                    'xpath': entry.get('xpath')
                }), 403

        # If not handpicked, try discovery to find a link
        print(f"No local link found. Starting discovery engine for {title}...")
        discovery_result = discover_book_link(isbn, title)
        
        if discovery_result:
            direct_link = discovery_result.get('link') if isinstance(discovery_result, dict) else discovery_result
            if direct_link:
                return jsonify({
                    'status': 'download_needed',
                    'message': "We found a copy! Download it now to read in your browser.",
                    'link': direct_link
                }), 403

        # Final Fallback
        return jsonify({
            'status': 'not_found',
            'error': "Direct download link not found. Please download the book to your collection first.",
            'fallback': f"https://www.google.com/search?q={requests.utils.quote(title + ' pdf download')}"
        }), 404

    except Exception as e:
        print(f"Read Book Critical Error: {e}")
        return jsonify({'error': "Error processing your request."}), 500

@app.route('/download_now', methods=['POST'])
@login_required
def download_now():
    """Explicitly trigger a download for a book"""
    data = request.json
    url = data.get('url')
    title = data.get('title')
    xpath = data.get('xpath')
    
    if not url or not title:
        return jsonify({'error': 'Missing URL or Title'}), 400
        
    try:
        # Trigger the automated downloader
        path = download_book(url, title, xpath)
        if path and os.path.exists(path):
            filename = os.path.basename(path)
            return jsonify({'status': 'success', 'filename': filename})
        return jsonify({'error': 'Download failed. Please try again.'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/view_reader/<path:filename>')
@login_required
def view_reader(filename):
    """Render the custom reader page"""
    # Try to find a nice title from a handpicked entry if possible
    display_title = filename.replace('.pdf', '').replace('.epub', '')
    for entry in handpicked_links:
        safe = get_safe_filename(entry['title'], '.pdf') # assume .pdf for comparison
        if safe.lower() == filename.lower() or safe.replace('.pdf', '.epub').lower() == filename.lower():
            display_title = entry['title']
            break
            
    return render_template('reader.html', filename=filename, title=display_title)

@app.route('/serve_book/<path:filename>')
@login_required
def serve_book(filename):
    """Directly serve the PDF file for the reader iframe"""
    download_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "downloads")
    return send_from_directory(download_dir, filename)


# --- Routes ---

@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        full_name = request.form.get('full_name')
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Check if email is already registered
        if User.query.filter_by(email=email).first():
            flash('This Gmail is already registered.')
            return redirect(url_for('signup'))
        
        # Create username from email (part before @)
        username = email.split('@')[0]
        
        new_user = User(
            username=username,
            email=email,
            full_name=full_name,
            password_hash=generate_password_hash(password)
        )
        db.session.add(new_user)
        db.session.commit()
        
        flash('Registration successful! Please sign in.')
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            # If interests are not set (first time login/onboarding skip), go to onboarding
            if not user.interests:
                return redirect(url_for('onboarding'))
            return redirect(url_for('home'))
        flash('Invalid Gmail or password.')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/onboarding', methods=['GET', 'POST'])
@login_required
def onboarding():
    if request.method == 'POST':
        interests = request.form.getlist('interests')
        current_user.interests = ",".join(interests)
        db.session.commit()
        return redirect(url_for('home'))
    genres = ["Fiction", "Mystery", "Thriller", "Sci-Fi", "Fantasy", "Romance", "History", "Biography", "Business", "Self-Help"]
    return render_template('onboarding.html', genres=genres)

@app.route('/home')
@login_required
def home():
    if not current_user.interests:
        return redirect(url_for('onboarding'))
    trending = get_trending_books(10)
    # Basic recommendation based on first interest for now
    user_interests = current_user.interests.split(',') if current_user.interests else []
    recommended = []
    if user_interests:
        # Search for a book matching one of the interests to seed recommendation
        match = models_cache['books_content'][models_cache['books_content']['title'].str.contains(user_interests[0], case=False, na=False)]
        if not match.empty:
            recommended = hybrid_recommendations(match.iloc[0]['title'])
            # Ensure pdf_link is present in recommended items
            for rec in recommended:
                info = models_cache['books_content'][models_cache['books_content']['title'] == rec['title']]
                if not info.empty:
                    link = info.iloc[0].get('pdf_link')
                    rec['pdf_link'] = link if not pd.isna(link) else None
    
    return render_template('home.html', trending=trending, recommended=recommended)

@app.route('/dashboard')
@login_required
def dashboard():
    activities = Activity.query.filter_by(user_id=current_user.id).order_by(Activity.timestamp.desc()).all()
    return render_template('dashboard.html', activities=activities)

@app.route('/track_activity', methods=['POST'])
@login_required
def track_activity():
    data = request.json
    activity = Activity(user_id=current_user.id, book_title=data['title'], action_type=data['action'])
    db.session.add(activity)
    db.session.commit()
    return jsonify({'status': 'success'})

@app.route('/search_books')
@login_required
def search_books():
    query = request.args.get('query', '').strip().lower()
    if not query:
        return jsonify([])
    
    user_interests = current_user.interests.lower().split(',') if current_user.interests else []
    
    # Search in full catalog using partial case-insensitive matching
    results = []
    # Using str.contains for partial match (case-insensitive)
    # We use models_cache['books_content'] which now holds the full catalog
    matches = models_cache['books_content'][models_cache['books_content']['title'].str.contains(query, case=False, na=False)]
    
    # Limit to top 15 results for UI performance
    for _, row in matches.head(15).iterrows():
        # Score boosting based on interest
        score = 0
        title_lower = str(row['title']).lower()
        if any(interest.strip() in title_lower for interest in user_interests if interest.strip()):
            score += 1
            
        results.append({
            'title': row['title'],
            'author': row['author'],
            'year': row['year'],
            'image_url': row['img_url'],
            'isbn': row['ISBN'],
            'pdf_link': row.get('pdf_link') if not pd.isna(row.get('pdf_link')) else None,
            'score': score
        })
    
    # Sort by score (interests first) then return
    results = sorted(results, key=lambda x: x['score'], reverse=True)
    return jsonify(results)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
