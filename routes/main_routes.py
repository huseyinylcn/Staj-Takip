from flask import Blueprint, render_template, request, jsonify, send_file
from services.staj_service import OgrenciService, ZiyaretService, DegerlendirmeService
from services.excel_service import ExcelService
import os
from werkzeug.utils import secure_filename

main_bp = Blueprint('main', __name__)

# Ana sayfa - Öğrenci listesi
@main_bp.route('/')
def index():
    """Ana sayfa"""
    return render_template('index.html')

# Öğrenci işlemleri
@main_bp.route('/api/ogrenciler', methods=['GET'])
def ogrencileri_getir():
    """Tüm öğrencileri getir"""
    try:
        ogrenciler = OgrenciService.tum_ogrencileri_getir()
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
        
        return jsonify({
            'basarili': True,
            'ogrenci': ogrenci.to_dict(),
            'ziyaretler': [z.to_dict() for z in ziyaretler],
            'degerlendirme': degerlendirme.to_dict() if degerlendirme else None
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
            telefon=data.get('telefon')
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
            telefon=data.get('telefon')
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

# Excel işlemleri
@main_bp.route('/api/excel/export', methods=['GET'])
def excel_export():
    """Öğrenci listesini Excel'e aktar"""
    try:
        dosya_yolu = ExcelService.ogrencileri_excel_aktar('ogrenci_listesi.xlsx')
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
    """Değerlendirme raporu oluştur"""
    try:
        dosya_yolu = ExcelService.degerlendirme_raporu_olustur('degerlendirme_raporu.xlsx')
        return send_file(dosya_yolu, as_attachment=True, download_name='degerlendirme_raporu.xlsx')
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
    """Harf notu dağılımını getir"""
    try:
        from models import StajDegerlendirme
        
        # Tüm değerlendirmeleri al
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

