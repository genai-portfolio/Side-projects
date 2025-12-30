import tkinter as tk
from tkinter import filedialog, messagebox, Toplevel
import cv2
import numpy as np
import mss
import threading
import time
import os
import datetime
import pyaudio
import wave
import subprocess
import sys


# ==========================
# AUDIO RECORDER MODULE
# ==========================
class AudioRecorder:
    def __init__(self):
        self.is_recording = False
        self.frames = []
        self.audio = pyaudio.PyAudio()
        self.stream = None
        self.filename = "temp_audio.wav"

    def start(self):
        self.is_recording = True
        self.frames = []
        # Standard settings for speech processing
        self.stream = self.audio.open(format=pyaudio.paInt16,
                                      channels=1,  # Mono is better for speech recognition later
                                      rate=44100,
                                      input=True,
                                      frames_per_buffer=1024)

        # Start the listener loop in a thread (daemon so it kills if app crashes)
        self.thread = threading.Thread(target=self.record_loop, daemon=True)
        self.thread.start()

    def record_loop(self):
        while self.is_recording:
            data = self.stream.read(1024)
            self.frames.append(data)

    def stop(self):
        self.is_recording = False
        if self.thread:
            self.thread.join()

        self.stream.stop_stream()
        self.stream.close()

        # Save to WAV
        wf = wave.open(self.filename, 'wb')
        wf.setnchannels(1)
        wf.setsampwidth(self.audio.get_sample_size(pyaudio.paInt16))
        wf.setframerate(44100)
        wf.writeframes(b''.join(self.frames))
        wf.close()


# ==========================
# MAIN APP
# ==========================
class ModernRecorder:
    def __init__(self, root):
        self.root = root
        self.root.title("Meeting Recorder Pro")
        self.root.geometry("500x450")  # Slightly taller for audio options
        self.root.resizable(False, False)

        # --- Theme Config ---
        self.bg_color = "#212121"
        self.fg_color = "#FFFFFF"
        self.accent_color = "#00E5FF"
        self.stop_color = "#FF1744"
        self.active_toggle = "#00C853"  # Green for ON

        self.root.configure(bg=self.bg_color)

        # --- State Variables ---
        self.is_recording = False
        self.monitor_area = None
        self.out_filename = ""
        self.audio_enabled = True  # Default to ON

        # Helpers
        self.audio_recorder = AudioRecorder()

        # --- Frames ---
        self.frame_home = tk.Frame(self.root, bg=self.bg_color)
        self.frame_recording = tk.Frame(self.root, bg=self.bg_color)

        self.setup_home_screen()
        self.setup_recording_screen()
        self.show_frame(self.frame_home)

    def show_frame(self, frame):
        self.frame_home.pack_forget()
        self.frame_recording.pack_forget()
        frame.pack(fill="both", expand=True)

    def setup_home_screen(self):
        # Header
        tk.Label(self.frame_home, text="RECORDER // PRO", font=("Impact", 24),
                 bg=self.bg_color, fg=self.accent_color).pack(pady=(30, 10))

        # Mode Section
        tk.Label(self.frame_home, text="1. Capture Area", font=("Arial", 10, "bold"), bg=self.bg_color, fg="#888").pack(
            pady=5)
        self.mode_var = tk.StringVar(value="full")
        container_mode = tk.Frame(self.frame_home, bg=self.bg_color)
        container_mode.pack(pady=5)

        self.btn_mode_full = tk.Button(container_mode, text="[ O ] Full Screen",
                                       command=lambda: self.set_mode("full"),
                                       width=15, bg=self.accent_color, relief="flat")
        self.btn_mode_full.grid(row=0, column=0, padx=5)

        self.btn_mode_custom = tk.Button(container_mode, text="[ + ] Custom Area",
                                         command=lambda: self.set_mode("custom"),
                                         width=15, bg="#424242", fg="white", relief="flat")
        self.btn_mode_custom.grid(row=0, column=1, padx=5)

        # Audio Section (NEW)
        tk.Label(self.frame_home, text="2. Audio Settings", font=("Arial", 10, "bold"), bg=self.bg_color,
                 fg="#888").pack(pady=(20, 5))

        self.btn_audio = tk.Button(self.frame_home, text="MICROPHONE: ON",
                                   command=self.toggle_audio,
                                   width=32, bg=self.active_toggle, fg="white", font=("Arial", 10, "bold"),
                                   relief="flat")
        self.btn_audio.pack(pady=5)

        # Start Button
        tk.Label(self.frame_home, text="3. Action", font=("Arial", 10, "bold"), bg=self.bg_color, fg="#888").pack(
            pady=(20, 5))
        self.btn_action = tk.Button(self.frame_home, text="INITIALIZE RECORDING",
                                    font=("Arial", 12, "bold"), bg=self.accent_color, fg="black",
                                    width=25, height=2, borderwidth=0, cursor="hand2",
                                    command=self.initiate_sequence)
        self.btn_action.pack(pady=10)

        self.lbl_status = tk.Label(self.frame_home, text="System Ready", font=("Consolas", 9), bg=self.bg_color,
                                   fg="#666")
        self.lbl_status.pack(pady=5)

    def setup_recording_screen(self):
        self.lbl_timer = tk.Label(self.frame_recording, text="00:00:00",
                                  font=("Impact", 45), bg=self.bg_color, fg=self.accent_color)
        self.lbl_timer.pack(pady=(60, 20))

        self.lbl_rec_stat = tk.Label(self.frame_recording, text="Recording...",
                                     font=("Arial", 12), bg=self.bg_color, fg="white")
        self.lbl_rec_stat.pack()

        tk.Button(self.frame_recording, text="STOP & SAVE",
                  font=("Arial", 12, "bold"), bg=self.stop_color, fg="white",
                  width=20, height=2, borderwidth=0, cursor="hand2",
                  command=self.stop_recording).pack(pady=50)

    # --- Logic ---
    def set_mode(self, mode):
        self.mode_var.set(mode)
        if mode == "full":
            self.btn_mode_full.config(bg=self.accent_color, fg="black")
            self.btn_mode_custom.config(bg="#424242", fg="white")
        else:
            self.btn_mode_full.config(bg="#424242", fg="white")
            self.btn_mode_custom.config(bg=self.accent_color, fg="black")

    def toggle_audio(self):
        self.audio_enabled = not self.audio_enabled
        if self.audio_enabled:
            self.btn_audio.config(text="MICROPHONE: ON", bg=self.active_toggle, fg="white")
        else:
            self.btn_audio.config(text="MICROPHONE: OFF", bg="#424242", fg="#888")

    def initiate_sequence(self):
        if self.mode_var.get() == "custom":
            self.root.iconify()
            self.launch_selection()
        else:
            with mss.mss() as sct:
                self.monitor_area = sct.monitors[1]
            self.start_countdown()

    def launch_selection(self):
        # Reuse previous selection logic (Simplified for brevity here)
        self.sel_root = Toplevel(self.root)
        self.sel_root.attributes("-fullscreen", True, "-alpha", 0.3)
        self.sel_root.config(bg="black", cursor="cross")
        self.sel_root.bind("<ButtonPress-1>", self.on_down)
        self.sel_root.bind("<B1-Motion>", self.on_drag)
        self.sel_root.bind("<ButtonRelease-1>", self.on_up)
        self.canvas = tk.Canvas(self.sel_root, bg="black", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.sel_root.attributes("-transparentcolor", "black")

    def on_down(self, event):
        self.start_x, self.start_y = event.x, event.y

    def on_drag(self, event):
        if hasattr(self, 'rect'): self.canvas.delete(self.rect)
        self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, event.x, event.y, outline="red", width=3)

    def on_up(self, event):
        x1, y1 = min(self.start_x, event.x), min(self.start_y, event.y)
        x2, y2 = max(self.start_x, event.x), max(self.start_y, event.y)
        self.monitor_area = {"top": y1, "left": x1, "width": x2 - x1, "height": y2 - y1}
        self.sel_root.destroy()
        self.root.deiconify()
        self.start_countdown()

    def start_countdown(self):
        # We save as mp4 directly now
        filename = filedialog.asksaveasfilename(defaultextension=".mp4", filetypes=[("MP4", "*.mp4")])
        if not filename: return
        self.out_filename = filename

        for i in range(3, 0, -1):
            self.btn_action.config(text=f"STARTING {i}...", bg="yellow")
            self.root.update()
            time.sleep(1)

        self.start_recording()

    def start_recording(self):
        self.is_recording = True
        self.start_time = datetime.datetime.now()
        self.show_frame(self.frame_recording)

        # Start Audio
        if self.audio_enabled:
            self.audio_recorder.start()

        # Start Video
        self.vid_thread = threading.Thread(target=self.record_video_loop)
        self.vid_thread.start()

        # Start Timer
        self.timer_thread = threading.Thread(target=self.update_timer)
        self.timer_thread.start()

    def update_timer(self):
        while self.is_recording:
            delta = datetime.datetime.now() - self.start_time
            self.lbl_timer.config(text=str(delta).split(".")[0])
            time.sleep(0.5)

    def record_video_loop(self):
        with mss.mss() as sct:
            # FIX: Use 'mp4v' (lowercase) instead of 'XVID'
            # This is the correct codec for .mp4 containers
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')

            # FIX: Change temp file extension to .mp4 to match the codec
            temp_filename = "temp_video.mp4"

            fps = 20.0
            w = self.monitor_area["width"]
            h = self.monitor_area["height"]

            out = cv2.VideoWriter(temp_filename, fourcc, fps, (w, h))

            while self.is_recording:
                img = np.array(sct.grab(self.monitor_area))
                # OpenCV uses BGR, MSS returns BGRA
                frame = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
                out.write(frame)

            out.release()

    def stop_recording(self):
        self.is_recording = False
        self.lbl_rec_stat.config(text="Processing...", fg="yellow")
        self.root.update()

        # Stop Audio
        if self.audio_enabled:
            self.audio_recorder.stop()

        # Wait for video thread
        if hasattr(self, 'vid_thread'):
            self.vid_thread.join()

        # MERGE LOGIC
        final_msg = ""
        if self.audio_enabled:
            self.lbl_rec_stat.config(text="Merging Audio/Video...", fg="cyan")
            self.root.update()
            success = self.merge_av()
            if success:
                final_msg = f"Saved to {self.out_filename}"
            else:
                final_msg = "Saved separately (FFmpeg missing)."
        else:
            # No audio, just rename temp video to final
            if os.path.exists("temp_video.avi"):
                os.replace("temp_video.avi", self.out_filename)
                final_msg = f"Saved Video to {self.out_filename}"

        messagebox.showinfo("Finished", final_msg)
        self.lbl_rec_stat.config(text="Done.")
        self.btn_action.config(text="INITIALIZE RECORDING", bg=self.accent_color)
        self.show_frame(self.frame_home)

    def merge_av(self):
        audio_file = "temp_audio.wav"
        video_file = "temp_video.mp4"  # <--- Updated to match the new temp name
        output_file = self.out_filename

        if not os.path.exists(audio_file) or not os.path.exists(video_file):
            return False

        # Command to merge
        cmd = [
            "ffmpeg", "-y",
            "-i", video_file,
            "-i", audio_file,
            "-c:v", "copy",  # Copy video stream directly (no re-encoding, fast!)
            "-c:a", "aac",  # Encode audio to AAC (standard for MP4)
            "-strict", "experimental",
            output_file
        ]

        try:
            # Hide console window for ffmpeg
            startupinfo = None
            if os.name == 'nt':
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

            subprocess.run(cmd, check=True, startupinfo=startupinfo)

            # Cleanup temps
            os.remove(video_file)
            os.remove(audio_file)
            return True
        except Exception as e:
            print(f"FFmpeg Merge Failed: {e}")
            return False


if __name__ == "__main__":
    root = tk.Tk()
    app = ModernRecorder(root)
    root.mainloop()