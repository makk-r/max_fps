import os
import sys
from pathlib import Path

pathdir = os.path.dirname(__file__)

pathpip = Path(pathdir) / "pip.txt"

os.system(f"pip install -r {str(pathpip)} --quiet --upgrade --no-cache-dir")

import customtkinter as ctk
import platform
import subprocess
import requests

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("400x200")
        self.title("Set FPS")
        if platform.system() == "Windows":
            os.system(f"pip install pywin32 --quiet --upgrade --no-cache-dir")
            
            self.fps = ctk.CTkLabel(self, text="FPS: ???")
            self.fps.pack(pady=20)

            self.slider = ctk.CTkSlider(self, from_=1, to=60, number_of_steps=60, command=self.slider_event)
            self.slider.pack(pady=20)

            switch_max_fps = ctk.CTkSwitch(self, text="Max FPS", command=self.switch_event)
            switch_max_fps.pack(pady=20)
        else:
            self.label = ctk.CTkLabel(self, text=f"ไม่ support {platform.system()}", font=("Arial", 30))
            self.label.pack(pady=20)
    
    def slider_event(self, value):
        self.fps.configure(text=f"FPS: {int(value)}")
    
    def limit_system_fps(self, rate):
        current_os = platform.system()
        # =================== ไม่มีการทดสอบ [AI ทำทั้งหมด] =======================
        if current_os == "Windows":
            try:
                if self.switch_max_fps.get() == 1:
                    # 1. ดึงข้อมูลหน้าจอปัจจุบัน
                    device = win32api.EnumDisplayDevices(None, 0)
                    settings = win32api.EnumDisplaySettings(device.DeviceName, win32con.ENUM_CURRENT_SETTINGS)
                    
                    # 2. แก้ไขค่าในตัวแปร settings
                    settings.DisplayFrequency = int(self.fps_entry.get()) # รับค่าจาก GUI
                    settings.Fields = win32con.DM_DISPLAYFREQUENCY
                    
                    # 3. สั่งให้ Windows "ยอมรับค่า" (สำคัญมาก ต้องอยู่ในเงื่อนไขเปิด)
                    result = win32api.ChangeDisplaySettings(settings, 0)
                    print("เปิดโหมด FPS สูงสำเร็จ")

                elif self.switch_max_fps.get() == 0:
                    # เมื่อปิด ให้คืนค่าพื้นฐานของ Windows (Registry Default)
                    win32api.ChangeDisplaySettings(None, 0)
                    print("คืนค่าหน้าจอปกติเรียบร้อย")
            
            except Exception as e:
                print(f"เกิดข้อผิดพลาดบน Windows: {e}")
        # =================== ไม่มีการทดสอบ [AI ทำทั้งหมด] =======================

if __name__ == "__main__":
    app = App()
    app.mainloop()