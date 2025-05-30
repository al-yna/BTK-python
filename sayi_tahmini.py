import tkinter as tk
import random
import time
import os
from PIL import Image, ImageTk

try:
    import winsound

    def play_sound_success():
        winsound.MessageBeep(winsound.MB_ICONASTERISK)

    def play_sound_fail():
        winsound.MessageBeep(winsound.MB_ICONHAND)

except ImportError:
    def play_sound_success():
        pass

    def play_sound_fail():
        pass


class SayiTahminOyunu:
    def __init__(self, root):
        self.root = root
        self.root.title("🎯 Sayı Tahmin Oyunu")
        self.root.geometry("600x600")
        self.root.resizable(False, False)

        self.canvas = tk.Canvas(self.root, width=600, height=600, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        # Arka plan resmi yükle
        if os.path.exists("arka_plan.jpg"):
            try:
                self.bg_image = Image.open("arka_plan.jpg")
                self.bg_image = self.bg_image.resize((600, 600), Image.Resampling.LANCZOS)
                self.bg_photo = ImageTk.PhotoImage(self.bg_image)
                self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")
            except Exception as e:
                print("⚠️ Arka plan resmi yüklenemedi:", e)
        else:
            print("❌ arka_plan.jpg dosyası bulunamadı. Lütfen aynı klasöre koy.")

        self.zorluk = None
        self.max_sayi = 100
        self.zaman_sinir = 20
        self.sayi = None
        self.tahmin_sayisi = 0
        self.baslangic_zamani = None
        self.puan = 0

        self.widgets = []

        self.create_main_menu()

    def clear_widgets(self):
        for w in self.widgets:
            self.canvas.delete(w)
        self.widgets.clear()

    def create_main_menu(self):
        self.clear_widgets()

        title = tk.Label(self.root, text="🎯 Sayı Tahmin Oyunu",
                         font=("Comic Sans MS", 28, "bold"),
                         fg="white", bg="#000000")
        w1 = self.canvas.create_window(300, 100, window=title)

        start_btn = tk.Button(self.root, text="Başla", font=("Arial", 16), bg="#10ac84", fg="white",
                              command=self.create_difficulty_menu)
        w2 = self.canvas.create_window(300, 200, window=start_btn)

        exit_btn = tk.Button(self.root, text="Çıkış", font=("Arial", 16), bg="#ff4757", fg="white",
                             command=self.root.destroy)
        w3 = self.canvas.create_window(300, 300, window=exit_btn)

        self.widgets.extend([w1, w2, w3])

    def create_difficulty_menu(self):
        self.clear_widgets()

        label = tk.Label(self.root, text="Zorluk Seçin", font=("Arial", 20, "bold"), bg="#000000", fg="white")
        w1 = self.canvas.create_window(300, 100, window=label)

        btn_easy = tk.Button(self.root, text="Kolay (1-50)", font=("Arial", 14), bg="#1dd1a1", fg="white",
                             command=lambda: self.set_difficulty(1))
        w2 = self.canvas.create_window(300, 180, window=btn_easy)

        btn_medium = tk.Button(self.root, text="Orta (1-100)", font=("Arial", 14), bg="#feca57", fg="white",
                               command=lambda: self.set_difficulty(2))
        w3 = self.canvas.create_window(300, 230, window=btn_medium)

        btn_hard = tk.Button(self.root, text="Zor (1-1000)", font=("Arial", 14), bg="#ff6b6b", fg="white",
                             command=lambda: self.set_difficulty(3))
        w4 = self.canvas.create_window(300, 280, window=btn_hard)

        btn_back = tk.Button(self.root, text="Geri Dön", font=("Arial", 12), bg="#8395a7", fg="white",
                             command=self.create_main_menu)
        w5 = self.canvas.create_window(300, 350, window=btn_back)

        exit_btn = tk.Button(self.root, text="Çıkış", font=("Arial", 14), bg="#ff4757", fg="white",
                             command=self.root.destroy)
        w6 = self.canvas.create_window(300, 410, window=exit_btn)

        self.widgets.extend([w1, w2, w3, w4, w5, w6])

    def set_difficulty(self, secim):
        if secim == 1:
            self.max_sayi = 50
            self.zaman_sinir = 30
        elif secim == 2:
            self.max_sayi = 100
            self.zaman_sinir = 20
        else:
            self.max_sayi = 1000
            self.zaman_sinir = 15
        self.zorluk = secim
        self.start_game()

    def start_game(self):
        self.sayi = random.randint(1, self.max_sayi)
        self.tahmin_sayisi = 0
        self.puan = 0
        self.baslangic_zamani = time.time()
        self.clear_widgets()
        self.play_game()

    def play_game(self):
        self.sonuc_label = tk.Label(self.root, text=f"1 ile {self.max_sayi} arasında bir sayı tuttum.",
                                    font=("Arial", 14), bg="#000000", fg="white")
        w1 = self.canvas.create_window(300, 50, window=self.sonuc_label)

        self.tahmin_entry = tk.Entry(self.root, font=("Arial", 18), justify="center")
        w2 = self.canvas.create_window(300, 100, window=self.tahmin_entry)

        tahmin_btn = tk.Button(self.root, text="Tahmin Et", font=("Arial", 14), bg="#00cec9", fg="white",
                               command=self.tahmin_et)
        w3 = self.canvas.create_window(300, 150, window=tahmin_btn)

        self.status_label = tk.Label(self.root, text="", font=("Arial", 14), bg="#000000", fg="white")
        w4 = self.canvas.create_window(300, 200, window=self.status_label)

        self.time_label = tk.Label(self.root, text=f"Zaman: {self.zaman_sinir} saniye", font=("Arial", 14),
                                   bg="#000000", fg="white")
        w5 = self.canvas.create_window(300, 250, window=self.time_label)

        exit_btn = tk.Button(self.root, text="Çıkış", font=("Arial", 14), bg="#ff4757", fg="white",
                             command=self.root.destroy)
        w6 = self.canvas.create_window(300, 300, window=exit_btn)

        self.widgets.extend([w1, w2, w3, w4, w5, w6])

        self.countdown(self.zaman_sinir)

    def tahmin_et(self):
        try:
            tahmin = int(self.tahmin_entry.get())
        except ValueError:
            self.status_label.config(text="Geçerli bir sayı girin!", fg="red")
            play_sound_fail()
            return

        self.tahmin_entry.delete(0, 'end')

        if tahmin < 1 or tahmin > self.max_sayi:
            self.status_label.config(text=f"1 ile {self.max_sayi} arasında olmalı!", fg="red")
            play_sound_fail()
            return

        self.tahmin_sayisi += 1

        if tahmin == self.sayi:
            geçen_zaman = time.time() - self.baslangic_zamani
            self.puan = max(0, int((self.zaman_sinir - geçen_zaman) * 10))
            play_sound_success()
            self.show_game_over_screen(kazandın=True)
        elif tahmin < self.sayi:
            self.status_label.config(text="Daha büyük bir sayı!", fg="orange")
            play_sound_fail()
        else:
            self.status_label.config(text="Daha küçük bir sayı!", fg="orange")
            play_sound_fail()

    def countdown(self, süre):
        if süre <= 0:
            play_sound_fail()
            self.show_game_over_screen(kazandın=False)
            return
        self.time_label.config(text=f"Zaman: {süre} saniye")
        self.root.after(1000, self.countdown, süre - 1)

    def show_game_over_screen(self, kazandın):
        self.clear_widgets()
        msg = "🎉 Doğru Tahmin!" if kazandın else f"⏰ Süre Bitti!\nSayı: {self.sayi}"
        color = "green" if kazandın else "red"
        label = tk.Label(self.root, text=msg, font=("Arial", 22, "bold"), fg=color, bg="#000000")
        w1 = self.canvas.create_window(300, 150, window=label)

        self.widgets.append(w1)

        if kazandın:
            puan_lbl = tk.Label(self.root, text=f"🎯 Puanınız: {self.puan}", font=("Arial", 18), fg="blue", bg="#000000")
            w2 = self.canvas.create_window(300, 220, window=puan_lbl)
            self.widgets.append(w2)

        btn_menu = tk.Button(self.root, text="↩️ Ana Menü", font=("Arial", 14), bg="#576574", fg="white",
                             command=self.create_main_menu)
        w3 = self.canvas.create_window(300, 300, window=btn_menu)

        btn_restart = tk.Button(self.root, text="🔄 Tekrar Oyna", font=("Arial", 14), bg="#1dd1a1", fg="white",
                                command=self.start_game)
        w4 = self.canvas.create_window(300, 350, window=btn_restart)

        exit_btn = tk.Button(self.root, text="Çıkış", font=("Arial", 14), bg="#ff4757", fg="white",
                             command=self.root.destroy)
        w5 = self.canvas.create_window(300, 400, window=exit_btn)

        self.widgets.extend([w3, w4, w5])


if __name__ == "__main__":
    root = tk.Tk()
    app = SayiTahminOyunu(root)
    root.mainloop()
