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
        try:
            arrival_times = list(map(int, self.entry_arrival.get().split(',')))
            burst_times = list(map(int, self.entry_burst.get().split(',')))
            n = len(arrival_times)

            if n != len(burst_times):
                messagebox.showerror("Input Error", "Arrival Times and Burst Times count must match.")
                return

            mode = self.mode_var.get()
            
            # Setup process dictionary
            processes = []
            for i in range(n):
                processes.append({
                    "pid": f"P{i+1}", "at": arrival_times[i], "bt": burst_times[i], 
                    "rt": burst_times[i], "ct": 0, "tat": 0, "wt": 0, "completed": False
                })

            current_time = 0
            completed_count = 0
            
            # Clear table
            for item in self.tree.get_children(): self.tree.delete(item)

            if mode == "Non-Preemptive":
                while completed_count < n:
                    # Find available processes that have arrived and are not completed
                    available = [p for p in processes if p["at"] <= current_time and not p["completed"]]
                    
                    if not available:
                        current_time += 1 # CPU is idle, advance time
                        continue
                    
                    # Sort available by Burst Time (the core SJF rule)
                    available.sort(key=lambda x: x["bt"])
                    current_process = available[0]
                    
                    # Execute process to completion
                    current_time += current_process["bt"]
                    current_process["ct"] = current_time
                    current_process["tat"] = current_process["ct"] - current_process["at"]
                    current_process["wt"] = current_process["tat"] - current_process["bt"]
                    current_process["completed"] = True
                    completed_count += 1

            elif mode == "Preemptive":
                while completed_count < n:
                    # Find available processes that have arrived and have remaining time > 0
                    available = [p for p in processes if p["at"] <= current_time and p["rt"] > 0]
                    
                    if not available:
                        current_time += 1 # CPU is idle, advance time
                        continue
                    
                    # Sort by Remaining Time (SRTF rule)
                    available.sort(key=lambda x: x["rt"])
                    current_process = available[0]
                    
                    # Execute for 1 unit of time
                    current_process["rt"] -= 1
                    current_time += 1
                    
                    # If process finishes
                    if current_process["rt"] == 0:
                        current_process["ct"] = current_time
                        current_process["tat"] = current_process["ct"] - current_process["at"]
                        current_process["wt"] = current_process["tat"] - current_process["bt"]
                        completed_count += 1

            # Render Table and Averages
            total_tat = sum(p["tat"] for p in processes)
            total_wt = sum(p["wt"] for p in processes)
            
            for p in processes:
                self.tree.insert("", tk.END, values=(p["pid"], p["at"], p["bt"], p["ct"], p["tat"], p["wt"]))

            self.lbl_averages.config(text=f"Average TAT: {(total_tat/n):.2f} ms  |  Average WT: {(total_wt/n):.2f} ms")

        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid integers separated by commas.")

    def clear_inputs(self):
        self.entry_arrival.delete(0, tk.END)
        self.entry_burst.delete(0, tk.END)
        for item in self.tree.get_children(): self.tree.delete(item)
        self.lbl_averages.config(text="Average TAT: 0.00 ms  |  Average WT: 0.00 ms")

if __name__ == "__main__":
    root = tk.Tk()
    app = SJFSimulator(root)
    root.mainloop()