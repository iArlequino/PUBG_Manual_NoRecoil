import tkinter as tk
from tkinter import messagebox, simpledialog
from tkinter import ttk
from PIL import Image, ImageTk
import win32api
import time
import pyttsx3
import json
import os
from datetime import datetime
import threading
import hashlib
import uuid
import numpy as np
from PIL import ImageGrab

def create_gradient(width, height, color1, color2):
    base = Image.new('RGB', (width, height), color1)
    top = Image.new('RGB', (width, height), color2)
    mask = Image.new('L', (width, height))
    mask_data = []
    for y in range(height):
        mask_data.extend([int(255 * (y / height))] * width)
    mask.putdata(mask_data)
    base.paste(top, (0, 0), mask)
    return ImageTk.PhotoImage(base)

def create_background_image(image_path):
    image = Image.open(image_path)
    return ImageTk.PhotoImage(image)

def get_hardware_id():
    return hashlib.md5(uuid.getnode().to_bytes(6, 'little')).hexdigest()

def validate_product_key(product_key):
    if product_key == "1169":
        return True
    hardware_id = get_hardware_id()
    expected_key = hashlib.md5(hardware_id.encode()).hexdigest()
    return product_key == expected_key

def prompt_for_product_key():
    product_key = tk.simpledialog.askstring("Product Key", "Enter your product key:")
    if not product_key or not validate_product_key(product_key):
        messagebox.showerror("Invalid Key", "The product key is invalid or already used on another computer.")
        root.destroy()
    else:
        with open("LIC.txt", "w") as file:
            file.write(product_key)

def check_product_key():
    if os.path.exists("LIC.txt"):
        with open("LIC.txt", "r") as file:
            product_key = file.read().strip()
            if not validate_product_key(product_key):
                prompt_for_product_key()
    else:
        prompt_for_product_key()

root = tk.Tk()
root.title('ROFLS')
root.resizable(0, 0)

# Инициализация синтезатора речи
engine = pyttsx3.init()
engine.setProperty('rate', 360)  # Скорость речи

# Окно
window_width = 1536
window_height = 864
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
position_top = int(screen_height / 2 - window_height / 2)
position_right = int(screen_width / 2 - window_width / 2)
root.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')

# Создание фонового изображения
background_image = create_background_image("img.jpg")
background_label = tk.Label(root, image=background_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# Создание фреймов для макета
left_frame = ttk.Frame(root)
left_frame.place(x=0, y=0, width=400, height=720)

right_frame = ttk.Frame(root)
right_frame.place(x=1136, y=0, width=400, height=720)

bottom_frame = ttk.Frame(root)
bottom_frame.place(x=0, y=720, width=1536, height=144)

recoil_patterns = [
    {"Down": 6.0, "Up": 0.0, "Left": 0.0, "Right": 0.0, "Recommendation": "Pattern 1.0: Stock G36/K2/Scar"},
    {"Down": 8.2, "Up": 0.0, "Left": 0.0, "Right": 0.0, "Recommendation": "Pattern 2.0: Stock M416/ACE"},
    {"Down": 8.7, "Up": 0.0, "Left": 0.0, "Right": 0.0, "Recommendation": "Pattern 3.0: Stock UG/AKM"},
    {"Down": 8.8, "Up": 0.0, "Left": 0.0, "Right": 0.0, "Recommendation": "Pattern 4.0: Stock FAMAS"},
    {"Down": 9.4, "Up": 0.0, "Left": 0.0, "Right": 0.0, "Recommendation": "Pattern 5.0: Stock BERYL"},
    
    {"Down": 5.0, "Up": 0.0, "Left": 0.0, "Right": 0.0, "Recommendation": "Pattern 1.1: Full grade G36/K2/Scar"},
    {"Down": 5.2, "Up": 0.0, "Left": 0.0, "Right": 0.0, "Recommendation": "Pattern 2.1: Full grade M416/ACE RED+Muzzle brake+Heavy stock"},
    {"Down": 6.9, "Up": 0.0, "Left": 0.0, "Right": 0.0, "Recommendation": "Pattern 3.1: Full grade AUG/AKM RED+Muzzle brake"},
    {"Down": 7.1, "Up": 0.0, "Left": 0.0, "Right": 0.0, "Recommendation": "Pattern 4.1: Full grade GROZA/FAMAS Muzzle brake"},
    {"Down": 7.6, "Up": 0.0, "Left": 0.0, "Right": 0.0, "Recommendation": "Pattern 5.1: Full grade BERYL RED+Muzzle brake"},

    {"Down": 21.0, "Up": 0.0, "Left": 0.0, "Right": 0.0, "Recommendation": "Pattern 1.3: Full grade G36/K2/Scar 3x"},
    {"Down": 21.1, "Up": 0.0, "Left": 0.0, "Right": 0.0, "Recommendation": "Pattern 2.3: Full grade M416/ACE RED+Muzzle brake+Heavy stock 3x"},
    {"Down": 28.8, "Up": 0.0, "Left": 0.0, "Right": 0.0, "Recommendation": "Pattern 3.3: AUG/AKM RED+Muzzle brake 3x"},
    {"Down": 30.9, "Up": 0.0, "Left": 0.0, "Right": 0.0, "Recommendation": "Pattern 4.3: GROZA/FAMAS Muzzle brake 3x"},
    {"Down": 34.8, "Up": 0.0, "Left": 0.0, "Right": 0.0, "Recommendation": "Pattern 5.3: BERYL RED+Muzzle brake 3x"},

    {"Down": 35.0, "Up": 0.0, "Left": 0.0, "Right": 0.0, "Recommendation": "Pattern 1.4: Full grade G36/K2/Scar 4x"},
    {"Down": 35.9, "Up": 0.0, "Left": 0.0, "Right": 0.0, "Recommendation": "Pattern 2.4: Full grade M416/ACE RED+Muzzle brake+Heavy stock 4x"},
    {"Down": 47.0, "Up": 0.0, "Left": 0.0, "Right": 0.0, "Recommendation": "Pattern 3.4: AUG/AKM RED+Muzzle brake 4x"},
    {"Down": 47.7, "Up": 0.0, "Left": 0.0, "Right": 0.0, "Recommendation": "Pattern 4.4: GROZA/FAMAS Muzzle brake 4x"},
    {"Down": 50.9, "Up": 0.0, "Left": 0.0, "Right": 0.0, "Recommendation": "Pattern 5.4: BERYL RED+Muzzle brake 4x"},

    {"Down": 46.7, "Up": 0.0, "Left": 0.0, "Right": 0.0, "Recommendation": "Pattern 1.6: Full grade G36/K2/Scar 6x"},
    {"Down": 48.7, "Up": 0.0, "Left": 0.0, "Right": 0.0, "Recommendation": "Pattern 2.6: Full grade M416/ACE RED+Muzzle brake+Heavy stock 6x"},
    {"Down": 59.7, "Up": 0.0, "Left": 0.0, "Right": 0.0, "Recommendation": "Pattern 3.6: AUG/AKM RED+Muzzle brake 6x"},
    {"Down": 62.7, "Up": 0.0, "Left": 0.0, "Right": 0.0, "Recommendation": "Pattern 4.6: GROZA/FAMAS Muzzle brake 6x"},
    {"Down": 64.0, "Up": 0.0, "Left": 0.0, "Right": 0.0, "Recommendation": "Pattern 5.6: BERYL RED+Muzzle brake 6x"}

]

# Проверка количества паттернов
assert len(recoil_patterns) == 25, "Количество паттернов должно быть 25"

current_pattern = 0
num_patterns = len(recoil_patterns)
vertical_sensitivity_multiplier = tk.DoubleVar(value=1.0)
resolution_sensitivity_multiplier = tk.DoubleVar(value=1.0)
resolution_choice = tk.StringVar(value="1920x1080")

# Множители для всех разрешений
resolution_multipliers = {
    "2560x1440": tk.DoubleVar(value=1.0),
    "1920x1080": tk.DoubleVar(value=1.0),
    "2304x1440": tk.DoubleVar(value=1.0),
    "1728x1080": tk.DoubleVar(value=1.0),
    "1920x1440": tk.DoubleVar(value=1.0),
    "1440x1080": tk.DoubleVar(value=1.0)
}

crouch_key = tk.StringVar(value="CTRL")
sound_muted = tk.BooleanVar(value=False)
spam_lmb_enabled = tk.BooleanVar(value=False)
mouse_button_choice = tk.StringVar(value="Mouse4")
recoil_mode = tk.StringVar(value="Toggle")

# Переменная для хранения текущего языка
current_language = tk.StringVar(value="EN")

# Переменные для хранения состояния макроса и мута оружий
macro_enabled = tk.BooleanVar(value=True)
mute_weapon1 = tk.BooleanVar(value=False)
mute_weapon2 = tk.BooleanVar(value=False)

def StatusChange():
    if StatusMode['text'] == "OFF":
        time.sleep(0.2)
        StatusMode.config(text="ON", foreground="green")
        if not sound_muted.get():
            engine.say("ON")
            engine.runAndWait()
    elif StatusMode['text'] == "ON":
        time.sleep(0.2)
        StatusMode.config(text="OFF", foreground="red")
        if not sound_muted.get():
            engine.say("OFF")
            engine.runAndWait()

def saveKey():
    key = KeyCombobox.get()
    return key

def on_key_press():
    keys = {
        0x25: "LEFT",
        0x27: "RIGHT", 
        0x26: "UP",     
        0x28: "DOWN",
        0x70: "F1", 0x71: "F2", 0x72: "F3", 0x73: "F4", 0x74: "F5", 0x75: "F6",
        0x76: "F7", 0x77: "F8", 0x78: "F9", 0x79: "F10", 0x7A: "F11", 0x7B: "F12",
        0x2E: "SUPR", 0x0D: "ENTER", 0x14: "CAPSLOCK", 0x90: "NUM_LOCK",
        0x11: "CTRL", 0x12: "ALT", 0x10: "SHIFT", 0x43: "C", 0x2D: "INS",
        0x31: "1", 0x32: "2"  # Добавлены клавиши 1 и 2
    }
    for key, name in keys.items():
        if win32api.GetKeyState(key) < 0 and name == saveKey():
            StatusChange()
            break
        elif win32api.GetKeyState(key) < 0 and name == "1":
            if mute_weapon1.get():
                macro_enabled.set(False)
                MacroStatusLabel.config(text="Macro: OFF", foreground="red")
                if not sound_muted.get():
                    engine.say("SN")
                    engine.runAndWait()
            else:
                macro_enabled.set(True)
                MacroStatusLabel.config(text="Macro: ON", foreground="green")
                if not sound_muted.get():
                    engine.say("R")
                    engine.runAndWait()
        elif win32api.GetKeyState(key) < 0 and name == "2":
            if mute_weapon2.get():
                macro_enabled.set(False)
                MacroStatusLabel.config(text="Macro: OFF", foreground="red")
                if not sound_muted.get():
                    engine.say("SN")
                    engine.runAndWait()
            else:
                macro_enabled.set(True)
                MacroStatusLabel.config(text="Macro: ON", foreground="green")
                if not sound_muted.get():
                    engine.say("R")
                    engine.runAndWait()
    if win32api.GetKeyState(0x25) < 0:
        switch_pattern('left')
    elif win32api.GetKeyState(0x27) < 0:
        switch_pattern('right')
    elif win32api.GetKeyState(0x26) < 0:
        switch_pattern('up')
    elif win32api.GetKeyState(0x28) < 0:
        switch_pattern('down')
    root.after(100, on_key_press)
root.after(100, on_key_press)

def save_patterns_to_file():
    with open("recoil_patterns.json", "w") as file:
        json.dump(recoil_patterns, file)

def load_patterns_from_file():
    global recoil_patterns
    try:
        with open("recoil_patterns.json", "r") as file:
            recoil_patterns = json.load(file)
    except FileNotFoundError:
        pass

def save_settings_to_file():
    settings = {
        "recoil_patterns": recoil_patterns,
        "on_off_key": KeyCombobox.get(),
        "crouch_key": crouch_key.get(),
        "vertical_sensitivity_multiplier": vertical_sensitivity_multiplier.get(),
        "resolution_sensitivity_multiplier": resolution_sensitivity_multiplier.get(),
        "current_language": current_language.get(),
        "macro_enabled": macro_enabled.get(),
        "mute_weapon1": mute_weapon1.get(),
        "mute_weapon2": mute_weapon2.get(),
        "sound_muted": sound_muted.get(),
        "spam_lmb_enabled": spam_lmb_enabled.get(),
        "mouse_button_choice": mouse_button_choice.get(),
        "recoil_mode": recoil_mode.get(),
        "resolution_choice": resolution_choice.get(),
        "resolution_multipliers": {key: var.get() for key, var in resolution_multipliers.items()}
    }
    with open("settings.json", "w", encoding='utf-8') as file:
        json.dump(settings, file, ensure_ascii=False, indent=4)

def load_settings_from_file():
    global recoil_patterns
    try:
        with open("settings.json", "r", encoding='utf-8') as file:
            settings = json.load(file)
            recoil_patterns = settings.get("recoil_patterns", recoil_patterns)
            KeyCombobox.set(settings.get("on_off_key", "F1"))
            crouch_key.set(settings.get("crouch_key", "CTRL"))
            vertical_sensitivity_multiplier.set(settings.get("vertical_sensitivity_multiplier", 1.0))
            resolution_sensitivity_multiplier.set(settings.get("resolution_sensitivity_multiplier", 1.0))
            current_language.set(settings.get("current_language", "EN"))
            macro_enabled.set(settings.get("macro_enabled", True))
            mute_weapon1.set(settings.get("mute_weapon1", False))
            mute_weapon2.set(settings.get("mute_weapon2", False))
            sound_muted.set(settings.get("sound_muted", False))
            spam_lmb_enabled.set(settings.get("spam_lmb_enabled", False))
            mouse_button_choice.set(settings.get("mouse_button_choice", "Mouse4"))
            recoil_mode.set(settings.get("recoil_mode", "Toggle"))
            resolution_choice.set(settings.get("resolution_choice", "1920x1080"))
            for key, var in resolution_multipliers.items():
                var.set(settings.get("resolution_multipliers", {}).get(key, 1.0))
            apply_language_settings()
    except FileNotFoundError:
        pass

def save_current_pattern():
    pattern = {
        "Down": float(RecoilDownSpinbox.get()), 
        "Up": float(RecoilUpSpinbox.get()),
        "Left": float(RecoilLeftSpinbox.get()), 
        "Right": float(RecoilRightSpinbox.get()),
        "Recommendation": RecommendationLabel['text']
    }
    recoil_patterns[current_pattern] = pattern
    save_settings_to_file()

def mouse_down():
    lmb_state = win32api.GetKeyState(0x01)
    return lmb_state < 0
root.after(100, mouse_down)

def switch_pattern(direction):
    global current_pattern
    previous_pattern = current_pattern
    save_current_pattern()
    if direction == 'left':
        current_pattern = (current_pattern - 1) % num_patterns
    elif direction == 'right':
        current_pattern = (current_pattern + 1) % num_patterns
    elif direction == 'up':
        current_pattern = (current_pattern + 5) % num_patterns
    elif direction == 'down':
        current_pattern = (current_pattern - 5) % num_patterns
    if current_pattern < 0:
        current_pattern += num_patterns
    if current_pattern != previous_pattern:
        load_current_pattern()
        pattern_number = (current_pattern % 5) + 1
        if current_pattern < 5:
            pattern_type = " stock"
        elif current_pattern < 10:
            pattern_type = ""
        elif current_pattern < 15:
            pattern_type = " 3x"
        elif current_pattern < 20:
            pattern_type = " 4x"
        else:
            pattern_type = " 6x"
        if not sound_muted.get():
            engine.say(f"Pattern {pattern_number}{pattern_type}")
            engine.runAndWait()

def load_current_pattern():
    global current_pattern
    if 0 <= current_pattern < num_patterns:
        pattern = recoil_patterns[current_pattern]
        RecoilDownSpinbox.delete(0, tk.END)
        RecoilDownSpinbox.insert(0, pattern["Down"])
        RecoilUpSpinbox.delete(0, tk.END)
        RecoilUpSpinbox.insert(0, pattern["Up"])
        RecoilLeftSpinbox.delete(0, tk.END)
        RecoilLeftSpinbox.insert(0, pattern["Left"])
        RecoilRightSpinbox.delete(0, tk.END)
        RecoilRightSpinbox.insert(0, pattern["Right"])
        pattern_number = (current_pattern % 5) + 1
        if current_pattern < 5:
            pattern_type = " stock"
        elif current_pattern < 10:
            pattern_type = ""
        elif current_pattern < 15:
            pattern_type = " 3x"
        elif current_pattern < 20:
            pattern_type = " 4x"
        else:
            pattern_type = " 6x"
        PatternLabel.config(text=f"Current Pattern: {current_pattern + 1} ({pattern_number}{pattern_type})")
        RecommendationLabel.config(text=f"{pattern.get('Recommendation', '')} (Index: {current_pattern + 1})")
    else:
        current_pattern = 0
        load_current_pattern()

def recoil():
    if macro_enabled.get() and ((recoil_mode.get() == "Toggle" and mouse_down() and StatusMode['text'] == 'ON') or (recoil_mode.get() == "Hold" and mouse_down() and win32api.GetKeyState(0x02) < 0)):
        Down = float(RecoilDownSpinbox.get()) / (vertical_sensitivity_multiplier.get() * resolution_sensitivity_multiplier.get())
        if win32api.GetKeyState(0x10) < 0:  # Проверка состояния клавиши SHIFT
            Down *= 1.2
            ShiftStatusLabel.config(text="SHIFT: ON", foreground="green")
        else:
            ShiftStatusLabel.config(text="SHIFT: OFF", foreground="red")
        
        crouch_key_code = {
            "CTRL": 0x11,
            "ALT": 0x12,
            "SHIFT": 0x10,
            "C": 0x43
        }.get(crouch_key.get(), 0x11)
        
        if win32api.GetKeyState(crouch_key_code) < 0:  # Проверка состояния клавиши приседания
            Down *= 0.9
            CrouchStatusLabel.config(text=f"{crouch_key.get()}: ON", foreground="green")
        else:
            CrouchStatusLabel.config(text=f"{crouch_key.get()}: OFF", foreground="red")
        
        Up = float(RecoilUpSpinbox.get())
        Left = float(RecoilLeftSpinbox.get())
        Right = float(RecoilRightSpinbox.get())
        win32api.mouse_event(0x0001, int(-abs(Left)), int(Down))
        win32api.mouse_event(0x0001, int(Right), int(-abs(Up)))
    root.after(10, recoil)
root.after(10, recoil)

def toggle_sound():
    if sound_muted.get():
        sound_muted.set(False)
        SoundButton.config(text="Mute Sound")
    else:
        sound_muted.set(True)
        SoundButton.config(text="Unmute Sound")

def clear_config():
    if os.path.exists("settings.json"):
        os.remove("settings.json")
    if os.path.exists("recoil_patterns.json"):
        os.remove("recoil_patterns.json")
    load_settings_from_file()
    load_current_pattern()
    update_last_modified_label()

def update_last_modified_label():
    if os.path.exists("settings.json"):
        last_modified = datetime.fromtimestamp(os.path.getmtime("settings.json")).strftime('%Y-%m-%d %H:%M:%S')
        LastModifiedLabel.config(text=f"Last Modified / Последнее изменение: {last_modified}")
    else:
        LastModifiedLabel.config(text="Last Modified / Последнее изменение: N/A")

def toggle_spam_lmb():
    if spam_lmb_enabled.get():
        spam_lmb_enabled.set(False)
        SpamLMBButton.config(text="Enable LMB Spam / Включить спам ЛКМ")
    else:
        spam_lmb_enabled.set(True)
        SpamLMBButton.config(text="Disable LMB Spam / Отключить спам ЛКМ")

def spam_lmb():
    while spam_lmb_enabled.get() and mouse_down():
        win32api.mouse_event(0x0002, 0, 0, 0, 0)  # Левый клик вниз
        win32api.mouse_event(0x0004, 0, 0, 0, 0)  # Левый клик вверх
        time.sleep(1/60)  # Задержка для 60 кликов в секунду

def on_mouse_button_press():
    mouse_button_code = {
        "Mouse4": 0x05,
        "Mouse5": 0x06
    }.get(mouse_button_choice.get(), 0x05)
    
    if win32api.GetKeyState(mouse_button_code) < 0:
        toggle_spam_lmb()
    if spam_lmb_enabled.get() and mouse_down():
        threading.Thread(target=spam_lmb).start()
    root.after(100, on_mouse_button_press)
root.after(100, on_mouse_button_press)

def toggle_recoil_mode():
    if recoil_mode.get() == "Toggle":
        recoil_mode.set("Hold")
        RecoilModeButton.config(text="Switch to Hold Mode / Переключить на режим при зажатой ПКМ")
    else:
        recoil_mode.set("Toggle")
        RecoilModeButton.config(text="Switch to Toggle Mode / Переключить на режим по кнопке")

def apply_language_settings():
    if current_language.get() == "EN":
        InstructionsLabel.config(text="Use Arrow Keys to switch patterns:\nLeft/Right to change pattern\nUp/Down to setup")
        PatternDescriptionLabel.config(text="Pattern example:\n[1 gun Stock] => [1 gun Grade 1x] => [1 gun Grade 3x] => [1 gun Grade 4x] => [1 gun Grade 6x]")
        StatusLabel.config(text="Status:")
        ShiftStatusLabel.config(text="SHIFT: OFF")
        CrouchKeyLabel.config(text="Crouch Key:")
        CrouchStatusLabel.config(text="CTRL: OFF")
        RecoilModeLabel.config(text="Recoil Mode:")
        RecoilModeButton.config(text="Switch to Hold Mode")
        SpamLMBButton.config(text="Enable LMB Spam")
        MouseButtonLabel.config(text="Setup:")
        ClearConfigButton.config(text="Clear Config")
        LastModifiedLabel.config(text="Last Modified: N/A")
        SoundButton.config(text="Mute Sound")
        LanguageButton.config(text="Switch to Russian")
    else:
        InstructionsLabel.config(text="Используйте клавиши со стрелками для переключения паттернов:\nВлево/Вправо для смены паттерна\nВверх/Вниз для выбора режима")
        PatternDescriptionLabel.config(text="Пример паттерна:\n[1 gun Stock] => [1 gun Grade 1x] => [1 gun Grade 3x] => [1 gun Grade 4x] => [1 gun Grade 6x]")
        StatusLabel.config(text="Статус:")
        ShiftStatusLabel.config(text="SHIFT: ВЫКЛ")
        CrouchKeyLabel.config(text="Клавиша приседания:")
        CrouchStatusLabel.config(text="CTRL: ВЫКЛ")
        RecoilModeLabel.config(text="Режим отдачи:")
        RecoilModeButton.config(text="Переключить на режим при зажатой ПКМ")
        SpamLMBButton.config(text="Включить спам ЛКМ")
        MouseButtonLabel.config(text="Настройки:")
        ClearConfigButton.config(text="Очистить конфиг")
        LastModifiedLabel.config(text="Последнее изменение: N/A")
        SoundButton.config(text="Отключить звук")
        LanguageButton.config(text="Switch to English")

# Добавим определение MouseButtonLabel
MouseButtonLabel = ttk.Label(left_frame, text="Setup:", font=("Segoe UI", 12))
MouseButtonLabel.pack(pady=5)

def toggle_language():
    if current_language.get() == "EN":
        current_language.set("RU")
    else:
        current_language.set("EN")
    apply_language_settings()
    save_settings_to_file()

def adjust_resolution_multiplier(resolution):
    resolution_sensitivity_multiplier.set(resolution_multipliers[resolution].get())

def update_resolution_multiplier(resolution):
    resolution_multipliers[resolution].set(resolution_sensitivity_multiplier.get())

def show_pattern_info():
    info_window = tk.Toplevel(root)
    info_window.title("Pattern Info")
    info_window.geometry("400x300")
    
    pattern_count_label = ttk.Label(info_window, text=f"Current number of patterns: {len(recoil_patterns)}", font=("Segoe UI", 12))
    pattern_count_label.pack(pady=10)
    
    add_pattern_button = ttk.Button(info_window, text="Add New Pattern", command=add_new_pattern)
    add_pattern_button.pack(pady=10)

def add_new_pattern():
    new_pattern = {
        "Down": 0.0, "Up": 0.0, "Left": 0.0, "Right": 0.0, "Recommendation": "New Pattern"
    }
    recoil_patterns.append(new_pattern)
    save_patterns_to_file()
    messagebox.showinfo("Pattern Added", "New pattern has been added successfully!")

def toggle_macro():
    if macro_enabled.get():
        macro_enabled.set(False)
        MacroStatusLabel.config(text="Macro: OFF", foreground="red")
    else:
        macro_enabled.set(True)
        MacroStatusLabel.config(text="Macro: ON", foreground="green")

def toggle_mute_weapon1():
    if mute_weapon1.get():
        mute_weapon1.set(False)
        MuteWeapon1Button.config(text="Mute Weapon 1")
    else:
        mute_weapon1.set(True)
        MuteWeapon1Button.config(text="Unmute Weapon 1")

def toggle_mute_weapon2():
    if mute_weapon2.get():
        mute_weapon2.set(False)
        MuteWeapon2Button.config(text="Mute Weapon 2")
    else:
        mute_weapon2.set(True)
        MuteWeapon2Button.config(text="Unmute Weapon 2")

style = ttk.Style()
style.theme_use('clam')

# Настройка цветов
style.configure('TFrame', background='#2E2E2E')
style.configure('TLabel', background='#2E2E2E', foreground='#D3D3D3', font=("Segoe UI", 10))
style.configure('TButton', background='#4B0082', foreground='#D3D3D3', font=("Segoe UI", 10, "bold"))
style.configure('TCombobox', fieldbackground='#4B0082', background='#2E2E2E', foreground='#D3D3D3', font=("Segoe UI", 10))
style.configure('TSpinbox', fieldbackground='#4B0082', background='#2E2E2E', foreground='#D3D3D3', font=("Segoe UI", 10))

# Настройка серого фона для определенных окон
style.configure('Gray.TFrame', background='#4B4B4B')
style.configure('Gray.TLabel', background='#4B4B4B', foreground='#D3D3D3', font=("Segoe UI", 10))
style.configure('Gray.TCombobox', fieldbackground='#4B4B4B', background='#4B4B4B', foreground='#D3D3D3', font=("Segoe UI", 10))
style.configure('Gray.TSpinbox', fieldbackground='#4B4B4B', background='#4B4B4B', foreground='#D3D3D3', font=("Segoe UI", 10))

# Чувствительность
ConfigFrame = ttk.Frame(left_frame, style='Gray.TFrame')
ConfigFrame.pack(pady=5, padx=10, anchor='w')
KeyLabel = ttk.Label(ConfigFrame, text="On/Off Key / Клавиша Вкл/Выкл:", font=("Segoe UI", 12), style='Gray.TLabel')
KeyLabel.grid(row=0, column=0, padx=5, pady=5, sticky='e')
KeyCombobox = ttk.Combobox(ConfigFrame, state="readonly", values=[
    "F1", "F2", "F3", "F4", "F5", "F6",
    "F7", "F8", "F9", "F11", "F12", "ENTER", "SUPR", "CAPSLOCK", "NUM_LOCK"
], width=10, font=("Segoe UI", 12), style='Gray.TCombobox')
KeyCombobox.grid(row=0, column=1, padx=5, pady=5, sticky='w')
KeyCombobox.current(0)

GeneralInfoLabel = ttk.Label(ConfigFrame, text="[Gen-50] [Vert-1.0] [Shoulder-50] [Sight-50] [XScope-35]", font=("Segoe UI", 10), style='Gray.TLabel')
GeneralInfoLabel.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

# Настройки отдачи
RecoilConfig = ttk.LabelFrame(left_frame, text="Recoil Settings / Настройки отдачи", padding=(10, 10), style='Gray.TFrame')
RecoilConfig.pack(pady=5, padx=10, anchor='w')
RecoilDownLabel = ttk.Label(RecoilConfig, text="Down / Вниз:", font=("Segoe UI", 10), style='Gray.TLabel')
RecoilDownLabel.grid(row=0, column=0, padx=5, pady=5, sticky='e')
RecoilDownSpinbox = ttk.Spinbox(RecoilConfig, from_=0, to=100, increment=0.1, width=6, font=("Segoe UI", 10), style='Gray.TSpinbox')
RecoilDownSpinbox.set(recoil_patterns[current_pattern]["Down"])
RecoilDownSpinbox.grid(row=0, column=1, padx=5, pady=5, sticky='w')
RecoilUpLabel = ttk.Label(RecoilConfig, text="Up / Вверх:", font=("Segoe UI", 10), style='Gray.TLabel')
RecoilUpLabel.grid(row=1, column=0, padx=5, pady=5, sticky='e')
RecoilUpSpinbox = ttk.Spinbox(RecoilConfig, from_=0, to=100, increment=0.1, width=6, font=("Segoe UI", 10), style='Gray.TSpinbox')
RecoilUpSpinbox.set(recoil_patterns[current_pattern]["Up"])
RecoilUpSpinbox.grid(row=1, column=1, padx=5, pady=5, sticky='w')
RecoilLeftLabel = ttk.Label(RecoilConfig, text="Left / Влево:", font=("Segoe UI", 10), style='Gray.TLabel')
RecoilLeftLabel.grid(row=2, column=0, padx=5, pady=5, sticky='e')
RecoilLeftSpinbox = ttk.Spinbox(RecoilConfig, from_=0, to=100, increment=0.1, width=6, font=("Segoe UI", 10), style='Gray.TSpinbox')
RecoilLeftSpinbox.set(recoil_patterns[current_pattern]["Left"])
RecoilLeftSpinbox.grid(row=2, column=1, padx=5, pady=5, sticky='w')
RecoilRightLabel = ttk.Label(RecoilConfig, text="Right / Вправо:", font=("Segoe UI", 10), style='Gray.TLabel')
RecoilRightLabel.grid(row=3, column=0, padx=5, pady=5, sticky='e')
RecoilRightSpinbox = ttk.Spinbox(RecoilConfig, from_=0, to=100, increment=0.1, width=6, font=("Segoe UI", 10), style='Gray.TSpinbox')
RecoilRightSpinbox.set(recoil_patterns[current_pattern]["Right"])
RecoilRightSpinbox.grid(row=3, column=1, padx=5, pady=5, sticky='w')

# Множитель вертикальной чувствительности
MultiplierFrame = ttk.LabelFrame(left_frame, text="Vertical Sensitivity Multiplier / Множитель вертикальной чувствительности", padding=(10, 10), style='Gray.TFrame')
MultiplierFrame.pack(pady=5, padx=10, anchor='w')
MultiplierLabel = ttk.Label(MultiplierFrame, text="Multiplier / Множитель:", font=("Segoe UI", 10), style='Gray.TLabel')
MultiplierLabel.grid(row=0, column=0, padx=5, pady=5, sticky='e')
MultiplierSpinbox = ttk.Spinbox(MultiplierFrame, from_=0.5, to=2.0, increment=0.1, textvariable=vertical_sensitivity_multiplier, width=6, font=("Segoe UI", 10), style='Gray.TSpinbox')
MultiplierSpinbox.grid(row=0, column=1, padx=5, pady=5, sticky='w')

# Множитель чувствительности для разрешения
ResolutionMultiplierLabel = ttk.Label(MultiplierFrame, text="Resolution Multiplier / Множитель разрешения:", font=("Segoe UI", 10), style='Gray.TLabel')
ResolutionMultiplierLabel.grid(row=1, column=0, padx=5, pady=5, sticky='e')
ResolutionMultiplierSpinbox = ttk.Spinbox(MultiplierFrame, from_=0.5, to=2.0, increment=0.1, textvariable=resolution_sensitivity_multiplier, width=6, font=("Segoe UI", 10), style='Gray.TSpinbox', command=lambda: update_resolution_multiplier(resolution_choice.get()))
ResolutionMultiplierSpinbox.grid(row=1, column=1, padx=5, pady=5, sticky='w')

# Добавить выбор разрешения экрана с чекбоксами
ResolutionFrame = ttk.LabelFrame(left_frame, text="Resolution / Разрешение", padding=(10, 10), style='Gray.TFrame')
ResolutionFrame.pack(pady=5, padx=10, anchor='w')

def create_resolution_checkbox(frame, text, value):
    return ttk.Radiobutton(frame, text=text, variable=resolution_choice, value=value, command=lambda: adjust_resolution_multiplier(value), style='Gray.TRadiobutton')

# Группа 16:9
Resolution169Label = ttk.Label(ResolutionFrame, text="16:9", font=("Segoe UI", 10), style='Gray.TLabel')
Resolution169Label.grid(row=0, column=0, padx=5, pady=5, sticky='w')
Resolution169_2560x1440 = create_resolution_checkbox(ResolutionFrame, "2560x1440", "2560x1440")
Resolution169_2560x1440.grid(row=1, column=0, padx=5, pady=5, sticky='w')
Resolution169_1920x1080 = create_resolution_checkbox(ResolutionFrame, "1920x1080", "1920x1080")
Resolution169_1920x1080.grid(row=2, column=0, padx=5, pady=5, sticky='w')

# Группа 16:10
Resolution1610Label = ttk.Label(ResolutionFrame, text="16:10", font=("Segoe UI", 10), style='Gray.TLabel')
Resolution1610Label.grid(row=0, column=1, padx=5, pady=5, sticky='w')
Resolution1610_2304x1440 = create_resolution_checkbox(ResolutionFrame, "2304x1440", "2304x1440")
Resolution1610_2304x1440.grid(row=1, column=1, padx=5, pady=5, sticky='w')
Resolution1610_1728x1080 = create_resolution_checkbox(ResolutionFrame, "1728x1080", "1728x1080")
Resolution1610_1728x1080.grid(row=2, column=1, padx=5, pady=5, sticky='w')

# Группа 4:3
Resolution43Label = ttk.Label(ResolutionFrame, text="4:3", font=("Segoe UI", 10), style='Gray.TLabel')
Resolution43Label.grid(row=0, column=2, padx=5, pady=5, sticky='w')
Resolution43_1920x1440 = create_resolution_checkbox(ResolutionFrame, "1920x1440", "1920x1440")
Resolution43_1920x1440.grid(row=1, column=2, padx=5, pady=5, sticky='w')
Resolution43_1440x1080 = create_resolution_checkbox(ResolutionFrame, "1440x1080", "1440x1080")
Resolution43_1440x1080.grid(row=2, column=2, padx=5, pady=5, sticky='w')

# Клавиша приседания
CrouchKeyFrame = ttk.Frame(left_frame, style='Gray.TFrame')
CrouchKeyFrame.pack(pady=5)
CrouchKeyLabel = ttk.Label(CrouchKeyFrame, text="Crouch Key / Клавиша приседания:", font=("Segoe UI", 12), style='Gray.TLabel')
CrouchKeyLabel.pack(side=tk.LEFT)
CrouchKeyCombobox = ttk.Combobox(CrouchKeyFrame, state="readonly", values=["CTRL", "ALT", "SHIFT", "C"], textvariable=crouch_key, width=10, font=("Segoe UI", 12), style='Gray.TCombobox')
CrouchKeyCombobox.pack(side=tk.LEFT, padx=5)
CrouchKeyCombobox.current(0)

# Добавить выбор режима работы отдачи
RecoilModeLabel = ttk.Label(left_frame, text="Recoil Mode / Режим отдачи:", font=("Segoe UI", 12))
RecoilModeLabel.pack(pady=5)
RecoilModeCombobox = ttk.Combobox(left_frame, state="readonly", values=["Toggle", "Hold"], textvariable=recoil_mode, width=10, font=("Segoe UI", 12))
RecoilModeCombobox.pack(pady=5)
RecoilModeCombobox.current(0)

# Кнопки на правом фрейме
SaveButton = ttk.Button(right_frame, text="Save Settings / Сохранить настройки", command=save_current_pattern)
SaveButton.pack(pady=5)
ClearConfigButton = ttk.Button(right_frame, text="Clear Config / Очистить конфиг", command=clear_config)
ClearConfigButton.pack(pady=5)
# Добавить подпись с датой последнего изменения
LastModifiedLabel = ttk.Label(right_frame, text="Last Modified / Последнее изменение: N/A", font=("Segoe UI", 10))
LastModifiedLabel.pack(pady=5)
RecoilModeButton = ttk.Button(right_frame, text="Switch to Hold Mode / Переключить на режим при зажатой ПКМ", command=toggle_recoil_mode)
RecoilModeButton.pack(pady=5)
SoundButton = ttk.Button(right_frame, text="Mute Sound", command=toggle_sound)
SoundButton.pack(pady=5)

# Добавить кнопку включения/выключения спама ЛКМ
SpamLMBButton = ttk.Button(right_frame, text="Enable LMB Spam / Включить спам ЛКМ", command=toggle_spam_lmb)
SpamLMBButton.pack(pady=5)

# Кнопка для отображения информации о паттернах
PatternInfoButton = ttk.Button(right_frame, text="Pattern Info", command=show_pattern_info)
PatternInfoButton.pack(pady=5)

# Кнопки для управления макросом и мута оружий
MuteWeapon1Button = ttk.Button(right_frame, text="Block Weapon 1", command=toggle_mute_weapon1)
MuteWeapon1Button.pack(pady=5)
MuteWeapon2Button = ttk.Button(right_frame, text="Block Weapon 2", command=toggle_mute_weapon2)
MuteWeapon2Button.pack(pady=5)

# Статус
StatusFrame = ttk.Frame(bottom_frame)
StatusFrame.pack(pady=5)
StatusLabel = ttk.Label(StatusFrame, text="Status:", font=("Segoe UI", 12))
StatusLabel.pack(side=tk.LEFT)
StatusMode = ttk.Label(StatusFrame, text="OFF", font=("Segoe UI", 12), foreground="red")
StatusMode.pack(side=tk.LEFT, padx=5)

# Статус SHIFT
ShiftStatusFrame = ttk.Frame(bottom_frame)
ShiftStatusFrame.pack(pady=5)
ShiftStatusLabel = ttk.Label(ShiftStatusFrame, text="SHIFT: OFF", font=("Segoe UI", 12), foreground="red")
ShiftStatusLabel.pack()

# Статус приседания
CrouchStatusFrame = ttk.Frame(bottom_frame)
CrouchStatusFrame.pack(pady=5)
CrouchStatusLabel = ttk.Label(CrouchStatusFrame, text="CTRL: OFF", font=("Segoe UI", 12), foreground="red")
CrouchStatusLabel.pack()

# Статус макроса
MacroStatusLabel = ttk.Label(bottom_frame, text="Macro: ON", font=("Segoe UI", 12), foreground="green")
MacroStatusLabel.pack(pady=5)

# Кнопка смены языка
LanguageButton = ttk.Button(right_frame, text="Переключить на русский", command=toggle_language)
LanguageButton.pack(pady=5)

# Паттерн
PatternLabel = ttk.Label(right_frame, text=f"Current Pattern: {current_pattern + 1}", font=("Segoe UI", 12))
PatternLabel.pack(pady=5)
RecommendationLabel = ttk.Label(right_frame, text=recoil_patterns[current_pattern]["Recommendation"], wraplength=350, font=("Segoe UI", 10))
RecommendationLabel.pack(pady=5)

# Описание работы паттернов
PatternDescriptionLabel = ttk.Label(right_frame, text="Pattern example:\n[1 gun Stock] => [1 gun Grade 1x] => [1 gun Grade 3x] => [1 gun Grade 4x] => [1 gun Grade 6x]", wraplength=350, font=("Segoe UI", 10), foreground="gray")
PatternDescriptionLabel.pack(pady=5)

# Инструкции
InstructionsLabel = ttk.Label(right_frame, text="Use Arrow Keys to switch patterns:\nLeft/Right to change pattern\nUp/Down to setup", font=("Segoe UI", 10), foreground="gray")
InstructionsLabel.pack(pady=5)

# Проверка ключа продукта перед запуском приложения
check_product_key()

load_settings_from_file()
load_current_pattern()
update_last_modified_label()
root.mainloop()




