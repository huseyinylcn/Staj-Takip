"""
Demo verileri oluşturma scripti
Test için örnek öğrenciler, ziyaret notları ve değerlendirmeler ekler
"""
from app import create_app
from database import db
from models import Ogrenci, ZiyaretNotu, StajDegerlendirme
from datetime import datetime, timedelta
import random

def demo_verileri_olustur():
    """Demo verileri oluştur"""
    app = create_app()
    
    with app.app_context():
        # Veritabanını temizle
        db.drop_all()
        db.create_all()
        
        print("📚 Demo verileri oluşturuluyor...\n")
        
        # Örnek öğrenciler
        ogrenciler_data = [
            ("Ahmet", "Yılmaz", "20210101", "05551234567"),
            ("Mehmet", "Demir", "20210102", "05559876543"),
            ("Ayşe", "Kaya", "20210103", "05551112233"),
            ("Fatma", "Şahin", "20210104", "05552223344"),
            ("Ali", "Öztürk", "20210105", "05553334455"),
            ("Zeynep", "Yıldız", "20210106", "05554445566"),
            ("Mustafa", "Arslan", "20210107", "05555556677"),
            ("Elif", "Çelik", "20210108", "05556667788"),
        ]
        
        ogrenciler = []
        for ad, soyad, no, tel in ogrenciler_data:
            ogrenci = Ogrenci(
                ad=ad,
                soyad=soyad,
                ogrenci_no=no,
                telefon=tel,
                kayit_tarihi=datetime.utcnow() - timedelta(days=random.randint(30, 90))
            )
            db.session.add(ogrenci)
            ogrenciler.append(ogrenci)
        
        db.session.commit()
        print(f"✅ {len(ogrenciler)} öğrenci eklendi")
        
        # Örnek ziyaret notları
        ziyaret_sablonlari = [
            "Öğrenci staj yerine düzenli olarak gidiyor. Çalışma performansı iyi.",
            "İş yerindeki görevlerini başarıyla yerine getiriyor. Disiplinli ve sorumluluk sahibi.",
            "Firma yetkilisiyle görüştüm. Öğrenciden çok memnunlar.",
            "Staj defterini düzenli tutuyor. Teknik bilgisi gelişiyor.",
            "İş yerinde aktif olarak çalışıyor. Takım çalışmasına yatkın.",
            "Öğrenci motivasyonu yüksek. İşine sahip çıkıyor.",
        ]
        
        ogretmenler = ["Dr. Ahmet YILMAZ", "Dr. Mehmet DEMİR", "Dr. Ayşe KAYA", "Dr. Fatma ŞAHİN"]
        
        toplam_ziyaret = 0
        for ogrenci in ogrenciler[:6]:  # İlk 6 öğrenciye ziyaret notu ekle
            ziyaret_sayisi = random.randint(2, 5)
            for i in range(ziyaret_sayisi):
                ziyaret = ZiyaretNotu(
                    ogrenci_id=ogrenci.id,
                    not_metni=random.choice(ziyaret_sablonlari),
                    ogretmen_adi=random.choice(ogretmenler),
                    tarih=datetime.utcnow() - timedelta(days=random.randint(1, 60))
                )
                db.session.add(ziyaret)
                toplam_ziyaret += 1
        
        db.session.commit()
        print(f"✅ {toplam_ziyaret} ziyaret notu eklendi")
        
        # Örnek değerlendirmeler
        degerlendirilen = 0
        for ogrenci in ogrenciler[:4]:  # İlk 4 öğrenciye değerlendirme ekle
            degerlendirme = StajDegerlendirme(
                ogrenci_id=ogrenci.id,
                isyeren_notu=round(random.uniform(20, 30), 1),
                icindekiler=round(random.uniform(6, 10), 1),
                firma_bilgisi=round(random.uniform(6, 10), 1),
                yazim_duzeni=round(random.uniform(6, 10), 1),
                resim_sekil=round(random.uniform(6, 10), 1),
                dil_kullanimi=round(random.uniform(12, 20), 1),
                sonuc_bolumu=round(random.uniform(6, 10), 1),
                defter_duzeni_mulakat=round(random.uniform(20, 30), 1)
            )
            degerlendirme.hesapla_toplam()
            db.session.add(degerlendirme)
            degerlendirilen += 1
        
        db.session.commit()
        print(f"✅ {degerlendirilen} öğrenci değerlendirildi")
        
        print("\n" + "="*50)
        print("🎉 DEMO VERİLERİ BAŞARIYLA OLUŞTURULDU!")
        print("="*50)
        print("\n📊 Özet:")
        print(f"   • Toplam Öğrenci: {len(ogrenciler)}")
        print(f"   • Toplam Ziyaret: {toplam_ziyaret}")
        print(f"   • Değerlendirilen: {degerlendirilen}")
        print("\n💡 Uygulamayı başlatın ve test edin!")
        print("   python app.py veya calistir.bat\n")

if __name__ == '__main__':
    demo_verileri_olustur()

