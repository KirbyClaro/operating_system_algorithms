import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os

class DiskSchedulingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Disk Scheduling Simulator")
        self.root.geometry("900x650")
        self.root.configure(bg="#2c3e50")

        # Simulation state variables
        self.sequence = []       # The order of execution
        self.current_step = 0    # Current index in the sequence
        self.total_seek_time = 0
        self.seek_sequence = []  # Full path including start

        self.setup_ui()

    def setup_ui(self):
        # --- Title Banner with Back to Main Menu Button ---
        title_frame = tk.Frame(self.root, bg="#34495e")
        title_frame.pack(fill=tk.X)

        # Main Menu Button
        self.menu_btn = tk.Button(title_frame, text="Main Menu", command=self.go_to_main_menu, bg="#e74c3c", fg="white", font=("Helvetica", 10, "bold"), padx=10, relief=tk.FLAT)
        self.menu_btn.pack(side=tk.LEFT, padx=15, pady=10)

        title_lbl = tk.Label(title_frame, text="Disk Scheduling Management", font=("Helvetica", 18, "bold"), fg="#ecf0f1", bg="#34495e", pady=10)
        title_lbl.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 100)) # Offset to keep title centered

        # --- Input Frame ---
        input_frame = tk.LabelFrame(self.root, text=" Configuration Inputs ", font=("Helvetica", 11, "bold"), fg="#ecf0f1", bg="#2c3e50", padx=15, pady=10)
        input_frame.pack(fill=tk.X, padx=15, pady=10)

        # Algorithm Selection
        tk.Label(input_frame, text="Select Algorithm:", fg="#ecf0f1", bg="#2c3e50").grid(row=0, column=0, sticky="w", pady=5)
        self.algo_var = tk.StringVar(value="FCFS")
        algos = ["FCFS", "SSTF", "SCAN", "C-SCAN", "LOOK", "C-LOOK"]
        self.algo_menu = ttk.Combobox(input_frame, textvariable=self.algo_var, values=algos, state="readonly", width=12)
        self.algo_menu.grid(row=0, column=1, padx=5, sticky="w")

        # Request Queue Input
        tk.Label(input_frame, text="Request Queue (comma-separated):", fg="#ecf0f1", bg="#2c3e50").grid(row=0, column=2, sticky="w", padx=10)
        self.queue_entry = tk.Entry(input_frame, width=30)
        self.queue_entry.insert(0, "98, 183, 37, 122, 14, 124, 65, 67")
        self.queue_entry.grid(row=0, column=3, padx=5, sticky="w")

        # Initial Head Position
        tk.Label(input_frame, text="Initial Head Pos:", fg="#ecf0f1", bg="#2c3e50").grid(row=1, column=0, sticky="w", pady=5)
        self.head_entry = tk.Entry(input_frame, width=8)
        self.head_entry.insert(0, "53")
        self.head_entry.grid(row=1, column=1, padx=5, sticky="w")

        # Disk Size / Direction
        tk.Label(input_frame, text="Max Disk Size:", fg="#ecf0f1", bg="#2c3e50").grid(row=1, column=2, sticky="w", padx=10)
        self.size_entry = tk.Entry(input_frame, width=8)
        self.size_entry.insert(0, "200")
        self.size_entry.grid(row=1, column=3, padx=5, sticky="w")

        tk.Label(input_frame, text="Direction (SCANs):", fg="#ecf0f1", bg="#2c3e50").grid(row=1, column=4, sticky="w", padx=10)
        self.dir_var = tk.StringVar(value="Left")
        self.dir_menu = ttk.Combobox(input_frame, textvariable=self.dir_var, values=["Left", "Right"], state="readonly", width=8)
        self.dir_menu.grid(row=1, column=5, padx=5, sticky="w")

        # Run Button
        self.run_btn = tk.Button(input_frame, text="Generate Simulation", command=self.calculate_scheduling, bg="#2ecc71", fg="white", font=("Helvetica", 10, "bold"), padx=10)
        self.run_btn.grid(row=0, column=4, columnspan=2, padx=15, sticky="e")

        # --- Simulation Display & Canvas ---
        sim_frame = tk.Frame(self.root, bg="#34495e", bd=2, relief=tk.SUNKEN)
        sim_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=5)

        self.canvas = tk.Canvas(sim_frame, bg="#ffffff")
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # --- Step Navigation & Info Footer ---
        footer_frame = tk.Frame(self.root, bg="#2c3e50", pady=10)
        footer_frame.pack(fill=tk.X, padx=15)

        # Back and Next Controls
        self.back_btn = tk.Button(footer_frame, text="◀ Back", command=self.prev_step, state=tk.DISABLED, width=10, font=("Helvetica", 10, "bold"))
        self.back_btn.pack(side=tk.LEFT, padx=5)

        self.next_btn = tk.Button(footer_frame, text="Next ▶", command=self.next_step, state=tk.DISABLED, width=10, font=("Helvetica", 10, "bold"))
        self.next_btn.pack(side=tk.LEFT, padx=5)

        # Metrics display
        self.status_lbl = tk.Label(footer_frame, text="Status: Waiting for input...", fg="#ecf0f1", bg="#2c3e50", font=("Helvetica", 11))
        self.status_lbl.pack(side=tk.RIGHT, padx=10)
        
   # --- Navigation Logic ---
    def go_to_main_menu(self):
        """Destroys this window and returns execution to main_viewer.py"""
        self.root.destroy()
        # If running from main_viewer, it naturally exits back to it. 
        # If opened independently, this safely relaunches main_viewer.py if it exists.
        if os.path.exists("main_viewer.py"):
            os.system(f"{sys.executable} main_viewer.py")

    # --- Disk Algorithms Implementations ---
    def calculate_scheduling(self):
        try:
            req_queue = [int(x.strip()) for x in self.queue_entry.get().split(",") if x.strip() != ""]
            head = int(self.head_entry.get())
            disk_size = int(self.size_entry.get())
            direction = self.dir_var.get().lower()
            algo = self.algo_var.get()
            

            if head >= disk_size or any(r >= disk_size for r in req_queue) or head < 0 or any(r < 0 for r in req_queue):
                raise ValueError("Head or requests cannot exceed track limits (0 to Disk Size - 1).")
        except ValueError as e:
            messagebox.showerror("Invalid Input", f"Please check your inputs.\nError: {e}")
            return

        self.seek_sequence = [head]
        self.total_seek_time = 0

        if algo == "FCFS":
            self.seek_sequence.extend(req_queue)
            
        elif algo == "SSTF":
            ready_list = req_queue.copy()
            curr_head = head
            while ready_list:
                closest = min(ready_list, key=lambda x: abs(x - curr_head))
                self.seek_sequence.append(closest)
                ready_list.remove(closest)
                curr_head = closest

        elif algo in ["SCAN", "C-SCAN", "LOOK", "C-LOOK"]:
            req_queue.sort()
            left = [x for x in req_queue if x < head]
            right = [x for x in req_queue if x >= head]

            if algo == "SCAN":
                if direction == "left":
                    self.seek_sequence.extend(reversed(left))
                    if left or right: self.seek_sequence.append(0)
                    self.seek_sequence.extend(right)
                else:
                    self.seek_sequence.extend(right)
                    if left or right: self.seek_sequence.append(disk_size - 1)
                    self.seek_sequence.extend(reversed(left))

            elif algo == "C-SCAN":
                if direction == "left":
                    self.seek_sequence.extend(reversed(left))
                    self.seek_sequence.append(0)
                    self.seek_sequence.append(disk_size - 1)
                    self.seek_sequence.extend(reversed(right))
                else:
                    self.seek_sequence.extend(right)
                    self.seek_sequence.append(disk_size - 1)
                    self.seek_sequence.append(0)
                    self.seek_sequence.extend(left)

            elif algo == "LOOK":
                if direction == "left":
                    self.seek_sequence.extend(reversed(left))
                    self.seek_sequence.extend(right)
                else:
                    self.seek_sequence.extend(right)
                    self.seek_sequence.extend(reversed(left))

            elif algo == "C-LOOK":
                if direction == "left":
                    self.seek_sequence.extend(reversed(left))
                    self.seek_sequence.extend(reversed(right))
                else:
                    self.seek_sequence.extend(right)
                    self.seek_sequence.extend(left)

        for i in range(len(self.seek_sequence) - 1):
            self.total_seek_time += abs(self.seek_sequence[i+1] - self.seek_sequence[i])

        self.current_step = 0
        self.back_btn.config(state=tk.DISABLED)
        self.next_btn.config(state=tk.NORMAL if len(self.seek_sequence) > 1 else tk.DISABLED)
        
        self.draw_chart(disk_size)

    # --- Canvas Simulation Renderer ---
    def draw_chart(self, disk_size):
        self.canvas.delete("all")
        
        c_width = self.canvas.winfo_width()
        c_height = self.canvas.winfo_height()
        
        if c_width <= 1: c_width = 860
        if c_height <= 1: c_height = 420

        padding_x = 50
        padding_y = 40
        
        graph_width = c_width - (2 * padding_x)
        def get_x(track_val):
            return padding_x + (track_val / (disk_size - 1)) * graph_width

        self.canvas.create_line(padding_x, padding_y, padding_x + graph_width, padding_y, fill="#7f8c8d", width=2)
        self.canvas.create_text(padding_x, padding_y - 15, text="0", font=("Helvetica", 9, "bold"))
        self.canvas.create_text(padding_x + graph_width, padding_y - 15, text=str(disk_size - 1), font=("Helvetica", 9, "bold"))

        total_steps = len(self.seek_sequence)
        step_height = (c_height - (2 * padding_y)) / max(total_steps - 1, 1)

        for i in range(self.current_step):
            x1 = get_x(self.seek_sequence[i])
            y1 = padding_y + (i * step_height)
            x2 = get_x(self.seek_sequence[i+1])
            y2 = padding_y + ((i + 1) * step_height)

            self.canvas.create_line(x1, y1, x2, y2, fill="#2980b9", width=2, arrow=tk.LAST)
            self.canvas.create_oval(x1-4, y1-4, x1+4, y1+4, fill="#e74c3c")
            self.canvas.create_text(x1, y1 - 12, text=str(self.seek_sequence[i]), font=("Helvetica", 8), fill="#34495e")

        if self.seek_sequence:
            last_idx = self.current_step
            xl = get_x(self.seek_sequence[last_idx])
            yl = padding_y + (last_idx * step_height)
            self.canvas.create_oval(xl-5, yl-5, xl+5, yl+5, fill="#2ecc71")
            self.canvas.create_text(xl, yl - 12, text=str(self.seek_sequence[last_idx]), font=("Helvetica", 9, "bold"), fill="#27ae60")

        curr_seek = 0
        for i in range(self.current_step):
            curr_seek += abs(self.seek_sequence[i+1] - self.seek_sequence[i])

        self.status_lbl.config(
            text=f"Step: {self.current_step}/{total_steps - 1}  |  Current Seek: {curr_seek}  |  Total Path Seek Time: {self.total_seek_time}"
        )

    def next_step(self):
        if self.current_step < len(self.seek_sequence) - 1:
            self.current_step += 1
            disk_size = int(self.size_entry.get())
            self.draw_chart(disk_size)
            self.back_btn.config(state=tk.NORMAL)
            
        if self.current_step == len(self.seek_sequence) - 1:
            self.next_btn.config(state=tk.DISABLED)

    def prev_step(self):
        if self.current_step > 0:
            self.current_step -= 1
            disk_size = int(self.size_entry.get())
            self.draw_chart(disk_size)
            self.next_btn.config(state=tk.NORMAL)
            
        if self.current_step == 0:
            self.back_btn.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = DiskSchedulingApp(root)
    root.bind("<Configure>", lambda e: app.draw_chart(int(app.size_entry.get())) if hasattr(app, 'seek_sequence') and app.seek_sequence else None)
    root.mainloop()