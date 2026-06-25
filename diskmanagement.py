import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os

class ModernDiskSchedulingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("OS Architecture & Algorithms: Disk Management")
        self.root.geometry("1050x780")
        self.root.minsize(950, 700)
        
        # New Light Theme Palette (White, Greys, and Bright Blue)
        self.colors = {
            "bg_dark": "#FFFFFF",       # Main app background (Very light grey/off-white)
            "bg_card": "#ffffff",       # Pure white for containers/inputs
            "text_light": "#0f172a",    # Dark slate for primary readable text
            "text_muted": "#64748b",    # Medium grey for secondary text/labels
            "accent_blue": "#0E4C6B",   # Deep blue highlights
            "btn_blue": "#104963",      # Vibrant blue for trigger buttons
            "accent_red": "#701d1d",    # Bright red for Main Menu
            "canvas_bg_start": "#ffffff",# Gradient start (Pure White)
            "canvas_bg_end": "#f1f5f9",  # Gradient end (Soft light blue-grey)
            "path_line": "#154e68",     # Light blue vector pathing
            "node_point": "#ffffff"     # White node inner markers
        }
        
        self.root.configure(bg=self.colors["bg_dark"])

        # Core Application State Engine
        self.seek_sequence = []
        self.current_step = 0
        self.total_seek_time = 0
        
        # Auto-Simulation Engine States
        self.is_playing = False
        self.auto_job = None

        # Build UI
        self.configure_styles()
        self.create_widgets()

    def configure_styles(self):
        """Initializes system TTK styling overrides."""
        self.style = ttk.Style()
        self.style.theme_use("clam")
        
        self.style.configure("TCombobox", 
            fieldbackground=self.colors["bg_card"], 
            background=self.colors["bg_card"], 
            foreground=self.colors["text_light"],
            bordercolor="#cbd5e1",
            lightcolor="#ffffff",
            darkcolor="#ffffff",
            arrowcolor=self.colors["text_light"]
        )

    def create_widgets(self):
        """Constructs centered grid structures and subcomponents."""
        # 1. Top Control Bar Header (Centered)
        self.header_frame = tk.Frame(self.root, bg=self.colors["bg_dark"], height=60)
        self.header_frame.pack(fill=tk.X, padx=20, pady=15)
        self.header_frame.pack_propagate(False)

        self.menu_btn = tk.Button(
            self.header_frame, text="🏠 Main Menu", command=self.go_to_main_menu,
            bg=self.colors["accent_red"], fg="white", font=("Segoe UI", 10, "bold"),
            bd=0, cursor="hand2", activebackground="#dc2626", activeforeground="white",
            padx=15
        )
        self.menu_btn.pack(side=tk.LEFT, fill=tk.Y)

        # Center-aligned Header Title Text
        self.title_lbl = tk.Label(
            self.header_frame, text="DISK SCHEDULING CONTROLLER", 
            font=("Segoe UI", 16, "bold"), fg=self.colors["text_light"], bg=self.colors["bg_dark"]
        )
        self.title_lbl.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=(0, 100))

        # 2. Centered Dashboard Configuration Layout Card
        self.center_wrapper = tk.Frame(self.root, bg=self.colors["bg_dark"])
        self.center_wrapper.pack(fill=tk.X, padx=20)

        # Added a thin border to the card so it pops against the off-white background
        self.input_card = tk.Frame(self.center_wrapper, bg=self.colors["bg_card"], highlightbackground="#e2e8f0", highlightthickness=1, padx=20, pady=15)
        self.input_card.pack(anchor=tk.CENTER)

        # Configuration UI Forms Grid Construction
        lbl_opts = {'font': ("Segoe UI", 9, "bold"), 'fg': self.colors["text_muted"], 'bg': self.colors["bg_card"]}
        # Changed text color to dark and insert cursor to black for visibility
        entry_opts = {'bg': self.colors["bg_card"], 'fg': self.colors["text_light"], 'bd': 1, 'relief': tk.SOLID, 'insertbackground': "black", 'font': ("Consolas", 11), 'justify': tk.CENTER}

        # Header Labels (Row 0)
        tk.Label(self.input_card, text="Strategy", **lbl_opts).grid(row=0, column=0, padx=15, pady=(5, 2))
        tk.Label(self.input_card, text="Track Cylinder Requests Queue", **lbl_opts).grid(row=0, column=1, padx=15, pady=(5, 2))
        tk.Label(self.input_card, text="Start Head", **lbl_opts).grid(row=0, column=2, padx=15, pady=(5, 2))
        tk.Label(self.input_card, text="Max Boundary", **lbl_opts).grid(row=0, column=3, padx=15, pady=(5, 2))
        tk.Label(self.input_card, text="Sweep Vector", **lbl_opts).grid(row=0, column=4, padx=15, pady=(5, 2))

        # Form Interactive Fields (Row 1)
        self.algo_var = tk.StringVar(value="FCFS")
        self.algo_menu = ttk.Combobox(self.input_card, textvariable=self.algo_var, values=["FCFS", "SSTF", "SCAN", "C-SCAN", "LOOK", "C-LOOK"], state="readonly", width=10)
        self.algo_menu.grid(row=1, column=0, padx=15, pady=(0, 10))

        self.queue_entry = tk.Entry(self.input_card, width=32, **entry_opts)
        self.queue_entry.insert(0, "98, 183, 37, 122, 14, 124, 65, 67")
        self.queue_entry.grid(row=1, column=1, padx=15, pady=(0, 10))

        self.head_entry = tk.Entry(self.input_card, width=8, **entry_opts)
        self.head_entry.insert(0, "53")
        self.head_entry.grid(row=1, column=2, padx=15, pady=(0, 10))

        self.size_entry = tk.Entry(self.input_card, width=8, **entry_opts)
        self.size_entry.insert(0, "200")
        self.size_entry.grid(row=1, column=3, padx=15, pady=(0, 10))

        self.dir_var = tk.StringVar(value="Left")
        self.dir_menu = ttk.Combobox(self.input_card, textvariable=self.dir_var, values=["Left", "Right"], state="readonly", width=8)
        self.dir_menu.grid(row=1, column=4, padx=15, pady=(0, 10))

        # Core Calculation Execution Trigger
        self.run_btn = tk.Button(
            self.input_card, text="⚡ Compute Vectors", command=self.calculate_scheduling,
            bg=self.colors["btn_blue"], fg="white", font=("Segoe UI", 10, "bold"),
            bd=0, cursor="hand2", activebackground="#0284c7", activeforeground="white", padx=15, pady=4
        )
        self.run_btn.grid(row=1, column=5, padx=15, pady=(0, 10))

        # 3. Canvas Screen Display Frame
        self.canvas_card = tk.Frame(self.root, bg=self.colors["bg_card"], highlightbackground="#e2e8f0", highlightthickness=1)
        self.canvas_card.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        self.canvas = tk.Canvas(self.canvas_card, bg=self.colors["canvas_bg_start"], bd=0, highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

        # 4. Universal Navigation Footer Frame
        self.footer_frame = tk.Frame(self.root, bg=self.colors["bg_dark"], height=60)
        self.footer_frame.pack(fill=tk.X, padx=20, pady=15)

        self.ctrl_layout = tk.Frame(self.footer_frame, bg=self.colors["bg_dark"])
        self.ctrl_layout.pack(anchor=tk.CENTER)

        btn_style = {'font': ("Segoe UI", 9, "bold"), 'bd': 0, 'cursor': "hand2", 'width': 12, 'pady': 6}
        
        self.back_btn = tk.Button(self.ctrl_layout, text="◀ Manual Back", command=self.prev_step, state=tk.DISABLED, bg="#e2e8f0", fg="#94a3b8", **btn_style)
        self.back_btn.pack(side=tk.LEFT, padx=6)

        self.play_btn = tk.Button(self.ctrl_layout, text="▶ Auto Play", command=self.toggle_auto_play, state=tk.DISABLED, bg="#e2e8f0", fg="#94a3b8", **btn_style)
        self.play_btn.pack(side=tk.LEFT, padx=6)

        self.next_btn = tk.Button(self.ctrl_layout, text="Manual Next ▶", command=self.next_step, state=tk.DISABLED, bg="#e2e8f0", fg="#94a3b8", **btn_style)
        self.next_btn.pack(side=tk.LEFT, padx=6)

        self.status_lbl = tk.Label(
            self.root, text="System State: Awaiting Analytical Initialization Routine Parameters.",
            font=("Consolas", 10), fg=self.colors["text_muted"], bg=self.colors["bg_dark"], justify=tk.CENTER
        )
        self.status_lbl.pack(fill=tk.X, side=tk.BOTTOM, pady=(0, 10))

    def draw_gradient_background(self, width, height):
        self.canvas.delete("gradient")
        steps = 64  
        sr, sg, sb = self.root.winfo_rgb(self.colors["canvas_bg_start"])
        er, eg, eb = self.root.winfo_rgb(self.colors["canvas_bg_end"])
        
        sr, sg, sb = sr >> 8, sg >> 8, sb >> 8
        er, eg, eb = er >> 8, eg >> 8, eb >> 8

        slice_h = height / steps
        for i in range(steps):
            t = i / steps
            r = int(sr + t * (er - sr))
            g = int(sg + t * (eg - sg))
            b = int(sb + t * (eb - sb))
            color_hex = f"#{r:02x}{g:02x}{b:02x}"
            
            self.canvas.create_rectangle(
                0, i * slice_h, width, (i + 1) * slice_h,
                fill=color_hex, outline=color_hex, tags="gradient"
            )
        self.canvas.tag_lower("gradient")

    def toggle_auto_play(self):
        if self.is_playing:
            self.pause_auto_play()
        else:
            self.start_auto_play()

    def start_auto_play(self):
        self.is_playing = True
        self.play_btn.config(text="⏸ Pause", bg=self.colors["accent_red"], fg="white")
        self.run_auto_loop()

    def pause_auto_play(self):
        self.is_playing = False
        self.play_btn.config(text="▶ Auto Play", bg=self.colors["btn_blue"], fg="white")
        if self.auto_job:
            self.root.after_cancel(self.auto_job)
            self.auto_job = None

    def run_auto_loop(self):
        if not self.is_playing:
            return
        if self.current_step < len(self.seek_sequence) - 1:
            self.next_step()
            self.auto_job = self.root.after(800, self.run_auto_loop)
        else:
            self.pause_auto_play()

    def calculate_scheduling(self):
        self.pause_auto_play()
        try:
            req_queue = [int(x.strip()) for x in self.queue_entry.get().split(",") if x.strip() != ""]
            head = int(self.head_entry.get())
            disk_size = int(self.size_entry.get())
            direction = self.dir_var.get().lower()
            algo = self.algo_var.get()

            if head >= disk_size or any(r >= disk_size for r in req_queue) or head < 0 or any(r < 0 for r in req_queue):
                raise ValueError("Cylinder paths overflow configured hardware limit boundaries.")
        except ValueError as e:
            messagebox.showerror("Validation Boundary Failure", f"Please check config inputs.\nError: {e}")
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
        self.update_navigation_buttons()
        self.draw_chart(disk_size)

    def draw_chart(self, disk_size):
        c_width = self.canvas.winfo_width()
        c_height = self.canvas.winfo_height()
        if c_width <= 1: c_width = 980
        if c_height <= 1: c_height = 450

        self.draw_gradient_background(c_width, c_height)
        self.canvas.delete("vector")

        padding_x, padding_y = 70, 55
        graph_width = c_width - (2 * padding_x)
        
        def get_x(track_val):
            return padding_x + (track_val / (disk_size - 1)) * graph_width

        # Coordinate Grid Axes Visualizations
        self.canvas.create_line(padding_x, padding_y, padding_x + graph_width, padding_y, fill="#94a3b8", width=2, tags="vector")
        self.canvas.create_text(padding_x, padding_y - 20, text="Cylinder 0", font=("Segoe UI", 9, "bold"), fill=self.colors["text_muted"], tags="vector")
        self.canvas.create_text(padding_x + graph_width, padding_y - 20, text=f"Cylinder {disk_size - 1}", font=("Segoe UI", 9, "bold"), fill=self.colors["text_muted"], tags="vector")

        total_steps = len(self.seek_sequence)
        step_height = (c_height - (2 * padding_y)) / max(total_steps - 1, 1)

        for i in range(self.current_step):
            x1, y1 = get_x(self.seek_sequence[i]), padding_y + (i * step_height)
            x2, y2 = get_x(self.seek_sequence[i+1]), padding_y + ((i + 1) * step_height)

            self.canvas.create_line(x1, y1, x2, y2, fill=self.colors["path_line"], width=3, arrow=tk.LAST, arrowshape=(10, 12, 4), tags="vector")
            self.canvas.create_oval(x1-4, y1-4, x1+4, y1+4, fill=self.colors["node_point"], outline=self.colors["accent_blue"], width=2, tags="vector")
            self.canvas.create_text(x1, y1 - 15, text=str(self.seek_sequence[i]), font=("Consolas", 9, "bold"), fill=self.colors["text_light"], tags="vector")

        if self.seek_sequence:
            xl = get_x(self.seek_sequence[self.current_step])
            yl = padding_y + (self.current_step * step_height)
            self.canvas.create_oval(xl-6, yl-6, xl+6, yl+6, fill=self.colors["accent_blue"], outline=self.colors["node_point"], width=2, tags="vector")
            self.canvas.create_text(xl, yl - 18, text=f"📍 Active Head: {self.seek_sequence[self.current_step]}", font=("Segoe UI", 9, "bold"), fill=self.colors["accent_blue"], tags="vector")

        curr_seek = sum(abs(self.seek_sequence[i+1] - self.seek_sequence[i]) for i in range(self.current_step))
        self.status_lbl.config(
            text=f"EXECUTION MATRIX STATUS  ->  Step: [{self.current_step}/{total_steps - 1}]    |    Accumulated Head Travel: [{curr_seek}] Tracks    |    Total Completed Algorithmic Cost Profile: [{self.total_seek_time}]",
            fg=self.colors["text_light"]
        )

    def next_step(self):
        if self.current_step < len(self.seek_sequence) - 1:
            self.current_step += 1
            self.draw_chart(int(self.size_entry.get()))
            self.update_navigation_buttons()
        else:
            self.pause_auto_play()

    def prev_step(self):
        if self.current_step > 0:
            self.current_step -= 1
            self.draw_chart(int(self.size_entry.get()))
            self.update_navigation_buttons()

    def update_navigation_buttons(self):
        total_len = len(self.seek_sequence)
        
        # Back Actions State Triggers
        if self.current_step == 0:
            self.back_btn.config(state=tk.DISABLED, bg="#e2e8f0", fg="#94a3b8")
        else:
            self.back_btn.config(state=tk.NORMAL, bg=self.colors["btn_blue"], fg="white")

        # Auto & Forward Step Logic Triggers
        if total_len <= 1:
            self.next_btn.config(state=tk.DISABLED, bg="#e2e8f0", fg="#94a3b8")
            self.play_btn.config(state=tk.DISABLED, bg="#e2e8f0", fg="#94a3b8")
        elif self.current_step == total_len - 1:
            self.next_btn.config(state=tk.DISABLED, bg="#e2e8f0", fg="#94a3b8")
            self.play_btn.config(state=tk.DISABLED, bg="#e2e8f0", fg="#94a3b8")
        else:
            self.next_btn.config(state=tk.NORMAL, bg=self.colors["btn_blue"], fg="white")
            if not self.is_playing:
                self.play_btn.config(state=tk.NORMAL, bg=self.colors["btn_blue"], fg="white")

    def go_to_main_menu(self):
        self.pause_auto_play()
        self.root.destroy()
        if os.path.exists("main_viewer.py"):
            os.system(f"{sys.executable} main_viewer.py")

if __name__ == "__main__":
    root = tk.Tk()
    app = ModernDiskSchedulingApp(root)
    root.bind("<Configure>", lambda e: app.draw_chart(int(app.size_entry.get())) if app.seek_sequence else None)
    root.mainloop()