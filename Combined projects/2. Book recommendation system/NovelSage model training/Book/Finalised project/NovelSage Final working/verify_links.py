import pandas as pd
import requests
import time
import os

# Configuration
INPUT_CSV = r"c:\Users\gamer\Gul-Friend-Project\NovelSage model training\data\BX-Books.csv"
OUTPUT_CSV = r"c:\Users\gamer\Gul-Friend-Project\NovelSage Final working\models\Verified-Books.csv"
START_ROW = 14648     # Index of the first book to process
END_ROW = 20000       # Index (exclusive) of the last book to process
TIMEOUT = (3, 5)
MAX_RETRIES = 2

def get_verified_link(isbn, title):
    # 1. Try Google Books API
    try:
        gb_url = f"https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}"
        for attempt in range(MAX_RETRIES):
            try:
                resp = requests.get(gb_url, timeout=TIMEOUT)
                data = resp.json()
                if 'items' in data:
                    vol = data['items'][0].get('volumeInfo', {})
                    acc = data['items'][0].get('accessInfo', {})
                    
                    # Direct PDF/EPUB if available
                    pdf_link = acc.get('pdf', {}).get('downloadLink')
                    if pdf_link: return pdf_link
                    
                    # webReader if FULL or SAMPLE
                    if acc.get('accessViewStatus') in ['FULL', 'SAMPLE']:
                        reader_link = acc.get('webReaderLink')
                        if reader_link: return reader_link
                break
            except requests.exceptions.Timeout:
                if attempt == MAX_RETRIES - 1: print(f"GB Timeout for {isbn}")
                time.sleep(1)
    except Exception as e:
        print(f"GB Error: {e}")

    # 2. Try Open Library / Archive.org
    try:
        ol_url = f"https://openlibrary.org/api/volumes/brief/isbn/{isbn}.json"
        for attempt in range(MAX_RETRIES):
            try:
                resp = requests.get(ol_url, timeout=TIMEOUT)
                data = resp.json()
                if data and str(isbn) in data:
                    records = data[str(isbn)].get('records', {})
                    for key in records:
                        ia_id = records[key].get('data', {}).get('identifiers', {}).get('archive', [None])[0]
                        if ia_id:
                            # Constructor for direct PDF link
                            direct_pdf = f"https://archive.org/download/{ia_id}/{ia_id}.pdf"
                            # Verify if link is live (HEAD request)
                            try:
                                head = requests.head(direct_pdf, timeout=TIMEOUT, allow_redirects=True)
                                if head.status_code == 200:
                                    return direct_pdf
                            except: pass
                            
                            # Fallback to general IA link if PDF construction fails
                            return f"https://archive.org/details/{ia_id}"
                break
            except requests.exceptions.Timeout:
                time.sleep(1)
    except Exception as e:
        print(f"OL Error: {e}")

    return None

def main():
    print(f"Loading {INPUT_CSV}...")
    # Read with semicolon delimiter
    try:
        # Use quoting=3 (csv.QUOTE_NONE) to handle the messed up double-double quotes
        df = pd.read_csv(INPUT_CSV, sep=';', encoding='latin-1', quoting=3, on_bad_lines='skip', low_memory=False)
        print("Raw Columns:", df.columns.tolist())
    except Exception as e:
        print(f"Read error: {e}")
        return

    # Cleanup quotes from column names
    df.columns = [c.strip('"') for c in df.columns]
    print("Cleaned columns:", df.columns.tolist())
    
    # Clean up values (strip excessive quotes)
    for col in df.columns:
        if df[col].dtype == object:
            df[col] = df[col].astype(str).str.strip('"').str.replace('""', '"')
    
    # Check for ISBN
    if 'ISBN' in df.columns:
        df['ISBN'] = df['ISBN'].str.strip()
    else:
        print("ERROR: ISBN column still not found!")
        return

    if 'Book-Title' in df.columns:
        df['Book-Title'] = df['Book-Title'].str.strip()
    else:
        print("ERROR: Book-Title column not found!")
        return
    
    subset = df.iloc[START_ROW:END_ROW].copy()
    total_to_process = len(subset)
    
    print(f"Verifying links for {total_to_process} books (Rows {START_ROW} to {END_ROW})...")
    verified_records = []
    
    for i, (idx, row) in enumerate(subset.iterrows()):
        isbn = row['ISBN']
        title = row['Book-Title']
        print(f"[{i+1}/{total_to_process}] (Source Row: {idx}) Checking {title} ({isbn})...")
        
        link = get_verified_link(isbn, title)
        if link:
            new_row = row.to_dict()
            new_row['pdf_link'] = link
            verified_records.append(new_row)
            print(f"Verified: {link}")
        
        # Save every 10 books (or at the end)
        if (i + 1) % 10 == 0 or (i + 1) == total_to_process:
            if verified_records:
                temp_df = pd.DataFrame(verified_records)
                mode = 'a' if os.path.exists(OUTPUT_CSV) else 'w'
                header = not os.path.exists(OUTPUT_CSV)
                temp_df.to_csv(OUTPUT_CSV, index=False, mode=mode, header=header)
                print(f"--- Saved batch to {OUTPUT_CSV} ---")
                verified_records = [] # Reset for next batch
        
        # Small delay to be nice to APIs
        time.sleep(0.1)
    
    print(f"Finished processing. Verified links saved to {OUTPUT_CSV}")

if __name__ == "__main__":
    main()
