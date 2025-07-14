import pyautogui
import time
import keyboard
import win32api, win32con
from selenium import webdriver
from selenium.webdriver.common.by import By
import easyocr

driver = webdriver.Chrome()
driver.set_window_size(1920, 1080)  # Set window size to full
driver.get("https://humanbenchmark.com/tests/number-memory")

def click(x, y):
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    time.sleep(0.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)

click(1037,838)  # accept cookies button
time.sleep(2)  # wait for the page to load
click(950, 600)  # start button
time.sleep(0.1)  # wait for the game to load

while not keyboard.is_pressed('q'):
    # Click on the game area to start the number memory test
    x,y, width, height = 475, 350, 1050, 250
    if pyautogui.pixel(918, 512) == (255, 255, 255) or pyautogui.pixel(921, 561) == (39, 121, 188): 
        screenshot = pyautogui.screenshot(region=(x, y, width, height))
        screenshot.save("number_screen.png")
        reader = easyocr.Reader(['en'])
        results = reader.readtext("number_screen.png",allowlist='0123456789')
        time.sleep(0.5)  
        #ocr zwraca wyniki listę krotek, gdzie pierwszy element to współrzędne, a drugi to tekst
        print("Wyniki OCR:", results)
    if results and pyautogui.pixel(1082, 350) == (255, 255, 255):
        #Trzeba przesortowac wyniki według współrzędnych Y zeby laczylo dolna liczbe do gorej a nie na odwrót
        sorted_results = sorted(results, key=lambda x: x[0][0][1])
        
        #
        number_text = ""
        for result in sorted_results:
            #usuwamy jeszcze potencjalne spacje i znaki nowej linii, bo result[1] zawiera
            # ale moga sie tam wkrasc jakies bledy w rozpoznaniu
            text = result[1].replace(" ", "").replace("\n", "")
            number_text += text
        
        print(f"Detected number: {number_text}")
        
        click(847,435)#click to input the number
        time.sleep(0.1)  # wait for the input field to be ready
        pyautogui.write(number_text)
        time.sleep(0.1) 
        click(965,551)  # click the submit button
        time.sleep(0.1)
        click(965,600)  # click the next button
        time.sleep(0.1)
    else:
        print("EROR - No number detected")
print("Script stopped, browser will remain open")
input("Press Enter to close the browser...")  
driver.quit()     