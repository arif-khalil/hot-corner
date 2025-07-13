import pyautogui
import time
import ctypes
import threading
import pystray
from PIL import Image, ImageDraw
import keyboard
from screeninfo import get_monitors

CORNER_THRESHOLD = 5
CHECK_INTERVAL = 0.2  # check 5 times per second
DEBOUNCE_DELAY = 1.0  # short cooldown after triggering

paused = False
running = True

def is_in_top_left_corner():
    x, y = pyautogui.position()
    threshold = CORNER_THRESHOLD

    for monitor in get_monitors():
        # Top-left of each monitor
        left = monitor.x
        top = monitor.y

        if left <= x <= left + threshold and top <= y <= top + threshold:
            return True
    return False

def win_tab():
    ctypes.windll.user32.keybd_event(0x5B, 0, 0, 0)  # Win key down
    ctypes.windll.user32.keybd_event(0x09, 0, 0, 0)  # Tab key down
    ctypes.windll.user32.keybd_event(0x09, 0, 2, 0)  # Tab key up
    ctypes.windll.user32.keybd_event(0x5B, 0, 2, 0)  # Win key up

def create_image():
    # Create an icon image (simple square with orange circle)
    width = 64
    height = 64
    image = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    dc = ImageDraw.Draw(image)
    dc.ellipse((8, 8, width - 8, height - 8), fill='orange')
    return image

def on_pause_resume(icon, item):
    global paused
    paused = not paused
    status = "Paused" if paused else "Running"
    print(f"Hot corner detection {status}")
    icon.update_menu()

def on_quit(icon, item):
    global running
    running = False
    icon.stop()

def run_hot_corner(icon):
    global paused, running
    print("Hot corner running. Press Ctrl+Alt+P to pause/resume.")

    # Register global hotkey Ctrl+Alt+P for pause/resume
    keyboard.add_hotkey('ctrl+alt+p', lambda: on_pause_resume(icon, None))

    while running:
        if not paused and is_in_top_left_corner():
            print("Top-left corner detected! Opening Task View (Win + Tab)")
            win_tab()
            time.sleep(DEBOUNCE_DELAY)  # debounce
        time.sleep(CHECK_INTERVAL)

icon = pystray.Icon("hotcorner", create_image(), "Hot Corner")

icon.menu = pystray.Menu(
    pystray.MenuItem(
        lambda item: "Resume" if paused else "Pause",
        on_pause_resume
    ),
    pystray.MenuItem("Quit", on_quit)
)

# Run hot corner detection in a separate thread to not block tray
threading.Thread(target=run_hot_corner, args=(icon,), daemon=True).start()

icon.run()
