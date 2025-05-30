import tkinter as tk
from tkinter import messagebox
import sqlite3

def tema_degistir(deger):
    if int(deger) == 1:
        pencere.configure(bg="#000000")
        baslik_label.configure(bg="#000000", fg="#FFCC00")
        malzeme_entry.configure(bg="#333333", fg="#FFFFFF", insertbackground="white")
        ara_buton.configure(bg="#FFCC00", fg="#000000", activebackground="#FFD700")
        tarif_listbox.configure(bg="#1C1C1C", fg="#FFFFFF", selectbackground="#FFCC00", selectforeground="#000000")
        detay_text.configure(bg="#1C1C1C", fg="#FFFFFF", insertbackground="white")
        slider_label.configure(bg="#000000", fg="#FFCC00")
    else:
        pencere.configure(bg="#F0F0F0")
        baslik_label.configure(bg="#F0F0F0", fg="#333333")
        malzeme_entry.configure(bg="#FFFFFF", fg="#000000", insertbackground="black")
        ara_buton.configure(bg="#CCCCCC", fg="#000000", activebackground="#BBBBBB")
        tarif_listbox.configure(bg="#FFFFFF", fg="#000000", selectbackground="#999999", selectforeground="#FFFFFF")
        detay_text.configure(bg="#FFFFFF", fg="#CD969669", insertbackground="black")
        slider_label.configure(bg="#F0F0F0", fg="#333333")

def tarif_ara():
    malzeme = malzeme_entry.get().lower()
    if not malzeme:
        messagebox.showwarning("Uyarı", "Lütfen bir malzeme girin.")
        return

    tarif_listbox.delete(0, tk.END)
    conn = sqlite3.connect("tarifler.db")
    cursor = conn.cursor()
    cursor.execute("SELECT isim, yapim FROM tarifler WHERE malzemeler LIKE ?", ('%' + malzeme + '%',))
    tarifler = cursor.fetchall()
    conn.close()

    if not tarifler:
        tarif_listbox.insert(tk.END, "Bu malzemeyle tarif bulunamadı.")
    else:
        for tarif in tarifler:
            tarif_listbox.insert(tk.END, tarif[0])
        global secili_tarifler
        secili_tarifler = tarifler

def detay_goster(event):
    secim = tarif_listbox.curselection()
    if secim:
        index = secim[0]
        detay_text.delete("1.0", tk.END)
        detay_text.insert(tk.END, f"Tarif:\n\n{secili_tarifler[index][1]}")

# Ana pencere
pencere = tk.Tk()
pencere.title("😋ᵞᵁᴹᴹᵞ😋 Tarif Bulucu 😋ᵞᵁᴹᴹᵞ😋")
pencere.geometry("800x500")
pencere.configure(bg="#000000")

# Başlık
baslik_label = tk.Label(pencere, text="🍔 Tarif Bulucu Uygulaması 🍔", font=("Helvetica", 22, "bold"), bg="#000000", fg="#FFCC00")
baslik_label.pack(pady=20)

# Malzeme arama kutusu ve buton
frame_ust = tk.Frame(pencere, bg="#000000")
frame_ust.pack(pady=10)

malzeme_entry = tk.Entry(frame_ust, font=("Helvetica", 14), width=30, bg="#333333", fg="#FFFFFF", insertbackground="white")
malzeme_entry.grid(row=0, column=0, padx=10)

ara_buton = tk.Button(frame_ust, text="Tarif Ara", font=("Helvetica", 14), bg="#FFCC00", fg="#000000", activebackground="#FFD700", command=tarif_ara)
ara_buton.grid(row=0, column=1, padx=10)

# Tarif listesi ve detay kısmı
frame_alt = tk.Frame(pencere, bg="#000000")
frame_alt.pack(pady=20)

tarif_listbox = tk.Listbox(frame_alt, font=("Helvetica", 13), width=30, height=12, bg="#1C1C1C", fg="#FFFFFF", selectbackground="#FFCC00", selectforeground="#000000")
tarif_listbox.grid(row=0, column=0, padx=20)
tarif_listbox.bind("<<ListboxSelect>>", detay_goster)

detay_text = tk.Text(frame_alt, font=("Helvetica", 13), width=40, height=12, wrap="word", bg="#1C1C1C", fg="#FFFFFF", insertbackground="white")
detay_text.grid(row=0, column=1, padx=20)

# Tema Değiştirme Sliderı
slider_label = tk.Label(pencere, text="🌓 Tema Modu", font=("Helvetica", 14), bg="#000000", fg="#FFCC00")
slider_label.pack(pady=10)

tema_slider = tk.Scale(pencere, from_=0, to=1, orient="horizontal", length=200, showvalue=0, command=tema_degistir, bg="#000000", troughcolor="#FFCC00", highlightthickness=0)
tema_slider.pack()

tema_slider.set(1)  # Başlangıçta dark mode

pencere.mainloop()
