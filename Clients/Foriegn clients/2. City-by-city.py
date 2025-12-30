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


def main():
    # Read credentials
    email, password = read_credentials()
    if not email or not password:
        print("Failed to read credentials")
        return

    print(f"Email: {email}")
    print("Password: ****\n")

    # ASK FOR STATE INPUT FIRST - BEFORE OPENING BROWSER
    print("=" * 50)
    print("STATE SELECTION")
    print("=" * 50)
    print("Available states: Alabama, Alaska, Arizona, Arkansas, California,")
    print("Colorado, Connecticut, Delaware, District of Columbia, Florida,")
    print("Georgia, Hawaii, Idaho, Illinois, Indiana, Iowa, Kansas, Kentucky,")
    print("Louisiana, Maine, Maryland, Massachusetts, Michigan, Minnesota,")
    print("Mississippi, Missouri, Montana, Nebraska, Nevada, New Hampshire,")
    print("New Jersey, New Mexico, New York, North Carolina, North Dakota,")
    print("Ohio, Oklahoma, Oregon, Pennsylvania, Rhode Island, South Carolina,")
    print("South Dakota, Tennessee, Texas, Utah, Vermont, Virginia, Washington,")
    print("West Virginia, Wisconsin, Wyoming")
    print("=" * 50)
    user_state_input = input("\nEnter state name (e.g., 'texas' or 'Texas') or press ENTER to download all: ").strip()

    # Normalize the input if provided
    selected_state = None
    download_all = False

    if user_state_input:
        selected_state = user_state_input.capitalize()
        print(f"✓ Will download data for: {selected_state}")
    else:
        download_all = True
        print(f"✓ Will download data for all states")

    print("=" * 50 + "\n")

    # Set up Chrome options for downloads
    chrome_options = webdriver.ChromeOptions()

    # Set download directory
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

    # Initialize Chrome driver with options
    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()

    try:
        # Navigate to login page
        print("\n[1] Navigating to login page...")
        driver.get("https://auth.leadscampus.com/")

        # Wait for page to load completely
        wait_for_page_load(driver, timeout=10)
        time.sleep(3)

        # Try to find and switch to iframe if exists
        print("[2] Checking for iframes...")
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        if iframes:
            print(f"   Found {len(iframes)} iframe(s), switching to first one...")
            driver.switch_to.frame(0)
            time.sleep(1)

        # Wait for email field and fill it
        print("[3] Waiting for email field...")
        try:
            email_field = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/div/div/div[2]/div/div/form/input[1]"))
            )
            print("[4] Entering email...")
            email_field.clear()
            email_field.send_keys(email)
        except Exception as e:
            print(f"   ✗ XPath failed, trying alternative selectors...")
            try:
                email_field = driver.find_element(By.CSS_SELECTOR, "input[type='email']")
                email_field.clear()
                email_field.send_keys(email)
            except:
                email_field = driver.find_element(By.NAME, "email")
                email_field.clear()
                email_field.send_keys(email)

        # Wait for password field and fill it
        print("[5] Entering password...")
        try:
            password_field = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/div/div/div[2]/div/div/form/input[2]"))
            )
            password_field.clear()
            password_field.send_keys(password)
        except Exception as e:
            print(f"   ✗ XPath failed, trying alternative selectors...")
            try:
                password_field = driver.find_element(By.CSS_SELECTOR, "input[type='password']")
                password_field.clear()
                password_field.send_keys(password)
            except:
                password_field = driver.find_element(By.NAME, "password")
                password_field.clear()
                password_field.send_keys(password)

        # Click login button
        print("[6] Clicking login button...")
        try:
            login_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/div[2]/div/div/form/div[3]/input"))
            )
            login_button.click()
        except Exception as e:
            print(f"   ✗ XPath failed, trying alternative selectors...")
            try:
                login_button = driver.find_element(By.CSS_SELECTOR, "input[type='submit']")
                login_button.click()
            except:
                login_button = driver.find_element(By.XPATH, "//button[@type='submit']")
                login_button.click()

        # Switch back to default content if we were in iframe
        driver.switch_to.default_content()

        # Wait for page to load
        print("[7] Waiting for login to complete...")
        time.sleep(2)
        if wait_for_page_load(driver, timeout=4):
            print("✓ Page loaded successfully")
        else:
            print("⚠ Page may not have loaded completely")
        time.sleep(2)

        # Navigate to SMS leads page
        print("\n[8] Navigating to SMS leads page...")
        driver.get("https://crm.leadscampus.com/smsleads.aspx")

        # Wait for SMS leads page to load
        wait_for_page_load(driver, timeout=10)
        time.sleep(2)
        print("✓ SMS leads page loaded successfully")

        # Hide chat widget if it exists
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

        # Click on the state dropdown
        print("\n[9] Opening state dropdown...")
        state_dropdown = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH,
                                        "/html/body/form/div[3]/div/div/div[2]/div[2]/div/div/div[1]/div[1]/div[2]/div[1]/div/span/span[1]/span"))
        )
        state_dropdown.click()
        time.sleep(1)
        print("✓ State dropdown opened")

        # Get the dropdown list container
        print("\n[10] Fetching states list...")
        states_container = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "ul.select2-results__options"))
        )

        # Find all state items
        state_items = states_container.find_elements(By.TAG_NAME, "li")

        # Extract state names (skip "-- Select State --")
        state_names = []
        for idx, state in enumerate(state_items, 1):
            state_name = state.text.strip()
            if state_name and state_name != "-- Select State --":
                state_names.append(state_name)

        print(f"\n✓ Found {len(state_names)} states available")

        # Determine which states to process based on user input
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
                print("Available states:", ", ".join(state_names[:10]), "...")
                input("\nPress Enter to close...")
                driver.quit()
                return

        # Close the dropdown
        driver.find_element(By.TAG_NAME, "body").click()
        time.sleep(0.5)

        # Track statistics
        successful_downloads = 0
        skipped_states = 0

        # NOW LOOP THROUGH SELECTED STATES ONLY
        print(f"[11] Starting download for {len(states_to_process)} state(s)...\n")

        for idx, state_name in enumerate(states_to_process, 1):
            try:
                print(f"[{idx}/{len(states_to_process)}] Processing: {state_name}")

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

                # Open dropdown - simplified approach
                print(f"    → Opening dropdown...")
                dropdown_opened = False

                try:
                    # Find dropdown element
                    state_dropdown = WebDriverWait(driver, 15).until(
                        EC.element_to_be_clickable((By.XPATH,
                                                    "/html/body/form/div[3]/div/div/div[2]/div[2]/div/div/div[1]/div[1]/div[2]/div[1]/div/span/span[1]/span"))
                    )

                    # Scroll to it
                    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", state_dropdown)
                    time.sleep(0.5)

                    # Click it
                    state_dropdown.click()
                    time.sleep(1)

                    # Verify it opened
                    WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "ul.select2-results__options"))
                    )
                    dropdown_opened = True
                    print(f"    ✓ Opened dropdown")

                except Exception as e:
                    print(f"    ✗ Could not open dropdown: {str(e)[:100]}\n")
                    skipped_states += 1
                    continue

                if not dropdown_opened:
                    skipped_states += 1
                    continue

                # Select state
                try:
                    states_container = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "ul.select2-results__options"))
                    )

                    # Find the state option
                    state_option = states_container.find_element(By.XPATH, f".//li[contains(text(), '{state_name}')]")
                    print(f"    → Found '{state_name}' in dropdown")

                    # Use regular click for Select2 items
                    state_option.click()
                    print(f"    ✓ Clicked on: {state_name}")

                    # Wait for dropdown to close and selection to register
                    time.sleep(2)

                    # Verify the selection
                    try:
                        selected_display = driver.find_element(By.XPATH,
                                                               "/html/body/form/div[3]/div/div/div[2]/div[2]/div/div/div[1]/div[1]/div[2]/div[1]/div/span/span[1]/span")
                        selected_text = selected_display.text.strip()
                        print(f"    → Dropdown now shows: '{selected_text}'")
                        if state_name in selected_text:
                            print(f"    ✓ Selection confirmed!")
                        else:
                            print(f"    ⚠ Selection may not have registered properly")
                    except:
                        print(f"    ⚠ Could not verify selection")

                except Exception as e:
                    print(f"    ✗ Could not select state: {str(e)[:100]}\n")
                    skipped_states += 1
                    continue

                # Wait for loading spinner to disappear
                try:
                    WebDriverWait(driver, 20).until(
                        EC.invisibility_of_element_located((By.ID, "cover-spin"))
                    )
                    print(f"    ✓ Loading complete")
                except:
                    print(f"    ⚠ Spinner still visible, proceeding...")
                    try:
                        driver.execute_script("document.getElementById('cover-spin').style.display = 'none';")
                    except:
                        pass

                # Wait 15 seconds for data to load
                print(f"    ⏳ Waiting 15 seconds for state data...")
                time.sleep(15)
                print(f"    → Current URL: {driver.current_url}")

                # Check lead count
                try:
                    leads_element = driver.find_element(By.XPATH,
                                                        "/html/body/form/div[3]/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div[1]/h1/span")
                    leads_text = leads_element.text.strip()
                    print(f"    → Leads display text: '{leads_text}'")

                    numbers = re.findall(r'[\d,]+', leads_text)
                    if numbers:
                        lead_count = int(numbers[0].replace(',', ''))
                        if lead_count == 0:
                            print(f"    ⚠ Skipping - 0 leads found\n")
                            skipped_states += 1
                            continue
                        print(f"    ✓ Found {lead_count:,} leads - proceeding with download")
                    else:
                        print(f"    ⚠ Could not parse lead count from '{leads_text}'")
                except Exception as e:
                    print(f"    ⚠ Could not check lead count: {str(e)[:100]}")
                    print(f"    → Proceeding anyway...")

                # Click download
                try:
                    print(f"    → Looking for download button...")
                    download_button = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH,
                                                        "/html/body/form/div[3]/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div[2]/a[1]"))
                    )

                    # Scroll to button
                    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", download_button)
                    time.sleep(0.5)

                    # Click with JavaScript
                    driver.execute_script("arguments[0].click();", download_button)
                    print(f"    ✓ Clicked download button")

                    # Wait 8 seconds for modal
                    print(f"    ⏳ Waiting 8 seconds for modal...")
                    time.sleep(8)

                except Exception as e:
                    print(f"    ✗ Could not click download button: {str(e)[:100]}\n")
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

        print("=" * 50)
        print(f"✓ Process completed!")
        print(f"✓ Downloaded: {successful_downloads}")
        print(f"⚠ Skipped: {skipped_states}")
        print(f"✓ Total: {len(states_to_process)}")
        print("=" * 50)

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