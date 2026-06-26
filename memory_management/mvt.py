import tkinter as tk
from tkinter import ttk, messagebox

class MVTSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Multiprogramming with a Variable number of Tasks (MVT)")
        self.root.geometry("750x650")
        self.root.configure(bg="#f4f4f9")

        style = ttk.Style()
        style.theme_use('clam')

        main_frame = tk.Frame(self.root, bg="#f4f4f9", padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(main_frame, text="MVT Memory Management", font=("Segoe UI", 16, "bold"), bg="#f4f4f9").pack(pady=(0, 15))

        # --- Input Section ---
        input_frame = tk.Frame(main_frame, bg="#f4f4f9")
        input_frame.pack(fill=tk.X, pady=10)

        tk.Label(input_frame, text="Total Memory Size (KB):", bg="#f4f4f9").grid(row=0, column=0, sticky="w", pady=5)
        self.entry_total_mem = ttk.Entry(input_frame, width=40)
        self.entry_total_mem.grid(row=0, column=1, padx=10, pady=5, sticky="w")
        self.entry_total_mem.insert(0, "1000")

        tk.Label(input_frame, text="Process Sizes (comma-separated KB):", bg="#f4f4f9").grid(row=1, column=0, sticky="w", pady=5)
        self.entry_processes = ttk.Entry(input_frame, width=40)
        self.entry_processes.grid(row=1, column=1, padx=10, pady=5, sticky="w")
        self.entry_processes.insert(0, "200, 350, 150, 400")

        # --- Buttons ---
        btn_frame = tk.Frame(main_frame, bg="#f4f4f9")
        btn_frame.pack(pady=15)

        ttk.Button(btn_frame, text="Run Simulation", command=self.calculate_mvt).pack(side=tk.LEFT, padx=5)
        
        # NEW: Visualizer Button
        ttk.Button(btn_frame, text="View Memory Map", command=self.show_memory_map).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(btn_frame, text="Clear", command=self.clear_inputs).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="⬅ Back", command=self.root.destroy).pack(side=tk.LEFT, padx=5)

        # --- Results Table ---
        columns = ("PID", "Process Size", "Allocated", "Dynamic Base Memory Block", "Internal Frag", "Status")
        self.tree = ttk.Treeview(main_frame, columns=columns, show="headings", height=8)
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=115, anchor=tk.CENTER)
        self.tree.pack(fill=tk.X, pady=10)

        # --- Summary Display ---
        self.lbl_summary = tk.Label(main_frame, text="Available Space (External Frag capacity): 0 KB", font=("Segoe UI", 11, "bold"), bg="#f4f4f9")
        self.lbl_summary.pack(pady=10)

        # State storage for visualization
        self.memory_state = []
        self.total_memory_simulated = 0
        self.remaining_mem_simulated = 0

    def calculate_mvt(self):
        try:
            total_mem = int(self.entry_total_mem.get())
            process_sizes = list(map(int, self.entry_processes.get().split(',')))

            remaining_mem = total_mem
            allocated_address = 0
            
            # Reset state for drawing
            self.memory_state = []
            self.total_memory_simulated = total_mem

            for item in self.tree.get_children():
                self.tree.delete(item)

            for i, p_size in enumerate(process_sizes):
                pid = f"P{i+1}"
                allocated = "No"
                assigned_block = "N/A"
                status = "Not Allocated (External Frag)"

                if remaining_mem >= p_size:
                    allocated = "Yes"
                    start_addr = allocated_address
                    end_addr = allocated_address + p_size
                    assigned_block = f"[{start_addr} - {end_addr} KB]"
                    
                    # Log the block for the memory map visualizer
                    self.memory_state.append({
                        "pid": pid,
                        "size": p_size,
                        "start": start_addr,
                        "end": end_addr
                    })

                    allocated_address += p_size
                    remaining_mem -= p_size
                    status = "Allocated Successfully"

                # Internal Frag is strictly 0 in MVT by architecture rules
                self.tree.insert("", tk.END, values=(pid, f"{p_size} KB", allocated, assigned_block, "0 KB", status))

            self.remaining_mem_simulated = remaining_mem
            self.lbl_summary.config(text=f"Available Space (External Frag capacity): {remaining_mem} KB")

        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid integers separated by commas.")

    def show_memory_map(self):
        if self.total_memory_simulated == 0:
            messagebox.showwarning("No Data", "Please run the simulation first.")
            return

        map_win = tk.Toplevel(self.root)
        map_win.title("MVT Memory Map Visualization")
        map_win.geometry("500x700")
        map_win.configure(bg="white")

        tk.Label(map_win, text="Physical Memory (RAM) - MVT", font=("Segoe UI", 16, "bold"), bg="white").pack(pady=10)

        # Legend
        legend_frame = tk.Frame(map_win, bg="white")
        legend_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(legend_frame, text="■ Dynamic Allocated Block", fg="#4CAF50", bg="white", font=("Segoe UI", 10, "bold")).pack(side=tk.LEFT, padx=30)
        tk.Label(legend_frame, text="■ Free Space (External Frag)", fg="#9E9E9E", bg="white", font=("Segoe UI", 10, "bold")).pack(side=tk.LEFT, padx=30)

        # Setup Canvas
        canvas_width = 300
        canvas_height = 500
        canvas = tk.Canvas(map_win, width=canvas_width, height=canvas_height, bg="#f0f0f0", highlightthickness=2, highlightbackground="#333")
        canvas.pack(pady=20)

        # Drawing Scale
        pixels_per_kb = canvas_height / self.total_memory_simulated
        y_offset = 0

        # Draw Allocated Processes tightly packed together
        for block in self.memory_state:
            block_height = block["size"] * pixels_per_kb
            
            # Draw Process Block (Green)
            canvas.create_rectangle(0, y_offset, canvas_width, y_offset + block_height, fill="#A5D6A7", outline="black")
            
            # Only draw text if the block is tall enough
            if block_height > 15:
                canvas.create_text(canvas_width/2, y_offset + (block_height/2), text=f"{block['pid']} ({block['size']} KB)", font=("Segoe UI", 10, "bold"))
            
            # Mark the boundary addresses on the left
            canvas.create_text(25, y_offset + 10, text=f"{block['start']}K", font=("Segoe UI", 8), fill="#333")
            
            y_offset += block_height

        # Draw the remaining free memory block at the end (External Fragmentation)
        if self.remaining_mem_simulated > 0:
            free_height = self.remaining_mem_simulated * pixels_per_kb
            canvas.create_rectangle(0, y_offset, canvas_width, y_offset + free_height, fill="#E0E0E0", outline="black", stipple="gray25")
            
            if free_height > 15:
                canvas.create_text(canvas_width/2, y_offset + (free_height/2), text=f"Free Space ({self.remaining_mem_simulated} KB)", font=("Segoe UI", 10, "bold"), fill="#616161")
            
            # Mark final boundary
            canvas.create_text(25, y_offset + 10, text=f"{self.total_memory_simulated - self.remaining_mem_simulated}K", font=("Segoe UI", 8), fill="#333")

    def clear_inputs(self):
        self.entry_total_mem.delete(0, tk.END)
        self.entry_total_mem.insert(0, "1000")
        self.entry_processes.delete(0, tk.END)
        self.entry_processes.insert(0, "200, 350, 150, 400")
        
        self.memory_state = []
        self.total_memory_simulated = 0
        self.remaining_mem_simulated = 0
        
        for item in self.tree.get_children(): 
            self.tree.delete(item)
        self.lbl_summary.config(text="Available Space (External Frag capacity): 0 KB")

if __name__ == "__main__":
    root = tk.Tk()
    app = MVTSimulator(root)
    root.mainloop()