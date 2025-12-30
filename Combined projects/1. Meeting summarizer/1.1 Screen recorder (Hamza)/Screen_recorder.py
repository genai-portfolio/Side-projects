import tkinter as tk
from tkinter import filedialog, messagebox, Toplevel
import cv2
import numpy as np
import mss
import threading
import time
import os
import datetime


class ModernRecorder:
    def __init__(self, root):
        self.root = root
        self.root.title("Meeting Recorder Pro")
        self.root.geometry("500x350")
        self.root.resizable(False, False)

        # --- Theme Config ---
        self.bg_color = "#212121"  # Dark Background
        self.fg_color = "#FFFFFF"  # White Text
        self.accent_color = "#00E5FF"  # Cyan Start Button
        self.stop_color = "#FF1744"  # Red Stop Button
        self.btn_text_color = "#000000"  # Black Text on buttons

        self.root.configure(bg=self.bg_color)

        # --- State Variables ---
        self.is_recording = False
        self.recording_start_time = None
        self.monitor_area = None
        self.out_filename = ""
        self.record_thread = None

        # --- Frames (Pages) ---
        self.frame_home = tk.Frame(self.root, bg=self.bg_color)
        self.frame_recording = tk.Frame(self.root, bg=self.bg_color)

        self.setup_home_screen()
        self.setup_recording_screen()

        # Start at Home
        self.show_frame(self.frame_home)

    # ==========================
    # UI SETUP
    # ==========================
    def show_frame(self, frame):
        self.frame_home.pack_forget()
        self.frame_recording.pack_forget()
        frame.pack(fill="both", expand=True)

    def setup_home_screen(self):
        # Header
        tk.Label(self.frame_home, text="RECORDER // PRO", font=("Impact", 24),
                 bg=self.bg_color, fg=self.accent_color).pack(pady=(30, 10))

        tk.Label(self.frame_home, text="Select Capture Mode", font=("Arial", 10),
                 bg=self.bg_color, fg="#AAAAAA").pack(pady=5)

        # Mode Selection (Radio Buttons styled differently)
        self.mode_var = tk.StringVar(value="full")

        container = tk.Frame(self.frame_home, bg=self.bg_color)
        container.pack(pady=10)

        # Custom Radio Styling (using Buttons that act like Radios visually)
        self.btn_mode_full = tk.Button(container, text="[ O ] Full Screen",
                                       command=lambda: self.set_mode("full"),
                                       width=15, bg=self.accent_color, fg=self.btn_text_color, relief="flat")
        self.btn_mode_full.grid(row=0, column=0, padx=5)

        self.btn_mode_custom = tk.Button(container, text="[ + ] Custom Area",
                                         command=lambda: self.set_mode("custom"),
                                         width=15, bg="#424242", fg="white", relief="flat")
        self.btn_mode_custom.grid(row=0, column=1, padx=5)

        # Status / Instructions
        self.lbl_status = tk.Label(self.frame_home, text="Ready to initialize...",
                                   font=("Consolas", 10), bg=self.bg_color, fg="#00E676")
        self.lbl_status.pack(pady=20)

        # Big Action Button
        self.btn_action = tk.Button(self.frame_home, text="INITIALIZE RECORDING",
                                    font=("Arial", 12, "bold"), bg=self.accent_color, fg=self.btn_text_color,
                                    width=25, height=2, borderwidth=0, cursor="hand2",
                                    command=self.initiate_sequence)
        self.btn_action.pack(pady=10)

    def setup_recording_screen(self):
        # Timer Display
        self.lbl_timer = tk.Label(self.frame_recording, text="00:00:00",
                                  font=("Impact", 40), bg=self.bg_color, fg=self.accent_color)
        self.lbl_timer.pack(pady=(50, 10))

        tk.Label(self.frame_recording, text="Recording in Progress",
                 font=("Arial", 10, "bold"), bg=self.bg_color, fg="#FFFFFF").pack()

        # Stop Button
        tk.Button(self.frame_recording, text="STOP & SAVE",
                  font=("Arial", 12, "bold"), bg=self.stop_color, fg="white",
                  width=20, height=2, borderwidth=0, cursor="hand2",
                  command=self.stop_recording).pack(pady=40)

    # ==========================
    # LOGIC
    # ==========================
    def set_mode(self, mode):
        self.mode_var.set(mode)
        # Visual Toggle logic
        if mode == "full":
            self.btn_mode_full.config(bg=self.accent_color, fg="black")
            self.btn_mode_custom.config(bg="#424242", fg="white")
        else:
            self.btn_mode_full.config(bg="#424242", fg="white")
            self.btn_mode_custom.config(bg=self.accent_color, fg="black")

    def initiate_sequence(self):
        mode = self.mode_var.get()
        if mode == "custom":
            self.lbl_status.config(text="Select area on screen...", fg="yellow")
            self.root.update()
            # Minimize main window so it doesn't block selection
            self.root.iconify()
            self.launch_selection_overlay()
        else:
            with mss.mss() as sct:
                self.monitor_area = sct.monitors[1]
            self.start_countdown_sequence()

    def launch_selection_overlay(self):
        # Transparent Overlay logic
        self.sel_root = Toplevel(self.root)
        self.sel_root.attributes("-fullscreen", True)
        self.sel_root.attributes("-alpha", 0.3)
        self.sel_root.config(bg="white")
        self.sel_root.config(cursor="cross")

        # Events
        self.sel_root.bind("<ButtonPress-1>", self.on_down)
        self.sel_root.bind("<B1-Motion>", self.on_drag)
        self.sel_root.bind("<ButtonRelease-1>", self.on_up)
        self.sel_root.bind("<Escape>", lambda e: self.cancel_selection())

        self.canvas = tk.Canvas(self.sel_root, bg="black", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        # Make canvas transparent-ish
        self.sel_root.attributes("-transparentcolor", "black")

    def on_down(self, event):
        self.start_x, self.start_y = event.x, event.y
        self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, 1, 1, outline="red", width=3)

    def on_drag(self, event):
        self.canvas.coords(self.rect, self.start_x, self.start_y, event.x, event.y)

    def on_up(self, event):
        x1, y1 = min(self.start_x, event.x), min(self.start_y, event.y)
        x2, y2 = max(self.start_x, event.x), max(self.start_y, event.y)

        # Ensure minimum size
        if (x2 - x1) < 50 or (y2 - y1) < 50:
            self.cancel_selection()
            return

        self.monitor_area = {"top": y1, "left": x1, "width": x2 - x1, "height": y2 - y1}
        self.sel_root.destroy()
        self.root.deiconify()  # Bring back main window
        self.start_countdown_sequence()

    def cancel_selection(self):
        self.sel_root.destroy()
        self.root.deiconify()
        self.lbl_status.config(text="Selection Cancelled", fg="red")

    def start_countdown_sequence(self):
        # Choose File First (Avoids delay after countdown)
        filename = filedialog.asksaveasfilename(defaultextension=".avi",
                                                filetypes=[("AVI files", "*.avi")])
        if not filename:
            self.lbl_status.config(text="File selection cancelled", fg="red")
            return

        self.out_filename = filename

        # 3-Second Countdown visual on button
        for i in range(3, 0, -1):
            self.btn_action.config(text=f"STARTING IN {i}...", bg="yellow")
            self.root.update()
            time.sleep(1)

        self.start_recording()

    def start_recording(self):
        self.is_recording = True
        self.recording_start_time = datetime.datetime.now()

        # Switch UI
        self.show_frame(self.frame_recording)

        # Start Threads
        self.record_thread = threading.Thread(target=self.record_loop)
        self.record_thread.start()

        self.timer_thread = threading.Thread(target=self.update_timer)
        self.timer_thread.start()

    def update_timer(self):
        while self.is_recording:
            now = datetime.datetime.now()
            delta = now - self.recording_start_time
            # Format time manually to avoid day errors
            total_seconds = int(delta.total_seconds())
            hours, remainder = divmod(total_seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            time_str = f"{hours:02}:{minutes:02}:{seconds:02}"

            try:
                self.lbl_timer.config(text=time_str)
            except:
                break  # UI killed
            time.sleep(0.5)

    def record_loop(self):
        with mss.mss() as sct:
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            fps = 20.0
            w = self.monitor_area["width"]
            h = self.monitor_area["height"]
            out = cv2.VideoWriter(self.out_filename, fourcc, fps, (w, h))

            while self.is_recording:
                img = sct.grab(self.monitor_area)
                frame = np.array(img)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
                out.write(frame)

            out.release()

    def stop_recording(self):
        self.is_recording = False
        messagebox.showinfo("Done", f"Recording saved to:\n{self.out_filename}")

        # Reset UI
        self.btn_action.config(text="INITIALIZE RECORDING", bg=self.accent_color)
        self.lbl_status.config(text="Ready for next session", fg="#00E676")
        self.show_frame(self.frame_home)


if __name__ == "__main__":
    root = tk.Tk()
    app = ModernRecorder(root)
    root.mainloop()