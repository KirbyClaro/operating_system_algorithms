import tkinter as tk
from tkinter import ttk, messagebox

class SJFSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Shortest Job First (SJF) Scheduling")
        self.root.geometry("650x600")
        self.root.configure(bg="#f4f4f9")

        style = ttk.Style()
        style.theme_use('clam')

        main_frame = tk.Frame(self.root, bg="#f4f4f9", padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(main_frame, text="SJF CPU Scheduling", font=("Segoe UI", 16, "bold"), bg="#f4f4f9").pack(pady=(0, 10))

        # --- Mode Selection (Preemptive vs Non-Preemptive) ---
        self.mode_var = tk.StringVar(value="Non-Preemptive")
        mode_frame = tk.Frame(main_frame, bg="#f4f4f9")
        mode_frame.pack(pady=5)
        
        ttk.Radiobutton(mode_frame, text="Non-Preemptive", variable=self.mode_var, value="Non-Preemptive").pack(side=tk.LEFT, padx=10)
        ttk.Radiobutton(mode_frame, text="Preemptive (SRTF)", variable=self.mode_var, value="Preemptive").pack(side=tk.LEFT, padx=10)

        # --- Input Section ---
        input_frame = tk.Frame(main_frame, bg="#f4f4f9")
        input_frame.pack(fill=tk.X, pady=10)

        tk.Label(input_frame, text="Arrival Times (comma-separated):", bg="#f4f4f9").grid(row=0, column=0, sticky="w", pady=5)
        self.entry_arrival = ttk.Entry(input_frame, width=40)
        self.entry_arrival.grid(row=0, column=1, padx=10, pady=5)
        self.entry_arrival.insert(0, "0, 1, 2, 3")

        tk.Label(input_frame, text="Burst Times (comma-separated):", bg="#f4f4f9").grid(row=1, column=0, sticky="w", pady=5)
        self.entry_burst = ttk.Entry(input_frame, width=40)
        self.entry_burst.grid(row=1, column=1, padx=10, pady=5)
        self.entry_burst.insert(0, "8, 4, 9, 5")

        # --- Buttons ---
        btn_frame = tk.Frame(main_frame, bg="#f4f4f9")
        btn_frame.pack(pady=10)

        ttk.Button(btn_frame, text="Run Simulation", command=self.calculate_sjf).pack(side=tk.LEFT, padx=10)
        ttk.Button(btn_frame, text="Clear", command=self.clear_inputs).pack(side=tk.LEFT, padx=10)
        ttk.Button(btn_frame, text="⬅ Back", command=self.root.destroy).pack(side=tk.LEFT, padx=10)

        # --- Results Table ---
        columns = ("PID", "AT", "BT", "CT", "TAT", "WT")
        self.tree = ttk.Treeview(main_frame, columns=columns, show="headings", height=8)
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=90, anchor=tk.CENTER)
        self.tree.pack(fill=tk.X, pady=10)

        # --- Averages Display ---
        self.lbl_averages = tk.Label(main_frame, text="Average TAT: 0.00 ms  |  Average WT: 0.00 ms", font=("Segoe UI", 11, "bold"), bg="#f4f4f9")
        self.lbl_averages.pack(pady=10)

    def calculate_sjf(self):
        print(f"Algorithm logic for {self.mode_var.get()} will go here!")

    def clear_inputs(self):
        self.entry_arrival.delete(0, tk.END)
        self.entry_burst.delete(0, tk.END)
        for item in self.tree.get_children(): self.tree.delete(item)
        self.lbl_averages.config(text="Average TAT: 0.00 ms  |  Average WT: 0.00 ms")

if __name__ == "__main__":
    root = tk.Tk()
    app = SJFSimulator(root)
    root.mainloop()