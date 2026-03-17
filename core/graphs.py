import matplotlib.pyplot as plt

def show_steps_line_chart(stats_manager):
    steps = stats_manager.get_steps_list()
    if not steps:
        return
    
    runs = list(range(1, len(steps) + 1))

    plt.figure(figsize=(6, 4))
    plt.plot(runs, steps, marker="o")
    plt.title("Run Lengths Over Trials")
    plt.xlabel("Run")
    plt.ylabel("Steps to Meeting")
    plt.grid(True)
    plt.tight_layout()
    plt.show()