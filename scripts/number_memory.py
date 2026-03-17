import pyautogui
import time
import keyboard
import easyocr
from common import as_tuple, click, create_driver, get_test_settings, is_color_match, start_test, wait_for_q_to_close

settings = get_test_settings("number_memory")
driver = create_driver(settings["url"])
start_test(as_tuple(settings["start_button"]))
reader = easyocr.Reader(["en"])

white_color = as_tuple(settings["white_color"])
white_tolerance = settings["white_tolerance"]
ocr_region = as_tuple(settings["ocr_region"])
ocr_image = settings["ocr_image"]
ocr_allowlist = settings["ocr_allowlist"]
ocr_confidence_threshold = settings["ocr_confidence_threshold"]
ocr_max_length_delta = settings["ocr_max_length_delta"]
expected_start_length = settings["expected_start_length"]
force_ocr_every_seconds = settings["force_ocr_every_seconds"]
show_number_pixels = [as_tuple(pixel) for pixel in settings["show_number_pixels"]]
input_ready_pixel = as_tuple(settings["input_ready_pixel"])
input_click = as_tuple(settings["input_click"])
submit_button = as_tuple(settings["submit_button"])
next_button = as_tuple(settings["next_button"])
post_ocr_wait_seconds = settings["post_ocr_wait_seconds"]
input_wait_seconds = settings["input_wait_seconds"]
loop_sleep_seconds = settings["loop_sleep_seconds"]
stop_key = settings["stop_key"]


def extract_digits(text):
    return "".join(char for char in text if char.isdigit())


def choose_best_number(ocr_results, expected_length):
    candidates = []
    for _, text, confidence in ocr_results:
        digits = extract_digits(text)
        if not digits:
            continue
        if confidence < ocr_confidence_threshold:
            continue
        if abs(len(digits) - expected_length) > ocr_max_length_delta:
            continue
        candidates.append((digits, confidence))

    if not candidates:
        return ""

    best_digits, _ = min(
        candidates,
        key=lambda item: (abs(len(item[0]) - expected_length), -item[1]),
    )
    return best_digits

error_printed = False
results = []
pending_number_text = ""
last_ocr_time = 0.0
expected_length = expected_start_length

while not keyboard.is_pressed(stop_key):
    marker_visible = any(
        is_color_match(pyautogui.pixel(pixel_x, pixel_y), white_color, white_tolerance)
        for pixel_x, pixel_y in show_number_pixels
    )

    now = time.time()
    should_read_ocr = marker_visible or (
        not pending_number_text and now - last_ocr_time >= force_ocr_every_seconds
    )

    if should_read_ocr:
        x, y, width, height = ocr_region
        screenshot = pyautogui.screenshot(region=(x, y, width, height))
        screenshot = screenshot.convert("L")
        screenshot.save(ocr_image)
        results = reader.readtext(ocr_image, allowlist=ocr_allowlist)
        last_ocr_time = now
        print("Wyniki OCR:", results)

        detected_number = choose_best_number(results, expected_length)
        if detected_number:
            pending_number_text = detected_number
            print(f"Detected number: {pending_number_text} (expected length: {expected_length})")
            error_printed = False

        time.sleep(post_ocr_wait_seconds)

    input_ready = is_color_match(pyautogui.pixel(*input_ready_pixel), white_color, white_tolerance)
    if pending_number_text and (input_ready or not marker_visible):
        print("Input screen detected - rozpoczynam pisanie liczby")

        click(*input_click)
        time.sleep(input_wait_seconds)
        pyautogui.write(pending_number_text)
        time.sleep(input_wait_seconds)
        click(*submit_button)
        time.sleep(input_wait_seconds)
        click(*next_button)
        time.sleep(input_wait_seconds)

        pending_number_text = ""
        expected_length += 1
        results = []
        error_printed = False
    else:
        if not error_printed and not pending_number_text:
            print("ERROR - No number detected")
            error_printed = True
        time.sleep(loop_sleep_seconds)

wait_for_q_to_close(driver)