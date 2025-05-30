import tkinter as tk
from tkinter import ttk
import random

def analiz_yap():
    cumle = giris_alani.get().lower()
    kelimeler = cumle.split()

    olumlu = ["harika", "muhteşem", "süper", "güzel", "iyi", "hoş"]
    olumsuz = ["kötü", "fena", "berbat", "rezalet", "çirkin", "korkunç"]

    pozitif_emojiler = ["😄", "✨", "😊", "🥳", "👍"]
    negatif_emojiler = ["😞", "💔", "😢", "😠", "👎"]
    notr_emojiler = ["😐", "🤔", "😶"]

    olumlu_sayi = sum(1 for kelime in kelimeler if kelime in olumlu)
    olumsuz_sayi = sum(1 for kelime in kelimeler if kelime in olumsuz)

    if olumlu_sayi > olumsuz_sayi:
        emoji = random.choice(pozitif_emojiler)
        sonuc_yazi = "CÜMLE POZİTİF"
        renk = "green"
    elif olumlu_sayi < olumsuz_sayi:
        emoji = random.choice(negatif_emojiler)
        sonuc_yazi = "CÜMLE NEGATİF"
        renk = "red"
    else:
        emoji = random.choice(notr_emojiler)
        sonuc_yazi = "CÜMLE NÖTR"
        renk = "gray"

    sonuc_etiketi.config(text=sonuc_yazi, fg=renk)
    emoji_etiketi.config(text=emoji)

# Ana pencere
pencere = tk.Tk()
pencere.title("Duygu Analiz Uygulaması")
pencere.geometry("400x400")

# Sekme sistemi
sekme_defteri = ttk.Notebook(pencere)
sekme1 = tk.Frame(sekme_defteri)
sekme_defteri.add(sekme1, text="Duygu Analizi")
sekme_defteri.pack(expand=1, fill="both")

# Sekme1 - Duygu Analizi Arayüzü
baslik = tk.Label(sekme1, text="Cümle Girin:", font=("Arial", 14))
baslik.pack(pady=10)

giris_alani = tk.Entry(sekme1, width=50, font=("Arial", 12))
giris_alani.pack(pady=5)

analiz_butonu = tk.Button(sekme1, text="Analiz Yap", command=analiz_yap, font=("Arial", 12))
analiz_butonu.pack(pady=10)

# Sonuç etiketi (büyük)
sonuc_etiketi = tk.Label(sekme1, text="", font=("Arial", 24, "bold"))
sonuc_etiketi.pack(pady=20)

# Emoji etiketi (büyük)
emoji_etiketi = tk.Label(sekme1, text="", font=("Arial", 60))
emoji_etiketi.pack(pady=10)

# Pencereyi başlat
pencere.mainloop()
