import pyautogui
import time
import keyboard
from common import as_tuple, click, get_test_settings

settings = get_test_settings("visual_memory")

#Color of correctly clicked button(white)
clicked_color = as_tuple(settings["clicked_color"])

#now its harder because every modulo 3 round the size of the grid increases by one row and column
#so the first and second round have 3x3 grid, the third and fourth round have 4x4 grid, etc.
#so i think about we have to get by how much grid size changes every 3 rounds
#and we then can calculate the different positions of the buttons every 3 rounds

def get_grid_size(round_number):
    # Calculate the grid size based on the round number
    #1-2 round 3x3 grid, 3-5 round 4x4 grid, 6-8 round 5x5 grid etc.
    if round_number < settings["max_grid_size_round"]:
        return 3 + (round_number // 3)
    else:
        return settings["max_grid_size"]
    
def get_button_positions(round_number):
    positions=[]
    grid_size = get_grid_size(round_number)
    
    # Calculate spacing based on round ranges
    spacing = settings["spacing_rules"][-1]["spacing"]
    for rule in settings["spacing_rules"]:
        if round_number < rule["max_round_exclusive"]:
            spacing = rule["spacing"]
            break

    x_positions = [settings["grid_base_x"] + i * spacing for i in range(grid_size)]
    y_positions = [settings["grid_base_y"] + i * spacing for i in range(grid_size)]

    return [(a,b) for b in y_positions for a in x_positions]

#3x3 -> 3*x=80
#4x4 -> 4*x=60
#5x5 -> 5*x=48

#print(get_button_positions(14))
print("Press ] to start checking for clicks...")
keyboard.wait(settings["start_key"])
print("] key pressed, starting to check for clicks...")

current_round_number = 1
clicks = []
last_flash_time = None
game_state = "waiting"  # "showing_pattern", "waiting_for_input"
pattern_complete = False

while not keyboard.is_pressed(settings["stop_key"]):
    positions = get_button_positions(current_round_number)
    
    #Check for flashing buttons
    white_buttons = []
    for pos in positions:
        if pyautogui.pixel(pos[0], pos[1]) == clicked_color:
            white_buttons.append(pos)
    
    # White buttons means we are in pattern showing case
    if white_buttons:
        for pos in white_buttons:
            if pos not in clicks:
                clicks.append(pos)
        last_flash_time = time.time()
        game_state = "showing_pattern"
        pattern_complete = False
    
    # If no white buttons and we were showing pattern pattern is complete
    elif game_state == "showing_pattern" and not white_buttons:
        if not pattern_complete:
            pattern_complete = True
        game_state = "waiting_for_input"
    
    # After pattern is shown wait a bit then click the sequence
    if game_state == "waiting_for_input" and last_flash_time and (time.time() - last_flash_time) >= settings["pattern_delay_seconds"]:
        for cl in clicks:
            click(cl[0], cl[1])
            time.sleep(settings["post_click_wait_seconds"])
       
        time.sleep(settings["post_round_wait_seconds"])
        
        clicks = []
        current_round_number += 1  
        game_state = "waiting"
        last_flash_time = None
    time.sleep(settings["loop_sleep_seconds"])