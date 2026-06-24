import tkinter as tk
from tkinter import ttk, messagebox

class FCFSSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("First-Come, First-Served (FCFS) Scheduling")
        self.root.geometry("650x550")
        self.root.configure(bg="#f4f4f9")

        style = ttk.Style()
        style.theme_use('clam')
        
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

    def calculate_fcfs(self):
        try:
            arrival_times = list(map(int, self.entry_arrival.get().split(',')))
            burst_times = list(map(int, self.entry_burst.get().split(',')))

            n = len(arrival_times)
            if n != len(burst_times):
                messagebox.showerror("Input Error", "Arrival Times and Burst Times count must match.")
                return

            processes = [{"pid": f"P{i+1}", "at": arrival_times[i], "bt": burst_times[i]} for i in range(n)]
            processes.sort(key=lambda x: x["at"])

            current_time, total_tat, total_wt = 0, 0, 0
            for item in self.tree.get_children(): self.tree.delete(item)

            for p in processes:
                if current_time < p["at"]: current_time = p["at"]
                
                current_time += p["bt"]
                p["ct"] = current_time
                p["tat"] = p["ct"] - p["at"]
                p["wt"] = p["tat"] - p["bt"]
                
                total_tat += p["tat"]
                total_wt += p["wt"]

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
    app = FCFSSimulator(root)
    root.mainloop()