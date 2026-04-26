import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def get_shadow_element(driver, selector_list):
    """
    Pierces through multiple shadow roots to find an element.
    """
    element = driver.execute_script('return document')
    for selector in selector_list:
        element = driver.execute_script('return arguments[0].querySelector(arguments[1])', element, selector)
        if element is None:
            return None
        # Check if there is a shadow root
        shadow_root = driver.execute_script('return arguments[0].shadowRoot', element)
        if shadow_root:
            element = shadow_root
    return element

def get_safe_filename(title, ext=".pdf"):
    """Generates a safe filename for a book title."""
    id_safe = "".join([c for c in title if c.isalnum() or c in (' ', '_', '-')]).strip()
    return f"{id_safe}{ext}"

def download_book(url, title, xpath=None):
    print(f"--- Starting Automated Download for: {title} ---")
    
    download_dir = os.path.join(os.getcwd(), "downloads")
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)

    # CHECK IF FILE ALREADY EXISTS
    # We check for both pdf and epub just in case
    for ext in ['.pdf', '.epub']:
        candidate_path = os.path.join(download_dir, get_safe_filename(title, ext))
        if os.path.exists(candidate_path):
            print(f"File already exists at: {candidate_path}. Skipping download.")
            return candidate_path

    # 0. Handle Google Drive URLs (Direct conversion)
    if "drive.google.com" in url:
        print("Detected Google Drive link. Converting to direct download...")
        try:
            # Extract file ID
            if "/file/d/" in url:
                file_id = url.split("/file/d/")[1].split("/")[0]
                direct_url = f"https://drive.google.com/uc?export=download&id={file_id}"
                print(f"Converted to: {direct_url}")
                # We can often just use requests for this directly
                return download_via_requests(direct_url, title)
        except Exception as e:
            print(f"Drive conversion error: {e}")


    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    
    # Set download preferences
    prefs = {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "plugins.always_open_pdf_externally": False 
    }
    chrome_options.add_experimental_option("prefs", prefs)

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        print(f"Navigating to {url}...")
        driver.get(url)
        
        # Wait until page/viewer is potentially ready
        time.sleep(20) 

        # 1. If it's a PDF Viewer (Shadow DOM)
        if "pdf-viewer" in driver.page_source or ".pdf" in url.lower():
            print(f"Attempting PDF Viewer Shadow DOM click...")
            script = """
            function getDownloadButton() {
                const pdfViewer = document.querySelector('pdf-viewer');
                if (!pdfViewer) return "pdf-viewer not found";
                const toolbar = pdfViewer.shadowRoot ? pdfViewer.shadowRoot.querySelector('viewer-toolbar') : null;
                if (!toolbar) return "viewer-toolbar not found";
                const downloadControls = toolbar.shadowRoot ? toolbar.shadowRoot.querySelector('viewer-download-controls') : null;
                if (!downloadControls) return "viewer-download-controls not found";
                const downloadButton = downloadControls.shadowRoot ? downloadControls.shadowRoot.querySelector('#download') : null;
                if (!downloadButton) return "download button (#download) not found";
                downloadButton.click();
                return "Clicked Successfully";
            }
            return getDownloadButton();
            """
            result = driver.execute_script(script)
            print(f"Shadow DOM Click Result: {result}")
            # Fallback to a broader search for any button that looks like download
            print("Broadening search for download button...")
            driver.execute_script("document.querySelectorAll('button, a, span').forEach(el => { if(el.innerText.toLowerCase().includes('download')) el.click(); })")

        # 2. If a general XPath is provided (ResearchGate etc)
        if xpath:
            print(f"Attempting to click specified XPath: {xpath}")
            try:
                # Check for ResearchGate specific block
                if "Temporarily Unavailable" in driver.title or "Access Denied" in driver.page_source:
                    print("!!! Detected ResearchGate/Cloudflare block !!!")
                
                # Try the user-provided XPath or a more robust text-based one
                try:
                    btn = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, xpath)))
                    btn.click()
                    print("XPath button clicked successfully.")
                except:
                    print("Direct XPath fail, trying robust text-based fallback...")
                    # ResearchGate's button often contains this text
                    fallback_xpath = "//span[contains(text(), 'Download full-text PDF')]"
                    btn = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, fallback_xpath)))
                    btn.click()
                    print("Text-based fallback click successful.")
                
            except Exception as e:
                print(f"XPath click failed: {e}")

        # Wait for file to appear in download dir
        max_wait = 60
        start_time = time.time()
        downloaded_file = None
        
        print("Waiting for download to complete...")
        while time.time() - start_time < max_wait:
            files = os.listdir(download_dir)
            # Look for non-crdownload files
            pdf_files = [f for f in files if (f.endswith('.pdf') or f.endswith('.epub')) and not f.endswith('.crdownload')]
            if pdf_files:
                # Get the most recent one
                pdf_files.sort(key=lambda x: os.path.getmtime(os.path.join(download_dir, x)), reverse=True)
                downloaded_file = os.path.join(download_dir, pdf_files[0])
                break
            time.sleep(1)

        if downloaded_file:
            safe_filename = get_safe_filename(title, ext)
            final_path = os.path.join(download_dir, safe_filename)
            
            os.replace(downloaded_file, final_path)
            print(f"Success! Downloaded: {final_path}")
            return final_path
        
        # Ultimate Fallback: If Selenium fails, try direct request
        print("Selenium download failed. Attempting direct requests fallback...")
        return download_via_requests(url, title)

    except Exception as e:
        print(f"Automated Downloader Error: {e}")
        return None
    finally:
        driver.quit()

def download_via_requests(url, title):
    download_dir = os.path.join(os.getcwd(), "downloads")
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)
        
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        }
        resp = requests.get(url, stream=True, timeout=20, headers=headers)
        
        # CRITICAL: Check Content-Type to avoid saving HTML error pages as PDF
        content_type = resp.headers.get('Content-Type', '').lower()
        print(f"Direct request response Content-Type: {content_type}")
        
        if 'text/html' in content_type:
            print("Error: Direct request returned HTML instead of a document file. Aborting.")
            return None
            
        if resp.status_code == 200:
            # Determine extension from content-type or url
            ext = ".pdf"
            if 'epub' in content_type or url.endswith('.epub'):
                ext = ".epub"
                
            safe_filename = get_safe_filename(title, ext)
            final_path = os.path.join(download_dir, safe_filename)
            with open(final_path, 'wb') as f:
                for chunk in resp.iter_content(chunk_size=8192):
                    f.write(chunk)
            print(f"Success via requests: {final_path}")
            return final_path
    except Exception as e:
        print(f"Requests download failed: {e}")
    return None

import requests # Needed for fallback

def batch_download_handpicked():
    """Reads handpicked_links.json and downloads all books."""
    print("\n--- Starting Batch Download of Handpicked Links ---")
    
    # Correct path to handpicked_links.json
    base_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(base_dir, "models", "handpicked_links.json")
    
    if not os.path.exists(json_path):
        print(f"Error: {json_path} not found.")
        return

    try:
        import json
        with open(json_path, 'r') as f:
            links = json.load(f)
            
        total = len(links)
        print(f"Found {total} books to process.")
        
        for idx, entry in enumerate(links, 1):
            title = entry.get('title')
            url = entry.get('link')
            xpath = entry.get('xpath')
            
            print(f"\n[{idx}/{total}] Processing: {title}")
            download_book(url, title, xpath)
            
        print("\n--- Batch Download Completed ---")
    except Exception as e:
        print(f"Batch Download Error: {e}")

if __name__ == "__main__":
    # Run batch download when script is executed directly
    batch_download_handpicked()
