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