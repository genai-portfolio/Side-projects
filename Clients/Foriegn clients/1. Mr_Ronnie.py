from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
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
        print("Failed to read credentials from requirements.txt")
        return

    print(f"Email: {email}")
    print("Password: ****")

    # Initialize Chrome driver
    driver = webdriver.Chrome()
    driver.maximize_window()

    try:
        # Navigate to login page
        print("\n[1] Navigating to login page...")
        driver.get("https://auth.leadscampus.com/")

        # Wait for page to load completely
        wait_for_page_load(driver, timeout=10)
        time.sleep(3)  # Extra wait for any dynamic content

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
            # Try alternative selectors
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

        # Wait for page to load (4 seconds max, but check if loaded)
        print("[7] Waiting for login to complete...")
        time.sleep(2)
        if wait_for_page_load(driver, timeout=4):
            print("✓ Page loaded successfully")
        else:
            print("⚠ Page may not have loaded completely")
        time.sleep(2)  # Additional rest time

        # Navigate to SMS leads page
        print("\n[8] Navigating to SMS leads page...")
        driver.get("https://crm.leadscampus.com/smsleads.aspx")

        # Wait for SMS leads page to load
        wait_for_page_load(driver, timeout=10)
        time.sleep(2)
        print("✓ SMS leads page loaded successfully")

        # Hide chat widget iframe that might block clicks
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
            pass  # If hiding fails, continue anyway

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

        # Extract state names (skip the first "-- Select State --" option)
        state_names = []
        for idx, state in enumerate(state_items, 1):
            state_name = state.text.strip()
            if state_name and state_name != "-- Select State --":
                state_names.append(state_name)

        print(f"\n✓ Found {len(state_names)} states to download:")
        print("=" * 50)
        for idx, state_name in enumerate(state_names, 1):
            print(f"{idx}. {state_name}")
        print("=" * 50)

        # Close the dropdown first (click somewhere else)
        driver.find_element(By.TAG_NAME, "body").click()
        time.sleep(0.5)

        # Now loop through each state and download
        print("\n[11] Starting download process...")
        for idx, state_name in enumerate(state_names, 1):
            try:
                print(f"\n[{idx}/{len(state_names)}] Processing: {state_name}")

                # Hide chat widget iframe that might block clicks
                try:
                    driver.execute_script("""
                        var chatWidgets = document.querySelectorAll('iframe[title*="chat"], iframe[title*="Chat"], iframe[id*="chat"]');
                        for (var i = 0; i < chatWidgets.length; i++) {
                            chatWidgets[i].style.display = 'none';
                            chatWidgets[i].style.visibility = 'hidden';
                        }
                    """)
                    print(f"    ✓ Hidden chat widget iframe")
                except:
                    pass  # If hiding fails, continue anyway

                # Ensure modal is fully closed before proceeding
                try:
                    modal = driver.find_element(By.ID, "kt_modal_download")
                    if modal.is_displayed():
                        print(f"    ⚠ Modal still open, closing it...")
                        try:
                            close_btn = modal.find_element(By.XPATH,
                                                           ".//button[contains(@class, 'btn-close') or contains(@class, 'close')]")
                            driver.execute_script("arguments[0].click();", close_btn)
                        except:
                            # Try to close modal with JavaScript
                            driver.execute_script("""
                                var modal = document.getElementById('kt_modal_download');
                                if (modal) {
                                    modal.style.display = 'none';
                                    modal.classList.remove('show');
                                    var backdrop = document.querySelector('.modal-backdrop');
                                    if (backdrop) backdrop.remove();
                                }
                            """)
                        # Wait for modal to be fully closed
                        WebDriverWait(driver, 5).until(
                            EC.invisibility_of_element_located((By.ID, "kt_modal_download"))
                        )
                        time.sleep(1)
                        print(f"    ✓ Modal closed")
                except:
                    pass  # Modal not present, that's fine

                # Wait for loading spinner to disappear
                try:
                    WebDriverWait(driver, 10).until(
                        EC.invisibility_of_element_located((By.ID, "cover-spin"))
                    )
                except:
                    # If spinner still visible, try to hide it
                    try:
                        driver.execute_script("document.getElementById('cover-spin').style.display = 'none';")
                    except:
                        pass

                # Close dropdown if it's already open (click outside)
                try:
                    driver.find_element(By.TAG_NAME, "body").click()
                    time.sleep(0.5)
                except:
                    pass

                # Scroll to dropdown to ensure it's visible
                try:
                    state_dropdown_element = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH,
                                                        "/html/body/form/div[3]/div/div/div[2]/div[2]/div/div/div[1]/div[1]/div[2]/div[1]/div/span/span[1]/span"))
                    )
                    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});",
                                          state_dropdown_element)
                    time.sleep(0.5)
                except:
                    pass

                # Open dropdown with retry logic and verification
                dropdown_opened = False
                max_retries = 5  # Increased retries
                for attempt in range(max_retries):
                    try:
                        print(f"    → Attempting to open dropdown (attempt {attempt + 1}/{max_retries})...")

                        # Ensure modal and spinner are gone before each attempt
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

                        # Re-find dropdown element on each attempt to avoid stale references
                        state_dropdown = WebDriverWait(driver, 15).until(
                            EC.element_to_be_clickable((By.XPATH,
                                                        "/html/body/form/div[3]/div/div/div[2]/div[2]/div/div/div[1]/div[1]/div[2]/div[1]/div/span/span[1]/span"))
                        )

                        # Scroll to dropdown
                        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});",
                                              state_dropdown)
                        time.sleep(0.3)

                        # Try JavaScript click first (more reliable)
                        driver.execute_script("arguments[0].click();", state_dropdown)
                        time.sleep(1.0)  # Wait a bit longer for dropdown to open

                        # Verify dropdown actually opened by checking for states container
                        try:
                            WebDriverWait(driver, 5).until(
                                EC.presence_of_element_located((By.CSS_SELECTOR, "ul.select2-results__options"))
                            )
                            dropdown_opened = True
                            print(f"    ✓ Dropdown opened successfully")
                            break
                        except:
                            # If verification failed, try regular click as fallback
                            print(f"    ⚠ Dropdown may not have opened, trying regular click...")
                            # Re-find element again
                            state_dropdown = WebDriverWait(driver, 10).until(
                                EC.element_to_be_clickable((By.XPATH,
                                                            "/html/body/form/div[3]/div/div/div[2]/div[2]/div/div/div[1]/div[1]/div[2]/div[1]/div/span/span[1]/span"))
                            )
                            state_dropdown.click()
                            time.sleep(1.0)

                            # Verify again
                            try:
                                WebDriverWait(driver, 5).until(
                                    EC.presence_of_element_located((By.CSS_SELECTOR, "ul.select2-results__options"))
                                )
                                dropdown_opened = True
                                print(f"    ✓ Dropdown opened with regular click")
                                break
                            except:
                                if attempt < max_retries - 1:
                                    print(f"    ⚠ Retrying...")
                                    time.sleep(2)
                                    continue
                    except Exception as click_error:
                        error_msg = str(click_error)[:150]
                        if attempt < max_retries - 1:
                            print(f"    ⚠ Click failed: {error_msg}, retrying...")
                            time.sleep(2)
                            continue
                        else:
                            raise Exception(f"Failed to open dropdown after {max_retries} attempts: {error_msg}")

                if not dropdown_opened:
                    raise Exception("Dropdown did not open after multiple attempts")

                # Find and click the specific state
                states_container = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "ul.select2-results__options"))
                )

                # Find the state by text
                state_option = states_container.find_element(By.XPATH, f".//li[contains(text(), '{state_name}')]")
                state_option.click()

                print(f"    ✓ Selected: {state_name}")

                # Wait for loading spinner to disappear and page to load
                try:
                    WebDriverWait(driver, 25).until(
                        EC.invisibility_of_element_located((By.ID, "cover-spin"))
                    )
                    print(f"    ✓ Page loaded (spinner disappeared)")
                except:
                    print(f"    ⚠ Loading spinner still visible, trying to hide it...")
                    try:
                        driver.execute_script("document.getElementById('cover-spin').style.display = 'none';")
                        print(f"    ✓ Forced spinner to hide")
                    except:
                        print(f"    ⚠ Could not hide spinner, proceeding anyway")

                # Wait for state data to load
                time.sleep(15)  # Wait 15 seconds for state data to load
                print(f"    → Current URL: {driver.current_url}")

                # Check if state has leads (skip if 0 leads)
                try:
                    leads_element = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH,
                                                        "/html/body/form/div[3]/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div[1]/h1/span"))
                    )
                    leads_text = leads_element.text.strip()
                    print(f"    → Leads text: {leads_text}")

                    # Extract number from text (e.g., "12,223 leads" or "0 leads")
                    # Remove commas and extract the number
                    numbers = re.findall(r'[\d,]+', leads_text)
                    if numbers:
                        # Remove commas and convert to int
                        lead_count = int(numbers[0].replace(',', ''))
                        if lead_count == 0:
                            print(f"    ⚠ Skipping {state_name} - 0 leads found")
                            continue
                        else:
                            print(f"    ✓ Found {lead_count} leads for {state_name}")
                    else:
                        # If we can't parse, check if text contains "0 leads"
                        if "0 leads" in leads_text.lower():
                            print(f"    ⚠ Skipping {state_name} - 0 leads found")
                            continue
                        else:
                            print(f"    ✓ Proceeding with download for {state_name}")
                except Exception as check_error:
                    print(f"    ⚠ Could not check leads count: {check_error}")
                    print(f"    → Proceeding anyway...")

                # Click download button
                try:
                    download_button = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH,
                                                        "/html/body/form/div[3]/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div[2]/a[1]"))
                    )
                    driver.execute_script("arguments[0].click();", download_button)
                    print(f"    ✓ Clicked download button")
                except Exception as click_error:
                    print(f"    ✗ Could not click download button: {click_error}")
                    continue

                # Wait for modal to appear with better waiting
                print(f"    ⏳ Waiting for modal to appear...")
                try:
                    WebDriverWait(driver, 15).until(
                        EC.presence_of_element_located((By.ID, "kt_modal_download"))
                    )
                    # Wait a bit more for modal to be fully visible
                    time.sleep(2)
                    print(f"    ✓ Modal appeared")
                except:
                    print(f"    ⚠ Modal may not have appeared, proceeding anyway...")
                    time.sleep(3)

                # Click the "Here" link in the modal with retry logic
                here_clicked = False
                max_here_retries = 3
                for here_attempt in range(max_here_retries):
                    try:
                        here_link = WebDriverWait(driver, 10).until(
                            EC.element_to_be_clickable(
                                (By.XPATH, "/html/body/form/div[3]/div/div/div[2]/div[3]/div/div/div[2]/div/span/a"))
                        )
                        # Try JavaScript click first
                        driver.execute_script("arguments[0].click();", here_link)
                        print(f"    ✓ Clicked 'Here' to download {state_name}")
                        here_clicked = True
                        break
                    except Exception as modal_error:
                        if here_attempt < max_here_retries - 1:
                            print(
                                f"    ⚠ Could not click 'Here' link (attempt {here_attempt + 1}/{max_here_retries}), retrying...")
                            time.sleep(2)
                            continue
                        else:
                            print(f"    ✗ Could not click 'Here' link after {max_here_retries} attempts: {modal_error}")
                            # Try to close modal before continuing
                            try:
                                driver.execute_script("""
                                    var modal = document.getElementById('kt_modal_download');
                                    if (modal) {
                                        modal.style.display = 'none';
                                        modal.classList.remove('show');
                                    }
                                """)
                            except:
                                pass
                            continue  # Skip to next state

                if not here_clicked:
                    continue  # Skip to next state if we couldn't click 'Here'

                # Wait a few seconds for download to start
                print(f"    ⏳ Waiting for download to start...")
                time.sleep(3)

                # Close the modal - ensure it's fully closed
                modal_closed = False
                max_close_retries = 3
                for close_attempt in range(max_close_retries):
                    try:
                        # First try to find and click close button
                        close_button = WebDriverWait(driver, 5).until(
                            EC.element_to_be_clickable(
                                (By.XPATH, "/html/body/form/div[3]/div/div/div[2]/div[3]/div/div/div[3]/button"))
                        )
                        driver.execute_script("arguments[0].click();", close_button)
                        time.sleep(1)

                        # Verify modal is closed
                        WebDriverWait(driver, 5).until(
                            EC.invisibility_of_element_located((By.ID, "kt_modal_download"))
                        )
                        modal_closed = True
                        print(f"    ✓ Closed modal")
                        break
                    except:
                        # Try alternative close method with JavaScript
                        try:
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
                            # Verify it's closed
                            try:
                                modal = driver.find_element(By.ID, "kt_modal_download")
                                if not modal.is_displayed():
                                    modal_closed = True
                                    print(f"    ✓ Closed modal with JavaScript")
                                    break
                            except:
                                modal_closed = True
                                print(f"    ✓ Closed modal with JavaScript")
                                break
                        except:
                            if close_attempt < max_close_retries - 1:
                                print(
                                    f"    ⚠ Could not close modal (attempt {close_attempt + 1}/{max_close_retries}), retrying...")
                                time.sleep(1)
                                continue
                            else:
                                print(
                                    f"    ⚠ Could not close modal after {max_close_retries} attempts, proceeding anyway...")
                                # Force close with JavaScript
                                driver.execute_script("""
                                    var modal = document.getElementById('kt_modal_download');
                                    if (modal) {
                                        modal.style.display = 'none';
                                        modal.classList.remove('show');
                                    }
                                    var backdrop = document.querySelector('.modal-backdrop');
                                    if (backdrop) backdrop.remove();
                                """)
                                break

                # Extra wait to ensure modal is fully closed before next iteration
                time.sleep(1)

                # Short wait before next iteration
                print(f"    ⏳ Waiting before next state...")
                time.sleep(2)

            except Exception as e:
                print(f"    ✗ Error with {state_name}: {e}")
                continue

        print("\n" + "=" * 50)
        print("✓ All downloads completed successfully!")
        print(f"✓ Total states processed: {len(state_names)}")
        print("=" * 50)

        # Keep browser open for inspection
        input("\nPress Enter to close the browser...")

    except Exception as e:
        print(f"\n✗ Error occurred: {e}")
        import traceback
        traceback.print_exc()

        # Debug: Save page source
        print("\n[DEBUG] Saving page source for inspection...")
        with open("page_source.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        print("✓ Page source saved to 'page_source.html'")

        # Keep browser open for manual inspection
        input("\nPress Enter to close the browser...")

    finally:
        driver.quit()
        print("\nBrowser closed.")


if __name__ == "__main__":
    main()