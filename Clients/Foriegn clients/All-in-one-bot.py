import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
try:
    from selenium.webdriver.chrome.service import Service
    from webdriver_manager.chrome import ChromeDriverManager
    WEBDRIVER_MANAGER_AVAILABLE = True
except ImportError:
    WEBDRIVER_MANAGER_AVAILABLE = False
from selenium.webdriver.common.action_chains import ActionChains
import time
import os
import re
import threading
from pathlib import Path

# Try to import pyautogui for fallback clicking
try:
    import pyautogui
    PYAUTOGUI_AVAILABLE = True
except ImportError:
    PYAUTOGUI_AVAILABLE = False


def wait_for_page_load(driver, timeout=10):
    """Wait for page to load completely"""
    try:
        WebDriverWait(driver, timeout).until(
            lambda d: d.execute_script('return document.readyState') == 'complete'
        )
        return True
    except TimeoutException:
        return False


def wait_for_download_to_start(download_dir, timeout=30, initial_files=None):
    """Wait for a new file to appear in the download directory"""
    if initial_files is None:
        initial_files = set(os.listdir(download_dir)) if os.path.exists(download_dir) else set()

    start_time = time.time()
    while time.time() - start_time < timeout:
        time.sleep(1)
        current_files = set(os.listdir(download_dir)) if os.path.exists(download_dir) else set()
        new_files = current_files - initial_files

        if new_files:
            return True

    return False


def wait_for_download_to_complete(download_dir, timeout=300):
    """Wait for all downloads to complete (no .crdownload or .tmp files)"""
    start_time = time.time()
    while time.time() - start_time < timeout:
        time.sleep(2)

        if os.path.exists(download_dir):
            files = os.listdir(download_dir)
            incomplete = [f for f in files if f.endswith('.crdownload') or f.endswith('.tmp') or f.endswith('.part')]

            if not incomplete:
                return True

        time.sleep(1)

    return False


def try_click_dropdown(driver, xpath, attempt_num, log_callback=None):
    """
    Try to click the dropdown using multiple strategies
    """
    def log(msg):
        if log_callback:
            log_callback(msg)

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
        return False

    # Strategy 1: Standard click
    try:
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
        time.sleep(0.5)
        element = driver.find_element(By.XPATH, xpath)
        element.click()
        return True
    except:
        pass

    # Strategy 2: JavaScript Click
    try:
        driver.execute_script("arguments[0].click();", element)
        return True
    except:
        pass

    # Strategy 3: ActionChains
    try:
        actions = ActionChains(driver)
        actions.move_to_element(element).click().perform()
        return True
    except:
        pass

    # Strategy 4: PyAutoGUI
    if PYAUTOGUI_AVAILABLE:
        try:
            rect = driver.execute_script("return arguments[0].getBoundingClientRect();", element)
            nav_height = driver.execute_script("return window.outerHeight - window.innerHeight;")
            if nav_height <= 0:
                nav_height = 110

            click_x = int(rect['x'] + rect['width'] / 2)
            click_y = int(rect['y'] + rect['height'] / 2 + nav_height)

            pyautogui.moveTo(click_x, click_y, duration=0.5)
            pyautogui.click()
            return True
        except:
            pass

    return False


def get_xpath_config(db_choice, data_type):
    """Get XPath configuration based on database and data type"""
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


class B2BScraperGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("B2B Leads Scraper - Professional Edition")
        self.root.geometry("950x750")
        self.root.resizable(True, True)

        # Variables
        self.is_running = False
        self.driver = None
        self.thread = None

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
        main_frame.rowconfigure(6, weight=1)

        # Title
        title_label = ttk.Label(main_frame, text="🏢 B2B Leads Scraper", style='Title.TLabel')
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

        # Database Selection
        ttk.Label(config_frame, text="Database:", style='Header.TLabel').grid(row=2, column=0, sticky=tk.W, pady=5)
        self.database_var = tk.StringVar(value="US Business Leads")
        database_combo = ttk.Combobox(config_frame, textvariable=self.database_var, width=37, state='readonly')
        database_combo['values'] = ("US Business Leads", "US New Businesses", "Timeshare Owners", "High Tech Leaders")
        database_combo.grid(row=2, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=5)

        # Data Type
        ttk.Label(config_frame, text="Data Type:", style='Header.TLabel').grid(row=3, column=0, sticky=tk.W, pady=5)
        data_frame = ttk.Frame(config_frame)
        data_frame.grid(row=3, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=5)

        self.data_type_var = tk.StringVar(value="emails")
        ttk.Radiobutton(data_frame, text="Emails", variable=self.data_type_var, value="emails").pack(side=tk.LEFT, padx=(0, 20))
        ttk.Radiobutton(data_frame, text="Phone Numbers", variable=self.data_type_var, value="phones").pack(side=tk.LEFT)

        # State Selection
        ttk.Label(config_frame, text="State Selection:", style='Header.TLabel').grid(row=4, column=0, sticky=tk.W, pady=5)
        state_frame = ttk.Frame(config_frame)
        state_frame.grid(row=4, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=5)

        self.state_mode = tk.StringVar(value="all")
        ttk.Radiobutton(state_frame, text="All States", variable=self.state_mode,
                        value="all", command=self.toggle_state_entry).pack(side=tk.LEFT, padx=(0, 20))
        ttk.Radiobutton(state_frame, text="Specific State:", variable=self.state_mode,
                        value="specific", command=self.toggle_state_entry).pack(side=tk.LEFT)

        self.state_var = tk.StringVar()
        self.state_entry = ttk.Entry(state_frame, textvariable=self.state_var, width=20, state='disabled')
        self.state_entry.pack(side=tk.LEFT, padx=(5, 0))

        # Download Folder
        ttk.Label(config_frame, text="Download Folder:", style='Header.TLabel').grid(row=5, column=0, sticky=tk.W, pady=5)
        self.download_folder_var = tk.StringVar(value=str(Path.home() / "Downloads"))
        download_entry = ttk.Entry(config_frame, textvariable=self.download_folder_var, width=40)
        download_entry.grid(row=5, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=5)

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
        logs_frame.grid(row=6, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
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

    def run_scraper(self):
        try:
            email = self.email_var.get().strip()
            password = self.password_var.get().strip()
            download_folder = self.download_folder_var.get().strip()

            # Get database selection
            db_map = {
                "US Business Leads": "1",
                "US New Businesses": "2",
                "Timeshare Owners": "3",
                "High Tech Leaders": "4"
            }
            db_choice = db_map[self.database_var.get()]
            db_name = self.database_var.get()

            # Get data type
            data_type = "1" if self.data_type_var.get() == "emails" else "2"
            data_name = "Emails" if data_type == "1" else "Phone Numbers"

            # Get URL
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
            target_url = url_map[db_choice][data_type]

            # Get XPath configuration
            xpath_config = get_xpath_config(db_choice, data_type)

            # Determine state selection
            if self.state_mode.get() == "all":
                download_all = True
                selected_state = None
                self.log(f"📋 Mode: Download ALL states")
            else:
                download_all = False
                selected_state = self.state_var.get().strip().title()
                self.log(f"📋 Mode: Download specific state - '{selected_state}'")

            self.log(f"📧 Email: {email}")
            self.log("🔑 Password: ****")
            self.log(f"🗄️ Database: {db_name}")
            self.log(f"📊 Data Type: {data_name}")
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
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--start-maximized")

            self.log("🌐 Initializing Chrome browser...")
            try:
                if WEBDRIVER_MANAGER_AVAILABLE:
                    service = Service(ChromeDriverManager().install())
                    self.driver = webdriver.Chrome(service=service, options=chrome_options)
                else:
                    self.driver = webdriver.Chrome(options=chrome_options)
            except Exception as e:
                self.log(f"✗ Failed to initialize Chrome: {str(e)}")
                self.stop_scraping()
                return

            self.driver.maximize_window()

            if not self.is_running:
                return

            # LOGIN
            self.log("\n[1] Navigating to login page...")
            self.driver.get("https://auth.leadscampus.com/")
            wait_for_page_load(self.driver, timeout=10)
            time.sleep(3)

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
                try:
                    login_button = self.driver.find_element(By.CSS_SELECTOR, "input[type='submit']")
                    login_button.click()
                except:
                    login_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
                    login_button.click()

            self.driver.switch_to.default_content()

            self.log("[6] Waiting for login to complete...")
            try:
                WebDriverWait(self.driver, 5).until(
                    EC.url_contains("Default.aspx")
                )
                self.log("✓ Login successful")
            except:
                self.log("⚠ 5s timeout reached, proceeding anyway...")

            if not self.is_running:
                return

            # Navigate to database page
            self.log(f"\n[7] Navigating to {db_name} page...")
            self.driver.get(target_url)
            wait_for_page_load(self.driver, timeout=10)
            time.sleep(2)
            self.log("✓ Page loaded successfully")

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
            try:
                try_click_dropdown(self.driver, xpath_config["dropdown"], 1, self.log)
            except:
                state_dropdown = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, xpath_config["dropdown"]))
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

            # Determine states to process
            if download_all:
                states_to_process = state_names
                self.log(f"✓ Will download ALL {len(states_to_process)} states")
            else:
                if selected_state in state_names:
                    states_to_process = [selected_state]
                    self.log(f"✓ Will download: {selected_state}")
                else:
                    self.log(f"\n✗ State '{selected_state}' not found!")
                    self.log("Available states:")
                    for idx, state_name in enumerate(state_names, 1):
                        self.log(f"  {idx}. {state_name}")
                    self.stop_scraping()
                    return

            self.log("=" * 50)
            self.log(f"States to download ({len(states_to_process)}):")
            for idx, state_name in enumerate(states_to_process, 1):
                self.log(f"{idx}. {state_name}")
            self.log("=" * 50)

            # Close dropdown
            try:
                self.driver.find_element(By.TAG_NAME, "body").click()
                time.sleep(0.5)
            except:
                pass

            if not self.is_running:
                return

            # Process each state
            self.log("\n[10] Starting download process...\n")
            successful_downloads = 0
            skipped_states = 0

            for idx, state_name in enumerate(states_to_process, 1):
                if not self.is_running:
                    break

                try:
                    self.log(f"\n[{idx}/{len(states_to_process)}] Processing: {state_name}")

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
                            EC.presence_of_element_located((By.XPATH, xpath_config["dropdown"]))
                        )
                        self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});",
                                                  state_dropdown_element)
                        time.sleep(0.5)
                    except:
                        pass

                    # Open dropdown with retry logic
                    dropdown_opened = False
                    max_retries = 5

                    for attempt in range(max_retries):
                        if not self.is_running:
                            break

                        self.log(f"    → Opening dropdown (attempt {attempt + 1}/{max_retries})...")
                        if try_click_dropdown(self.driver, xpath_config["dropdown"], attempt + 1, self.log):
                            try:
                                WebDriverWait(self.driver, 5).until(
                                    EC.presence_of_element_located((By.CSS_SELECTOR, "ul.select2-results__options"))
                                )
                                dropdown_opened = True
                                self.log(f"    ✓ Dropdown opened successfully")
                                break
                            except:
                                self.log(f"    ⚠ Click seemed successful but dropdown didn't appear. Retrying...")
                                time.sleep(1)
                        else:
                            self.log(f"    ⚠ Click attempt failed. Retrying...")
                            time.sleep(2)

                    if not dropdown_opened:
                        raise Exception("Dropdown did not open")

                    if not self.is_running:
                        break

                    # Select state
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

                    time.sleep(3)

                    # Check lead count
                    try:
                        self.log(f"    ⏳ Waiting for leads count to update...")
                        leads_text = "0 Leads"
                        max_leads_wait = 20
                        leads_start_time = time.time()

                        while time.time() - leads_start_time < max_leads_wait:
                            try:
                                leads_element = WebDriverWait(self.driver, 5).until(
                                    EC.presence_of_element_located((By.XPATH, xpath_config["leads_count"]))
                                )
                                leads_text = leads_element.text.strip()

                                numbers = re.findall(r'[\d,]+', leads_text)
                                if numbers:
                                    current_count = int(numbers[0].replace(',', ''))
                                    if current_count > 0:
                                        break
                            except:
                                pass

                            time.sleep(1)

                        self.log(f"    → Leads: {leads_text}")

                        numbers = re.findall(r'[\d,]+', leads_text)
                        if numbers:
                            lead_count = int(numbers[0].replace(',', ''))
                            if lead_count == 0:
                                self.log(f"    ⚠ Skipping {state_name} - 0 leads found")
                                skipped_states += 1
                                continue
                            else:
                                self.log(f"    ✓ Found {lead_count:,} leads")
                        elif "0 leads" in leads_text.lower():
                            self.log(f"    ⚠ Skipping {state_name} - 0 leads found")
                            skipped_states += 1
                            continue
                    except Exception as check_error:
                        self.log(f"    ⚠ Could not check leads count, proceeding...")

                    if not self.is_running:
                        break

                    # Click download button
                    try:
                        download_button = WebDriverWait(self.driver, 10).until(
                            EC.presence_of_element_located((By.XPATH, xpath_config["download_button"]))
                        )
                        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", download_button)
                        time.sleep(0.5)
                        self.driver.execute_script("arguments[0].click();", download_button)
                        self.log(f"    ✓ Clicked download button")
                    except Exception as e:
                        self.log(f"    ✗ Could not click download button")
                        skipped_states += 1
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

                    # Capture files before download
                    initial_download_files = set(os.listdir(download_folder)) if os.path.exists(download_folder) else set()

                    # Click "Here" link
                    here_clicked = False
                    max_here_retries = 3
                    for here_attempt in range(max_here_retries):
                        if not self.is_running:
                            break

                        try:
                            here_link = WebDriverWait(self.driver, 10).until(
                                EC.element_to_be_clickable(
                                    (By.XPATH, "/html/body/form/div[3]/div/div/div[2]/div[3]/div/div/div[2]/div/span/a"))
                            )
                            self.driver.execute_script("arguments[0].click();", here_link)
                            self.log(f"    ✓ Clicked 'Here' link")
                            here_clicked = True
                            break
                        except:
                            if here_attempt < max_here_retries - 1:
                                self.log(f"    ⚠ Could not click 'Here' link, retrying...")
                                time.sleep(2)
                                continue
                            else:
                                self.log(f"    ✗ Could not click 'Here' link")
                                skipped_states += 1

                    if not here_clicked:
                        continue

                    # Wait for download
                    self.log(f"    ⏳ Waiting for download...")
                    download_started = wait_for_download_to_start(download_folder, timeout=30, initial_files=initial_download_files)

                    if download_started:
                        download_completed = wait_for_download_to_complete(download_folder, timeout=300)

                        if download_completed:
                            successful_downloads += 1
                            self.log(f"    ✓ Download successful")

                            # Rename file
                            try:
                                final_files = set(os.listdir(download_folder)) if os.path.exists(download_folder) else set()
                                new_files = final_files - initial_download_files

                                valid_new_files = [f for f in new_files if not (f.endswith('.crdownload') or f.endswith('.tmp') or f.endswith('.part'))]

                                if len(valid_new_files) == 1:
                                    original_filename = valid_new_files[0]
                                    safe_state_name = state_name.replace(" ", "_")
                                    new_filename = f"{safe_state_name}_{original_filename}"

                                    old_path = os.path.join(download_folder, original_filename)
                                    new_path = os.path.join(download_folder, new_filename)

                                    if os.path.exists(new_path):
                                        try:
                                            os.remove(new_path)
                                        except:
                                            pass

                                    os.rename(old_path, new_path)
                                    self.log(f"    ✓ Renamed to: {new_filename}")
                                    self.log(f"    📁 Saved to: {download_folder}")
                                elif len(valid_new_files) > 1:
                                    self.log(f"    ⚠ Multiple files found, skipping rename")
                                else:
                                    self.log(f"    ⚠ Could not identify file for renaming")

                            except Exception as rename_error:
                                self.log(f"    ⚠ Rename failed: {rename_error}")

                        else:
                            self.log(f"    ⚠ Download may not have completed")
                            skipped_states += 1
                    else:
                        self.log(f"    ⚠ Download did not start")
                        skipped_states += 1

                    # Close modal
                    try:
                        close_button = WebDriverWait(self.driver, 5).until(
                            EC.element_to_be_clickable(
                                (By.XPATH, "/html/body/form/div[3]/div/div/div[2]/div[3]/div/div/div[3]/button"))
                        )
                        self.driver.execute_script("arguments[0].click();", close_button)
                        time.sleep(1)
                        self.log(f"    ✓ Closed modal")
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

                    # Wait before next iteration
                    self.log(f"    ⏳ Waiting before next state...")
                    time.sleep(3)

                except Exception as e:
                    self.log(f"    ✗ Error with {state_name}: {str(e)[:100]}")
                    skipped_states += 1
                    continue

            self.log("\n" + "=" * 50)
            self.log("✓ All downloads completed!")
            self.log(f"✓ Successful downloads: {successful_downloads}")
            self.log(f"⚠ Skipped states: {skipped_states}")
            self.log(f"✓ Total states processed: {len(states_to_process)}")
            if successful_downloads > 0:
                self.log(f"📁 Files saved to: {download_folder}")
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
    app = B2BScraperGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()