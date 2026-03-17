import pyautogui
import time
import keyboard
from common import as_tuple, click, create_driver, get_test_settings, start_test, wait_for_q_to_close


settings = get_test_settings("sequence_memory")
driver = create_driver(settings["url"])
start_test(as_tuple(settings["start_button"]))

#Color of correctly clicked button(white)
clicked_color = as_tuple(settings["clicked_color"])

#all positions of buttons where first is left top corner second is middle top third is right top corner etc.
#for future program gonna take screenshot of the game and find buttons positions automatically
x_positions = settings["x_positions"]
y_positions = settings["y_positions"]

positions=[]
for x in x_positions:
    for y in y_positions:
        positions.append((x,y))


stop_key = settings["stop_key"]
clicks=[]
last_flash_time = None
while not keyboard.is_pressed(stop_key):
    for pos in positions:
        if pyautogui.pixel(pos[0], pos[1]) == clicked_color:
            if len(clicks)==0 or clicks[-1] != pos:
                clicks.append(pos)
                last_flash_time = time.time()
    if last_flash_time and time.time() - last_flash_time >= settings["flash_timeout_seconds"]:
        for cl in clicks:
            click(cl[0], cl[1])
        clicks=[]  
        last_flash_time = None         
    time.sleep(settings["loop_sleep_seconds"])
    print(f"Clicks: {clicks}")  # Debugging output to see the clicks being registered

wait_for_q_to_close(driver)