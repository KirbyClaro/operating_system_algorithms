import tkinter as tk
from tkinter import ttk, messagebox

class MVTSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Multiprogramming with a Variable number of Tasks (MVT)")
        self.root.geometry("750x600")
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

    def calculate_mvt(self):
        try:
            total_mem = int(self.entry_total_mem.get())
            process_sizes = list(map(int, self.entry_processes.get().split(',')))
            
            remaining_mem = total_mem
            allocated_address = 0
            
            for item in self.tree.get_children(): 
                self.tree.delete(item)

            for i, p_size in enumerate(process_sizes):
                allocated = "No"
                assigned_block = "N/A"
                status = "Not Allocated (External Frag)"
                
                if remaining_mem >= p_size:
                    allocated = "Yes"
                    assigned_block = f"[{allocated_address} - {allocated_address + p_size} KB]"
                    allocated_address += p_size
                    remaining_mem -= p_size
                    status = "Allocated Successfully"
                
                # Internal Frag is strictly 0 in MVT by architecture rules
                self.tree.insert("", tk.END, values=(f"P{i+1}", f"{p_size} KB", allocated, assigned_block, "0 KB", status))

            self.lbl_summary.config(text=f"Remaining Free Space (Available Memory): {remaining_mem} KB")

        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid integers separated by commas.")

    def clear_inputs(self):
        self.entry_total_mem.delete(0, tk.END)
        self.entry_total_mem.insert(0, "1000")
        self.entry_processes.delete(0, tk.END)
        self.entry_processes.insert(0, "200, 350, 150, 400")
        for item in self.tree.get_children(): self.tree.delete(item)
        self.lbl_summary.config(text="Available Space (External Frag capacity): 0 KB")

if __name__ == "__main__":
    root = tk.Tk()
    app = MVTSimulator(root)
    root.mainloop()