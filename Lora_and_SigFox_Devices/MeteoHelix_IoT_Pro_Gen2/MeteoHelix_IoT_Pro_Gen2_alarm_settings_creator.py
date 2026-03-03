#Meteo Helix Alarm Settings creator ver.***
#generate hexa string, which can be used to set-up Meteohelix alarm
import sys
import math
import tkinter as tk
from tkinter import ttk

class creator:
    bitLenAlarmType = 2
    bitLenTime  = 9
    bitLenUL    = 2         #spolocny pre vsetky
    bitLenTemp  = 10
    bitLenHum   = 7
    bitLenPress = 13
    bitLenMinInterval = 10
    bitLenDebug = 9

    def __init__(self, alarmType, snoozeTime, tempUpperLower, lowTemp, upTemp, humUpperLower, lowHum, upHum, pressUpperLower, lowPress, upPress, minInterval, debug):
        self.alarmType = alarmType
        self.snoozeTime = snoozeTime

        self.tempUpperLower = tempUpperLower
        self.lowTemp  = lowTemp
        self.upTemp   = upTemp

        self.humUpperLower = humUpperLower
        self.lowHum = lowHum
        self.upHum = upHum

        self.pressUpperLower = pressUpperLower
        self.lowPress = lowPress
        self.upPress = upPress
        self.minInterval = minInterval
        self.debug = debug

        self.alarmString = [0] * 96


    def createAlarm(self):
        self.alarmType = list(str(bin(int(str(int(self.alarmType))))[2:].zfill(self.bitLenAlarmType)))
        self.snoozeTime = list(str(bin(int(str(int(self.snoozeTime/120))))[2:].zfill(self.bitLenTime)))

        self.tempUpperLower = list(str(bin(int(str(int(self.tempUpperLower))))[2:].zfill(self.bitLenUL)))
        self.lowTemp = list(str(bin(int(str(int(((self.lowTemp*10)+500)))))[2:].zfill(self.bitLenTemp)))
        self.upTemp =  list(str(bin(int(str(int(((self.upTemp*10)+500)))))[2:].zfill(self.bitLenTemp)))

        self.humUpperLower = list(str(bin(int(str(int(self.humUpperLower))))[2:].zfill(self.bitLenUL)))
        self.upHum = list(str(bin(int(str(int(self.upHum))))[2:].zfill(self.bitLenHum)))
        self.lowHum = list(str(bin(int(str(int(self.lowHum))))[2:].zfill(self.bitLenHum)))

        self.pressUpperLower = list(str(bin(int(str(int(self.pressUpperLower))))[2:].zfill(self.bitLenUL)))
        self.upPress =  list(str(bin(int(str(int(((self.upPress/10)-3000)))))[2:].zfill(self.bitLenPress)))
        self.lowPress = list(str(bin(int(str(int(((self.lowPress/10)-3000)))))[2:].zfill(self.bitLenPress)))

        self.minInterval = 728 / math.sqrt(self.minInterval)
        self.minInterval = list(str(bin(int(str(int(self.minInterval))))[2:].zfill(self.bitLenMinInterval)))
        self.debug = list(str(bin(int(str(int(self.debug))))[2:].zfill(self.bitLenDebug)))

        self.alarmString = self.alarmType + self.snoozeTime + self.tempUpperLower + self.lowTemp + self.upTemp + self.humUpperLower + self.lowHum + self.upHum + self.pressUpperLower + self.lowPress + self.upPress + self.minInterval + self.debug
        self.alarmString = hex(int(''.join(self.alarmString),2))

        value = int(self.alarmString.replace("0x", ""), 16)
        return f"{value:08x}"


# --- Parameter definitions: (label, range_hint, default_value, is_float) ---
PARAMS = [
    ("Alarm Type",            "0-3",       "3",     False),
    ("Snooze Time [s]",       "0-61440, multiply of 120", "120", False),
    ("Temp Upper/Lower",      "0=OFF 1=Low 2=Up 3=Both",  "0",  False),
    ("Low Temperature [C]",   "-50 to 50", "-16.4", True),
    ("Up Temperature [C]",    "-50 to 50", "2.8",   True),
    ("Hum Upper/Lower",       "0=OFF 1=Low 2=Up 3=Both",  "3",  False),
    ("Low Humidity [%]",      "0-100",     "66",    False),
    ("Up Humidity [%]",       "0-100",     "85",    False),
    ("Press Upper/Lower",     "0=OFF 1=Low 2=Up 3=Both",  "1",  False),
    ("Low Pressure [Pa]",     "0-108300",  "57300", False),
    ("Up Pressure [Pa]",      "0-108300",  "84610", False),
    ("Min Interval [s]",          "0-1023, default 364",       "42", False),
    ("Debug",                 "0-512, not used",           "256",False),
]


def build_gui():
    root = tk.Tk()
    root.title("MeteoHelix IoT Pro Gen2 - Alarm Settings Creator")
    root.resizable(False, False)

    style = ttk.Style()
    style.configure("TLabel", padding=(4, 2))
    style.configure("TEntry", padding=(4, 2))

    # --- Header ---
    ttk.Label(root, text="MeteoHelix IoT Pro Gen2 - Alarm Settings Creator",
              font=("Segoe UI", 12, "bold")).grid(row=0, column=0, columnspan=3, pady=(10, 6))

    # --- Column headers ---
    ttk.Label(root, text="Parameter", font=("Segoe UI", 9, "bold")).grid(row=1, column=0, sticky="w", padx=(10, 4))
    ttk.Label(root, text="Range", font=("Segoe UI", 9, "bold")).grid(row=1, column=1, sticky="w", padx=4)
    ttk.Label(root, text="Value", font=("Segoe UI", 9, "bold")).grid(row=1, column=2, sticky="w", padx=(4, 10))

    ttk.Separator(root, orient="horizontal").grid(row=2, column=0, columnspan=3, sticky="ew", padx=10, pady=2)

    # --- Parameter rows ---
    entries = []
    for i, (label, hint, default, _) in enumerate(PARAMS):
        row = i + 3
        ttk.Label(root, text=label).grid(row=row, column=0, sticky="w", padx=(10, 4))
        ttk.Label(root, text=hint, foreground="gray").grid(row=row, column=1, sticky="w", padx=4)
        entry = ttk.Entry(root, width=14)
        entry.insert(0, default)
        entry.grid(row=row, column=2, sticky="w", padx=(4, 10))
        entries.append(entry)

    ttk.Separator(root, orient="horizontal").grid(row=len(PARAMS)+3, column=0, columnspan=3, sticky="ew", padx=10, pady=6)

    # --- Output area ---
    out_row = len(PARAMS) + 4

    ttk.Label(root, text="Alarm Payload (hex):", font=("Segoe UI", 9, "bold")).grid(
        row=out_row, column=0, sticky="w", padx=(10, 4))
    output_var = tk.StringVar()
    output_entry = ttk.Entry(root, textvariable=output_var, width=30, font=("Consolas", 11))
    output_entry.grid(row=out_row, column=1, columnspan=2, sticky="ew", padx=(4, 10))

    # --- Status label for errors ---
    status_var = tk.StringVar()
    status_label = ttk.Label(root, textvariable=status_var, foreground="red")
    status_label.grid(row=out_row+1, column=0, columnspan=3, padx=10, sticky="w")

    # --- Generate button callback ---
    def on_generate():
        status_var.set("")
        output_var.set("")
        try:
            vals = []
            for j, (label, _, _, is_float) in enumerate(PARAMS):
                text = entries[j].get().strip()
                vals.append(float(text) if is_float else int(text))

            d = creator(*vals)
            result = d.createAlarm()
            output_var.set(result)
        except Exception as e:
            status_var.set(f"Error: {e}")

    # --- Copy to clipboard callback ---
    def on_copy():
        text = output_var.get()
        if text:
            root.clipboard_clear()
            root.clipboard_append(text)
            status_var.set("Copied to clipboard")
            root.after(2000, lambda: status_var.set(""))

    btn_row = out_row + 2
    btn_frame = ttk.Frame(root)
    btn_frame.grid(row=btn_row, column=0, columnspan=3, pady=(4, 10))
    ttk.Button(btn_frame, text="Generate", command=on_generate).pack(side="left", padx=6)
    ttk.Button(btn_frame, text="Copy to Clipboard", command=on_copy).pack(side="left", padx=6)

    root.mainloop()


if __name__ == "__main__":
    build_gui()