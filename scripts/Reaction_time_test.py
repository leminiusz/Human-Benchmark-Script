import pyautogui
import time
import keyboard
from common import as_tuple, click, create_driver, get_test_settings, start_test, wait_for_q_to_close


settings = get_test_settings("reaction_time_test")
driver = create_driver(settings["url"])
start_test(as_tuple(settings["start_button"]))
#for me position is (456,374) CHANGE TO YOUR NEEDS
x, y = as_tuple(settings["pixel_position"])
colors = settings["colors"]
armed_color = as_tuple(colors["armed"])
waiting_color = as_tuple(colors["waiting"])
go_color = as_tuple(colors["go"])
stop_key = settings["stop_key"]
counter = 0
while not keyboard.is_pressed(stop_key) and counter < settings["max_rounds"]:
    current_color= pyautogui.pixel(x, y)
    if current_color == armed_color:
        click(x,y)
        time.sleep(settings["post_armed_click_wait_seconds"])
        while current_color == waiting_color:
            if keyboard.is_pressed(stop_key):
                break
            current_color = pyautogui.pixel(x, y)
        time.sleep(settings["post_round_wait_seconds"])
    elif current_color == go_color:
            click(x,y)
            counter += 1
            time.sleep(settings["post_round_wait_seconds"])

wait_for_q_to_close(driver)
    