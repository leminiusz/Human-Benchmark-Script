import json
import time
from functools import lru_cache
from pathlib import Path

import keyboard
import win32api
import win32con

SETTINGS_PATH = Path(__file__).with_name("settings.json")


@lru_cache(maxsize=1)
def load_settings():
    with SETTINGS_PATH.open("r", encoding="utf-8") as settings_file:
        return json.load(settings_file)


def get_common_settings():
    return load_settings()["common"]


def get_test_settings(test_name):
    return load_settings()[test_name]


def as_tuple(values):
    return tuple(values)


def is_color_match(actual_color, expected_color, tolerance=0):
    return all(abs(actual - expected) <= tolerance for actual, expected in zip(actual_color, expected_color))


def create_driver(url):
    from selenium import webdriver

    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get(url)
    return driver


def click(x, y):
    click_hold_seconds = get_common_settings()["click_hold_seconds"]
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    time.sleep(click_hold_seconds)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)


def accept_cookies():
    common_settings = get_common_settings()
    click(*as_tuple(common_settings["cookie_button_position"]))
    time.sleep(common_settings["cookie_wait_seconds"])


def start_test(start_button_position):
    post_start_wait_seconds = get_common_settings()["post_start_wait_seconds"]
    accept_cookies()
    click(*start_button_position)
    time.sleep(post_start_wait_seconds)


def wait_for_q_to_close(driver):
    close_key = get_common_settings()["close_key"]
    print(f"Test finished. Press '{close_key}' to close the browser...")
    keyboard.wait(close_key)
    driver.quit()