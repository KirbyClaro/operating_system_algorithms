import tkinter as tk
from tkinter import ttk, messagebox

class FCFSSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("FCFS Scheduling - Setup")
        self.root.geometry("650x500")
        self.root.configure(bg="#f4f4f9")

        main_frame = tk.Frame(self.root, bg="#f4f4f9", padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(main_frame, text="FCFS CPU Scheduling", font=("Segoe UI", 16, "bold"), bg="#f4f4f9").pack(pady=(0, 15))

        # --- Input Section ---
        input_frame = tk.Frame(main_frame, bg="#f4f4f9")
        input_frame.pack(fill=tk.X, pady=10)

        tk.Label(input_frame, text="Arrival Times (comma-separated):", bg="#f4f4f9").grid(row=0, column=0, sticky="w", pady=5)
        self.entry_arrival = ttk.Entry(input_frame, width=40)
        self.entry_arrival.grid(row=0, column=1, padx=10, pady=5)
        self.entry_arrival.insert(0, "0, 2, 4, 6")

        tk.Label(input_frame, text="Burst Times (comma-separated):", bg="#f4f4f9").grid(row=1, column=0, sticky="w", pady=5)
        self.entry_burst = ttk.Entry(input_frame, width=40)
        self.entry_burst.grid(row=1, column=1, padx=10, pady=5)
        self.entry_burst.insert(0, "4, 3, 1, 2")

        # --- Buttons ---
        btn_frame = tk.Frame(main_frame, bg="#f4f4f9")
        btn_frame.pack(pady=15)

        ttk.Button(btn_frame, text="Run Simulation", command=self.calculate_fcfs).pack(side=tk.LEFT, padx=10)
        ttk.Button(btn_frame, text="⬅ Back", command=self.root.destroy).pack(side=tk.LEFT, padx=10)

    def calculate_fcfs(self):
        # Placeholder for the next commit
        print("Algorithm logic will go here!")

if __name__ == "__main__":
    root = tk.Tk()
    app = FCFSSimulator(root)
    root.mainloop()