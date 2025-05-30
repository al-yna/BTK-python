import random

import google.generativeai as genai

import os



# --- GOOGLE GEMINI API ANAHTARINIZI BURAYA YAPIŞTIRIN ---

# Kendi API anahtarınızı tırnaklar arasına yapıştırmayı unutmayın!

# Bu anahtarı kimseyle paylaşmamaya özen gösterin.

GOOGLE_API_KEY = "AIzaSyCTMmkhZ36RVB_5-H6Z8by1CmOqcf89xJQ" # <-- BURAYI DEĞİŞTİRİN!



# Gemini API'yi yapılandır

genai.configure(api_key=GOOGLE_API_KEY)



# Kullanılacak Gemini modelini seçin. 'gemini-pro' metin tabanlı sohbetler için idealdir.

model = genai.GenerativeModel('gemini-1.5-flash')



print("Merhaba! Ben akıllı bir chatbotum ve Google Gemini tarafından destekleniyorum. 😊")

print("Bana her şeyi sorabilirsin! Çıkmak için 'bay bay' yaz.")



# Gemini'den yanıt alınamadığında kullanılacak varsayılan hata/anlamadım yanıtları

varsayilan_hata_yanitlari = [

    "Üzgünüm, şu an sana yanıt veremiyorum. Bir sorun oluştu veya isteğini anlayamadım.",

    "Şu an teknik bir sorun yaşıyorum. Lütfen daha sonra tekrar deneyin veya başka bir şey sorun.",

    "Bunu şu anda işleyemiyorum, lütfen tekrar deneyin."

]



# --- Ana Chatbot Döngüsü ---

while True:

    kullanici_girisi = input("Siz: ").strip() # Kullanıcının girdisini al ve baştaki/sondaki boşlukları kaldır



    # Çıkış komutu kontrolü

    if kullanici_girisi.lower() == "bay bay":

        print("Chatbot: Güle güle! Tekrar görüşmek üzere!")

        break # Döngüden çık ve programı sonlandır



    # Boş girdi kontrolü

    if not kullanici_girisi:

        print("Chatbot: Lütfen bir şeyler yaz.")

        continue # Döngünün başına dön



    try:

        # Gemini API'ye kullanıcının girdisini gönder ve yanıtı al

        # generate_content metin oluşturur.

        response = model.generate_content(kullanici_girisi)



        # Gemini'den gelen yanıtı ekrana yazdır

        # Yanıt nesnesi 'text' özelliğini içerir

        print(f"Chatbot: {response.text}")



    except Exception as e:

        # API isteği sırasında bir hata oluşursa (örneğin internet bağlantısı, API anahtarı hatası vb.)

        print(f"Chatbot: {random.choice(varsayilan_hata_yanitlari)}")

        # Geliştirme aşamasında hatayı görmek için (son sürümde bu satır kaldırılabilir)

        print(f"Hata detayı: {e}")
