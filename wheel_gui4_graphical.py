import tkinter as tk
import time
import threading
import serial
import math
import winsound
from tkinter import font as tkfont


class SteeringWheelSensorSimulation:
    def __init__(self, master):
        self.master = master
        master.title("Direksiyon Sensör Takip Sistemi")
        master.geometry("1100x650")
        master.configure(bg='#F0F4F8')

        # Sensör verileri
        self.touch_sensors = [0] * 12  # 12 dokunma sensörü
        self.temperature = 0  # Parmak sıcaklığı
        self.pulse_rate = 0  # Nabız

        # Doğru tutuş noktaları
        self.correct_grip_indices = [2, 3, 9, 10]

        # Custom Fonts
        self.title_font = tkfont.Font(
            family="Segoe UI", size=16, weight="bold")
        self.value_font = tkfont.Font(family="Segoe UI", size=14)
        self.status_font = tkfont.Font(family="Segoe UI", size=12)

        # UI Elemanları
        self.create_ui()

        # Veri okuma thread'i
        self.running = True
        self.serial_thread = threading.Thread(
            target=self.read_serial_data)
        self.serial_thread.daemon = True
        self.serial_thread.start()

        # Uyarı seslerini engellemek için zamanlayıcı
        self.last_warning_time = {
            "temperature": 0,
            "pulse": 0,
            "grip": 0
        }
        self.warning_interval = 5  # saniye

    def create_ui(self):
        # Ana çerçeveyi iki bölüme ayır
        self.main_frame = tk.Frame(self.master, bg='#F0F4F8')
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=20)

        # Sol taraf (Direksiyon)
        self.steering_frame = tk.Frame(
            self.main_frame, width=700, height=600, bg='white',
            highlightthickness=1, highlightbackground='#E1E5EA', relief=tk.RAISED)
        self.steering_frame.pack(side=tk.LEFT, padx=5)
        self.steering_frame.pack_propagate(False)
        self.steering_frame.configure(borderwidth=2, relief=tk.GROOVE)

        # Direksiyon Başlığı
        self.steering_title = tk.Label(
            self.steering_frame, text="Direksiyon Tutuş Analizi",
            font=self.title_font, bg='white', fg='#2C3E50')
        self.steering_title.pack(pady=10)

        # Direksiyon Canvas
        self.canvas = tk.Canvas(
            self.steering_frame, width=450, height=450, bg='#F8F9FA', highlightthickness=0)
        self.canvas.pack(pady=20)

        self.draw_realistic_steering_wheel()

        # Sensör noktaları
        self.sensor_points = []
        for i in range(12):
            angle = i * 30 - 90
            x = 225 + 180 * math.cos(math.radians(angle))  # Dışa daha yakın
            y = 225 + 180 * math.sin(math.radians(angle))
            point = self.canvas.create_oval(x-12, y-12, x+12, y+12,
                                            fill='#E0E0E0', outline='#757575', width=2)
            self.sensor_points.append(point)

            # Doğru tutuş noktaları için belirgin çerçeve
            if i in self.correct_grip_indices:
                self.canvas.create_oval(x-14, y-14, x+14, y+14,
                                        outline='#FF5733', width=3)

            # Noktaların indekslerini yazdır
            self.canvas.create_text(x, y, text=str(
                i), font=self.status_font, fill='#34495E')

        # Sağ taraf (Sağlık Verileri)
        self.create_health_section()

    def draw_realistic_steering_wheel(self):
        center_x, center_y = 225, 225
        inner_radius, outer_radius = 100, 180

        # Dış çember
        self.canvas.create_oval(center_x - outer_radius, center_y - outer_radius,
                                center_x + outer_radius, center_y + outer_radius,
                                width=18, outline='#2C3E50', fill='#F5F5DC')  # Krem rengi

        # İç çember
        self.canvas.create_oval(center_x - inner_radius, center_y - inner_radius,
                                center_x + inner_radius, center_y + inner_radius,
                                width=10, outline='#2C3E50', fill='')

        # Direksiyon kolları
        for angle in [0, 90, 180, 270]:
            start_x = center_x + inner_radius * math.cos(math.radians(angle))
            start_y = center_y + inner_radius * math.sin(math.radians(angle))
            end_x = center_x + outer_radius * math.cos(math.radians(angle))
            end_y = center_y + outer_radius * math.sin(math.radians(angle))
            self.canvas.create_line(
                start_x, start_y, end_x, end_y, width=10, fill='#2C3E50')

    def create_health_section(self):
        self.health_frame = tk.Frame(
            self.main_frame, bg='white', width=500, height=600)
        self.health_frame.pack(side=tk.RIGHT, padx=5)
        self.health_frame.pack_propagate(False)

        tk.Label(self.health_frame, text="Sıcaklık",
                 font=self.title_font, bg='white').pack(pady=10)
        self.temp_value_label = tk.Label(
            self.health_frame, text="-- °C", font=self.value_font, bg='white')
        self.temp_value_label.pack()
        self.temp_status_label = tk.Label(
            self.health_frame, text="", font=self.status_font, bg='white', fg='#E74C3C')
        self.temp_status_label.pack(pady=5)

        tk.Label(self.health_frame, text="Nabız",
                 font=self.title_font, bg='white').pack(pady=10)
        self.pulse_value_label = tk.Label(
            self.health_frame, text="-- bpm", font=self.value_font, bg='white')
        self.pulse_value_label.pack()
        self.pulse_status_label = tk.Label(
            self.health_frame, text="", font=self.status_font, bg='white', fg='#E74C3C')
        self.pulse_status_label.pack(pady=5)

        tk.Label(self.health_frame, text="Tutuş Durumu",
                 font=self.title_font, bg='white').pack(pady=10)
        self.grip_status_label = tk.Label(
            self.health_frame, text="--", font=self.value_font, bg='white')
        self.grip_status_label.pack()

        self.missing_grip_label = tk.Label(
            self.health_frame, text="", font=self.status_font, bg='white', fg='#E74C3C')
        self.missing_grip_label.pack(pady=5)

    def read_serial_data(self):
        try:
            ser = serial.Serial('COM5', 9600, timeout=1)  # Arduino'ya bağlan
            time.sleep(2)  # Bağlantı için biraz bekle
        except serial.SerialException as e:
            print("Seri port bağlantısı hata: ", e)
            return

        while self.running:
            try:
                line = ser.readline().decode('utf-8').strip()
                if line:
                    self.process_serial_data(line)
            except Exception as e:
                print("Veri okuma hata: ", e)

    def process_serial_data(self, data):
        try:
            parts = data.split()
            if len(parts) != 3:
                return

            touch_data = parts[0]
            temperature = float(parts[1])
            pulse = int(parts[2])

            # Sensör verilerini güncelle
            for i in range(12):
                self.touch_sensors[i] = int(touch_data[i])

            self.temperature = temperature
            self.pulse_rate = pulse

            self.update_ui()
        except ValueError:
            print("Geçersiz veri formatı: ", data)

    def update_ui(self):
        # Sensör noktalarını güncelle
        for i, value in enumerate(self.touch_sensors):
            if i in self.correct_grip_indices:
                color = '#2ECC71' if value > 0 else '#E74C3C'
            else:
                color = '#2ECC71' if value > 0 else '#E0E0E0'
            self.canvas.itemconfig(self.sensor_points[i], fill=color)

        # Sağlık verilerini güncelle
        self.temp_value_label.config(text=f"{self.temperature} °C")
        self.pulse_value_label.config(text=f"{self.pulse_rate} bpm")

        # Sıcaklık kontrolü
        current_time = time.time()
        temp_status = ""
        if self.temperature > 37.8:
            temp_status = "Yüksek Sıcaklık DİKKAT"
            self.temp_status_label.config(fg='#E74C3C')
            if current_time - self.last_warning_time["temperature"] > self.warning_interval:
                self.play_warning_sound("sounds/sicaklik_yuksek.wav")
                self.last_warning_time["temperature"] = current_time

        elif self.temperature < 20.2:
            temp_status = "Düşük Sıcaklık DİKKAT"
            self.temp_status_label.config(fg='#E74C3C')
            if current_time - self.last_warning_time["temperature"] > self.warning_interval:
                self.play_warning_sound("sounds/sicaklik_dusuk.wav")
                self.last_warning_time["temperature"] = current_time
        else:
            temp_status = "Sıcaklık Normal"
            self.temp_status_label.config(fg='#2ECC71')
        self.temp_status_label.config(text=temp_status)

        # Nabız kontrolü
        pulse_status = ""
        if self.pulse_rate > 120:
            pulse_status = "Yüksek Nabız - Sürüşe Ara Verin!"
            self.pulse_status_label.config(fg='#E74C3C')
            if current_time - self.last_warning_time["pulse"] > self.warning_interval:
                self.play_warning_sound("sounds/nabiz_yuksek.wav")
                self.last_warning_time["pulse"] = current_time
        elif self.pulse_rate < 60:
            pulse_status = "Düşük Nabız - Sürüşe Ara Verin!"
            self.pulse_status_label.config(fg='#E74C3C')
            if current_time - self.last_warning_time["pulse"] > self.warning_interval:
                self.play_warning_sound("sounds/nabiz_dusuk.wav")
                self.last_warning_time["pulse"] = current_time
        else:
            pulse_status = "Nabız Normal"
            self.pulse_status_label.config(fg='#2ECC71')
        self.pulse_status_label.config(text=pulse_status)

        # Tutuş durumu kontrolü
        missing_grip = [
            str(i) for i in self.correct_grip_indices if self.touch_sensors[i] == 0]
        if missing_grip:
            grip_status = "Yanlış Tutuş"
            self.grip_status_label.config(text=grip_status, fg='#E74C3C')
            self.missing_grip_label.config(
                text=f"Tutup Bırakmayın: {', '.join(missing_grip)}", fg='#E74C3C')
            if current_time - self.last_warning_time["grip"] > self.warning_interval:
                self.play_warning_sound("sounds/direksiyon_konum.wav")
                self.last_warning_time["grip"] = current_time
        else:
            grip_status = "Doğru Tutuş"
            self.grip_status_label.config(text=grip_status, fg='#2ECC71')
            self.missing_grip_label.config(text="", fg='#2ECC71')

    def play_warning_sound(self, filename):
        try:
            winsound.PlaySound(
                filename, winsound.SND_FILENAME | winsound.SND_ASYNC)
        except:
            print("Ses uyarısı çalıştırılamadı.")

    def on_close(self):
        self.running = False
        self.master.destroy()


def main():
    root = tk.Tk()
    app = SteeringWheelSensorSimulation(root)
    root.protocol("WM_DELETE_WINDOW", app.on_close)
    root.mainloop()


if __name__ == "__main__":
    main()
