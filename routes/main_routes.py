from flask import Blueprint, render_template, request, jsonify, send_file
from services.staj_service import OgrenciService, ZiyaretService, DegerlendirmeService, NormalDonemService, SinifService
from services.excel_service import ExcelService
import os
from werkzeug.utils import secure_filename

main_bp = Blueprint('main', __name__)

# Ana sayfa - Öğrenci listesi
@main_bp.route('/')
def index():
    """Ana sayfa"""
    return render_template('index.html')

# Sınıf işlemleri
@main_bp.route('/api/siniflar', methods=['GET'])
def siniflari_getir():
    """Tüm sınıfları getir"""
    try:
        siniflar = SinifService.tum_siniflari_getir()
        return jsonify({
            'basarili': True,
            'siniflar': [s.to_dict() for s in siniflar]
        })
    except Exception as e:
        return jsonify({'basarili': False, 'hata': str(e)}), 500

@main_bp.route('/api/siniflar', methods=['POST'])
def sinif_ekle():
    """Yeni sınıf ekle"""
    try:
        data = request.get_json()
        sinif = SinifService.sinif_ekle(ad=data['ad'])
        return jsonify({
            'basarili': True,
            'mesaj': 'Sınıf başarıyla eklendi',
            'sinif': sinif.to_dict()
        })
    except ValueError as e:
        return jsonify({'basarili': False, 'hata': str(e)}), 400
    except Exception as e:
        return jsonify({'basarili': False, 'hata': str(e)}), 500

@main_bp.route('/api/siniflar/<int:sinif_id>', methods=['PUT'])
def sinif_guncelle(sinif_id):
    """Sınıf güncelle"""
    try:
        data = request.get_json()
        sinif = SinifService.sinif_guncelle(sinif_id=sinif_id, ad=data['ad'])
        return jsonify({
            'basarili': True,
            'mesaj': 'Sınıf başarıyla güncellendi',
            'sinif': sinif.to_dict()
        })
    except ValueError as e:
        return jsonify({'basarili': False, 'hata': str(e)}), 400
    except Exception as e:
        return jsonify({'basarili': False, 'hata': str(e)}), 500

@main_bp.route('/api/siniflar/<int:sinif_id>', methods=['DELETE'])
def sinif_sil(sinif_id):
    """Sınıf sil"""
    try:
        SinifService.sinif_sil(sinif_id)
        return jsonify({
            'basarili': True,
            'mesaj': 'Sınıf başarıyla silindi'
        })
    except ValueError as e:
        return jsonify({'basarili': False, 'hata': str(e)}), 400
    except Exception as e:
        return jsonify({'basarili': False, 'hata': str(e)}), 500

# Öğrenci işlemleri
@main_bp.route('/api/ogrenciler', methods=['GET'])
def ogrencileri_getir():
    """Tüm öğrencileri getir (opsiyonel: sınıf filtresi)"""
    try:
        sinif_id = request.args.get('sinif_id', type=int)
        ogrenciler = OgrenciService.tum_ogrencileri_getir(sinif_id=sinif_id)
        return jsonify({
            'basarili': True,
            'ogrenciler': [o.to_dict() for o in ogrenciler]
        })
    except Exception as e:
        return jsonify({'basarili': False, 'hata': str(e)}), 500

@main_bp.route('/api/ogrenciler/<int:ogrenci_id>', methods=['GET'])
def ogrenci_detay(ogrenci_id):
    """Öğrenci detayları"""
    try:
        ogrenci = OgrenciService.ogrenci_getir(ogrenci_id)
        if not ogrenci:
            return jsonify({'basarili': False, 'hata': 'Öğrenci bulunamadı'}), 404
        
        # Ziyaret notlarını al
        ziyaretler = ZiyaretService.ogrenci_ziyaretlerini_getir(ogrenci_id)
        
        # Değerlendirmeyi al
        degerlendirme = DegerlendirmeService.degerlendirme_getir(ogrenci_id)
        
        # Normal dönem değerlendirmesini al
        normal_donem = NormalDonemService.degerlendirme_getir(ogrenci_id)
        
        return jsonify({
            'basarili': True,
            'ogrenci': ogrenci.to_dict(),
            'ziyaretler': [z.to_dict() for z in ziyaretler],
            'degerlendirme': degerlendirme.to_dict() if degerlendirme else None,
            'normal_donem': normal_donem.to_dict() if normal_donem else None
        })
    except Exception as e:
        return jsonify({'basarili': False, 'hata': str(e)}), 500

@main_bp.route('/api/ogrenciler', methods=['POST'])
def ogrenci_ekle():
    """Yeni öğrenci ekle"""
    try:
        data = request.get_json()
        ogrenci = OgrenciService.ogrenci_ekle(
            ad=data['ad'],
            soyad=data['soyad'],
            ogrenci_no=data['ogrenci_no'],
            telefon=data.get('telefon'),
            sinif_id=data.get('sinif_id')
        )
        return jsonify({
            'basarili': True,
            'mesaj': 'Öğrenci başarıyla eklendi',
            'ogrenci': ogrenci.to_dict()
        })
    except ValueError as e:
        return jsonify({'basarili': False, 'hata': str(e)}), 400
    except Exception as e:
        return jsonify({'basarili': False, 'hata': str(e)}), 500

@main_bp.route('/api/ogrenciler/<int:ogrenci_id>', methods=['PUT'])
def ogrenci_guncelle(ogrenci_id):
    """Öğrenci güncelle"""
    try:
        data = request.get_json()
        ogrenci = OgrenciService.ogrenci_guncelle(
            ogrenci_id=ogrenci_id,
            ad=data.get('ad'),
            soyad=data.get('soyad'),
            telefon=data.get('telefon'),
            sinif_id=data.get('sinif_id')
        )
        return jsonify({
            'basarili': True,
            'mesaj': 'Öğrenci başarıyla güncellendi',
            'ogrenci': ogrenci.to_dict()
        })
    except ValueError as e:
        return jsonify({'basarili': False, 'hata': str(e)}), 400
    except Exception as e:
        return jsonify({'basarili': False, 'hata': str(e)}), 500

@main_bp.route('/api/ogrenciler/<int:ogrenci_id>', methods=['DELETE'])
def ogrenci_sil(ogrenci_id):
    """Öğrenci sil"""
    try:
        OgrenciService.ogrenci_sil(ogrenci_id)
        return jsonify({
            'basarili': True,
            'mesaj': 'Öğrenci başarıyla silindi'
        })
    except ValueError as e:
        return jsonify({'basarili': False, 'hata': str(e)}), 400
    except Exception as e:
        return jsonify({'basarili': False, 'hata': str(e)}), 500

# Ziyaret notu işlemleri
@main_bp.route('/api/ziyaretler', methods=['POST'])
def ziyaret_notu_ekle():
    """Ziyaret notu ekle"""
    try:
        data = request.get_json()
        ziyaret = ZiyaretService.ziyaret_notu_ekle(
            ogrenci_id=data['ogrenci_id'],
            not_metni=data['not_metni'],
            ogretmen_adi=data.get('ogretmen_adi')
        )
        return jsonify({
            'basarili': True,
            'mesaj': 'Ziyaret notu başarıyla eklendi',
            'ziyaret': ziyaret.to_dict()
        })
    except ValueError as e:
        return jsonify({'basarili': False, 'hata': str(e)}), 400
    except Exception as e:
        return jsonify({'basarili': False, 'hata': str(e)}), 500

@main_bp.route('/api/ziyaretler/<int:ziyaret_id>', methods=['DELETE'])
def ziyaret_sil(ziyaret_id):
    """Ziyaret notunu sil"""
    try:
        ZiyaretService.ziyaret_sil(ziyaret_id)
        return jsonify({
            'basarili': True,
            'mesaj': 'Ziyaret notu başarıyla silindi'
        })
    except ValueError as e:
        return jsonify({'basarili': False, 'hata': str(e)}), 400
    except Exception as e:
        return jsonify({'basarili': False, 'hata': str(e)}), 500

# Değerlendirme işlemleri
@main_bp.route('/api/degerlendirme/<int:ogrenci_id>', methods=['GET'])
def degerlendirme_getir(ogrenci_id):
    """Öğrenci değerlendirmesini getir"""
    try:
        degerlendirme = DegerlendirmeService.degerlendirme_getir(ogrenci_id)
        return jsonify({
            'basarili': True,
            'degerlendirme': degerlendirme.to_dict()
        })
    except Exception as e:
        return jsonify({'basarili': False, 'hata': str(e)}), 500

@main_bp.route('/api/degerlendirme/<int:ogrenci_id>', methods=['POST'])
def degerlendirme_guncelle(ogrenci_id):
    """Değerlendirme güncelle"""
    try:
        data = request.get_json()
        degerlendirme = DegerlendirmeService.degerlendirme_guncelle(
            ogrenci_id=ogrenci_id,
            **data
        )
        return jsonify({
            'basarili': True,
            'mesaj': 'Değerlendirme başarıyla güncellendi',
            'degerlendirme': degerlendirme.to_dict()
        })
    except Exception as e:
        return jsonify({'basarili': False, 'hata': str(e)}), 500

# Normal dönem değerlendirme işlemleri
@main_bp.route('/api/normal-donem/<int:ogrenci_id>', methods=['GET'])
def normal_donem_getir(ogrenci_id):
    """Öğrenci normal dönem değerlendirmesini getir"""
    try:
        degerlendirme = NormalDonemService.degerlendirme_getir(ogrenci_id)
        return jsonify({
            'basarili': True,
            'degerlendirme': degerlendirme.to_dict()
        })
    except Exception as e:
        return jsonify({'basarili': False, 'hata': str(e)}), 500

@main_bp.route('/api/normal-donem/<int:ogrenci_id>', methods=['POST'])
def normal_donem_guncelle(ogrenci_id):
    """Normal dönem değerlendirmesini güncelle"""
    try:
        data = request.get_json()
        degerlendirme = NormalDonemService.degerlendirme_guncelle(
            ogrenci_id=ogrenci_id,
            **data
        )
        return jsonify({
            'basarili': True,
            'mesaj': 'Normal dönem değerlendirmesi başarıyla güncellendi',
            'degerlendirme': degerlendirme.to_dict()
        })
    except Exception as e:
        return jsonify({'basarili': False, 'hata': str(e)}), 500

# Excel işlemleri
@main_bp.route('/api/excel/export', methods=['GET'])
def excel_export():
    """Öğrenci listesini Excel'e aktar (opsiyonel: sınıf filtresi)"""
    try:
        sinif_id = request.args.get('sinif_id', type=int)
        dosya_yolu = ExcelService.ogrencileri_excel_aktar('ogrenci_listesi.xlsx', sinif_id=sinif_id)
        return send_file(dosya_yolu, as_attachment=True, download_name='ogrenci_listesi.xlsx')
    except Exception as e:
        return jsonify({'basarili': False, 'hata': str(e)}), 500

@main_bp.route('/api/excel/import', methods=['POST'])
def excel_import():
    """Excel'den öğrenci içe aktar"""
    try:
        if 'file' not in request.files:
            return jsonify({'basarili': False, 'hata': 'Dosya bulunamadı'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'basarili': False, 'hata': 'Dosya seçilmedi'}), 400
        
        if file and file.filename.endswith(('.xlsx', '.xls')):
            filename = secure_filename(file.filename)
            dosya_yolu = os.path.join('uploads', filename)
            
            # uploads klasörü yoksa oluştur
            os.makedirs('uploads', exist_ok=True)
            
            file.save(dosya_yolu)
            sonuc = ExcelService.ogrencileri_excel_ice_aktar(dosya_yolu)
            
            # Geçici dosyayı sil
            os.remove(dosya_yolu)
            
            return jsonify(sonuc)
        else:
            return jsonify({'basarili': False, 'hata': 'Geçersiz dosya formatı'}), 400
    except Exception as e:
        return jsonify({'basarili': False, 'hata': str(e)}), 500

@main_bp.route('/api/excel/rapor', methods=['GET'])
def excel_rapor():
    """Staj değerlendirme raporu oluştur (opsiyonel: sınıf filtresi)"""
    try:
        sinif_id = request.args.get('sinif_id', type=int)
        dosya_yolu = ExcelService.degerlendirme_raporu_olustur('staj_degerlendirme_raporu.xlsx', sinif_id=sinif_id)
        return send_file(dosya_yolu, as_attachment=True, download_name='staj_degerlendirme_raporu.xlsx')
    except Exception as e:
        return jsonify({'basarili': False, 'hata': str(e)}), 500

@main_bp.route('/api/excel/rapor/normal-donem', methods=['GET'])
def excel_rapor_normal_donem():
    """Normal dönem notları raporu oluştur (opsiyonel: sınıf filtresi)"""
    try:
        sinif_id = request.args.get('sinif_id', type=int)
        dosya_yolu = ExcelService.normal_donem_raporu_olustur('normal_donem_raporu.xlsx', sinif_id=sinif_id)
        return send_file(dosya_yolu, as_attachment=True, download_name='normal_donem_raporu.xlsx')
    except Exception as e:
        return jsonify({'basarili': False, 'hata': str(e)}), 500

# Öğrenci detay sayfası
@main_bp.route('/ogrenci/<int:ogrenci_id>')
def ogrenci_detay_sayfa(ogrenci_id):
    """Öğrenci detay sayfası"""
    return render_template('ogrenci_detay.html', ogrenci_id=ogrenci_id)

# İstatistik API'leri
@main_bp.route('/api/istatistikler/harf-notlari', methods=['GET'])
def harf_notu_istatistikleri():
    """Harf notu dağılımını getir (opsiyonel: sınıf filtresi)"""
    try:
        from models import StajDegerlendirme, Ogrenci
        
        sinif_id = request.args.get('sinif_id', type=int)
        
        # Sınıf filtresi varsa uygula
        if sinif_id:
            ogrenci_ids = [o.id for o in Ogrenci.query.filter_by(sinif_id=sinif_id).all()]
            degerlendirmeler = StajDegerlendirme.query.filter(StajDegerlendirme.ogrenci_id.in_(ogrenci_ids)).all()
        else:
            degerlendirmeler = StajDegerlendirme.query.all()
        
        # Harf notlarını say
        harf_notu_sayilari = {}
        for deg in degerlendirmeler:
            if deg.harf_notu:
                harf_notu_sayilari[deg.harf_notu] = harf_notu_sayilari.get(deg.harf_notu, 0) + 1
        
        return jsonify({
            'basarili': True,
            'harf_notlari': harf_notu_sayilari
        })
    except Exception as e:
        return jsonify({'basarili': False, 'hata': str(e)}), 500

