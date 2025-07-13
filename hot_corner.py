import pyautogui
import time
import ctypes
import threading
import pystray
from PIL import Image, ImageDraw
import keyboard
from screeninfo import get_monitors
import atexit

CORNER_THRESHOLD = 5
CHECK_INTERVAL = 0.1  # check 10 times per second (improved responsiveness)
DEBOUNCE_DELAY = 0.3  # cooldown after triggering
MONITOR_REFRESH_INTERVAL = 5.0  # refresh monitor info every 5 seconds

paused = False
running = True
monitors_cache = None
last_monitor_check = 0

def get_cached_monitors():
    """Get monitor information with caching to reduce CPU usage"""
    global monitors_cache, last_monitor_check
    current_time = time.time()
    if monitors_cache is None or (current_time - last_monitor_check) > MONITOR_REFRESH_INTERVAL:
        try:
            monitors_cache = get_monitors()
            last_monitor_check = current_time
        except Exception as e:
            print(f"Error getting monitors: {e}")
            # Fallback to primary monitor if available
            if monitors_cache is None:
                monitors_cache = []
    return monitors_cache

def is_in_top_left_corner():
    """Check if cursor is in top-left corner of any monitor"""
    try:
        x, y = pyautogui.position()
        threshold = CORNER_THRESHOLD

        for monitor in get_cached_monitors():
            # Top-left of each monitor
            left = monitor.x
            top = monitor.y

            if left <= x <= left + threshold and top <= y <= top + threshold:
                return True
    except Exception as e:
        print(f"Error checking cursor position: {e}")
    return False

def win_tab():
    """Trigger Windows Task View (Win + Tab)"""
    try:
        ctypes.windll.user32.keybd_event(0x5B, 0, 0, 0)  # Win key down
        ctypes.windll.user32.keybd_event(0x09, 0, 0, 0)  # Tab key down
        ctypes.windll.user32.keybd_event(0x09, 0, 2, 0)  # Tab key up
        ctypes.windll.user32.keybd_event(0x5B, 0, 2, 0)  # Win key up
    except Exception as e:
        print(f"Error sending key combination: {e}")

def create_image():
    """Create an icon image for the system tray"""
    width = 64
    height = 64
    image = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    dc = ImageDraw.Draw(image)
    dc.ellipse((8, 8, width - 8, height - 8), fill='orange')
    return image

def on_pause_resume(icon, item):
    """Toggle pause/resume state"""
    global paused
    paused = not paused
    status = "Paused" if paused else "Running"
    print(f"Hot corner detection {status}")
    if icon:
        icon.update_menu()

def on_quit(icon, item):
    """Quit the application"""
    global running
    running = False
    cleanup()
    if icon:
        icon.stop()

def cleanup():
    """Clean up resources"""
    try:
        keyboard.unhook_all()
        print("Cleanup completed")
    except Exception as e:
        print(f"Error during cleanup: {e}")

def run_hot_corner(icon):
    """Main hot corner detection loop"""
    global paused, running
    print("Hot corner running. Press Ctrl+Alt+P to pause/resume.")

    # Register global hotkey Ctrl+Alt+P for pause/resume
    try:
        keyboard.add_hotkey('ctrl+alt+p', lambda: on_pause_resume(icon, None))
    except Exception as e:
        print(f"Error registering hotkey: {e}")

    last_trigger_time = 0
    
    while running:
        try:
            if not paused:
                current_time = time.time()
                
                # Check if enough time has passed since last trigger (debounce)
                if (current_time - last_trigger_time) >= DEBOUNCE_DELAY:
                    if is_in_top_left_corner():
                        print("Top-left corner detected! Opening Task View (Win + Tab)")
                        win_tab()
                        last_trigger_time = current_time
                        
                        # Wait for cursor to leave corner before checking again
                        while is_in_top_left_corner() and running:
                            time.sleep(0.05)  # Short sleep while waiting
                            
        except Exception as e:
            print(f"Error in hot corner loop: {e}")
            
        time.sleep(CHECK_INTERVAL)

def main():
    """Main function to start the application"""
    global icon
    
    # Set up cleanup on exit
    atexit.register(cleanup)
    
    try:
        icon = pystray.Icon("hotcorner", create_image(), "Hot Corner")

        icon.menu = pystray.Menu(
            pystray.MenuItem(
                lambda item: "Resume" if paused else "Pause",
                on_pause_resume
            ),
            pystray.MenuItem("Quit", on_quit)
        )

        # Run hot corner detection in a separate thread to not block tray
        detection_thread = threading.Thread(target=run_hot_corner, args=(icon,), daemon=True)
        detection_thread.start()

        # Start the system tray icon
        icon.run()
        
    except Exception as e:
        print(f"Error starting application: {e}")
        cleanup()

if __name__ == "__main__":
    main()