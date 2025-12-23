from database import db
from models import Ogrenci, ZiyaretNotu, StajDegerlendirme

class OgrenciService:
    """Öğrenci işlemleri servisi"""
    
    @staticmethod
    def tum_ogrencileri_getir():
        """Tüm öğrencileri getir"""
        return Ogrenci.query.order_by(Ogrenci.kayit_tarihi.desc()).all()
    
    @staticmethod
    def ogrenci_getir(ogrenci_id):
        """ID'ye göre öğrenci getir"""
        return Ogrenci.query.get(ogrenci_id)
    
    @staticmethod
    def ogrenci_ekle(ad, soyad, ogrenci_no, telefon=None):
        """Yeni öğrenci ekle"""
        # Aynı öğrenci numarası var mı kontrol et
        mevcut = Ogrenci.query.filter_by(ogrenci_no=ogrenci_no).first()
        if mevcut:
            raise ValueError(f"Bu öğrenci numarası ({ogrenci_no}) zaten kayıtlı!")
        
        ogrenci = Ogrenci(
            ad=ad,
            soyad=soyad,
            ogrenci_no=ogrenci_no,
            telefon=telefon
        )
        db.session.add(ogrenci)
        db.session.commit()
        return ogrenci
    
    @staticmethod
    def ogrenci_guncelle(ogrenci_id, ad=None, soyad=None, telefon=None):
        """Öğrenci bilgilerini güncelle"""
        ogrenci = Ogrenci.query.get(ogrenci_id)
        if not ogrenci:
            raise ValueError("Öğrenci bulunamadı!")
        
        if ad:
            ogrenci.ad = ad
        if soyad:
            ogrenci.soyad = soyad
        if telefon:
            ogrenci.telefon = telefon
        
        db.session.commit()
        return ogrenci
    
    @staticmethod
    def ogrenci_sil(ogrenci_id):
        """Öğrenciyi sil"""
        ogrenci = Ogrenci.query.get(ogrenci_id)
        if not ogrenci:
            raise ValueError("Öğrenci bulunamadı!")
        
        db.session.delete(ogrenci)
        db.session.commit()
        return True

class ZiyaretService:
    """Ziyaret notu işlemleri servisi"""
    
    @staticmethod
    def ziyaret_notu_ekle(ogrenci_id, not_metni, ogretmen_adi=None):
        """Yeni ziyaret notu ekle"""
        ogrenci = Ogrenci.query.get(ogrenci_id)
        if not ogrenci:
            raise ValueError("Öğrenci bulunamadı!")
        
        ziyaret = ZiyaretNotu(
            ogrenci_id=ogrenci_id,
            not_metni=not_metni,
            ogretmen_adi=ogretmen_adi
        )
        db.session.add(ziyaret)
        db.session.commit()
        return ziyaret
    
    @staticmethod
    def ogrenci_ziyaretlerini_getir(ogrenci_id):
        """Öğrencinin tüm ziyaret notlarını getir"""
        return ZiyaretNotu.query.filter_by(ogrenci_id=ogrenci_id).order_by(ZiyaretNotu.tarih.desc()).all()
    
    @staticmethod
    def ziyaret_sil(ziyaret_id):
        """Ziyaret notunu sil"""
        ziyaret = ZiyaretNotu.query.get(ziyaret_id)
        if not ziyaret:
            raise ValueError("Ziyaret notu bulunamadı!")
        
        db.session.delete(ziyaret)
        db.session.commit()
        return True

class DegerlendirmeService:
    """Staj değerlendirme işlemleri servisi"""
    
    @staticmethod
    def degerlendirme_getir(ogrenci_id):
        """Öğrencinin staj değerlendirmesini getir"""
        degerlendirme = StajDegerlendirme.query.filter_by(ogrenci_id=ogrenci_id).first()
        if not degerlendirme:
            # Yoksa yeni oluştur
            degerlendirme = StajDegerlendirme(ogrenci_id=ogrenci_id)
            db.session.add(degerlendirme)
            db.session.commit()
        return degerlendirme
    
    @staticmethod
    def degerlendirme_guncelle(ogrenci_id, **kriterler):
        """Staj değerlendirmesini güncelle"""
        degerlendirme = DegerlendirmeService.degerlendirme_getir(ogrenci_id)
        
        # Kriterleri güncelle
        for key, value in kriterler.items():
            if hasattr(degerlendirme, key) and value is not None:
                setattr(degerlendirme, key, float(value))
        
        # Toplam ve harf notunu hesapla
        degerlendirme.hesapla_toplam()
        
        db.session.commit()
        return degerlendirme

