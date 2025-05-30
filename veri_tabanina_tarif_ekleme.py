import sqlite3

tarifler = [
    {
        "isim": "Menemen",
        "malzemeler": "Yumurta, domates, yeşil biber, tuz, karabiber, sıvı yağ",
        "yapim": """1. Yeşil biberleri küçük küçük doğrayıp tavada sıvı yağda kavurun.
2. Domatesleri küçük küpler halinde doğrayıp ekleyin, suyunu çekene kadar pişirin.
3. Tuz ve karabiber ekleyin.
4. Yumurtaları kırıp karıştırarak pişirin, isteğe göre kıvamını ayarlayın.
5. Sıcak servis yapın.""",
        "zorluk": "Basit",
        "resim": "resimler/menemen.jpg"
    },
    {
        "isim": "Hünkar Beğendi",
        "malzemeler": "Patlıcan, süt, un, tereyağı, kıyma, soğan, domates, tuz, karabiber",
        "yapim": """1. Patlıcanları közleyip kabuklarını soyun ve ezin.
2. Süt, un ve tereyağını tencerede karıştırarak beşamel sos yapın.
3. Beşamel sosun içine patlıcan püresini ekleyip iyice karıştırın.
4. Ayrı tavada kıymayı ince kıyılmış soğanla kavurun, domatesleri ekleyip pişirin.
5. Servis tabağına patlıcan püresini yayın, üzerine kıymalı harcı koyun.
6. Sıcak servis yapın.""",
        "zorluk": "Orta",
        "resim": "resimler/hunkar.jpg"
    },
    {
        "isim": "İmam Bayıldı",
        "malzemeler": "Patlıcan, soğan, sarımsak, domates, maydanoz, zeytinyağı, tuz, karabiber",
        "yapim": """1. Patlıcanları alacalı soyun, ortadan ikiye bölün ve tuzlu suda bekletin.
2. Kızgın yağda patlıcanları hafif kızartıp bir fırın kabına dizin.
3. Soğanları ve sarımsağı doğrayıp zeytinyağında kavurun.
4. Domatesleri ekleyip pişirin, tuz ve karabiberle tatlandırın.
5. Bu harcı patlıcanların üzerine dökün.
6. Önceden ısıtılmış 180 derecelik fırında 30-40 dakika pişirin.
7. Maydanozla süsleyip soğuk servis yapın.""",
        "zorluk": "Orta",
        "resim": "resimler/imambayildi.jpg"
    },
    {
        "isim": "Karnıyarık",
        "malzemeler": "Patlıcan, kıyma, soğan, domates, biber, sarımsak, maydanoz, tuz, karabiber, sıvı yağ",
        "yapim": """1. Patlıcanları alacalı soyun, ortadan uzunlamasına yarıp içini oyun.
2. Tuzlu suda bekletip kızgın yağda kızartın.
3. Soğanı doğrayıp sıvı yağda kavurun, kıymayı ekleyip pişirin.
4. Domates, biber ve sarımsağı ekleyip pişirmeye devam edin.
5. Maydanoz ve baharatlarla tatlandırın.
6. Patlıcanların içini kıymalı harçla doldurun.
7. Fırın kabına dizip üzerlerine domates dilimleri koyun.
8. 180 derece fırında 30-40 dakika pişirin.""",
        "zorluk": "Orta",
        "resim": "resimler/karnibarik.jpg"
    },
    {
        "isim": "Baklava",
        "malzemeler": "Un, su, yumurta, tereyağı, ceviz, toz şeker, su, limon suyu",
        "yapim": """1. Un, su, yumurta ile hamur yoğurun ve 24 eşit parçaya bölün.
2. Her parçayı çok ince açıp tereyağı sürün, üst üste dizin.
3. Tepsiye yerleştirip iç harcını (ceviz, şeker karışımı) yayın.
4. Kat kat hamur açıp harcın üstüne yerleştirin.
5. Dilimleyip tereyağı sürün.
6. Önceden ısıtılmış fırında 180 derecede 40-50 dakika pişirin.
7. Şerbeti için su, şeker ve limon suyunu kaynatıp soğutun.
8. Fırından çıkar çıkmaz üzerine şerbet dökün.
9. Şerbeti çekince servis yapın.""",
        "zorluk": "Zor",
        "resim": "resimler/baklava.jpg"
    },
    {
        "isim": "Kısır",
        "malzemeler": "İnce bulgur, domates salçası, yeşil soğan, maydanoz, taze nane, limon suyu, zeytinyağı, tuz, karabiber, biber salçası",
        "yapim": """1. İnce bulguru derin bir kaba koyun, üzerine kaynar su ekleyip şişmeye bırakın.
2. Salçaları, ince kıyılmış yeşillikleri ekleyip karıştırın.
3. Limon suyu, zeytinyağı, tuz ve baharatları ilave edin.
4. İyice yoğurun ve servis yapın.""",
        "zorluk": "Basit",
        "resim": "resimler/kisir.jpg"
    },
    {
        "isim": "Su Böreği",
        "malzemeler": "Yufka, peynir, maydanoz, yumurta, süt, tereyağı",
        "yapim": """1. Yufkaları haşlamak için geniş bir tencerede su kaynatın.
2. Yufkaları tek tek kaynar sudan geçirip çıkarın.
3. Peynir ve maydanozu karıştırın.
4. Fırın tepsisini yağlayın, bir kat yufka koyun.
5. Üzerine peynirli harçtan serpin.
6. Kat kat yufka ve harcı dizin.
7. Üstüne süt, yumurta ve eritilmiş tereyağı karışımını dökün.
8. Önceden ısıtılmış 180 derecelik fırında 30-40 dakika pişirin.""",
        "zorluk": "Orta",
        "resim": "resimler/suboregi.jpg"
    },
    {
        "isim": "Kuru Fasulye",
        "malzemeler": "Kuru fasulye, soğan, domates, biber salçası, sıvı yağ, tuz, karabiber",
        "yapim": """1. Kuru fasulyeyi gece önceden suda bekletin.
2. Soğanları doğrayıp yağda kavurun.
3. Salçayı ekleyip karıştırın.
4. Fasulyeyi süzüp tencereye alın, üzerini geçecek kadar su ekleyin.
5. Tuz ve baharatları koyun, fasulyeler yumuşayana kadar pişirin.
6. Yanında pilav ile servis yapın.""",
        "zorluk": "Basit",
        "resim": "resimler/kurufasulye.jpg"
    },
    {
        "isim": "Lahmacun",
        "malzemeler": "Un, maya, su, kıyma, domates, soğan, biber, maydanoz, tuz, baharatlar",
        "yapim": """1. Hamur malzemelerini karıştırıp mayalanmaya bırakın.
2. Kıymayı, ince doğranmış sebzelerle karıştırın.
3. Hamuru ince açıp kıymalı harcı yayın.
4. Çok sıcak fırında 5-7 dakika pişirin.
5. Yanında yeşillik ve limonla servis yapın.""",
        "zorluk": "Orta",
        "resim": "resimler/lahmacun.jpg"
    },
    {
        "isim": "Köfte",
        "malzemeler": "Kıyma, soğan, ekmek içi, yumurta, maydanoz, tuz, karabiber",
        "yapim": """1. Soğanı rendeleyin, maydanozu ince kıyın.
2. Tüm malzemeleri karıştırıp yoğurun.
3. Köfte şekli verip yağda kızartın veya fırında pişirin.
4. Sıcak servis yapın.""",
        "zorluk": "Basit",
        "resim": "resimler/kofte.jpg"
    }
]

def veritabani_olustur():
    conn = sqlite3.connect("tarifler.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tarifler (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        isim TEXT,
        malzemeler TEXT,
        yapim TEXT,
        zorluk TEXT,
        resim TEXT
    )
    """)
    conn.commit()
    conn.close()

def tarifleri_ekle():
    conn = sqlite3.connect("tarifler.db")
    cursor = conn.cursor()
    for t in tarifler:
        cursor.execute("""
            INSERT INTO tarifler (isim, malzemeler, yapim, zorluk, resim)
            VALUES (?, ?, ?, ?, ?)
        """, (t["isim"], t["malzemeler"], t["yapim"], t["zorluk"], t["resim"]))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    veritabani_olustur()
    tarifleri_ekle()
    print("Tarifler veritabanına başarıyla eklendi!")
