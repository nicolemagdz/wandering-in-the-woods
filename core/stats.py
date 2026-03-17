import csv
from pathlib import Path

class StatsManager:
    # Stores and analyzes simulation results

    def __init__(self):
        self.run_history = [] # list of dicts: {"steps": int}

    def record_run(self, steps):
        self.run_history.append({"steps": steps})

    def get_summary(self):
        if not self.run_history:
            return None
        
        steps_list = [r["steps"] for r in self.run_history]
        return {
            "min": min(steps_list),
            "max": max(steps_list),
            "avg": sum(steps_list) / len(steps_list),
            "count": len(steps_list),
        }
    
    def get_steps_list(self):
        return [r["steps"] for r in self.run_history]

    def export_to_csv(self, filename="run_stats.csv"):
        path = Path(filename)
        with path.open("w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["run", "steps"])
            writer.writeheader()
            for i, r in enumerate(self.run_history, start=1):
                writer.writerow({"run": i, "steps": r["steps"]})