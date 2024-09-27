from tkinter import *
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from mpl_toolkits.axes_grid1 import host_subplot
import time

def view_generation(steps_data):
    root = Tk()
    root.title("View Generation")
    root.geometry("1920x1080")
    root.attributes('-fullscreen', True)
    root.configure(background="black")

    canvas = Canvas(root, bg="black", width=1920, height=1080, highlightthickness=0)
    canvas.place(x=0, y=0)

    step_label = Label(root, width=10, height=1, text="step 0", fg="white", bg="black")
    step_label.pack(side=TOP, anchor="e", padx=10, pady=10)

    exit_button = Button(root, width=8, height=2, text="Exit", command=root.destroy)
    exit_button.pack(side=TOP, anchor="e", padx=10, pady=10)

    root.update()

    world_size = len(steps_data[0]["map"])
    map_size = 700
    cell_size = map_size / world_size
    root_width = root.winfo_width()
    root_height = root.winfo_height()
    start_x = (root_width - map_size) * 0.5
    start_y = (root_height - map_size) * 0.5

    canvas.create_rectangle(start_x, start_y, root_width - start_x, root_height - start_y, fill="", outline="white", width=4)
    canvas.update()
    time.sleep(1)

    for step in range(len(steps_data)):
        step_data = steps_data[step]
        step_map = step_data["map"]

        try:
            canvas.delete("cell")
            step_label.config(text=f"step {step}")
        except:
            break

        for y in range(world_size):
            for x in range(world_size):
                # Choose color for the pixel
                color = "black"
                if step_map[x][y] == 1:
                    color = "lime"

                x_pos = start_x + (x * cell_size)
                y_pos = start_y + (y * cell_size)
                canvas.create_rectangle(x_pos, y_pos, x_pos + cell_size, y_pos + cell_size, fill=color, width="0", tags="cell")
        
        canvas.update()
        time.sleep(0.1)
    
    try:
        root.destroy()
    except:
        return

def view_evolution_chart(gens_stats : list, population : int):
    survived_list = [gen_stats["survived"] for gen_stats in gens_stats]
    diversity_list = [gen_stats["diversity"] for gen_stats in gens_stats]

    host = host_subplot(111)
    par = host.twinx()

    host.set_xlabel("Generation")
    host.set_ylabel("Survived")
    par.set_ylabel("Diversity")

    p1, = host.plot(survived_list, label="Survived")
    p2, = par.plot(diversity_list, label="Diversity")
    
    host.set_ylim((0, population + 1))
    par.set_ylim((0, 1.01))

    host.legend(labelcolor="linecolor")
    host.yaxis.get_label().set_color(p1.get_color())
    par.yaxis.get_label().set_color(p2.get_color())

    plt.show()