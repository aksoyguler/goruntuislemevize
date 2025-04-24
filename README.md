🖐️ El Hareketi ile Ekran Parlakligi Kontrol Sistemi
Bu Python projesi, kullanicinin isaret parmagiyla bas parmagi arasindaki mesafeyi algilayarak, ekranin parlakligini otomatik olarak ayarlar. Proje, MediaPipe kullanarak el tespiti yapar ve screen_brightness_control kutuphanesiyle parlaklik seviyesini degistirir.

⚙️ Gereksinimler
Python 3.7+

Bir webcam

Windows isletim sistemi (screen_brightness_control kutuphanesi nedeniyle)

🧩 Kullanilan Kutuphaneler
mediapipe

opencv-python

numpy

screen_brightness_control

🔧 Kurulum
Gerekli kutuphaneleri yukleyin:

bash
Kopyala
Düzenle
pip install mediapipe opencv-python numpy screen_brightness_control
hand_landmarker.task dosyasini MediaPipe Model Zoo adresinden indirip, proje klasorune koyun.

🚀 Calistirma
bash
Kopyala
Düzenle
python el_parlaklik_kontrol.py
Kamera acilir ve elinizi goruntuye dogru tuttugunuzda isaret ve bas parmak arasi mesafe algilanir.

Parmaklarin arasi acildikca parlaklik artar, kapatildikca parlaklik azalir.

Programi kapatmak icin Q tusuna basin.

📌 Notlar
Su anda sadece tek el icin calisir.

Sistem Windows ortaminda calisir. Diger isletim sistemlerinde screen_brightness_control farkli sekilde calisir veya desteklenmez.

Farkli islevler (ses kontrolu, uygulama acma vb.) entegre edilebilir.

🧠 Gelistirici Notlari
Proje, el hareketleriyle kullanici arayuzu kontrol etme hedefli daha genis bir sistemin parcasidir.

Ileride el pozisyonlarina bagli farkli komutlar eklenmesi planlanmaktadir.

