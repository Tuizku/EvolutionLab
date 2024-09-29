import os
import json
from lab.lab import Lab
from lab.bytedna import ByteDNA
import lab.view as view


# Add color codes to a string
colorcodes = {
    "red": "\033[31m",
    "green": "\033[32m",
    "blue": "\033[34m",
    "yellow": "\033[33m",
    "magenta": "\033[35m",
    "cyan": "\033[36m"
}
def colorstr(text, color):
    if settings["use_colors"]: return colorcodes[color] + text + "\033[0m"
    else: return text

# User input with a colored hint
def inp(text):
    return input(colorstr(text, "blue"))




# --- MANAGER ---

path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "lab_manager_settings.json")
settings = { "use_colors": True }
lab = None
bytedna = None
saved_steps = None

def open_lab_manager(_lab : Lab, _bytedna : ByteDNA):
    load_manager_settings()
    
    global lab, bytedna
    lab = _lab
    bytedna = _bytedna

    print(colorstr("lab manager console opened. use 'help' to get started.", "green"))

    # Start the lab manager's main loop
    while (True):
        command = input("/")
        
        match command:
            case "help":
                cmd_help()
            case "exit":
                lab.save_gens()
                exit()
            case "use_colors":
                cmd_use_colors()
            case "gen":
                print(colorstr(f"gen {lab.gen}", "green"))
            case "run_generation":
                cmd_run_generation()
            case "run_generations":
                cmd_run_generations()
            case "view_generation":
                cmd_view_generation()
            case "view_chart":
                cmd_view_chart()

def load_manager_settings():
    if os.path.isfile(path) == False:
        save_manager_settings()

    global settings
    with open(path, "r") as file:
        settings = json.loads(file.read())

def save_manager_settings():
    global settings
    with open(path, "w") as file:
        file.write(json.dumps(settings))




# --- COMMAND FUNCTIONS ---

help_text = """exit = saves lab generations and exits
use_colors = enable/disable colors in console. some consoles don't support colors.
gen = prints the latest lab generation number
run_generation = runs a single generation
run_generations = runs multiple generations
view_generation = visualizes lastly saved generation by frame (run_generation + save_steps = Yes)
view_chart = visualizes the entire evolution on a chart"""
def cmd_help():
    print(colorstr(help_text, "magenta"))

def cmd_run_generation():
    global lab, bytedna, saved_steps

    # User inputs
    save_steps = inp("save steps (yes/no): ") == "yes"
    new_gen = inp("is this a new generation (yes/no): ") == "yes"

    # Uses latest lab genomes if new_gen.
    # Else user can input a gen number, which genomes are used.
    genomes = None
    if new_gen == False:
        run_gen_num = inp("use genomes from an old gen. blank = use newest (int/blank): ")
        if run_gen_num != "":
            try:
                # If answer was an int and lab has processed that gen before, it uses that gen's genomes.
                run_gen_num = int(run_gen_num)
                if run_gen_num <= lab.gen:
                    all_genomes, stats = lab.load_gens()
                    genomes_bytes = lab.bytedna.gene_bytes * lab.bytedna.genome_len * lab.population
                    genomes = all_genomes[run_gen_num * genomes_bytes : run_gen_num * genomes_bytes + genomes_bytes]
                
                else:
                    print(colorstr("gen num was above the newest gen, so using newest genomes", "red"))
            except:
                print(colorstr("gen num was not blank nor acceptable int", "red"))
        
    # Run
    saved_steps = lab.run_generation(genomes=genomes, new_gen=new_gen, return_steps_data=save_steps)
    
    # End print
    if new_gen: print(colorstr(f"finished, gen = {lab.gen}", "green"))
    else: print(colorstr("finished, no gen added", "green"))

def cmd_run_generations():
    global lab, bytedna, saved_steps

    try:
        count = int(inp("count (int): "))
        lab.run_generations(count)
        print(colorstr("finished", "green"))
    except:
        print(colorstr("count was not a valid integer", "red"))

def cmd_view_generation():
    global lab, bytedna, saved_steps
    if saved_steps != None:
        view.view_generation(saved_steps)
    else: print(colorstr("no saved steps - first run a generation with 'save_steps' enabled.", "red"))

def cmd_view_chart():
    genomes, stats = lab.load_gens()
    view.view_evolution_chart(stats, lab.population)

def cmd_use_colors():
    global settings
    settings["use_colors"] = inp("use colors in console (yes/no): ") == "yes"
    save_manager_settings()
    print(colorstr("lab settings updated and saved", "green"))
