import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk
import win32api
import winsound
import time

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

root = tk.Tk()
root.title('ROFLS')
root.resizable(0, 0)

# Window
window_width = 500
window_height = 800
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
position_top = int(screen_height / 2 - window_height / 2)
position_right = int(screen_width / 2 - window_width / 2)
root.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')

# Create gradient background
gradient = create_gradient(window_width, window_height, '#4B0082', '#2E2E2E')
background_label = tk.Label(root, image=gradient)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

recoil_patterns = [
    {"Down": 5.0, "Up": 0.0, "Left": 0.0, "Right": 0.0, "Recommendation": "Pattern 1: Full grade G36/K2/Scar"},
    {"Down": 5.2, "Up": 0.0, "Left": 0.0, "Right": 0.0, "Recommendation": "Pattern 2: Full grade M416/ACE RED+Muzzle brake+Heavy stock"},
    {"Down": 6.9, "Up": 0.0, "Left": 0.0, "Right": 0.0, "Recommendation": "Pattern 3: AUG/AKM RED+Muzzle brake"},
    {"Down": 7.1, "Up": 0.0, "Left": 0.0, "Right": 0.0, "Recommendation": "Pattern 4: GROZA/FAMAS Muzzle brake"},
    {"Down": 7.6, "Up": 0.0, "Left": 0.0, "Right": 0.0, "Recommendation": "Pattern 5: BERYL RED+Muzzle brake"},
    {"Down": 18.0, "Up": 0.0, "Left": 0.0, "Right": 0.0, "Recommendation": "Pattern 6: Full grade SLR/SKS"},

    {"Down": 21.0, "Up": 0.0, "Left": 0.0, "Right": 0.0, "Recommendation": "Pattern 7: G36/K2/Scar 3x"},
    {"Down": 21.1, "Up": 0.0, "Left": 0.0, "Right": 0.0, "Recommendation": "Pattern 8: M416 3x"},
    {"Down": 26.5, "Up": 0.0, "Left": 0.0, "Right": 0.0, "Recommendation": "Pattern 9: AUG/AKM 3x"},
    {"Down": 27.7, "Up": 0.0, "Left": 0.0, "Right": 0.0, "Recommendation": "Pattern 10: GROZA/FAMAS Muzzle brake 3x"},
    {"Down": 29.9, "Up": 0.0, "Left": 0.0, "Right": 0.0, "Recommendation": "Pattern 11: BERYL RED+Muzzle brake 3x"}
]
current_pattern = 0
num_patterns = len(recoil_patterns)
vertical_sensitivity_multiplier = tk.DoubleVar(value=1.0)
crouch_key = tk.StringVar(value="CTRL")

def StatusChange():
    if StatusMode['text'] == "OFF":
        time.sleep(0.2)
        StatusMode.config(text="ON", foreground="green")
        winsound.Beep(1000, 420)
    elif StatusMode['text'] == "ON":
        time.sleep(0.2)
        StatusMode.config(text="OFF", foreground="red")
        winsound.Beep(2500, 400)

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
        0x11: "CTRL", 0x12: "ALT", 0x10: "SHIFT", 0x43: "C"
    }
    for key, name in keys.items():
        if win32api.GetKeyState(key) < 0 and name == saveKey():
            StatusChange()
            break
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

def save_current_pattern():
    pattern = {
        "Down": float(RecoilDownSpinbox.get()), 
        "Up": float(RecoilUpSpinbox.get()),
        "Left": float(RecoilLeftSpinbox.get()), 
        "Right": float(RecoilRightSpinbox.get()),
        "Recommendation": RecommendationLabel['text']
    }
    recoil_patterns[current_pattern] = pattern

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
        current_pattern = (current_pattern - 5) % num_patterns
    elif direction == 'down':
        current_pattern = (current_pattern + 5) % num_patterns
    if current_pattern != previous_pattern:
        load_current_pattern()
        winsound.Beep(800, 200)

def load_current_pattern():
    pattern = recoil_patterns[current_pattern]
    RecoilDownSpinbox.delete(0, tk.END)
    RecoilDownSpinbox.insert(0, pattern["Down"])
    RecoilUpSpinbox.delete(0, tk.END)
    RecoilUpSpinbox.insert(0, pattern["Up"])
    RecoilLeftSpinbox.delete(0, tk.END)
    RecoilLeftSpinbox.insert(0, pattern["Left"])
    RecoilRightSpinbox.delete(0, tk.END)
    RecoilRightSpinbox.insert(0, pattern["Right"])
    PatternLabel.config(text=f"Current Pattern: {current_pattern + 1}")
    RecommendationLabel.config(text=pattern.get("Recommendation", ""))

def recoil():
    if mouse_down() and StatusMode['text'] == 'ON':
        Down = float(RecoilDownSpinbox.get()) / vertical_sensitivity_multiplier.get()
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

style = ttk.Style()
style.theme_use('clam')

# Настройка цветов
style.configure('TFrame', background='#2E2E2E')
style.configure('TLabel', background='#2E2E2E', foreground='#D3D3D3', font=("Segoe UI", 10))
style.configure('TButton', background='#4B0082', foreground='#D3D3D3', font=("Segoe UI", 10, "bold"))
style.configure('TCombobox', fieldbackground='#4B0082', background='#2E2E2E', foreground='#D3D3D3', font=("Segoe UI", 10))
style.configure('TSpinbox', fieldbackground='#4B0082', background='#2E2E2E', foreground='#D3D3D3', font=("Segoe UI", 10))

#Status
TitleFrame = ttk.Frame(root)
TitleFrame.pack(pady=10)
TitleLabel = ttk.Label(TitleFrame, text="iArlequino NoRecoil", font=("Segoe UI", 16, "bold"))
TitleLabel.pack()
StatusFrame = ttk.Frame(root)
StatusFrame.pack(pady=5)
StatusLabel = ttk.Label(StatusFrame, text="Status:", font=("Segoe UI", 12))
StatusLabel.pack(side=tk.LEFT)
StatusMode = ttk.Label(StatusFrame, text="OFF", font=("Segoe UI", 12), foreground="red")
StatusMode.pack(side=tk.LEFT, padx=5)

#Sensitivity
ConfigFrame = ttk.Frame(root)
ConfigFrame.pack(pady=5)
KeyLabel = ttk.Label(ConfigFrame, text="On/Off Key:", font=("Segoe UI", 12))
KeyLabel.grid(row=0, column=0, padx=5, pady=5, sticky='e')
KeyCombobox = ttk.Combobox(ConfigFrame, state="readonly", values=[
    "F1", "F2", "F3", "F4", "F5", "F6",
    "F7", "F8", "F9", "F11", "F12", "ENTER", "SUPR", "CAPSLOCK", "NUM_LOCK"
], width=10, font=("Segoe UI", 12))
KeyCombobox.grid(row=0, column=1, padx=5, pady=5, sticky='w')
KeyCombobox.current(0)
GeneralInfoLabel = ttk.Label(ConfigFrame, text="[Gen-50] [Vert-1.0] [Shoulder-50] [Sight-50] [XScope-35]", font=("Segoe UI", 10))
GeneralInfoLabel.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

#Recoil
RecoilConfig = ttk.LabelFrame(root, text="Settings", padding=(10, 10))
RecoilConfig.pack(pady=5)
RecoilDownLabel = ttk.Label(RecoilConfig, text="Down", font=("Segoe UI", 10))
RecoilDownLabel.grid(row=0, column=0, padx=5, pady=5)
RecoilDownSpinbox = ttk.Spinbox(RecoilConfig, from_=0, to=100, increment=0.1, width=6, font=("Segoe UI", 10))
RecoilDownSpinbox.set(recoil_patterns[current_pattern]["Down"])
RecoilDownSpinbox.grid(row=1, column=0, padx=5, pady=5)
RecoilUpLabel = ttk.Label(RecoilConfig, text="Up", font=("Segoe UI", 10))
RecoilUpLabel.grid(row=0, column=1, padx=5, pady=5)
RecoilUpSpinbox = ttk.Spinbox(RecoilConfig, from_=0, to=100, increment=0.1, width=6, font=("Segoe UI", 10))
RecoilUpSpinbox.set(recoil_patterns[current_pattern]["Up"])
RecoilUpSpinbox.grid(row=1, column=1, padx=5, pady=5)
RecoilLeftLabel = ttk.Label(RecoilConfig, text="Left", font=("Segoe UI", 10))
RecoilLeftLabel.grid(row=0, column=2, padx=5, pady=5)
RecoilLeftSpinbox = ttk.Spinbox(RecoilConfig, from_=0, to=100, increment=0.1, width=6, font=("Segoe UI", 10))
RecoilLeftSpinbox.set(recoil_patterns[current_pattern]["Left"])
RecoilLeftSpinbox.grid(row=1, column=2, padx=5, pady=5)
RecoilRightLabel = ttk.Label(RecoilConfig, text="Right", font=("Segoe UI", 10))
RecoilRightLabel.grid(row=0, column=3, padx=5, pady=5)
RecoilRightSpinbox = ttk.Spinbox(RecoilConfig, from_=0, to=100, increment=0.1, width=6, font=("Segoe UI", 10))
RecoilRightSpinbox.set(recoil_patterns[current_pattern]["Right"])
RecoilRightSpinbox.grid(row=1, column=3, padx=5, pady=5)
SaveButton = ttk.Button(RecoilConfig, text="Save Settings", command=save_current_pattern)
SaveButton.grid(row=2, column=0, columnspan=4, padx=5, pady=10)

# Vertical Sensitivity Multiplier
MultiplierFrame = ttk.LabelFrame(root, text="Vertical Sensitivity Multiplier", padding=(10, 10))
MultiplierFrame.pack(pady=5)
MultiplierLabel = ttk.Label(MultiplierFrame, text="Multiplier", font=("Segoe UI", 10))
MultiplierLabel.grid(row=0, column=0, padx=5, pady=5)
MultiplierSpinbox = ttk.Spinbox(MultiplierFrame, from_=0.5, to=2.0, increment=0.1, textvariable=vertical_sensitivity_multiplier, width=6, font=("Segoe UI", 10))
MultiplierSpinbox.grid(row=1, column=0, padx=5, pady=5)

# SHIFT Status
ShiftStatusFrame = ttk.Frame(root)
ShiftStatusFrame.pack(pady=5)
ShiftStatusLabel = ttk.Label(ShiftStatusFrame, text="SHIFT: OFF", font=("Segoe UI", 12), foreground="red")
ShiftStatusLabel.pack()

# Crouch Key
CrouchKeyFrame = ttk.Frame(root)
CrouchKeyFrame.pack(pady=5)
CrouchKeyLabel = ttk.Label(CrouchKeyFrame, text="Crouch Key:", font=("Segoe UI", 12))
CrouchKeyLabel.pack(side=tk.LEFT)
CrouchKeyCombobox = ttk.Combobox(CrouchKeyFrame, state="readonly", values=["CTRL", "ALT", "SHIFT", "C"], textvariable=crouch_key, width=10, font=("Segoe UI", 12))
CrouchKeyCombobox.pack(side=tk.LEFT, padx=5)
CrouchKeyCombobox.current(0)

# Crouch Status
CrouchStatusFrame = ttk.Frame(root)
CrouchStatusFrame.pack(pady=5)
CrouchStatusLabel = ttk.Label(CrouchStatusFrame, text="CTRL: OFF", font=("Segoe UI", 12), foreground="red")
CrouchStatusLabel.pack()

#Pattern
PatternLabel = ttk.Label(root, text=f"Current Pattern: {current_pattern + 1}", font=("Segoe UI", 12))
PatternLabel.pack(pady=5)
RecommendationLabel = ttk.Label(root, text=recoil_patterns[current_pattern]["Recommendation"], wraplength=350, font=("Segoe UI", 10))
RecommendationLabel.pack(pady=5)

#Instructions
InstructionsLabel = ttk.Label(root, text="Use Arrow Keys to switch patterns:\nLeft/Right to change pattern\nUp/Down to jump 5 patterns", font=("Segoe UI", 10), foreground="gray")
InstructionsLabel.pack(pady=5)

#StatusBar
StatusBar = ttk.Label(root, text="Ready", relief=tk.SUNKEN, anchor='w', font=("Segoe UI", 10))
StatusBar.pack(side=tk.BOTTOM, fill=tk.X)

load_current_pattern()
root.mainloop()



