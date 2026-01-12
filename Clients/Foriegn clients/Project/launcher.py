import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import sys
import os


try:
    import B2B
except ImportError:
    B2B = None

try:
    import B2C
except ImportError:
    B2C = None

class LeadsCampusLauncher:
    def __init__(self, root):
        self.root = root
        self.root.title("LeadsCampus Scraper Launcher")
        self.root.geometry("800x600")
        self.root.resizable(False, False)
        
        # Center window on screen
        self.center_window()
        
        # Configure background color
        self.root.configure(bg='#2c3e50')
        
        self.create_widgets()
        
        # Check if modules are available
        if not B2B or not B2C:
            self.root.after(100, self.warn_missing_modules)
    
    def warn_missing_modules(self):
        missing = []
        if not B2B: missing.append("B2B.py")
        if not B2C: missing.append("B2C.py")
        self.show_error(f"Warning: The following files were not found or have errors:\n{', '.join(missing)}\n\nPlease ensure they are in the same folder as launcher.py")

    def center_window(self):
        """Center the window on the screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def create_widgets(self):
        # Main container
        main_frame = tk.Frame(self.root, bg='#2c3e50')
        main_frame.pack(expand=True, fill='both', padx=40, pady=40)
        
        # Title
        title_label = tk.Label(
            main_frame,
            text="LeadsCampus Scraper",
            font=('Arial', 32, 'bold'),
            fg='#ecf0f1',
            bg='#2c3e50'
        )
        title_label.pack(pady=(0, 20))
        
        # Subtitle
        subtitle_label = tk.Label(
            main_frame,
            text="Select the scraper you want to run",
            font=('Arial', 14),
            fg='#bdc3c7',
            bg='#2c3e50'
        )
        subtitle_label.pack(pady=(0, 30))
        
        # Buttons container
        buttons_frame = tk.Frame(main_frame, bg='#2c3e50')
        buttons_frame.pack(expand=True)
        
        # B2C Button
        b2c_button = tk.Button(
            buttons_frame,
            text="B2C Scraper",
            font=('Arial', 18, 'bold'),
            fg='white',
            bg='#3498db',
            activebackground='#2980b9',
            activeforeground='white',
            width=20,
            height=3,
            cursor='hand2',
            relief='flat',
            command=self.launch_b2c
        )
        b2c_button.pack(pady=15)
        
        # Add hover effect for B2C button
        b2c_button.bind('<Enter>', lambda e: b2c_button.config(bg='#2980b9'))
        b2c_button.bind('<Leave>', lambda e: b2c_button.config(bg='#3498db'))
        
        # B2B Button
        b2b_button = tk.Button(
            buttons_frame,
            text="B2B Scraper",
            font=('Arial', 18, 'bold'),
            fg='white',
            bg='#27ae60',
            activebackground='#229954',
            activeforeground='white',
            width=20,
            height=3,
            cursor='hand2',
            relief='flat',
            command=self.launch_b2b
        )
        b2b_button.pack(pady=15)
        
        # Add hover effect for B2B button
        b2b_button.bind('<Enter>', lambda e: b2b_button.config(bg='#229954'))
        b2b_button.bind('<Leave>', lambda e: b2b_button.config(bg='#27ae60'))
        
        # Footer
        footer_label = tk.Label(
            main_frame,
            text="© 2026 LeadsCampus - Professional Lead Scraping Solutions",
            font=('Arial', 9),
            fg='#7f8c8d',
            bg='#2c3e50'
        )
        footer_label.pack(side='bottom', pady=(20, 0))

    def launch_b2c(self):
        """Launch the B2C scraper"""
        if not B2C:
            self.show_error("B2C module not loaded correctly.")
            return
        
        try:
            # We must destroy the current root before starting a new mainloop
            self.root.destroy()
            # Call the main function of the B2C module
            B2C.main()
        except Exception as e:
            # Re-create a root for error display if destroyed
            temp_root = tk.Tk()
            temp_root.withdraw()
            messagebox.showerror("Error", f"Failed to launch B2C scraper:\n{str(e)}")
            temp_root.destroy()

    def launch_b2b(self):
        """Launch the B2B scraper"""
        if not B2B:
            self.show_error("B2B module not loaded correctly.")
            return
            
        try:
            # We must destroy the current root before starting a new mainloop
            self.root.destroy()
            # Call the main function of the B2B module
            B2B.main()
        except Exception as e:
            # Re-create a root for error display if destroyed
            temp_root = tk.Tk()
            temp_root.withdraw()
            messagebox.showerror("Error", f"Failed to launch B2B scraper:\n{str(e)}")
            temp_root.destroy()
    
    def show_error(self, message):
        """Show error message in a popup"""
        error_window = tk.Toplevel(self.root)
        error_window.title("Error")
        error_window.geometry("400x150")
        error_window.resizable(False, False)
        error_window.configure(bg='#e74c3c')
        
        # Center error window
        error_window.update_idletasks()
        x = (error_window.winfo_screenwidth() // 2) - 200
        y = (error_window.winfo_screenheight() // 2) - 75
        error_window.geometry(f'400x150+{x}+{y}')
        
        # Error message
        error_label = tk.Label(
            error_window,
            text=message,
            font=('Arial', 11),
            fg='white',
            bg='#e74c3c',
            wraplength=350,
            justify='center'
        )
        error_label.pack(expand=True, pady=20)
        
        # OK button
        ok_button = tk.Button(
            error_window,
            text="OK",
            font=('Arial', 10, 'bold'),
            fg='white',
            bg='#c0392b',
            activebackground='#a93226',
            width=10,
            command=error_window.destroy
        )
        ok_button.pack(pady=(0, 20))


def main():
    root = tk.Tk()
    app = LeadsCampusLauncher(root)
    root.mainloop()


if __name__ == "__main__":
    main()
