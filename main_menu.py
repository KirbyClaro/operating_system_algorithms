import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import os
import sys

class OSProjectDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("OS Architecture & Algorithms Dashboard")
        self.root.geometry("900x700") # Expanded slightly to fit the 2x2 grid beautifully
        self.root.configure(bg="#2d2d2d")

        # --- Styling ---
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Header.TLabel", font=("Segoe UI", 24, "bold"), background="#2d2d2d", foreground="#ffffff")
        style.configure("Category.TLabel", font=("Segoe UI", 14, "bold"), background="#2d2d2d", foreground="#4da6ff")
        style.configure("Launch.TButton", font=("Segoe UI", 11), padding=6)

        # --- Header ---
        header_frame = tk.Frame(self.root, bg="#1e1e1e", pady=20)
        header_frame.pack(fill=tk.X)
        ttk.Label(header_frame, text="Operating System Algorithms", style="Header.TLabel").pack()
        ttk.Label(header_frame, text="Select a module to launch the interactive simulation", background="#1e1e1e", foreground="#aaaaaa", font=("Segoe UI", 10)).pack()

        # --- Main Content Area (Grid Setup) ---
        content_frame = tk.Frame(self.root, bg="#2d2d2d", padx=40, pady=30)
        content_frame.pack(fill=tk.BOTH, expand=True)

        # Configure a 2x2 grid
        content_frame.columnconfigure(0, weight=1)
        content_frame.columnconfigure(1, weight=1)
        content_frame.rowconfigure(0, weight=1)
        content_frame.rowconfigure(1, weight=1)

        # --- Quadrant 1: CPU Scheduling (Top Left) ---
        cpu_frame = tk.Frame(content_frame, bg="#2d2d2d")
        cpu_frame.grid(row=0, column=0, sticky="n", padx=20, pady=10)
        
        ttk.Label(cpu_frame, text="CPU Scheduling", style="Category.TLabel").pack(pady=(0, 15))
        self.create_launch_button(cpu_frame, "First-Come, First-Served", "cpu_scheduling/first_come_first_served.py")
        self.create_launch_button(cpu_frame, "Shortest Job First", "cpu_scheduling/shortest_job_first.py")
        self.create_launch_button(cpu_frame, "Priority Scheduling", "cpu_scheduling/priority.py")
        self.create_launch_button(cpu_frame, "Round Robin", "cpu_scheduling/round_robin.py")

        # --- Quadrant 2: Memory Management (Top Right) ---
        mem_frame = tk.Frame(content_frame, bg="#2d2d2d")
        mem_frame.grid(row=0, column=1, sticky="n", padx=20, pady=10)
        
        ttk.Label(mem_frame, text="Memory Management", style="Category.TLabel").pack(pady=(0, 15))
        self.create_launch_button(mem_frame, "MFT (Fixed Tasks)", "memory_management/mft.py")
        self.create_launch_button(mem_frame, "MVT (Variable Tasks)", "memory_management/mvt.py")

        # --- Quadrant 3: Virtual Memory (Bottom Left) ---
        vm_frame = tk.Frame(content_frame, bg="#2d2d2d")
        vm_frame.grid(row=1, column=0, sticky="n", padx=20, pady=20)
        
        ttk.Label(vm_frame, text="Virtual Memory", style="Category.TLabel").pack(pady=(0, 15))
        self.create_launch_button(vm_frame, "FIFO Replacement", "virtual_memory/fifo_replacement.py")
        self.create_launch_button(vm_frame, "LRU Replacement", "virtual_memory/lru_replacement.py")
        self.create_launch_button(vm_frame, "LFU Replacement", "virtual_memory/lfu_replacement.py")
        self.create_launch_button(vm_frame, "MFU Replacement", "virtual_memory/mfu_replacement.py")
        self.create_launch_button(vm_frame, "Optimal Replacement", "virtual_memory/opt_replacement.py")

        # --- Quadrant 4: Disk Scheduling (Bottom Right) ---
        disk_frame = tk.Frame(content_frame, bg="#2d2d2d")
        disk_frame.grid(row=1, column=1, sticky="n", padx=20, pady=20)
        
        ttk.Label(disk_frame, text="Disk Scheduling", style="Category.TLabel").pack(pady=(0, 15))
        self.create_launch_button(disk_frame, "Disk Management", "disk_scheduling/diskmanagement.py")

        # --- Exit Button ---
        ttk.Button(self.root, text="Exit Dashboard", command=self.root.destroy, style="Launch.TButton").pack(side=tk.BOTTOM, pady=20)

    def create_launch_button(self, parent, text, filepath):
        """Creates a button that runs the specified python file when clicked."""
        btn = ttk.Button(parent, text=text, style="Launch.TButton", 
                         command=lambda: self.launch_program(filepath))
        btn.pack(fill=tk.X, pady=5)

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