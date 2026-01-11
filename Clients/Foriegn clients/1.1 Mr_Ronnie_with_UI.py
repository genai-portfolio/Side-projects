import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import re
import threading
import os
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class DownloadHandler(FileSystemEventHandler):
    """Monitor downloads folder and rename files with state prefix"""

    def __init__(self, current_state, download_folder, log_callback):
        self.current_state = current_state
        self.download_folder = download_folder
        self.log_callback = log_callback
        self.processed_files = set()

    def on_created(self, event):
        if event.is_directory:
            return

        file_path = event.src_path
        file_name = os.path.basename(file_path)

        # Wait for file to finish downloading
        time.sleep(2)

        # Check if it's a CSV or Excel file and hasn't been processed
        if (file_name.endswith(('.csv', '.xlsx', '.xls')) and
                file_name not in self.processed_files and
                not file_name.startswith(self.current_state)):

            try:
                # Wait for file to be completely written
                max_wait = 10
                for _ in range(max_wait):
                    try:
                        with open(file_path, 'rb') as f:
                            f.read(1)
                        break
                    except:
                        time.sleep(1)

                # Rename file with state prefix
                new_name = f"{self.current_state}_{file_name}"
                new_path = os.path.join(self.download_folder, new_name)

                # Rename the file
                os.rename(file_path, new_path)
                self.processed_files.add(file_name)
                self.log_callback(f"    ✓ Renamed file to: {new_name}")
                return new_path  # Return the new file path
            except Exception as e:
                self.log_callback(f"    ⚠ Could not rename file: {e}")


class StateScraperGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("State Leads Scraper - Professional Edition")
        self.root.geometry("900x700")
        self.root.resizable(True, True)

        # Variables
        self.is_running = False
        self.driver = None
        self.thread = None
        self.observer = None
        self.downloaded_files = []  # Track downloaded files

        # Styling
        style = ttk.Style()
        style.theme_use('clam')

        # Configure colors
        style.configure('Title.TLabel', font=('Arial', 16, 'bold'), foreground='#2c3e50')
        style.configure('Header.TLabel', font=('Arial', 10, 'bold'), foreground='#34495e')
        style.configure('Start.TButton', font=('Arial', 10, 'bold'), foreground='white', background='#27ae60')
        style.configure('Stop.TButton', font=('Arial', 10, 'bold'), foreground='white', background='#e74c3c')

        self.create_widgets()

    def create_widgets(self):
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(5, weight=1)

        # Title
        title_label = ttk.Label(main_frame, text="🌎 State Leads Scraper", style='Title.TLabel')
        title_label.grid(row=0, column=0, pady=(0, 20), sticky=tk.W)

        # Configuration Frame
        config_frame = ttk.LabelFrame(main_frame, text="Configuration", padding="10")
        config_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        config_frame.columnconfigure(1, weight=1)

        # Email
        ttk.Label(config_frame, text="Email:", style='Header.TLabel').grid(row=0, column=0, sticky=tk.W, pady=5)
        self.email_var = tk.StringVar(value="ronnie.hudson43@gmail.com")
        email_entry = ttk.Entry(config_frame, textvariable=self.email_var, width=40)
        email_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=5)

        # Password
        ttk.Label(config_frame, text="Password:", style='Header.TLabel').grid(row=1, column=0, sticky=tk.W, pady=5)
        self.password_var = tk.StringVar(value="55netsdowin7HHY%")
        password_entry = ttk.Entry(config_frame, textvariable=self.password_var, show="*", width=40)
        password_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=5)

        # State Selection
        ttk.Label(config_frame, text="State Selection:", style='Header.TLabel').grid(row=2, column=0, sticky=tk.W,
                                                                                     pady=5)
        state_frame = ttk.Frame(config_frame)
        state_frame.grid(row=2, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=5)

        self.state_mode = tk.StringVar(value="all")
        ttk.Radiobutton(state_frame, text="All States", variable=self.state_mode,
                        value="all", command=self.toggle_state_entry).pack(side=tk.LEFT, padx=(0, 20))
        ttk.Radiobutton(state_frame, text="Specific State:", variable=self.state_mode,
                        value="specific", command=self.toggle_state_entry).pack(side=tk.LEFT)

        self.state_var = tk.StringVar()
        self.state_entry = ttk.Entry(state_frame, textvariable=self.state_var, width=20, state='disabled')
        self.state_entry.pack(side=tk.LEFT, padx=(5, 0))

        # Download Folder
        ttk.Label(config_frame, text="Download Folder:", style='Header.TLabel').grid(row=3, column=0, sticky=tk.W,
                                                                                     pady=5)
        self.download_folder_var = tk.StringVar(value=str(Path.home() / "Downloads"))
        download_entry = ttk.Entry(config_frame, textvariable=self.download_folder_var, width=40)
        download_entry.grid(row=3, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=5)

        # Control Buttons Frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, pady=(0, 10), sticky=tk.W)

        self.start_button = ttk.Button(button_frame, text="▶ Start Scraping",
                                       command=self.start_scraping, style='Start.TButton', width=20)
        self.start_button.pack(side=tk.LEFT, padx=(0, 10))

        self.stop_button = ttk.Button(button_frame, text="⬛ Stop",
                                      command=self.stop_scraping, style='Stop.TButton',
                                      width=15, state='disabled')
        self.stop_button.pack(side=tk.LEFT)

        # Status Frame
        status_frame = ttk.Frame(main_frame)
        status_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(0, 10))

        ttk.Label(status_frame, text="Status:", style='Header.TLabel').pack(side=tk.LEFT, padx=(0, 10))
        self.status_label = ttk.Label(status_frame, text="Ready", foreground='#27ae60', font=('Arial', 10, 'bold'))
        self.status_label.pack(side=tk.LEFT)

        # Progress Bar
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.grid(row=4, column=0, sticky=(tk.W, tk.E), pady=(0, 10))

        # Logs Frame
        logs_frame = ttk.LabelFrame(main_frame, text="Activity Logs", padding="10")
        logs_frame.grid(row=5, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        logs_frame.columnconfigure(0, weight=1)
        logs_frame.rowconfigure(0, weight=1)

        # Logs Text Area
        self.logs_text = scrolledtext.ScrolledText(logs_frame, wrap=tk.WORD, height=20,
                                                   font=('Consolas', 9), bg='#2c3e50',
                                                   fg='#ecf0f1', insertbackground='white')
        self.logs_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Clear Logs Button
        clear_button = ttk.Button(logs_frame, text="Clear Logs", command=self.clear_logs)
        clear_button.grid(row=1, column=0, pady=(5, 0), sticky=tk.E)

        self.log("Application initialized and ready.")

    def toggle_state_entry(self):
        if self.state_mode.get() == "specific":
            self.state_entry.config(state='normal')
        else:
            self.state_entry.config(state='disabled')

    def log(self, message):
        """Add message to logs with timestamp"""
        timestamp = time.strftime("%H:%M:%S")
        self.logs_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.logs_text.see(tk.END)
        self.root.update_idletasks()

    def clear_logs(self):
        self.logs_text.delete(1.0, tk.END)

    def update_status(self, text, color='#27ae60'):
        self.status_label.config(text=text, foreground=color)

    def start_scraping(self):
        if self.is_running:
            return

        # Validate inputs
        email = self.email_var.get().strip()
        password = self.password_var.get().strip()

        if not email or not password:
            messagebox.showerror("Error", "Please enter both email and password!")
            return

        if self.state_mode.get() == "specific":
            state = self.state_var.get().strip()
            if not state:
                messagebox.showerror("Error", "Please enter a state name!")
                return

        # Disable controls
        self.is_running = True
        self.start_button.config(state='disabled')
        self.stop_button.config(state='normal')
        self.update_status("Running...", '#e67e22')
        self.progress.start(10)

        # Clear logs
        self.clear_logs()

        # Start scraping in a separate thread
        self.thread = threading.Thread(target=self.run_scraper, daemon=True)
        self.thread.start()

    def stop_scraping(self):
        if not self.is_running:
            return

        self.log("\n⚠ Stop requested. Cleaning up...")
        self.is_running = False

        # Stop file observer
        if self.observer:
            try:
                self.observer.stop()
                self.observer = None
            except:
                pass

        # Show download summary before closing
        if self.downloaded_files:
            self.log(f"\n📊 Download Summary:")
            self.log(f"   ✓ Successfully downloaded {len(self.downloaded_files)} file(s)")
            for state in self.downloaded_files:
                self.log(f"     - {state}")
        else:
            self.log("\n⚠ No downloads were verified")

        # Close browser
        if self.driver:
            try:
                self.log("🌐 Closing Chrome browser...")
                self.driver.quit()
                self.driver = None
                self.log("✓ Browser closed")
            except:
                pass

        # Update UI
        self.progress.stop()
        self.start_button.config(state='normal')
        self.stop_button.config(state='disabled')
        self.update_status("Stopped", '#e74c3c')
        self.log("✓ Scraper stopped successfully.")

    def wait_for_page_load(self, timeout=10):
        """Wait for page to load completely"""
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda d: d.execute_script('return document.readyState') == 'complete'
            )
            return True
        except TimeoutException:
            self.log("⚠ Page load timeout")
            return False

    def normalize_state_name(self, state_name):
        """Normalize state name for comparison (title case)"""
        return state_name.strip().title()

    def wait_for_download(self, download_folder, state_name, timeout=60):
        """Wait for a file to be downloaded and verify it's complete, then rename with state prefix"""
        try:
            # Get initial files in download folder
            initial_files = set()
            if os.path.exists(download_folder):
                initial_files = set(os.listdir(download_folder))

            start_time = time.time()
            downloaded_file = None

            # Wait for new file to appear
            while time.time() - start_time < timeout:
                if not self.is_running:
                    return False

                current_files = set(os.listdir(download_folder))
                new_files = current_files - initial_files

                # Look for CSV or Excel files (not .crdownload or .tmp)
                for file in new_files:
                    if file.endswith(('.csv', '.xlsx', '.xls')) and not file.endswith('.crdownload'):
                        # Check if file contains state name or is a valid data file
                        file_path = os.path.join(download_folder, file)

                        # Wait for file to finish downloading (no .crdownload)
                        if os.path.exists(file_path):
                            # Check if file size is stable (download complete)
                            try:
                                size1 = os.path.getsize(file_path)
                                time.sleep(2)
                                size2 = os.path.getsize(file_path)

                                if size1 == size2 and size1 > 0:
                                    downloaded_file = file
                                    self.log(f"    → Detected downloaded file: {file}")

                                    # Rename file with state prefix if not already prefixed
                                    if not file.startswith(state_name):
                                        try:
                                            new_name = f"{state_name}_{file}"
                                            new_path = os.path.join(download_folder, new_name)

                                            # Wait a bit to ensure file is fully written
                                            time.sleep(1)

                                            # Rename the file
                                            os.rename(file_path, new_path)
                                            self.log(f"    ✓ Renamed to: {new_name}")
                                        except Exception as rename_error:
                                            self.log(f"    ⚠ Could not rename file: {str(rename_error)[:50]}")

                                    return True
                            except:
                                pass

                time.sleep(1)

            # Timeout reached
            self.log(f"    ⚠ Download timeout after {timeout}s")
            return False

        except Exception as e:
            self.log(f"    ⚠ Error checking download: {str(e)[:50]}")
            return False

    def run_scraper(self):
        try:
            email = self.email_var.get().strip()
            password = self.password_var.get().strip()
            download_folder = self.download_folder_var.get().strip()

            # Determine state selection
            if self.state_mode.get() == "all":
                download_all = True
                target_state = None
                self.log("📋 Mode: Download ALL states")
            else:
                download_all = False
                target_state = self.normalize_state_name(self.state_var.get())
                self.log(f"📋 Mode: Download specific state - '{target_state}'")

            self.log(f"📧 Email: {email}")
            self.log("🔑 Password: ****")
            self.log(f"📁 Download Folder: {download_folder}\n")

            # Initialize Chrome driver with download preferences
            chrome_options = webdriver.ChromeOptions()
            prefs = {
                "download.default_directory": download_folder,
                "download.prompt_for_download": False,
                "download.directory_upgrade": True,
                "safebrowsing.enabled": True
            }
            chrome_options.add_experimental_option("prefs", prefs)

            self.log("🌐 Initializing Chrome browser...")
            self.driver = webdriver.Chrome(options=chrome_options)
            self.driver.maximize_window()

            if not self.is_running:
                return

            # Navigate to login page
            self.log("\n[1] Navigating to login page...")
            self.driver.get("https://auth.leadscampus.com/")
            self.wait_for_page_load(timeout=10)
            time.sleep(3)

            # Check for iframes
            self.log("[2] Checking for iframes...")
            iframes = self.driver.find_elements(By.TAG_NAME, "iframe")
            if iframes:
                self.log(f"   Found {len(iframes)} iframe(s), switching to first one...")
                self.driver.switch_to.frame(0)
                time.sleep(1)

            if not self.is_running:
                return

            # Fill email
            self.log("[3] Entering email...")
            try:
                email_field = WebDriverWait(self.driver, 15).until(
                    EC.presence_of_element_located((By.XPATH, "/html/body/div/div/div[2]/div/div/form/input[1]"))
                )
                email_field.clear()
                email_field.send_keys(email)
            except:
                self.log("   ⚠ XPath failed, trying alternative selectors...")
                try:
                    email_field = self.driver.find_element(By.CSS_SELECTOR, "input[type='email']")
                    email_field.clear()
                    email_field.send_keys(email)
                except:
                    email_field = self.driver.find_element(By.NAME, "email")
                    email_field.clear()
                    email_field.send_keys(email)

            # Fill password
            self.log("[4] Entering password...")
            try:
                password_field = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "/html/body/div/div/div[2]/div/div/form/input[2]"))
                )
                password_field.clear()
                password_field.send_keys(password)
            except:
                self.log("   ⚠ XPath failed, trying alternative selectors...")
                try:
                    password_field = self.driver.find_element(By.CSS_SELECTOR, "input[type='password']")
                    password_field.clear()
                    password_field.send_keys(password)
                except:
                    password_field = self.driver.find_element(By.NAME, "password")
                    password_field.clear()
                    password_field.send_keys(password)

            if not self.is_running:
                return

            # Click login
            self.log("[5] Clicking login button...")
            try:
                login_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/div[2]/div/div/form/div[3]/input"))
                )
                login_button.click()
            except:
                self.log("   ⚠ XPath failed, trying alternative selectors...")
                try:
                    login_button = self.driver.find_element(By.CSS_SELECTOR, "input[type='submit']")
                    login_button.click()
                except:
                    login_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
                    login_button.click()

            self.driver.switch_to.default_content()

            self.log("[6] Waiting for login to complete...")
            time.sleep(2)
            if self.wait_for_page_load(timeout=4):
                self.log("✓ Login successful")
            time.sleep(2)

            if not self.is_running:
                return

            # Navigate to SMS leads page
            self.log("\n[7] Navigating to SMS leads page...")
            self.driver.get("https://crm.leadscampus.com/smsleads.aspx")
            self.wait_for_page_load(timeout=10)
            time.sleep(2)
            self.log("✓ SMS leads page loaded successfully")

            # Hide chat widget
            try:
                self.driver.execute_script("""
                    var chatWidgets = document.querySelectorAll('iframe[title*="chat"], iframe[title*="Chat"], iframe[id*="chat"]');
                    for (var i = 0; i < chatWidgets.length; i++) {
                        chatWidgets[i].style.display = 'none';
                        chatWidgets[i].style.visibility = 'hidden';
                    }
                """)
            except:
                pass

            if not self.is_running:
                return

            # Open state dropdown
            self.log("\n[8] Opening state dropdown...")
            state_dropdown = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH,
                                            "/html/body/form/div[3]/div/div/div[2]/div[2]/div/div/div[1]/div[1]/div[2]/div[1]/div/span/span[1]/span"))
            )
            state_dropdown.click()
            time.sleep(1)
            self.log("✓ State dropdown opened")

            # Get states list
            self.log("\n[9] Fetching states list...")
            states_container = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "ul.select2-results__options"))
            )

            state_items = states_container.find_elements(By.TAG_NAME, "li")
            state_names = []
            for state in state_items:
                state_name = state.text.strip()
                if state_name and state_name != "-- Select State --":
                    state_names.append(state_name)

            self.log(f"✓ Found {len(state_names)} total states available")

            # Filter states based on selection
            if download_all:
                states_to_download = state_names
                self.log(f"✓ Will download ALL {len(states_to_download)} states")
            else:
                matching_states = [s for s in state_names if self.normalize_state_name(s) == target_state]

                if not matching_states:
                    self.log(f"\n✗ State '{target_state}' not found!")
                    self.log("Available states:")
                    for idx, state_name in enumerate(state_names, 1):
                        self.log(f"  {idx}. {state_name}")
                    self.stop_scraping()
                    return

                states_to_download = matching_states
                self.log(f"✓ Found matching state: '{states_to_download[0]}'")

            self.log("=" * 50)
            self.log(f"States to download ({len(states_to_download)}):")
            for idx, state_name in enumerate(states_to_download, 1):
                self.log(f"{idx}. {state_name}")
            self.log("=" * 50)

            # Close dropdown
            self.driver.find_element(By.TAG_NAME, "body").click()
            time.sleep(0.5)

            if not self.is_running:
                return

            # Process each state
            self.log("\n[10] Starting download process...\n")
            for idx, state_name in enumerate(states_to_download, 1):
                if not self.is_running:
                    break

                try:
                    self.log(f"[{idx}/{len(states_to_download)}] Processing: {state_name}")

                    # Setup file monitoring for this state
                    event_handler = DownloadHandler(state_name, download_folder, self.log)
                    self.observer = Observer()
                    self.observer.schedule(event_handler, download_folder, recursive=False)
                    self.observer.start()

                    # Hide chat widget
                    try:
                        self.driver.execute_script("""
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
                        modal = self.driver.find_element(By.ID, "kt_modal_download")
                        if modal.is_displayed():
                            self.log(f"    ⚠ Modal still open, closing it...")
                            try:
                                close_btn = modal.find_element(By.XPATH,
                                                               ".//button[contains(@class, 'btn-close') or contains(@class, 'close')]")
                                self.driver.execute_script("arguments[0].click();", close_btn)
                            except:
                                self.driver.execute_script("""
                                    var modal = document.getElementById('kt_modal_download');
                                    if (modal) {
                                        modal.style.display = 'none';
                                        modal.classList.remove('show');
                                        var backdrop = document.querySelector('.modal-backdrop');
                                        if (backdrop) backdrop.remove();
                                    }
                                """)
                            WebDriverWait(self.driver, 5).until(
                                EC.invisibility_of_element_located((By.ID, "kt_modal_download"))
                            )
                            time.sleep(1)
                    except:
                        pass

                    # Wait for spinner to disappear
                    try:
                        WebDriverWait(self.driver, 10).until(
                            EC.invisibility_of_element_located((By.ID, "cover-spin"))
                        )
                    except:
                        try:
                            self.driver.execute_script("document.getElementById('cover-spin').style.display = 'none';")
                        except:
                            pass

                    # Close dropdown if open
                    try:
                        self.driver.find_element(By.TAG_NAME, "body").click()
                        time.sleep(0.5)
                    except:
                        pass

                    # Scroll to dropdown
                    try:
                        state_dropdown_element = WebDriverWait(self.driver, 10).until(
                            EC.presence_of_element_located((By.XPATH,
                                                            "/html/body/form/div[3]/div/div/div[2]/div[2]/div/div/div[1]/div[1]/div[2]/div[1]/div/span/span[1]/span"))
                        )
                        self.driver.execute_script(
                            "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});",
                            state_dropdown_element)
                        time.sleep(0.5)
                    except:
                        pass

                    # Open dropdown with multi-strategy retry logic
                    dropdown_opened = False
                    max_retries = 5
                    for attempt in range(max_retries):
                        if not self.is_running:
                            break

                        try:
                            self.log(f"    → Opening dropdown (attempt {attempt + 1}/{max_retries})...")

                            # Ensure modal and spinner are gone
                            try:
                                self.driver.execute_script("""
                                    var modal = document.getElementById('kt_modal_download');
                                    if (modal && modal.style.display !== 'none') {
                                        modal.style.display = 'none';
                                        modal.classList.remove('show');
                                    }
                                    var spinner = document.getElementById('cover-spin');
                                    if (spinner) spinner.style.display = 'none';

                                    // Remove any overlays that might block clicks
                                    var backdrops = document.querySelectorAll('.modal-backdrop');
                                    backdrops.forEach(function(backdrop) { backdrop.remove(); });
                                """)
                            except:
                                pass

                            state_dropdown = WebDriverWait(self.driver, 15).until(
                                EC.element_to_be_clickable((By.XPATH,
                                                            "/html/body/form/div[3]/div/div/div[2]/div[2]/div/div/div[1]/div[1]/div[2]/div[1]/div/span/span[1]/span"))
                            )

                            self.driver.execute_script(
                                "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});",
                                state_dropdown)
                            time.sleep(0.5)

                            # Try multiple clicking strategies
                            click_strategies = [
                                ("JavaScript click",
                                 lambda: self.driver.execute_script("arguments[0].click();", state_dropdown)),
                                ("Regular Selenium click", lambda: state_dropdown.click()),
                                ("ActionChains click", lambda: webdriver.ActionChains(self.driver).move_to_element(
                                    state_dropdown).click().perform()),
                                ("ActionChains with pause",
                                 lambda: webdriver.ActionChains(self.driver).move_to_element(state_dropdown).pause(
                                     0.5).click().perform()),
                                ("Direct focus + click", lambda: (
                                    self.driver.execute_script("arguments[0].focus();", state_dropdown),
                                    time.sleep(0.2),
                                    state_dropdown.click()
                                )),
                            ]

                            for strategy_name, click_func in click_strategies:
                                try:
                                    self.log(f"       Trying: {strategy_name}")
                                    click_func()
                                    time.sleep(1.0)

                                    # Verify dropdown opened
                                    try:
                                        WebDriverWait(self.driver, 3).until(
                                            EC.presence_of_element_located(
                                                (By.CSS_SELECTOR, "ul.select2-results__options"))
                                        )
                                        dropdown_opened = True
                                        self.log(f"    ✓ Dropdown opened successfully with {strategy_name}")
                                        break
                                    except:
                                        self.log(f"       {strategy_name} didn't open dropdown, trying next...")
                                        continue
                                except Exception as strategy_error:
                                    self.log(f"       {strategy_name} failed: {str(strategy_error)[:50]}")
                                    continue

                            if dropdown_opened:
                                break

                            if attempt < max_retries - 1:
                                self.log(f"    ⚠ All strategies failed, retrying...")
                                time.sleep(2)
                                continue

                        except Exception as click_error:
                            if attempt < max_retries - 1:
                                self.log(f"    ⚠ Error: {str(click_error)[:50]}, retrying...")
                                time.sleep(2)
                                continue
                            else:
                                raise Exception(f"Failed to open dropdown after {max_retries} attempts")

                    if not dropdown_opened:
                        raise Exception("Dropdown did not open")

                    if not self.is_running:
                        break

                    # Find and click state
                    states_container = WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "ul.select2-results__options"))
                    )

                    state_option = states_container.find_element(By.XPATH, f".//li[contains(text(), '{state_name}')]")
                    state_option.click()
                    self.log(f"    ✓ Selected: {state_name}")

                    # Wait for loading
                    try:
                        WebDriverWait(self.driver, 25).until(
                            EC.invisibility_of_element_located((By.ID, "cover-spin"))
                        )
                        self.log(f"    ✓ Page loaded")
                    except:
                        try:
                            self.driver.execute_script("document.getElementById('cover-spin').style.display = 'none';")
                        except:
                            pass

                    time.sleep(15)

                    # Check lead count
                    try:
                        leads_element = WebDriverWait(self.driver, 10).until(
                            EC.presence_of_element_located((By.XPATH,
                                                            "/html/body/form/div[3]/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div[1]/h1/span"))
                        )
                        leads_text = leads_element.text.strip()
                        self.log(f"    → Leads: {leads_text}")

                        numbers = re.findall(r'[\d,]+', leads_text)
                        if numbers:
                            lead_count = int(numbers[0].replace(',', ''))
                            if lead_count == 0:
                                self.log(f"    ⚠ Skipping {state_name} - 0 leads found")
                                # Stop observer
                                self.observer.stop()
                                self.observer = None
                                continue
                            else:
                                self.log(f"    ✓ Found {lead_count:,} leads")
                        elif "0 leads" in leads_text.lower():
                            self.log(f"    ⚠ Skipping {state_name} - 0 leads found")
                            # Stop observer
                            self.observer.stop()
                            self.observer = None
                            continue
                    except Exception as check_error:
                        self.log(f"    ⚠ Could not check leads count, proceeding...")

                    if not self.is_running:
                        break

                    # Click download button
                    try:
                        download_button = WebDriverWait(self.driver, 10).until(
                            EC.presence_of_element_located((By.XPATH,
                                                            "/html/body/form/div[3]/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div[2]/a[1]"))
                        )
                        self.driver.execute_script("arguments[0].click();", download_button)
                        self.log(f"    ✓ Clicked download button")
                    except Exception as click_error:
                        self.log(f"    ✗ Could not click download button")
                        continue

                    # Wait for modal
                    self.log(f"    ⏳ Waiting for modal...")
                    try:
                        WebDriverWait(self.driver, 15).until(
                            EC.presence_of_element_located((By.ID, "kt_modal_download"))
                        )
                        time.sleep(2)
                        self.log(f"    ✓ Modal appeared")
                    except:
                        self.log(f"    ⚠ Modal may not have appeared")
                        time.sleep(3)

                    # Click "Here" link
                    here_clicked = False
                    max_here_retries = 3
                    for here_attempt in range(max_here_retries):
                        if not self.is_running:
                            break

                        try:
                            here_link = WebDriverWait(self.driver, 10).until(
                                EC.element_to_be_clickable(
                                    (
                                    By.XPATH, "/html/body/form/div[3]/div/div/div[2]/div[3]/div/div/div[2]/div/span/a"))
                            )
                            self.driver.execute_script("arguments[0].click();", here_link)
                            self.log(f"    ✓ Downloading {state_name}...")
                            here_clicked = True
                            break
                        except:
                            if here_attempt < max_here_retries - 1:
                                time.sleep(2)
                                continue
                            else:
                                self.log(f"    ✗ Could not click 'Here' link")
                                continue

                    if not here_clicked:
                        continue

                    # Wait for download to start and complete
                    self.log(f"    ⏳ Waiting for download to complete...")
                    download_verified = self.wait_for_download(download_folder, state_name, timeout=60)

                    if download_verified:
                        self.log(f"    ✓ Download completed and verified")
                        self.downloaded_files.append(state_name)
                    else:
                        self.log(f"    ⚠ Could not verify download completion")

                    # Close modal
                    modal_closed = False
                    max_close_retries = 3
                    for close_attempt in range(max_close_retries):
                        try:
                            close_button = WebDriverWait(self.driver, 5).until(
                                EC.element_to_be_clickable(
                                    (By.XPATH, "/html/body/form/div[3]/div/div/div[2]/div[3]/div/div/div[3]/button"))
                            )
                            self.driver.execute_script("arguments[0].click();", close_button)
                            time.sleep(1)

                            WebDriverWait(self.driver, 5).until(
                                EC.invisibility_of_element_located((By.ID, "kt_modal_download"))
                            )
                            modal_closed = True
                            self.log(f"    ✓ Modal closed")
                            break
                        except:
                            try:
                                self.driver.execute_script("""
                                    var modal = document.getElementById('kt_modal_download');
                                    if (modal) {
                                        modal.style.display = 'none';
                                        modal.classList.remove('show');
                                        var backdrop = document.querySelector('.modal-backdrop');
                                        if (backdrop) backdrop.remove();
                                    }
                                """)
                                time.sleep(1)
                                modal_closed = True
                                self.log(f"    ✓ Modal closed with JavaScript")
                                break
                            except:
                                if close_attempt < max_close_retries - 1:
                                    time.sleep(1)
                                    continue

                    # Stop observer for this state
                    if self.observer:
                        self.observer.stop()
                        self.observer = None

                    time.sleep(1)
                    self.log(f"    ⏳ Waiting before next state...\n")
                    time.sleep(2)

                except Exception as e:
                    self.log(f"    ✗ Error with {state_name}: {str(e)[:100]}")
                    # Stop observer on error
                    if self.observer:
                        try:
                            self.observer.stop()
                            self.observer = None
                        except:
                            pass
                    continue

            self.log("\n" + "=" * 50)
            self.log("✓ All downloads completed successfully!")
            self.log(f"✓ Total states processed: {len(states_to_download)}")
            self.log(f"✓ Files downloaded: {len(self.downloaded_files)}")
            if self.downloaded_files:
                self.log("Downloaded states:")
                for state in self.downloaded_files:
                    self.log(f"  - {state}")
            self.log("=" * 50)

            # Cleanup
            self.stop_scraping()

        except Exception as e:
            self.log(f"\n✗ Error occurred: {str(e)}")
            import traceback
            self.log(traceback.format_exc())
            self.stop_scraping()


def main():
    root = tk.Tk()
    app = StateScraperGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()