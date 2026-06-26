import tkinter as tk
from tkinter import ttk, messagebox

class MFTSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Multiprogramming with a Fixed number of Tasks (MFT)")
        self.root.geometry("750x650")
        self.root.configure(bg="#f4f4f9")

        style = ttk.Style()
        style.theme_use('clam')

        main_frame = tk.Frame(self.root, bg="#f4f4f9", padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(main_frame, text="MFT Memory Management", font=("Segoe UI", 16, "bold"), bg="#f4f4f9").pack(pady=(0, 15))

        # --- Input Section ---
        input_frame = tk.Frame(main_frame, bg="#f4f4f9")
        input_frame.pack(fill=tk.X, pady=10)

        tk.Label(input_frame, text="Total Memory Size (KB):", bg="#f4f4f9").grid(row=0, column=0, sticky="w", pady=5)
        self.entry_total_mem = ttk.Entry(input_frame, width=40)
        self.entry_total_mem.grid(row=0, column=1, padx=10, pady=5, sticky="w")
        self.entry_total_mem.insert(0, "1000")

        tk.Label(input_frame, text="Partition Sizes (comma-separated KB):", bg="#f4f4f9").grid(row=1, column=0, sticky="w", pady=5)
        self.entry_partitions = ttk.Entry(input_frame, width=40)
        self.entry_partitions.grid(row=1, column=1, padx=10, pady=5, sticky="w")
        self.entry_partitions.insert(0, "200, 300, 500")

        tk.Label(input_frame, text="Process Sizes (comma-separated KB):", bg="#f4f4f9").grid(row=2, column=0, sticky="w", pady=5)
        self.entry_processes = ttk.Entry(input_frame, width=40)
        self.entry_processes.grid(row=2, column=1, padx=10, pady=5, sticky="w")
        self.entry_processes.insert(0, "150, 350, 200, 450")

        # --- Buttons ---
        btn_frame = tk.Frame(main_frame, bg="#f4f4f9")
        btn_frame.pack(pady=15)

        ttk.Button(btn_frame, text="Run Simulation", command=self.calculate_mft).pack(side=tk.LEFT, padx=5)
        
        # NEW: Visualizer Button
        ttk.Button(btn_frame, text="View Memory Map", command=self.show_memory_map).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(btn_frame, text="Clear", command=self.clear_inputs).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="⬅ Back", command=self.root.destroy).pack(side=tk.LEFT, padx=5)

        # --- Results Table ---
        columns = ("PID", "Process Size", "Allocated", "Assigned Partition", "Internal Frag", "Status")
        self.tree = ttk.Treeview(main_frame, columns=columns, show="headings", height=8)
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=115, anchor=tk.CENTER)
        self.tree.pack(fill=tk.X, pady=10)

        # --- Summary Display ---
        self.lbl_summary = tk.Label(main_frame, text="Total Internal Fragmentation: 0 KB   |   Unused Partition Space: 0 KB", font=("Segoe UI", 11, "bold"), bg="#f4f4f9")
        self.lbl_summary.pack(pady=10)

        # State storage for the memory visualization
        self.memory_state = []
        self.total_memory_simulated = 0

    def calculate_mft(self):
        try:
            total_mem = int(self.entry_total_mem.get())
            partitions = list(map(int, self.entry_partitions.get().split(',')))
            process_sizes = list(map(int, self.entry_processes.get().split(',')))

            if sum(partitions) > total_mem:
                messagebox.showerror("Input Error", "Sum of partitions exceeds total memory size.")
                return

            # Keep track of partition state using dictionaries for easier drawing later
            self.memory_state = [
                {"id": i+1, "size": sz, "occupied": False, "pid": "", "p_size": 0, "frag": 0} 
                for i, sz in enumerate(partitions)
            ]
            self.total_memory_simulated = total_mem
            total_int_frag = 0

            for item in self.tree.get_children():
                self.tree.delete(item)

            for i, p_size in enumerate(process_sizes):
                pid = f"P{i+1}"
                allocated = "No"
                assigned_part = "N/A"
                int_frag = 0
                status = "Waiting"

                # First-fit assignment strategy for fixed sizes
                for part in self.memory_state:
                    if not part["occupied"] and part["size"] >= p_size:
                        # Allocate the process
                        part["occupied"] = True
                        part["pid"] = pid
                        part["p_size"] = p_size
                        part["frag"] = part["size"] - p_size

                        allocated = "Yes"
                        assigned_part = f"Part {part['id']} ({part['size']} KB)"
                        int_frag = part["frag"]
                        total_int_frag += int_frag
                        status = "Allocated"
                        break

                if allocated == "No":
                    if p_size > max(partitions):
                        status = "Exceeds Max Partition"
                    else:
                        status = "No Free Partition"

                self.tree.insert("", tk.END, values=(pid, f"{p_size} KB", allocated, assigned_part, f"{int_frag} KB", status))

            # Calculate unused space (partitions that are completely empty)
            unused_mem = sum(part["size"] for part in self.memory_state if not part["occupied"])
            self.lbl_summary.config(text=f"Total Internal Fragmentation: {total_int_frag} KB   |   Unused Partition Space: {unused_mem} KB")

        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid integers separated by commas.")

    def show_memory_map(self):
        if not self.memory_state:
            messagebox.showwarning("No Data", "Please run the simulation first.")
            return

        map_win = tk.Toplevel(self.root)
        map_win.title("MFT Memory Map Visualization")
        map_win.geometry("500x700")
        map_win.configure(bg="white")

        tk.Label(map_win, text="Physical Memory (RAM)", font=("Segoe UI", 16, "bold"), bg="white").pack(pady=10)

        # Legend
        legend_frame = tk.Frame(map_win, bg="white")
        legend_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(legend_frame, text="■ Allocated Process", fg="#4CAF50", bg="white", font=("Segoe UI", 10, "bold")).pack(side=tk.LEFT, padx=15)
        tk.Label(legend_frame, text="■ Internal Fragmentation", fg="#F44336", bg="white", font=("Segoe UI", 10, "bold")).pack(side=tk.LEFT, padx=15)
        tk.Label(legend_frame, text="■ Free Partition", fg="#9E9E9E", bg="white", font=("Segoe UI", 10, "bold")).pack(side=tk.LEFT, padx=15)

        # Setup Canvas
        canvas_width = 300
        canvas_height = 500
        canvas = tk.Canvas(map_win, width=canvas_width, height=canvas_height, bg="#f0f0f0", highlightthickness=2, highlightbackground="#333")
        canvas.pack(pady=20)

        # Drawing Scale
        pixels_per_kb = canvas_height / self.total_memory_simulated
        y_offset = 0

        # Draw Partitions
        for part in self.memory_state:
            part_height = part["size"] * pixels_per_kb
            
            # Draw an outer box for the fixed partition boundary
            canvas.create_rectangle(0, y_offset, canvas_width, y_offset + part_height, outline="black", width=2)
            
            if part["occupied"]:
                # Draw Process Block (Green)
                process_height = part["p_size"] * pixels_per_kb
                canvas.create_rectangle(0, y_offset, canvas_width, y_offset + process_height, fill="#A5D6A7", outline="black")
                canvas.create_text(canvas_width/2, y_offset + (process_height/2), text=f"{part['pid']} ({part['p_size']} KB)", font=("Segoe UI", 10, "bold"))
                
                # Draw Internal Fragmentation Block (Red)
                if part["frag"] > 0:
                    frag_y_start = y_offset + process_height
                    frag_height = part["frag"] * pixels_per_kb
                    canvas.create_rectangle(0, frag_y_start, canvas_width, frag_y_start + frag_height, fill="#EF9A9A", outline="black", stipple="gray50") # Stipple gives a hatched look on windows
                    
                    # Only draw text if space is big enough
                    if frag_height > 15:
                        canvas.create_text(canvas_width/2, frag_y_start + (frag_height/2), text=f"Wasted: {part['frag']} KB", font=("Segoe UI", 9, "italic"), fill="#B71C1C")
            else:
                # Draw Free Partition Block (Gray)
                canvas.create_rectangle(0, y_offset, canvas_width, y_offset + part_height, fill="#E0E0E0", outline="black")
                canvas.create_text(canvas_width/2, y_offset + (part_height/2), text=f"Free Partition {part['id']} ({part['size']} KB)", font=("Segoe UI", 10, "bold"), fill="#616161")

            y_offset += part_height

        # Draw Unpartitioned Space (If total partitions < total memory)
        partitioned_sum = sum(p["size"] for p in self.memory_state)
        if partitioned_sum < self.total_memory_simulated:
            leftover_kb = self.total_memory_simulated - partitioned_sum
            leftover_height = leftover_kb * pixels_per_kb
            canvas.create_rectangle(0, y_offset, canvas_width, y_offset + leftover_height, fill="#BDBDBD", outline="black", stipple="gray25")
            
            if leftover_height > 15:
                canvas.create_text(canvas_width/2, y_offset + (leftover_height/2), text=f"Unpartitioned Space ({leftover_kb} KB)", font=("Segoe UI", 10, "bold"), fill="#424242")

    def clear_inputs(self):
        self.entry_total_mem.delete(0, tk.END)
        self.entry_total_mem.insert(0, "1000")
        self.entry_partitions.delete(0, tk.END)
        self.entry_partitions.insert(0, "200, 300, 500")
        self.entry_processes.delete(0, tk.END)
        self.entry_processes.insert(0, "150, 350, 200, 450")
        
        self.memory_state = []
        for item in self.tree.get_children(): 
            self.tree.delete(item)
        self.lbl_summary.config(text="Total Internal Fragmentation: 0 KB   |   Unused Partition Space: 0 KB")

if __name__ == "__main__":
    root = tk.Tk()
    app = MFTSimulator(root)
    root.mainloop()