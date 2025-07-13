# 🖱️ Hot Corner for Windows

![Python](https://img.shields.io/badge/python-3.7+-blue.svg)
![Platform](https://img.shields.io/badge/platform-Windows-lightgrey.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

Ubuntu-style hot corner for Windows using Python — trigger an action (like opening Task View) when your mouse hits the top-left corner of **any monitor**.

Runs in the system tray with support for pause/resume and multi-monitor setups.

---

## 🚀 Features

- ✅ Top-left corner triggers `Win + Tab` (Task View)
- ✅ Supports multiple monitors
- ✅ Runs quietly in system tray
- ✅ Pause/resume with tray menu or `Ctrl + Alt + P`
- ✅ Lightweight and minimal

---

## 🛠️ Setup

### 1. Clone the repo

```bash
git clone https://github.com/arif-khalil/hot-corner.git
cd hot-corner
````

### 2. Create a virtual environment

```bash
python -m venv .venv
.\.venv\Scripts\activate  # On Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

Or install manually:

```bash
pip install pyautogui pystray pillow keyboard screeninfo
```

---

## ▶️ Run the Script

```bash
python hot_corner.py
```

* The app will minimize to the system tray.
* Move your cursor to the top-left corner of any screen to trigger `Win + Tab`.
* Use `Ctrl + Alt + P` to pause/resume detection.

---

## 🧊 Build a Standalone `.exe`

### 1. Install PyInstaller

```bash
pip install pyinstaller
```

### 2. Build the executable

```bash
pyinstaller --onefile --windowed --icon=icon.ico hot_corner.py
```

* Output will be in the `dist/` folder as `hot_corner.exe`
* No console window will appear thanks to `--windowed`

---

## 🧠 Future Ideas

* Configurable corners and actions
* Custom tray icons and themes
* Settings UI

---

Made with ❤️ for Windows users with Ubuntu muscle memory.
