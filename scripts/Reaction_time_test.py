import pyautogui
import time
import keyboard
import random
import win32api, win32con
from selenium import webdriver
from selenium.webdriver.common.by import By


driver = webdriver.Chrome()
driver.maximize_window()
driver.get("https://humanbenchmark.com/tests/reactiontime")

def click(x, y):
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    time.sleep(0.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)


click(1050,807)  # accept cookies button
time.sleep(2)  # wait for the page to load
click(955, 434)  # start button
time.sleep(0.1)  # wait for the game to load
#for me position is (456,374) CHANGE TO YOUR NEEDS
x,y = 456,374
counter = 0
while not keyboard.is_pressed('q') and counter < 5:
    current_color= pyautogui.pixel(x, y)
    if current_color==(43,135,209):
        click(x,y)
        time.sleep(0.1)
        while current_color==(206,58,34):
            if keyboard.is_pressed('q'):    
                break
        time.sleep(0.5)
    elif current_color==(75,219,106):
            click(x,y)
            counter += 1
            time.sleep(0.5)
print("Script stopped, browser will remain open")
input("Press Enter to close the browser...")  
driver.quit()        
    