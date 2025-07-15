import pyautogui
import time
import keyboard
import random
import win32api, win32con
from selenium import webdriver
from selenium.webdriver.common.by import By


driver = webdriver.Chrome()
driver.maximize_window()
driver.get("https://humanbenchmark.com/tests/sequence")

def click(x, y):
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    time.sleep(0.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)

click(1050,807)  # accept cookies button
time.sleep(2)  # wait for the page to load
click(949, 579)  # start button
time.sleep(0.1)  # wait for the game to load

#normal color of buttons 
normal_color = (36, 114, 192)

#Color of correctly clicked button(white)
clicked_color = (255, 255, 255)

#all positions of buttons where first is left top corner second is middle top third is right top corner etc.
#for future program gonna take screenshot of the game and find buttons positions automatically
x_positions = [815,945,1083]

y_positions = [333,467,600]

positions=[]
for x in x_positions:
    for y in y_positions:
        positions.append((x,y))


clicks=[]
last_flash_time = None
while not keyboard.is_pressed('q'):
    for pos in positions:
        if pyautogui.pixel(pos[0], pos[1]) == clicked_color:
            if len(clicks)==0 or clicks[-1] != pos:
                clicks.append(pos)
                last_flash_time = time.time()
    if last_flash_time and time.time() - last_flash_time >= 3:
        for cl in clicks:
            click(cl[0], cl[1])
        clicks=[]  
        last_flash_time = None         
    time.sleep(0.1)  # Sleep to prevent high CPU usage
    print(f"Clicks: {clicks}")  # Debugging output to see the clicks being registered
print("Script stopped, browser will remain open")
input("Press Enter to close the browser...")  
driver.quit()     