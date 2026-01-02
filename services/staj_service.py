from database import db
from models import Ogrenci, ZiyaretNotu, StajDegerlendirme, NormalDonemDegerlendirme, Sinif

class OgrenciService:
    """Öğrenci işlemleri servisi"""
    
    @staticmethod
    def tum_ogrencileri_getir(sinif_id=None):
        """Tüm öğrencileri getir (opsiyonel: sınıf filtresi)"""
        query = Ogrenci.query
        if sinif_id:
            query = query.filter_by(sinif_id=sinif_id)
        return query.order_by(Ogrenci.kayit_tarihi.desc()).all()
    
    @staticmethod
    def ogrenci_getir(ogrenci_id):
        """ID'ye göre öğrenci getir"""
        return Ogrenci.query.get(ogrenci_id)
    
    @staticmethod
    def ogrenci_ekle(ad, soyad, ogrenci_no, telefon=None, sinif_id=None):
        """Yeni öğrenci ekle"""
        # Aynı öğrenci numarası var mı kontrol et
        mevcut = Ogrenci.query.filter_by(ogrenci_no=ogrenci_no).first()
        if mevcut:
            raise ValueError(f"Bu öğrenci numarası ({ogrenci_no}) zaten kayıtlı!")
        
        ogrenci = Ogrenci(
            ad=ad,
            soyad=soyad,
            ogrenci_no=ogrenci_no,
            telefon=telefon,
            sinif_id=sinif_id
        )
        db.session.add(ogrenci)
        db.session.commit()
        return ogrenci
    
    @staticmethod
    def ogrenci_guncelle(ogrenci_id, ad=None, soyad=None, telefon=None, sinif_id=None):
        """Öğrenci bilgilerini güncelle"""
        ogrenci = Ogrenci.query.get(ogrenci_id)
        if not ogrenci:
            raise ValueError("Öğrenci bulunamadı!")
        
        if ad:
            ogrenci.ad = ad
        if soyad:
            ogrenci.soyad = soyad
        if telefon is not None:
            ogrenci.telefon = telefon
        if sinif_id is not None:
            ogrenci.sinif_id = sinif_id if sinif_id else None
        
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

class NormalDonemService:
    """Normal dönem değerlendirme işlemleri servisi"""
    
    @staticmethod
    def degerlendirme_getir(ogrenci_id):
        """Öğrencinin normal dönem değerlendirmesini getir"""
        degerlendirme = NormalDonemDegerlendirme.query.filter_by(ogrenci_id=ogrenci_id).first()
        if not degerlendirme:
            # Yoksa yeni oluştur
            degerlendirme = NormalDonemDegerlendirme(ogrenci_id=ogrenci_id)
            db.session.add(degerlendirme)
            db.session.commit()
        return degerlendirme
    
    @staticmethod
    def degerlendirme_guncelle(ogrenci_id, **kriterler):
        """Normal dönem değerlendirmesini güncelle"""
        degerlendirme = NormalDonemService.degerlendirme_getir(ogrenci_id)
        
        # Kriterleri güncelle
        for key, value in kriterler.items():
            if hasattr(degerlendirme, key):
                if key == 'devamsizlik_durumu':
                    # Boolean değer
                    degerlendirme.devamsizlik_durumu = bool(value) if value is not None else False
                elif value is not None and value != '':
                    # Float değerler (None olabilir)
                    if key.endswith('_puani') and (value == '' or value is None):
                        setattr(degerlendirme, key, None)
                    else:
                        try:
                            setattr(degerlendirme, key, float(value))
                        except (ValueError, TypeError):
                            pass
        
        # Tüm notları hesapla
        degerlendirme.hesapla_tum_notlar()
        
        db.session.commit()
        return degerlendirme

class SinifService:
    """Sınıf işlemleri servisi"""
    
    @staticmethod
    def tum_siniflari_getir():
        """Tüm sınıfları getir"""
        return Sinif.query.order_by(Sinif.ad.asc()).all()
    
    @staticmethod
    def sinif_getir(sinif_id):
        """ID'ye göre sınıf getir"""
        return Sinif.query.get(sinif_id)
    
    @staticmethod
    def sinif_ekle(ad):
        """Yeni sınıf ekle"""
        # Aynı sınıf adı var mı kontrol et
        mevcut = Sinif.query.filter_by(ad=ad).first()
        if mevcut:
            raise ValueError(f"Bu sınıf adı ({ad}) zaten kayıtlı!")
        
        sinif = Sinif(ad=ad)
        db.session.add(sinif)
        db.session.commit()
        return sinif
    
    @staticmethod
    def sinif_guncelle(sinif_id, ad):
        """Sınıf bilgilerini güncelle"""
        sinif = Sinif.query.get(sinif_id)
        if not sinif:
            raise ValueError("Sınıf bulunamadı!")
        
        # Aynı ad başka sınıfta var mı kontrol et
        mevcut = Sinif.query.filter_by(ad=ad).first()
        if mevcut and mevcut.id != sinif_id:
            raise ValueError(f"Bu sınıf adı ({ad}) zaten başka bir sınıfta kullanılıyor!")
        
        sinif.ad = ad
        db.session.commit()
        return sinif
    
    @staticmethod
    def sinif_sil(sinif_id):
        """Sınıfı sil"""
        sinif = Sinif.query.get(sinif_id)
        if not sinif:
            raise ValueError("Sınıf bulunamadı!")
        
        # Sınıfta öğrenci var mı kontrol et
        ogrenci_sayisi = Ogrenci.query.filter_by(sinif_id=sinif_id).count()
        if ogrenci_sayisi > 0:
            raise ValueError(f"Bu sınıfta {ogrenci_sayisi} öğrenci bulunuyor. Önce öğrencileri başka sınıfa taşıyın veya silin!")
        
        db.session.delete(sinif)
        db.session.commit()
        return True

