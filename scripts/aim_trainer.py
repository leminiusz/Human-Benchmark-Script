import pyautogui
import keyboard
from common import as_tuple, click, create_driver, get_test_settings, start_test, wait_for_q_to_close

settings = get_test_settings("aim_trainer")
driver = create_driver(settings["url"])

region = as_tuple(settings["scan_region"])
target_color = as_tuple(settings["target_color"])
scan_step = settings["scan_step"]
stop_key = settings["stop_key"]
max_hits = settings["max_hits"]
start_test(as_tuple(settings["start_button"]))

counter=0
while not keyboard.is_pressed(stop_key) and counter < max_hits:
    pic = pyautogui.screenshot(region=region)
    width, height = pic.size
    
    found_target = False
    for x in range(0, width, scan_step):
        if found_target:
            break
        for y in range(0, height, scan_step):
            r, g, b = pic.getpixel((x, y))
            #check if the pixel color matches the target color
            if (r, g, b) == target_color:
                click(x + region[0], y + region[1])
                counter +=1  
                found_target = True
                #time.sleep(0.01)  
                break  
    # Small delay to prevent overwhelming the CPU
    #time.sleep(0.01)
wait_for_q_to_close(driver)