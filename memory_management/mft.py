import tkinter as tk
from tkinter import ttk, messagebox

class MFTSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Multiprogramming with a Fixed number of Tasks (MFT)")
        self.root.geometry("750x600")
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
        self.lbl_summary = tk.Label(main_frame, text="Total Internal Fragmentation: 0 KB  |  Unused Partition Space: 0 KB", font=("Segoe UI", 11, "bold"), bg="#f4f4f9")
        self.lbl_summary.pack(pady=10)

    def calculate_mft(self):
        try:
            total_mem = int(self.entry_total_mem.get())
            partitions = list(map(int, self.entry_partitions.get().split(',')))
            process_sizes = list(map(int, self.entry_processes.get().split(',')))
            
            if sum(partitions) > total_mem:
                messagebox.showerror("Input Error", "Sum of partitions exceeds total memory size.")
                return

            # Keep track of partition state: [size, is_occupied]
            part_status = [[sz, False] for sz in partitions]
            total_int_frag = 0
            
            for item in self.tree.get_children(): 
                self.tree.delete(item)

            for i, p_size in enumerate(process_sizes):
                allocated = "No"
                assigned_part = "N/A"
                int_frag = 0
                status = "Waiting"
                
                # First-fit assignment strategy for fixed sizes
                for idx, part in enumerate(part_status):
                    if not part[1] and part[0] >= p_size:
                        part_status[idx][1] = True
                        allocated = "Yes"
                        assigned_part = f"P{idx+1} ({part[0]} KB)"
                        int_frag = part[0] - p_size
                        total_int_frag += int_frag
                        status = "Allocated"
                        break
                
                if allocated == "No":
                    if p_size > max(partitions):
                        status = "Exceeds Max Partition"
                    else:
                        status = "No Free Partition"

                self.tree.insert("", tk.END, values=(f"P{i+1}", f"{p_size} KB", allocated, assigned_part, f"{int_frag} KB", status))

            unused_mem = sum(part[0] for part in part_status if not part[1])
            self.lbl_summary.config(text=f"Total Internal Fragmentation: {total_int_frag} KB  |  Unused Partition Space: {unused_mem} KB")

        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid integers separated by commas.")

    def clear_inputs(self):
        self.entry_total_mem.delete(0, tk.END)
        self.entry_total_mem.insert(0, "1000")
        self.entry_partitions.delete(0, tk.END)
        self.entry_partitions.insert(0, "200, 300, 500")
        self.entry_processes.delete(0, tk.END)
        self.entry_processes.insert(0, "150, 350, 200, 450")
        for item in self.tree.get_children(): self.tree.delete(item)
        self.lbl_summary.config(text="Total Internal Fragmentation: 0 KB  |  Unused Partition Space: 0 KB")

if __name__ == "__main__":
    root = tk.Tk()
    app = App = MFTSimulator(root)
    root.mainloop()