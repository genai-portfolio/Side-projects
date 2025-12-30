from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import os
import re


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


def wait_for_leads_to_load(driver, max_wait=60, check_interval=10):
    """Wait for leads count to be populated and stable with interval checks"""
    print(f"    ⏳ Waiting for leads to load (max {max_wait}s, checking every {check_interval}s)...")

    last_count = None
    stable_count = 0
    start_time = time.time()
    check_number = 0

    while time.time() - start_time < max_wait:
        check_number += 1
        elapsed = int(time.time() - start_time)
        print(f"    → Check #{check_number} at {elapsed}s...")

        try:
            # Wait for loading spinner to disappear
            try:
                WebDriverWait(driver, 3).until(
                    EC.invisibility_of_element_located((By.ID, "cover-spin"))
                )
                print(f"       ✓ Loading spinner cleared")
            except:
                print(f"       ⏳ Spinner still active or not found")

            # Try to get the leads count
            leads_element = driver.find_element(By.XPATH,
                                                "/html/body/form/div[3]/div/div/div[2]/div[2]/div/div/div[2]/div[3]/div/div[1]/h1/span")
            leads_text = leads_element.text.strip()

            # Extract number from text
            numbers = re.findall(r'[\d,]+', leads_text)
            if numbers:
                current_count = numbers[0]

                # Check if count is stable (same for 2 consecutive checks)
                if current_count == last_count:
                    stable_count += 1
                    print(f"       → Count stable: {current_count} (match #{stable_count})")
                    if stable_count >= 2:
                        lead_count = int(current_count.replace(',', ''))
                        print(f"    ✓ Leads loaded: {lead_count:,}")
                        return lead_count
                else:
                    stable_count = 0
                    last_count = current_count
                    print(f"       → Count changed to: {current_count}")
            else:
                print(f"       ⏳ No count found yet")

        except Exception as e:
            print(f"       ⚠ Could not read leads: {str(e)[:50]}")

        # Wait for the check interval before next check
        if time.time() - start_time < max_wait:
            time.sleep(check_interval)

    print(f"    ⚠ Timeout after {max_wait}s")
    return None


def wait_for_download_button(driver, max_wait=30, check_interval=5):
    """Wait for download button to be clickable with interval checks"""
    print(f"    ⏳ Waiting for download button (max {max_wait}s, checking every {check_interval}s)...")

    start_time = time.time()
    check_number = 0

    while time.time() - start_time < max_wait:
        check_number += 1
        elapsed = int(time.time() - start_time)
        print(f"    → Check #{check_number} at {elapsed}s...")

        try:
            # Check if button exists and is visible
            download_button = driver.find_element(By.XPATH,
                                                  "/html/body/form/div[3]/div/div/div[2]/div[2]/div/div/div[2]/div[3]/div/div[2]/a[1]")

            # Check if button is displayed and enabled
            if download_button.is_displayed() and download_button.is_enabled():
                # Additional check: make sure it's not disabled by CSS
                disabled_attr = download_button.get_attribute("disabled")
                class_attr = download_button.get_attribute("class") or ""

                if not disabled_attr and "disabled" not in class_attr.lower():
                    print(f"    ✓ Download button ready")
                    return download_button
                else:
                    print(f"       ⏳ Button disabled via attributes/CSS")
            else:
                print(f"       ⏳ Button not displayed or enabled")

        except Exception as e:
            print(f"       ⚠ Button not found: {str(e)[:40]}")

        # Wait for the check interval before next check
        if time.time() - start_time < max_wait:
            time.sleep(check_interval)

    print(f"    ⚠ Download button timeout after {max_wait}s")
    return None


def main():
    # Read credentials
    email, password = read_credentials()
    if not email or not password:
        print("Failed to read credentials")
        return

    print(f"Email: {email}")
    print("Password: ****\n")

    # DATABASE SELECTION
    print("=" * 60)
    print("DATABASE SELECTION")
    print("=" * 60)
    print("1. US Business Leads")
    print("2. US New Businesses")
    print("3. Timeshare Owners")
    print("4. High Tech Leaders")
    print("=" * 60)

    db_choice = input("Select database (1-4): ").strip()

    # DATA TYPE SELECTION
    print("\n" + "=" * 60)
    print("DATA TYPE")
    print("=" * 60)
    print("1. Emails")
    print("2. Phone Numbers")
    print("=" * 60)

    data_type = input("Select data type (1-2): ").strip()

    # Determine URL based on selections
    url_map = {
        "1": {  # US Business Leads
            "1": "https://crm.leadscampus.com/businessmailingleads.aspx",
            "2": "https://crm.leadscampus.com/businessleads.aspx"
        },
        "2": {  # US New Businesses
            "1": "https://crm.leadscampus.com/businessmailingleads.aspx?specialcategory=NewBusiness",
            "2": "https://crm.leadscampus.com/businessleads.aspx?specialCategory=NewBusiness"
        },
        "3": {  # Timeshare Owners
            "1": "https://crm.leadscampus.com/timeshareownersdatabase.aspx?em=1",
            "2": "https://crm.leadscampus.com/timeshareownersdatabase.aspx"
        },
        "4": {  # High Tech Leaders
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
        return

    target_url = url_map[db_choice][data_type]
    print(f"\n✓ Selected: {db_names[db_choice]} - {data_names[data_type]}")
    print(f"✓ Target URL: {target_url}")

    # STATE SELECTION
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

    user_state_input = input("\nEnter state name (e.g., 'texas') or press ENTER for all: ").strip()

    selected_state = None
    download_all = False

    if user_state_input:
        selected_state = user_state_input.capitalize()
        print(f"✓ Will download data for: {selected_state}")
    else:
        download_all = True
        print(f"✓ Will download data for all states")

    print("=" * 60 + "\n")

    # Set up Chrome options
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

    print(f"✓ Download directory: {download_dir}")

    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()

    try:
        # LOGIN
        print("\n[1] Navigating to login page...")
        driver.get("https://auth.leadscampus.com/")
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
            print(f"   ✗ XPath failed, trying alternatives...")
            email_field = driver.find_element(By.CSS_SELECTOR, "input[type='email']")
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
            password_field = driver.find_element(By.CSS_SELECTOR, "input[type='password']")
            password_field.clear()
            password_field.send_keys(password)

        print("[6] Clicking login button...")
        try:
            login_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/div[2]/div/div/form/div[3]/input"))
            )
            login_button.click()
        except:
            login_button = driver.find_element(By.CSS_SELECTOR, "input[type='submit']")
            login_button.click()

        driver.switch_to.default_content()

        print("[7] Waiting for login to complete...")
        time.sleep(2)
        if wait_for_page_load(driver, timeout=4):
            print("✓ Page loaded successfully")
        time.sleep(2)

        # NAVIGATE TO SELECTED DATABASE
        print(f"\n[8] Navigating to {db_names[db_choice]} page...")
        driver.get(target_url)
        wait_for_page_load(driver, timeout=10)
        time.sleep(2)
        print("✓ Page loaded successfully")

        # Hide chat widget
        try:
            driver.execute_script("""
                var chatWidgets = document.querySelectorAll('iframe[title*="chat"]');
                for (var i = 0; i < chatWidgets.length; i++) {
                    chatWidgets[i].style.display = 'none';
                }
            """)
        except:
            pass

        # Open state dropdown
        print("\n[9] Opening state dropdown...")
        state_dropdown = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH,
                                        "/html/body/form/div[3]/div/div/div[2]/div[2]/div/div/div[1]/div[1]/div[2]/div[1]/div/span/span[1]/span"))
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
            print(f"✓ Will process all {len(state_names)} states\n")
        else:
            if selected_state in state_names:
                states_to_process = [selected_state]
                print(f"✓ Will process ONLY: {selected_state}\n")
            else:
                print(f"✗ ERROR: '{selected_state}' not found!")
                input("\nPress Enter to close...")
                driver.quit()
                return

        driver.find_element(By.TAG_NAME, "body").click()
        time.sleep(0.5)

        successful_downloads = 0
        skipped_states = 0

        print(f"[11] Starting download for {len(states_to_process)} state(s)...\n")

        for idx, state_name in enumerate(states_to_process, 1):
            try:
                print(f"[{idx}/{len(states_to_process)}] Processing: {state_name}")

                # Open dropdown
                print(f"    → Opening dropdown...")
                state_dropdown = WebDriverWait(driver, 15).until(
                    EC.element_to_be_clickable((By.XPATH,
                                                "/html/body/form/div[3]/div/div/div[2]/div[2]/div/div/div[1]/div[1]/div[2]/div[1]/div/span/span[1]/span"))
                )
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", state_dropdown)
                time.sleep(0.5)
                state_dropdown.click()
                time.sleep(1)

                WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "ul.select2-results__options"))
                )
                print(f"    ✓ Opened dropdown")

                # Select state
                states_container = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "ul.select2-results__options"))
                )
                state_option = states_container.find_element(By.XPATH, f".//li[contains(text(), '{state_name}')]")
                print(f"    → Found '{state_name}'")
                state_option.click()
                print(f"    ✓ Clicked on: {state_name}")
                time.sleep(2)

                # NEW: Wait for leads to load with smart timeout
                lead_count = wait_for_leads_to_load(driver, max_wait=60)

                if lead_count is None:
                    print(f"    ⚠ Skipping - could not load leads\n")
                    skipped_states += 1
                    continue

                if lead_count == 0:
                    print(f"    ⚠ Skipping - 0 leads\n")
                    skipped_states += 1
                    continue

                # NEW: Wait for download button to be ready
                download_button = wait_for_download_button(driver, max_wait=30)

                if download_button is None:
                    print(f"    ✗ Download button not available\n")
                    skipped_states += 1
                    continue

                # Download
                try:
                    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", download_button)
                    time.sleep(0.5)
                    driver.execute_script("arguments[0].click();", download_button)
                    print(f"    ✓ Clicked download")
                    time.sleep(8)
                except Exception as e:
                    print(f"    ✗ Could not click download: {str(e)[:50]}\n")
                    skipped_states += 1
                    continue

                # Click Here
                try:
                    here_link = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH,
                                                    "/html/body/form/div[3]/div/div/div[2]/div[3]/div/div/div[2]/div/span/a"))
                    )
                    driver.execute_script("arguments[0].click();", here_link)
                    print(f"    ✓ Download started")
                    successful_downloads += 1
                    time.sleep(3)
                except:
                    print(f"    ✗ Could not start download\n")
                    skipped_states += 1
                    continue

                # Close modal
                try:
                    close_button = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH,
                                                    "/html/body/form/div[3]/div/div/div[2]/div[3]/div/div/div[3]/button"))
                    )
                    driver.execute_script("arguments[0].click();", close_button)
                    time.sleep(1)
                except:
                    driver.execute_script("""
                        var modal = document.getElementById('kt_modal_download');
                        if (modal) modal.style.display = 'none';
                    """)

                print(f"    ✓ Completed\n")
                time.sleep(2)

            except Exception as e:
                print(f"    ✗ Error: {str(e)[:100]}\n")
                skipped_states += 1

        print("=" * 60)
        print(f"✓ Process completed!")
        print(f"✓ Downloaded: {successful_downloads}")
        print(f"⚠ Skipped: {skipped_states}")
        print(f"✓ Total: {len(states_to_process)}")
        print("=" * 60)

        input("\nPress Enter to close...")

    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        input("\nPress Enter to close...")

    finally:
        driver.quit()
        print("\nBrowser closed.")


if __name__ == "__main__":
    main()