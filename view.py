from tkinter import *
import time

def view_generation(steps_data):
    root = Tk()
    root.title("View Generation")
    root.geometry("720x720")

    canvas = Canvas(root, bg="black", width=720, height=720)
    canvas.pack()

    world_size = len(steps_data[0]["map"])
    for step in range(len(steps_data)):
        step_data = steps_data[step]
        step_map = step_data["map"]

        try:
            canvas.delete("all")
        except:
            print("generation view ended")
            break

        for y in range(world_size):
            for x in range(world_size):
                # Choose color for the pixel
                color = "black"
                if step_map[x][y] == 1:
                    color = "lime"

                canvas.create_rectangle(x * 20, y * 20, x * 20 + 20, y * 20 + 20, fill=color, width="0")
        
        canvas.update()
        time.sleep(0.1)