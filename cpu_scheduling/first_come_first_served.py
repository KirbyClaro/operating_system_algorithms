import tkinter as tk
from tkinter import ttk, messagebox
import random

class FCFSSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("First-Come, First-Served (FCFS) Scheduling")
        self.root.geometry("700x550")
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

        ttk.Button(btn_frame, text="Run Simulation", command=self.calculate_fcfs).pack(side=tk.LEFT, padx=5)
        
        # NEW: Gantt Chart Button
        ttk.Button(btn_frame, text="View Gantt Chart", command=self.show_gantt_chart).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(btn_frame, text="Clear", command=self.clear_inputs).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="⬅ Back", command=self.root.destroy).pack(side=tk.LEFT, padx=5)

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

        # NEW: Store timeline for the Gantt Chart
        self.timeline = []

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
            self.timeline = [] # Reset timeline
            
            for item in self.tree.get_children(): self.tree.delete(item)

            for p in processes:
                # Handle Idle Time
                if current_time < p["at"]: 
                    self.timeline.append({"pid": "Idle", "start": current_time, "end": p["at"]})
                    current_time = p["at"]
                
                # Log execution block
                start_time = current_time
                current_time += p["bt"]
                self.timeline.append({"pid": p["pid"], "start": start_time, "end": current_time})

                p["ct"] = current_time
                p["tat"] = p["ct"] - p["at"]
                p["wt"] = p["tat"] - p["bt"]
                
                total_tat += p["tat"]
                total_wt += p["wt"]

                self.tree.insert("", tk.END, values=(p["pid"], p["at"], p["bt"], p["ct"], p["tat"], p["wt"]))

            self.lbl_averages.config(text=f"Average TAT: {(total_tat/n):.2f} ms  |  Average WT: {(total_wt/n):.2f} ms")

        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid integers separated by commas.")

    # NEW: Gantt Chart Generator
    def show_gantt_chart(self):
        if not self.timeline:
            messagebox.showwarning("No Data", "Please run the simulation first.")
            return

        # Create Popup Window
        gantt_win = tk.Toplevel(self.root)
        gantt_win.title("Gantt Chart")
        gantt_win.geometry("800x250")
        gantt_win.configure(bg="white")

        tk.Label(gantt_win, text="Execution Timeline", font=("Segoe UI", 14, "bold"), bg="white").pack(pady=10)

        # Setup Canvas
        canvas_width = 720
        canvas_height = 100
        canvas = tk.Canvas(gantt_win, width=canvas_width, height=canvas_height, bg="white", highlightthickness=0)
        canvas.pack(pady=20)

        total_time = self.timeline[-1]["end"]
        if total_time == 0: return

        # Draw the blocks
        x_offset = 20
        usable_width = canvas_width - 40
        
        # Color mapping for processes
        colors = ["#FF9999", "#99CCFF", "#99FF99", "#FFCC99", "#CC99FF", "#FFFF99"]
        process_colors = {"Idle": "#E0E0E0"}

        for block in self.timeline:
            pid = block["pid"]
            start = block["start"]
            end = block["end"]
            duration = end - start
            
            # Assign color if not assigned yet
            if pid not in process_colors:
                process_colors[pid] = colors[len(process_colors) % len(colors)]

            # Calculate pixel width based on time ratio
            block_width = (duration / total_time) * usable_width
            
            # Draw Rectangle
            canvas.create_rectangle(x_offset, 20, x_offset + block_width, 70, fill=process_colors[pid], outline="black")
            
            # Draw Process ID text in the middle of the block
            text_x = x_offset + (block_width / 2)
            canvas.create_text(text_x, 45, text=pid, font=("Segoe UI", 10, "bold"))

            # Draw time markers at the bottom edges
            canvas.create_text(x_offset, 85, text=str(start), font=("Segoe UI", 9))
            
            x_offset += block_width

        # Draw the final time marker at the very end
        canvas.create_text(x_offset, 85, text=str(total_time), font=("Segoe UI", 9))

    def clear_inputs(self):
        self.entry_arrival.delete(0, tk.END)
        self.entry_burst.delete(0, tk.END)
        self.timeline = []
        for item in self.tree.get_children(): self.tree.delete(item)
        self.lbl_averages.config(text="Average TAT: 0.00 ms  |  Average WT: 0.00 ms")

if __name__ == "__main__":
    root = tk.Tk()
    app = FCFSSimulator(root)
    root.mainloop()