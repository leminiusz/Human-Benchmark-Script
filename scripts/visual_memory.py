import pyautogui
import time
import keyboard
import random
import win32api, win32con

def click(x, y):
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    time.sleep(0.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)

#normal color of buttons 
normal_color = (36, 114, 192)

#Color of correctly clicked button(white)
clicked_color = (255, 255, 255)

#now its harder because every modulo 3 round the size of the grid increases by one row and column
#so the first and second round have 3x3 grid, the third and fourth round have 4x4 grid, etc.
#so i think about we have to get by how much grid size changes every 3 rounds
#and we then can calculate the different positions of the buttons every 3 rounds

#default positions of the buttons
#these are the positions of the buttons in the first and second round
x_positions = [815,945,1083]
y_positions = [333,467,600]

def get_grid_size(round_number):
    # Calculate the grid size based on the round number
    return 3 + (round_number // 3)

def get_button_positions(round_number):
    positions=[]
    grid_size = get_grid_size(round_number)
    
    # Calculate spacing based on round ranges
    if round_number <= 3:
        spacing = 130
    elif round_number <= 6:
        spacing = 130 - 30  
    elif round_number <= 9:
        spacing = 130 - 60  
    else:
        group = (round_number - 1) // 3
        spacing = 100 - (group * 30)
        if spacing < 20:  
            spacing = 20
    x_positions = [800 + i * spacing for i in range(grid_size)]
    y_positions = [315 + i * spacing for i in range(grid_size)]

    return [(a,b) for b in y_positions for a in x_positions]

#3x3 -> 3*x=80
#4x4 -> 4*x=60
#5x5 -> 5*x=48

print("Press ] to start checking for clicks...")
keyboard.wait("]")
print("] key pressed, starting to check for clicks...")

current_round_number = 1
clicks=[]
last_flash_time = None

while not keyboard.is_pressed('q'):
    positions = get_button_positions(current_round_number)
    for pos in positions:
        if pyautogui.pixel(pos[0],pos[1])==clicked_color:
            if len(clicks) == 0 or clicks[-1] != pos:
                clicks.append(pos)
                last_flash_time = time.time()
    if last_flash_time and time.time() - last_flash_time >= 3:
        for cl in clicks:
            click(cl[0],cl[1]) 
        clicks=[]
        last_flash_time=None
    time.sleep(0.3)
    current_round_number+=1
    print(f"clicks: {clicks}")
