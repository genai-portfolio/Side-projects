from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
import time
import os
import re

# Try to import pyautogui for fallback clicking
try:
    import pyautogui
    PYAUTOGUI_AVAILABLE = True
except ImportError:
    PYAUTOGUI_AVAILABLE = False


def read_credentials():
    email = "ronnie.hudson43@gmail.com"
    password = "55netsdowin7HHY%"
    return email, password


def wait_for_page_load(driver, timeout=10):
    """Wait for page to load completely"""
    try:
        WebDriverWait(driver, timeout).until(
            lambda d: d.execute_script('return document.readyState') == 'complete'
        )
        return True
    except TimeoutException:
        print("Page load timeout")
        return False


def wait_for_download_to_start(download_dir, timeout=30, initial_files=None):
    """Wait for a new file to appear in the download directory"""
    print(f"    ⏳ Monitoring download directory for new files...")

    # Get initial file list if not provided
    if initial_files is None:
        initial_files = set(os.listdir(download_dir)) if os.path.exists(download_dir) else set()

    start_time = time.time()
    while time.time() - start_time < timeout:
        time.sleep(1)
        current_files = set(os.listdir(download_dir)) if os.path.exists(download_dir) else set()
        new_files = current_files - initial_files

        # Check for new files (including .crdownload for Chrome)
        if new_files:
            print(f"    ✓ Download started: {', '.join(new_files)}")
            return True

    print(f"    ⚠ No new download detected within {timeout} seconds")
    return False


def wait_for_download_to_complete(download_dir, timeout=300):
    """Wait for all downloads to complete (no .crdownload or .tmp files)"""
    print(f"    ⏳ Waiting for download to complete (max {timeout}s)...")

    start_time = time.time()
    while time.time() - start_time < timeout:
        time.sleep(2)

        if os.path.exists(download_dir):
            files = os.listdir(download_dir)
            # Check if there are any incomplete downloads
            incomplete = [f for f in files if f.endswith('.crdownload') or f.endswith('.tmp') or f.endswith('.part')]

            if not incomplete:
                print(f"    ✓ Download completed successfully")
                return True
            else:
                elapsed = int(time.time() - start_time)
                if elapsed % 10 == 0:  # Print every 10 seconds to avoid spam
                    print(f"    → Still downloading ({elapsed}s): {incomplete[0]}...")

        time.sleep(1)

    print(f"    ⚠ Download did not complete within {timeout} seconds")
    return False


def try_click_dropdown(driver, xpath, attempt_num):
    """
    Try to click the dropdown using multiple strategies:
    1. Standard Selenium Click
    2. JavaScript Click
    3. ActionChains Click
    4. PyAutoGUI Click (fallback if available)
    """
    print(f"    → Attempting to open dropdown (attempt {attempt_num})...")

    # Ensure modal and spinner are gone before any click
    try:
        driver.execute_script("""
            var modal = document.getElementById('kt_modal_download');
            if (modal && modal.style.display !== 'none') {
                modal.style.display = 'none';
                modal.classList.remove('show');
            }
            var spinner = document.getElementById('cover-spin');
            if (spinner) spinner.style.display = 'none';
        """)
    except:
        pass

    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
    except:
        print("      ✗ Element not found for clicking")
        return False

    # Strategy 1: Standard Search & Click
    try:
        # print("      [1] Trying standard click...")
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
        time.sleep(0.5)
        # Re-find element to avoid stale reference after scroll
        element = driver.find_element(By.XPATH, xpath)
        element.click()
        return True
    except Exception as e:
        pass

    # Strategy 2: JavaScript Click (usually most robust)
    try:
        # print("      [2] Trying JavaScript click...")
        driver.execute_script("arguments[0].click();", element)
        return True
    except Exception as e:
        pass

    # Strategy 3: ActionChains
    try:
        print("      [3] Trying ActionChains click...")
        actions = ActionChains(driver)
        actions.move_to_element(element).click().perform()
        return True
    except Exception as e:
        print(f"      ✗ ActionChains click failed: {str(e)[:50]}")

    # Strategy 4: PyAutoGUI (Physical Mouse Click)
    if PYAUTOGUI_AVAILABLE:
        try:
            print("      [4] Trying PyAutoGUI physical click...")
            # Get element position relative to viewport
            rect = driver.execute_script("return arguments[0].getBoundingClientRect();", element)
            
            nav_height = driver.execute_script("return window.outerHeight - window.innerHeight;")
            if nav_height <= 0: nav_height = 110
            
            click_x = int(rect['x'] + rect['width'] / 2)
            click_y = int(rect['y'] + rect['height'] / 2 + nav_height)
            
            pyautogui.moveTo(click_x, click_y, duration=0.5)
            pyautogui.click()
            return True
        except Exception as e:
            print(f"      ✗ PyAutoGUI click failed: {str(e)[:50]}")
    
    return False


def get_xpath_config(db_choice, data_type):
    """Get XPath configuration based on database and data type"""

    # Database 1 (US Business Leads)
    if db_choice == "1":
        if data_type == "1":  # Emails
            return {
                "dropdown": "/html/body/form/div[3]/div/div/div[2]/div[2]/div/div/div[1]/div[1]/div[2]/div[1]/div/span/span[1]/span/span[1]",
                "leads_count": "/html/body/form/div[3]/div/div/div[2]/div[2]/div/div/div[2]/div[3]/div/div[1]/h1/span",
                "download_button": "/html/body/form/div[3]/div/div/div[2]/div[2]/div/div/div[2]/div[3]/div/div[2]/a[1]"
            }
        else:  # Phone Numbers
            return {
                "dropdown": "/html/body/form/div[3]/div/div/div[2]/div[2]/div/div/div[1]/div[1]/div[2]/div[1]/div/span/span[1]/span",
                "leads_count": "/html/body/form/div[3]/div/div/div[2]/div[2]/div/div/div[2]/div[3]/div/div[1]/h1/span",
                "download_button": "/html/body/form/div[3]/div/div/div[2]/div[2]/div/div/div[2]/div[3]/div/div[2]/a[1]"
            }

    # Database 2 (US New Businesses)
    elif db_choice == "2":
        if data_type == "1":  # Emails
            return {
                "dropdown": "/html/body/form/div[3]/div/div/div[2]/div[2]/div/div/div[1]/div[1]/div[2]/div[1]/div/span/span[1]/span/span[1]",
                "leads_count": "/html/body/form/div[3]/div/div/div[2]/div[2]/div/div/div[2]/div[3]/div/div[1]/h1/span",
                "download_button": "/html/body/form/div[3]/div/div/div[2]/div[2]/div/div/div[2]/div[3]/div/div[2]/a[1]"
            }
        else:  # Phone Numbers
            return {
                "dropdown": "/html/body/form/div[3]/div/div/div[2]/div[2]/div/div/div[1]/div[1]/div[2]/div[1]/div/span/span[1]/span/span[1]",
                "leads_count": "/html/body/form/div[3]/div/div/div[2]/div[2]/div/div/div[2]/div[3]/div/div[1]/h1/span",
                "download_button": "/html/body/form/div[3]/div/div/div[2]/div[2]/div/div/div[2]/div[3]/div/div[2]/a[1]"
            }

    # Database 3 (Timeshare Owners)
    elif db_choice == "3":
        if data_type == "1":  # Emails
            return {
                "dropdown": "/html/body/form/div[3]/div/div/div[2]/div[2]/div/div/div[1]/div/div[2]/div[1]/div/span/span[1]/span/span[1]",
                "leads_count": "/html/body/form/div[3]/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div[1]/h1/span",
                "download_button": "/html/body/form/div[3]/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div[2]/a[1]"
            }
        else:  # Phone Numbers
            return {
                "dropdown": "/html/body/form/div[3]/div/div/div[2]/div[2]/div/div/div[1]/div/div[2]/div[1]/div/span/span[1]/span/span[1]",
                "leads_count": "/html/body/form/div[3]/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div[1]/h1/span",
                "download_button": "/html/body/form/div[3]/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div[2]/a[1]"
            }

    # Database 4 (High Tech Leaders)
    elif db_choice == "4":
        if data_type == "1":  # Emails
            return {
                "dropdown": "/html/body/form/div[3]/div/div/div[2]/div[2]/div/div/div[1]/div[1]/div[2]/div[1]/div/span/span[1]/span/span[1]",
                "leads_count": "/html/body/form/div[3]/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div[1]/h1/span",
                "download_button": "/html/body/form/div[3]/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div[2]/a[1]"
            }
        else:  # Phone Numbers
            return {
                "dropdown": "/html/body/form/div[3]/div/div/div[2]/div[2]/div/div/div[1]/div[1]/div[2]/div[1]/div/span/span[1]/span/span[1]",
                "leads_count": "/html/body/form/div[3]/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div[1]/h1/span",
                "download_button": "/html/body/form/div[3]/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div[2]/a[1]"
            }


def get_user_selections():
    """Get database, data type, and state selections from user"""
    print("\n" + "=" * 60)
    print("DATABASE SELECTION")
    print("=" * 60)
    print("1. US Business Leads")
    print("2. US New Businesses")
    print("3. Timeshare Owners")
    print("4. High Tech Leaders")
    print("=" * 60)

    db_choice = input("Select database (1-4): ").strip()

    print("\n" + "=" * 60)
    print("DATA TYPE")
    print("=" * 60)
    print("1. Emails")
    print("2. Phone Numbers")
    print("=" * 60)

    data_type = input("Select data type (1-2): ").strip()

    # URL mapping
    url_map = {
        "1": {
            "1": "https://crm.leadscampus.com/businessmailingleads.aspx",
            "2": "https://crm.leadscampus.com/businessleads.aspx"
        },
        "2": {
            "1": "https://crm.leadscampus.com/businessmailingleads.aspx?specialcategory=NewBusiness",
            "2": "https://crm.leadscampus.com/businessleads.aspx?specialCategory=NewBusiness"
        },
        "3": {
            "1": "https://crm.leadscampus.com/timeshareownersdatabase.aspx?em=1",
            "2": "https://crm.leadscampus.com/timeshareownersdatabase.aspx"
        },
        "4": {
            "1": "https://crm.leadscampus.com/hightechleadersdatabase.aspx?em=1",
            "2": "https://crm.leadscampus.com/hightechleadersdatabase.aspx"
        }
    }

    db_names = {
        "1": "US Business Leads",
        "2": "US New Businesses",
        "3": "Timeshare Owners",
        "4": "High Tech Leaders"
    }

    data_names = {"1": "Emails", "2": "Phone Numbers"}

    if db_choice not in url_map or data_type not in data_names:
        print("\n✗ Invalid selection!")
        return None, None, None, None, None, None

    target_url = url_map[db_choice][data_type]
    print(f"\n✓ Selected: {db_names[db_choice]} - {data_names[data_type]}")
    print(f"✓ Target URL: {target_url}")

    # Get XPath configuration (now includes dropdown xpath)
    xpath_config = get_xpath_config(db_choice, data_type)

    # State selection
    print("\n" + "=" * 60)
    print("STATE SELECTION")
    print("=" * 60)
    print("Available states: Alabama, Alaska, Arizona, Arkansas, California,")
    print("Colorado, Connecticut, Delaware, District of Columbia, Florida,")
    print("Georgia, Hawaii, Idaho, Illinois, Indiana, Iowa, Kansas, Kentucky,")
    print("Louisiana, Maine, Maryland, Massachusetts, Michigan, Minnesota,")
    print("Mississippi, Missouri, Montana, Nebraska, Nevada, New Hampshire,")
    print("New Jersey, New Mexico, New York, North Carolina, North Dakota,")
    print("Ohio, Oklahoma, Oregon, Pennsylvania, Rhode Island, South Carolina,")
    print("South Dakota, Tennessee, Texas, Utah, Vermont, Virginia, Washington,")
    print("West Virginia, Wisconsin, Wyoming")
    print("=" * 60)
    print("\nOptions:")
    print("  - Type 'all' to download all states")
    print("  - Type a state name (e.g., 'Texas') for a specific state")
    print("=" * 60)

    user_input = input("\nYour choice: ").strip().lower()

    download_all = (user_input == 'all')
    selected_state = None if download_all else user_input.title()

    if download_all:
        print(f"\n✓ Will download data for ALL states")
    else:
        print(f"\n✓ Will download data for: {selected_state}")

    return target_url, db_names[db_choice], download_all, selected_state, db_choice, xpath_config


def main():
    # Get user selections
    result = get_user_selections()
    if result[0] is None:
        return

    target_url, db_name, download_all, selected_state, db_choice, xpath_config = result

    # Read credentials
    email, password = read_credentials()
    if not email or not password:
        print("Failed to read credentials")
        return

    print(f"\nEmail: {email}")
    print("Password: ****")

    # Set up Chrome with download directory
    chrome_options = webdriver.ChromeOptions()
    download_dir = os.path.join(os.getcwd(), "downloads")
    os.makedirs(download_dir, exist_ok=True)

    prefs = {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    }
    chrome_options.add_experimental_option("prefs", prefs)

    # Add options to prevent timeout issues
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--start-maximized")

    print(f"✓ Download directory: {download_dir}")
    print(f"\nInitializing Chrome WebDriver...")

    try:
        # Try with WebDriver Manager first
        try:
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=chrome_options)
        except:
            # Fallback to simple initialization
            driver = webdriver.Chrome(options=chrome_options)
        print("✓ Chrome WebDriver initialized successfully\n")
    except Exception as e:
        print(f"✗ Failed to initialize Chrome WebDriver: {e}")
        print("\nTroubleshooting tips:")
        print("1. Make sure Chrome browser is installed")
        print("2. Try: pip install --upgrade selenium")
        print("3. Check if Chrome is already running and close it")
        input("\nPress Enter to exit...")
        return

    driver.maximize_window()

    try:
        # LOGIN
        print("[1] Navigating to login page...")
        try:
            driver.get("https://auth.leadscampus.com/")
        except Exception as nav_error:
            print(f"✗ Navigation error: {nav_error}")
            print("\nPossible issues:")
            print("- Internet connection problem")
            print("- Website is down")
            raise

        wait_for_page_load(driver, timeout=10)
        time.sleep(3)

        print("[2] Checking for iframes...")
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        if iframes:
            print(f"   Found {len(iframes)} iframe(s), switching to first one...")
            driver.switch_to.frame(0)
            time.sleep(1)

        print("[3] Waiting for email field...")
        try:
            email_field = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/div/div/div[2]/div/div/form/input[1]"))
            )
            print("[4] Entering email...")
            email_field.clear()
            email_field.send_keys(email)
        except:
            print(f"   ✗ XPath failed, trying alternative selectors...")
            try:
                email_field = driver.find_element(By.CSS_SELECTOR, "input[type='email']")
                email_field.clear()
                email_field.send_keys(email)
            except:
                email_field = driver.find_element(By.NAME, "email")
                email_field.clear()
                email_field.send_keys(email)

        print("[5] Entering password...")
        try:
            password_field = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/div/div/div[2]/div/div/form/input[2]"))
            )
            password_field.clear()
            password_field.send_keys(password)
        except:
            try:
                password_field = driver.find_element(By.CSS_SELECTOR, "input[type='password']")
                password_field.clear()
                password_field.send_keys(password)
            except:
                password_field = driver.find_element(By.NAME, "password")
                password_field.clear()
                password_field.send_keys(password)

        print("[6] Clicking login button...")
        try:
            login_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/div[2]/div/div/form/div[3]/input"))
            )
            login_button.click()
        except:
            try:
                login_button = driver.find_element(By.CSS_SELECTOR, "input[type='submit']")
                login_button.click()
            except:
                login_button = driver.find_element(By.XPATH, "//button[@type='submit']")
                login_button.click()

        driver.switch_to.default_content()

        print("[7] Waiting for login to complete...")
        # optimized wait as requested: checks for home page URL or max 5s
        try:
             WebDriverWait(driver, 5).until(
                EC.url_contains("Default.aspx")
            )
             print("✓ Reached home page (Default.aspx)")
        except:
            print("⚠ 5s timeout reached or not on Default.aspx, proceeding anyway...")

        # NAVIGATE TO SELECTED DATABASE
        print(f"\n[8] Navigating to {db_name} page...")
        driver.get(target_url)
        wait_for_page_load(driver, timeout=10)
        time.sleep(2)
        print("✓ Page loaded successfully")

        # Hide chat widget
        try:
            driver.execute_script("""
                var chatWidgets = document.querySelectorAll('iframe[title*="chat"], iframe[title*="Chat"], iframe[id*="chat"]');
                for (var i = 0; i < chatWidgets.length; i++) {
                    chatWidgets[i].style.display = 'none';
                    chatWidgets[i].style.visibility = 'hidden';
                }
            """)
            print("✓ Hidden chat widget iframe")
        except:
            pass

        # Open state dropdown with correct XPath from config
        print("\n[9] Opening state dropdown...")
        try:
             try_click_dropdown(driver, xpath_config["dropdown"], 1)
        except:
            state_dropdown = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, xpath_config["dropdown"]))
            )
            state_dropdown.click()
            
        time.sleep(1)
        print("✓ State dropdown opened")

        # Get states list
        print("\n[10] Fetching states list...")
        states_container = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "ul.select2-results__options"))
        )

        state_items = states_container.find_elements(By.TAG_NAME, "li")
        state_names = []
        for state in state_items:
            state_name = state.text.strip()
            if state_name and state_name != "-- Select State --":
                state_names.append(state_name)

        print(f"\n✓ Found {len(state_names)} states available")

        # Determine states to process
        states_to_process = []

        if download_all:
            states_to_process = state_names
            print(f"✓ Will process all {len(state_names)} states")
            print("=" * 50)
            for idx, st in enumerate(state_names, 1):
                print(f"{idx}. {st}")
            print("=" * 50)
        else:
            if selected_state in state_names:
                states_to_process = [selected_state]
                print(f"✓ Will process ONLY: {selected_state}")
            else:
                print(f"✗ ERROR: '{selected_state}' not found in available states!")
                input("\nPress Enter to close...")
                driver.quit()
                return

        # Close dropdown
        try:
            driver.find_element(By.TAG_NAME, "body").click()
            time.sleep(0.5)
        except:
            pass

        # Download process
        print(f"\n[11] Starting download process for {len(states_to_process)} state(s)...\n")
        successful_downloads = 0
        skipped_states = 0

        for idx, state_name in enumerate(states_to_process, 1):
            try:
                print(f"\n[{idx}/{len(states_to_process)}] Processing: {state_name}")

                # Hide chat widget
                try:
                    driver.execute_script("""
                        var chatWidgets = document.querySelectorAll('iframe[title*="chat"], iframe[title*="Chat"], iframe[id*="chat"]');
                        for (var i = 0; i < chatWidgets.length; i++) {
                            chatWidgets[i].style.display = 'none';
                            chatWidgets[i].style.visibility = 'hidden';
                        }
                    """)
                except:
                    pass

                # Ensure modal is closed
                try:
                    modal = driver.find_element(By.ID, "kt_modal_download")
                    if modal.is_displayed():
                        print(f"    ⚠ Modal still open, closing it...")
                        driver.execute_script("""
                            var modal = document.getElementById('kt_modal_download');
                            if (modal) {
                                modal.style.display = 'none';
                                modal.classList.remove('show');
                                var backdrop = document.querySelector('.modal-backdrop');
                                if (backdrop) backdrop.remove();
                            }
                        """)
                        time.sleep(1)
                except:
                    pass

                # Wait for loading spinner to disappear
                try:
                    WebDriverWait(driver, 10).until(
                        EC.invisibility_of_element_located((By.ID, "cover-spin"))
                    )
                except:
                    try:
                        driver.execute_script("document.getElementById('cover-spin').style.display = 'none';")
                    except:
                        pass

                # Close dropdown if open
                try:
                    driver.find_element(By.TAG_NAME, "body").click()
                    time.sleep(0.5)
                except:
                    pass

                # Determine correct dropdown XPath from config
                dropdown_xpath = xpath_config["dropdown"]

                # Scroll to dropdown
                try:
                    state_dropdown_element = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, dropdown_xpath))
                    )
                    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});",
                                          state_dropdown_element)
                    time.sleep(0.5)
                except:
                    pass

                # Open dropdown with retry logic using NEW FUNCTION
                dropdown_opened = False
                max_retries = 5
                
                # Check if we successfully opened it using our multi-strategy approach
                for attempt in range(max_retries):
                     if try_click_dropdown(driver, dropdown_xpath, attempt + 1):
                         # Verify dropdown opened
                        try:
                            WebDriverWait(driver, 5).until(
                                EC.presence_of_element_located((By.CSS_SELECTOR, "ul.select2-results__options"))
                            )
                            dropdown_opened = True
                            print(f"    ✓ Dropdown opened successfully")
                            break
                        except:
                            print(f"    ⚠ Click seemed successful but dropdown list did not appear. Retrying...")
                            time.sleep(1)
                     else:
                        print(f"    ⚠ Click attempt failed. Retrying...")
                        time.sleep(2)

                if not dropdown_opened:
                    raise Exception("Dropdown did not open after multiple robust attempts")

                # Select state
                states_container = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "ul.select2-results__options"))
                )
                state_option = states_container.find_element(By.XPATH, f".//li[contains(text(), '{state_name}')]")
                state_option.click()
                print(f"    ✓ Selected: {state_name}")

                # Wait for loading spinner
                try:
                    WebDriverWait(driver, 25).until(
                        EC.invisibility_of_element_located((By.ID, "cover-spin"))
                    )
                    print(f"    ✓ Page loaded (spinner disappeared)")
                except:
                    try:
                        driver.execute_script("document.getElementById('cover-spin').style.display = 'none';")
                        print(f"    ✓ Forced spinner to hide")
                    except:
                        pass

                # Wait for data to load
                time.sleep(3)
                print(f"    → Current URL: {driver.current_url}")

                # Check lead count using correct XPath with retry logic
                try:
                    print(f"    ⏳ Waiting for leads count to update...")
                    leads_text = "0 Leads"
                    max_leads_wait = 20  # Wait up to 20 seconds for leads to load
                    leads_start_time = time.time()
                    
                    while time.time() - leads_start_time < max_leads_wait:
                        try:
                            leads_element = WebDriverWait(driver, 5).until(
                                EC.presence_of_element_located((By.XPATH, xpath_config["leads_count"]))
                            )
                            leads_text = leads_element.text.strip()
                            
                            # Check if valid number found
                            numbers = re.findall(r'[\d,]+', leads_text)
                            if numbers:
                                current_count = int(numbers[0].replace(',', ''))
                                if current_count > 0:
                                    break # Found valid leads!
                        except:
                            pass
                            
                        time.sleep(1)
                    
                    print(f"    → Leads text: {leads_text}")

                    numbers = re.findall(r'[\d,]+', leads_text)
                    if numbers:
                        lead_count = int(numbers[0].replace(',', ''))
                        if lead_count == 0:
                            print(f"    ⚠ Skipping {state_name} - 0 leads found")
                            skipped_states += 1
                            continue
                        else:
                            print(f"    ✓ Found {lead_count:,} leads for {state_name}")
                    else:
                        if "0 leads" in leads_text.lower():
                            print(f"    ⚠ Skipping {state_name} - 0 leads found")
                            skipped_states += 1
                            continue
                        else:
                            print(f"    ✓ Proceeding with download for {state_name}")
                except Exception as e:
                    print(f"    ⚠ Could not check leads count: {str(e)[:80]}")
                    print(f"    → Proceeding anyway...")

                # Click download button using correct XPath
                try:
                    download_button = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, xpath_config["download_button"]))
                    )
                    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", download_button)
                    time.sleep(0.5)
                    driver.execute_script("arguments[0].click();", download_button)
                    print(f"    ✓ Clicked download button")
                except Exception as e:
                    print(f"    ✗ Could not click download button: {str(e)[:80]}")
                    skipped_states += 1
                    continue

                # Wait for modal
                print(f"    ⏳ Waiting for modal to appear...")
                try:
                    WebDriverWait(driver, 15).until(
                        EC.presence_of_element_located((By.ID, "kt_modal_download"))
                    )
                    time.sleep(2)
                    print(f"    ✓ Modal appeared")
                except:
                    print(f"    ⚠ Modal may not have appeared, proceeding anyway...")
                    time.sleep(3)

                # Capture files BEFORE clicking "Here" to track the new download accurately
                initial_download_files = set(os.listdir(download_dir)) if os.path.exists(download_dir) else set()

                # Click "Here" link to start download
                here_clicked = False
                max_here_retries = 3
                for here_attempt in range(max_here_retries):
                    try:
                        here_link = WebDriverWait(driver, 10).until(
                            EC.element_to_be_clickable(
                                (By.XPATH, "/html/body/form/div[3]/div/div/div[2]/div[3]/div/div/div[2]/div/span/a"))
                        )
                        driver.execute_script("arguments[0].click();", here_link)
                        print(f"    ✓ Clicked 'Here' link to initiate download")
                        here_clicked = True
                        break
                    except Exception as e:
                        if here_attempt < max_here_retries - 1:
                            print(f"    ⚠ Could not click 'Here' link, retrying...")
                            time.sleep(2)
                            continue
                        else:
                            print(f"    ✗ Could not click 'Here' link after {max_here_retries} attempts")
                            skipped_states += 1

                if not here_clicked:
                    continue

                # Wait for the download to actually start and complete
                # Pass initial_download_files to ensure we catch it even if it started instantly
                download_started = wait_for_download_to_start(download_dir, timeout=30, initial_files=initial_download_files)

                if download_started:
                    # UPDATED timeout to 300s via default arg change
                    download_completed = wait_for_download_to_complete(download_dir, timeout=300)

                    if download_completed:
                        successful_downloads += 1
                        print(f"    ✓ Download successful for {state_name}")

                        # RENAME FILE LOGIC
                        try:
                            # Check files again
                            final_files = set(os.listdir(download_dir)) if os.path.exists(download_dir) else set()
                            new_files = final_files - initial_download_files
                            
                            # Filter out partials just in case (though wait_for_download_to_complete should have handled it)
                            valid_new_files = [f for f in new_files if not (f.endswith('.crdownload') or f.endswith('.tmp') or f.endswith('.part'))]
                            
                            if len(valid_new_files) == 1:
                                original_filename = valid_new_files[0]
                                # Create safe state name (Use underscore for spaces)
                                safe_state_name = state_name.replace(" ", "_")
                                
                                new_filename = f"{safe_state_name}_{original_filename}"
                                
                                old_path = os.path.join(download_dir, original_filename)
                                new_path = os.path.join(download_dir, new_filename)
                                
                                # Overwrite if exists
                                if os.path.exists(new_path):
                                    try:
                                        os.remove(new_path)
                                    except:
                                        pass
                                
                                os.rename(old_path, new_path)
                                print(f"    ✓ Renamed file to: {new_filename}")
                            elif len(valid_new_files) > 1:
                                print(f"    ⚠ Multiple new files found, skipping rename to avoid confusion: {valid_new_files}")
                            else:
                                print(f"    ⚠ Could not identify the new file for renaming")
                                
                        except Exception as rename_error:
                             print(f"    ⚠ Rename failed: {rename_error}")

                    else:
                        print(f"    ⚠ Download may not have completed for {state_name}")
                        skipped_states += 1
                else:
                    print(f"    ⚠ Download did not start for {state_name}")
                    skipped_states += 1

                # Close modal
                try:
                    close_button = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable(
                            (By.XPATH, "/html/body/form/div[3]/div/div/div[2]/div[3]/div/div/div[3]/button"))
                    )
                    driver.execute_script("arguments[0].click();", close_button)
                    time.sleep(1)
                    print(f"    ✓ Closed modal")
                except:
                    driver.execute_script("""
                        var modal = document.getElementById('kt_modal_download');
                        if (modal) {
                            modal.style.display = 'none';
                            modal.classList.remove('show');
                            var backdrop = document.querySelector('.modal-backdrop');
                            if (backdrop) backdrop.remove();
                        }
                    """)

                # Wait before next iteration
                print(f"    ⏳ Waiting before next state...")
                time.sleep(3)

            except Exception as e:
                print(f"    ✗ Error with {state_name}: {str(e)[:100]}")
                skipped_states += 1
                continue

        # Summary
        print("\n" + "=" * 50)
        print("✓ All downloads completed!")
        print(f"✓ Successful downloads: {successful_downloads}")
        print(f"⚠ Skipped states: {skipped_states}")
        print(f"✓ Total states processed: {len(states_to_process)}")
        print("=" * 50)

        input("\nPress Enter to close the browser...")

    except Exception as e:
        print(f"\n✗ Error occurred: {e}")
        import traceback
        traceback.print_exc()

        # Try to save page source only if driver is still accessible
        try:
            print("\n[DEBUG] Saving page source for inspection...")
            with open("page_source.html", "w", encoding="utf-8") as f:
                f.write(driver.page_source)
            print("✓ Page source saved to 'page_source.html'")
        except Exception as save_error:
            print(f"⚠ Could not save page source: {save_error}")

        input("\nPress Enter to close the browser...")

    finally:
        try:
            driver.quit()
            print("\nBrowser closed.")
        except:
            print("\nBrowser was already closed.")


if __name__ == "__main__":
    main()