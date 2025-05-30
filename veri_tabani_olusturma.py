import sqlite3

# Veritabanına bağlan (yoksa oluşturur)
conn = sqlite3.connect("tarifler.db")

# İmleç oluştur
c = conn.cursor()

# Tablo oluştur
c.execute("""
CREATE TABLE IF NOT EXISTS tarifler (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    isim TEXT,
    malzemeler TEXT,
    hazirlik TEXT,
    zorluk TEXT,
    resim TEXT
)
""")

# Değişiklikleri kaydet ve kapat
conn.commit()
conn.close()

print("Veritabanı ve tablo hazır!")
