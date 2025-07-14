import pyautogui
import time
import keyboard
import win32api, win32con
from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
driver.maximize_window()
driver.get("https://humanbenchmark.com/tests/aim")

def click(x, y):
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    time.sleep(0.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)

region = 467,220,970,540  # Define the region to capture
click(1050,807)  # accept cookies button
time.sleep(2)  # wait for the page to load
click(955, 434)  # start button
time.sleep(0.1)  # wait for the game to load

counter=0
while not keyboard.is_pressed('q') and counter < 30:
    pic = pyautogui.screenshot(region=region)
    width, height = pic.size
    
    found_target = False
    for x in range(0, width, 5):  
        if found_target:
            break
        for y in range(0, height, 5):
            r, g, b = pic.getpixel((x, y))
            #check if the pixel color matches the target color
            if (r, g, b) == (149, 195, 232):
                click(x + region[0], y + region[1])
                counter +=1  
                found_target = True
                time.sleep(0.05)  
                break  
    # Small delay to prevent overwhelming the CPU
    time.sleep(0.01)
print("Script stopped, browser will remain open")
input("Press Enter to close the browser...")  
driver.quit() 