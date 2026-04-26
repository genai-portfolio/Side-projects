import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from fpdf import FPDF

def create_pdf_from_text(text, output_path, title):
    """Generate a clean PDF from book text"""
    try:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)
        
        # Add Title
        pdf.set_font("Helvetica", "B", 16)
        pdf.cell(0, 10, title, ln=True, align="C")
        pdf.ln(10)
        
        # Add Body
        pdf.set_font("Helvetica", size=12)
        # Clean text for PDF compatibility (Latin-1)
        clean_text = text.encode('latin-1', 'replace').decode('latin-1')
        pdf.multi_cell(0, 10, clean_text)
        
        pdf.output(output_path)
        print(f"PDF generated successfully: {output_path}")
        return True
    except Exception as e:
        print(f"PDF Generation Error: {e}")
        return False

def deep_search_for_book(isbn, title):
    """
    Hyper-Aggressive Scraper: Uses Selenium to find download links across multiple sources.
    """
    print(f"--- TRIGGERING HYPER-AGGRESSIVE DEEP SEARCH for: {title} ---")
    
    chrome_options = Options()
    chrome_options.add_argument("--headless") 
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36")

    driver = None
    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # Multiple queries for redundancy
        queries = [
            f'"{title}" pdf download free',
            f'"{title}" site:archive.org'
        ]
        
        for search_query in queries:
            print(f"Searching: {search_query}...")
            driver.get(f"https://www.google.com/search?q={requests.utils.quote(search_query)}")
            
            try:
                WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "search")))
            except: continue
            
            # Find all links
            results = driver.find_elements(By.CSS_SELECTOR, "div.g a")
            
            for res in results:
                try:
                    href = res.get_attribute("href")
                    alt_text = res.text.lower()
                    
                    if not href or "google.com" in href: continue

                    # 1. Archive.org Specialized Handling (Very Reliable)
                    if "archive.org/details/" in href:
                        # Extract the identifier cleanly
                        ia_id = href.split('details/')[-1].strip('/').split('?')[0].split('/')[0]
                        # Construction of direct PDF link
                        direct_pdf = f"https://archive.org/download/{ia_id}/{ia_id}.pdf"
                        print(f"Constructed Archive.org PDF: {direct_pdf}")
                        return {'type': 'direct', 'link': direct_pdf}

                    # 2. Direct PDF Detection
                    if href.lower().endswith('.pdf') or "pdf" in alt_text:
                        print(f"Detected potential PDF link: {href}")
                        # Return immediately for speed - app.py will verify via GET
                        return {'type': 'direct', 'link': href}
                    
                    # 3. Known "High Success" Domains
                    if any(domain in href for domain in ['z-lib', 'pdfdrive', 'oceanofpdf', 'manualslib', 'slideshare']):
                        print(f"Found trusted archive: {href}")
                        return {'type': 'online', 'link': href}
                except: continue

        return None

    except Exception as e:
        print(f"Deep Search Critical Error: {e}")
        return None
    finally:
        if driver: driver.quit()

if __name__ == "__main__":
    # Test
    res = deep_search_for_book("034538475X", "The Witching Hour")
    print("Result:", res)
