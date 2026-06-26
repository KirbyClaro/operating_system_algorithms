import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import os
import sys

class OSProjectDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("OS Architecture & Algorithms Dashboard")
        self.root.geometry("950x750")
        
        # --- Color Palette ---
        self.bg_color = "#121212"       
        self.card_color = "#1e1e1e"     
        self.text_color = "#ffffff"     
        self.sub_text = "#aaaaaa"       
        self.accent_color = "#4da6ff"   
        self.btn_bg = "#2d2d2d"         
        self.btn_hover = "#3d3d3d"      

        self.root.configure(bg=self.bg_color)

        # --- Styling ---
        style = ttk.Style()
        style.theme_use('clam')
        
        # Text Styles
        style.configure("Title.TLabel", font=("Segoe UI", 26, "bold"), background=self.bg_color, foreground=self.text_color)
        style.configure("Subtitle.TLabel", font=("Segoe UI", 11), background=self.bg_color, foreground=self.sub_text)
        style.configure("Category.TLabel", font=("Segoe UI", 13, "bold"), background=self.card_color, foreground=self.accent_color)
        
        # Button Styles (Removes default borders and adds padding)
        style.configure("Launch.TButton", font=("Segoe UI", 10, "bold"), padding=10, background=self.btn_bg, foreground=self.text_color, borderwidth=0)
        style.map("Launch.TButton", background=[("active", self.btn_hover)])

        # --- Header ---
        header_frame = tk.Frame(self.root, bg=self.bg_color, pady=30)
        header_frame.pack(fill=tk.X)
        ttk.Label(header_frame, text="OS ALGORITHMS DASHBOARD", style="Title.TLabel").pack()
        ttk.Label(header_frame, text="Select a module to launch the interactive simulation suite", style="Subtitle.TLabel").pack(pady=(5, 0))

        # --- Main Content Area (Grid Setup) ---
        content_frame = tk.Frame(self.root, bg=self.bg_color, padx=40, pady=10)
        content_frame.pack(fill=tk.BOTH, expand=True)

        content_frame.columnconfigure(0, weight=1)
        content_frame.columnconfigure(1, weight=1)
        content_frame.rowconfigure(0, weight=1)
        content_frame.rowconfigure(1, weight=1)

        # --- Quadrant 1: CPU Scheduling ---
        cpu_frame = self.create_card(content_frame, 0, 0, "CPU Scheduling")
        self.create_launch_button(cpu_frame, "▶ First-Come, First-Served", "cpu_scheduling/first_come_first_served.py")
        self.create_launch_button(cpu_frame, "▶ Shortest Job First", "cpu_scheduling/shortest_job_first.py")
        self.create_launch_button(cpu_frame, "▶ Priority Scheduling", "cpu_scheduling/priority.py")
        self.create_launch_button(cpu_frame, "▶ Round Robin", "cpu_scheduling/round_robin.py")

        # --- Quadrant 2: Memory Management ---
        mem_frame = self.create_card(content_frame, 0, 1, "Memory Management")
        self.create_launch_button(mem_frame, "▶ MFT (Fixed Tasks)", "memory_management/mft.py")
        self.create_launch_button(mem_frame, "▶ MVT (Variable Tasks)", "memory_management/mvt.py")

        # --- Quadrant 3: Virtual Memory ---
        vm_frame = self.create_card(content_frame, 1, 0, "Virtual Memory")
        self.create_launch_button(vm_frame, "▶ FIFO Replacement", "virtual_memory/fifo_replacement.py")
        self.create_launch_button(vm_frame, "▶ LRU Replacement", "virtual_memory/lru_replacement.py")
        self.create_launch_button(vm_frame, "▶ LFU Replacement", "virtual_memory/lfu_replacement.py")
        self.create_launch_button(vm_frame, "▶ MFU Replacement", "virtual_memory/mfu_replacement.py")
        self.create_launch_button(vm_frame, "▶ Optimal Replacement", "virtual_memory/opt_replacement.py")

        # --- Quadrant 4: Disk Scheduling ---
        disk_frame = self.create_card(content_frame, 1, 1, "Disk Scheduling")
        self.create_launch_button(disk_frame, "▶ Disk Management", "disk_scheduling/diskmanagement.py")

        # --- Exit Button ---
        exit_frame = tk.Frame(self.root, bg=self.bg_color)
        exit_frame.pack(fill=tk.X, side=tk.BOTTOM, pady=25)
        ttk.Button(exit_frame, text="✖ Exit Dashboard", command=self.root.destroy, style="Launch.TButton", cursor="hand2").pack()

    def create_card(self, parent, row, col, title):
        """Creates a styled 'card' frame for each category to separate them visually."""
        # Outer frame to act as a subtle 1px border
        outer_frame = tk.Frame(parent, bg="#333333", padx=1, pady=1) 
        outer_frame.grid(row=row, column=col, sticky="nsew", padx=15, pady=15)
        
        # Inner frame (the actual card background)
        inner_frame = tk.Frame(outer_frame, bg=self.card_color, padx=25, pady=25)
        inner_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(inner_frame, text=title.upper(), style="Category.TLabel").pack(pady=(0, 10), anchor="w")
        
        # Decorative blue line under the title
        separator = tk.Frame(inner_frame, bg=self.accent_color, height=2)
        separator.pack(fill=tk.X, pady=(0, 15))
        
        return inner_frame

    def create_launch_button(self, parent, text, filepath):
        """Creates a button that runs the specified python file when clicked."""
        # Added cursor="hand2" so the mouse turns into a pointer finger when hovering over buttons
        btn = ttk.Button(parent, text=text, style="Launch.TButton", cursor="hand2",
                         command=lambda: self.launch_program(filepath))
        btn.pack(fill=tk.X, pady=6)

    def launch_program(self, filepath):
        """Uses subprocess to open the selected python file as a new application."""
        base_dir = os.path.dirname(os.path.abspath(__file__))
        full_path = os.path.join(base_dir, filepath)

        if os.path.exists(full_path):
            try:
                subprocess.Popen([sys.executable, full_path])
            except Exception as e:
                messagebox.showerror("Execution Error", f"Failed to launch {filepath}.\nError: {e}")
        else:
            messagebox.showerror("File Not Found", f"Could not find the file:\n{filepath}\n\nPlease check your folder structure.")

if __name__ == "__main__":
    root = tk.Tk()
    app = OSProjectDashboard(root)
    root.mainloop()