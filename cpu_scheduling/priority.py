import tkinter as tk
from tkinter import ttk, messagebox

class PrioritySimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Priority Scheduling")
        self.root.geometry("750x650")
        self.root.configure(bg="#f4f4f9")

        style = ttk.Style()
        style.theme_use('clam')

        main_frame = tk.Frame(self.root, bg="#f4f4f9", padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(main_frame, text="Priority CPU Scheduling", font=("Segoe UI", 16, "bold"), bg="#f4f4f9").pack(pady=(0, 5))
        tk.Label(main_frame, text="(Lower number = Higher priority)", font=("Segoe UI", 10, "italic"), bg="#f4f4f9", fg="#555").pack(pady=(0, 10))

        # --- Mode Selection ---
        self.mode_var = tk.StringVar(value="Non-Preemptive")
        mode_frame = tk.Frame(main_frame, bg="#f4f4f9")
        mode_frame.pack(pady=5)
        
        ttk.Radiobutton(mode_frame, text="Non-Preemptive", variable=self.mode_var, value="Non-Preemptive").pack(side=tk.LEFT, padx=10)
        ttk.Radiobutton(mode_frame, text="Preemptive", variable=self.mode_var, value="Preemptive").pack(side=tk.LEFT, padx=10)

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

        tk.Label(input_frame, text="Priorities (comma-separated):", bg="#f4f4f9").grid(row=2, column=0, sticky="w", pady=5)
        self.entry_priority = ttk.Entry(input_frame, width=40)
        self.entry_priority.grid(row=2, column=1, padx=10, pady=5)
        self.entry_priority.insert(0, "3, 1, 4, 2")

        # --- Buttons ---
        btn_frame = tk.Frame(main_frame, bg="#f4f4f9")
        btn_frame.pack(pady=10)

        ttk.Button(btn_frame, text="Run Simulation", command=self.calculate_priority).pack(side=tk.LEFT, padx=5)
        
        # NEW: Gantt Chart Button
        ttk.Button(btn_frame, text="View Gantt Chart", command=self.show_gantt_chart).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(btn_frame, text="Clear", command=self.clear_inputs).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="⬅ Back", command=self.root.destroy).pack(side=tk.LEFT, padx=5)

        # --- Results Table ---
        columns = ("PID", "Priority", "AT", "BT", "CT", "TAT", "WT")
        self.tree = ttk.Treeview(main_frame, columns=columns, show="headings", height=8)
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=80, anchor=tk.CENTER)
        self.tree.pack(fill=tk.X, pady=10)

        # --- Averages Display ---
        self.lbl_averages = tk.Label(main_frame, text="Average TAT: 0.00 ms  |  Average WT: 0.00 ms", font=("Segoe UI", 11, "bold"), bg="#f4f4f9")
        self.lbl_averages.pack(pady=10)

        # NEW: Store timeline for the Gantt Chart
        self.timeline = []

    def calculate_priority(self):
        try:
            arrival_times = list(map(int, self.entry_arrival.get().split(',')))
            burst_times = list(map(int, self.entry_burst.get().split(',')))
            priorities = list(map(int, self.entry_priority.get().split(',')))
            n = len(arrival_times)

            if not (n == len(burst_times) == len(priorities)):
                messagebox.showerror("Input Error", "Arrival Times, Burst Times, and Priorities count must match.")
                return

            mode = self.mode_var.get()
            
            processes = []
            for i in range(n):
                processes.append({
                    "pid": f"P{i+1}", "priority": priorities[i], "at": arrival_times[i], 
                    "bt": burst_times[i], "rt": burst_times[i], 
                    "ct": 0, "tat": 0, "wt": 0, "completed": False
                })

            current_time = 0
            completed_count = 0
            self.timeline = [] # Reset timeline
            
            for item in self.tree.get_children(): self.tree.delete(item)

            if mode == "Non-Preemptive":
                while completed_count < n:
                    available = [p for p in processes if p["at"] <= current_time and not p["completed"]]
                    
                    if not available:
                        # Log Idle Time (coalescing consecutive idle ms)
                        if not self.timeline or self.timeline[-1]["pid"] != "Idle":
                            self.timeline.append({"pid": "Idle", "start": current_time, "end": current_time + 1})
                        else:
                            self.timeline[-1]["end"] += 1
                        current_time += 1 
                        continue
                    
                    available.sort(key=lambda x: (x["priority"], x["at"]))
                    current_process = available[0]
                    
                    # Log execution block
                    start_time = current_time
                    current_time += current_process["bt"]
                    self.timeline.append({"pid": current_process["pid"], "start": start_time, "end": current_time})

                    current_process["ct"] = current_time
                    current_process["tat"] = current_process["ct"] - current_process["at"]
                    current_process["wt"] = current_process["tat"] - current_process["bt"]
                    current_process["completed"] = True
                    completed_count += 1

            elif mode == "Preemptive":
                while completed_count < n:
                    available = [p for p in processes if p["at"] <= current_time and p["rt"] > 0]
                    
                    if not available:
                        # Log Idle Time
                        if not self.timeline or self.timeline[-1]["pid"] != "Idle":
                            self.timeline.append({"pid": "Idle", "start": current_time, "end": current_time + 1})
                        else:
                            self.timeline[-1]["end"] += 1
                        current_time += 1
                        continue
                    
                    available.sort(key=lambda x: (x["priority"], x["at"]))
                    current_process = available[0]
                    
                    # Log execution block (coalescing 1ms ticks)
                    if not self.timeline or self.timeline[-1]["pid"] != current_process["pid"]:
                        self.timeline.append({"pid": current_process["pid"], "start": current_time, "end": current_time + 1})
                    else:
                        self.timeline[-1]["end"] += 1

                    current_process["rt"] -= 1
                    current_time += 1
                    
                    if current_process["rt"] == 0:
                        current_process["ct"] = current_time
                        current_process["tat"] = current_process["ct"] - current_process["at"]
                        current_process["wt"] = current_process["tat"] - current_process["bt"]
                        completed_count += 1

            # Render Table
            total_tat = sum(p["tat"] for p in processes)
            total_wt = sum(p["wt"] for p in processes)
            
            for p in processes:
                self.tree.insert("", tk.END, values=(p["pid"], p["priority"], p["at"], p["bt"], p["ct"], p["tat"], p["wt"]))

            self.lbl_averages.config(text=f"Average TAT: {(total_tat/n):.2f} ms  |  Average WT: {(total_wt/n):.2f} ms")

        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid integers separated by commas.")

    # NEW: Gantt Chart Generator
    def show_gantt_chart(self):
        if not self.timeline:
            messagebox.showwarning("No Data", "Please run the simulation first.")
            return

        gantt_win = tk.Toplevel(self.root)
        gantt_win.title(f"Gantt Chart - {self.mode_var.get()} Priority")
        gantt_win.geometry("800x250")
        gantt_win.configure(bg="white")

        tk.Label(gantt_win, text=f"Execution Timeline ({self.mode_var.get()})", font=("Segoe UI", 14, "bold"), bg="white").pack(pady=10)

        canvas_width = 720
        canvas_height = 100
        canvas = tk.Canvas(gantt_win, width=canvas_width, height=canvas_height, bg="white", highlightthickness=0)
        canvas.pack(pady=20)

        total_time = self.timeline[-1]["end"]
        if total_time == 0: return

        x_offset = 20
        usable_width = canvas_width - 40
        colors = ["#FF9999", "#99CCFF", "#99FF99", "#FFCC99", "#CC99FF", "#FFFF99"]
        process_colors = {"Idle": "#E0E0E0"}

        for block in self.timeline:
            pid = block["pid"]
            start = block["start"]
            end = block["end"]
            duration = end - start
            
            if pid not in process_colors:
                process_colors[pid] = colors[len(process_colors) % len(colors)]

            block_width = (duration / total_time) * usable_width
            
            canvas.create_rectangle(x_offset, 20, x_offset + block_width, 70, fill=process_colors[pid], outline="black")
            
            # Only draw text if the block is wide enough to fit it
            if block_width > 20:
                text_x = x_offset + (block_width / 2)
                canvas.create_text(text_x, 45, text=pid, font=("Segoe UI", 10, "bold"))

            canvas.create_text(x_offset, 85, text=str(start), font=("Segoe UI", 9))
            x_offset += block_width

        canvas.create_text(x_offset, 85, text=str(total_time), font=("Segoe UI", 9))

    def clear_inputs(self):
        self.entry_arrival.delete(0, tk.END)
        self.entry_burst.delete(0, tk.END)
        self.entry_priority.delete(0, tk.END)
        self.timeline = []
        for item in self.tree.get_children(): self.tree.delete(item)
        self.lbl_averages.config(text="Average TAT: 0.00 ms  |  Average WT: 0.00 ms")

if __name__ == "__main__":
    root = tk.Tk()
    app = PrioritySimulator(root)
    root.mainloop()