// API yardımcı fonksiyonları
async function apiCall(url, method = 'GET', data = null) {
    const options = {
        method: method,
        headers: {
            'Content-Type': 'application/json',
        }
    };
    
    if (data) {
        options.body = JSON.stringify(data);
    }
    
    try {
        const response = await fetch(url, options);
        return await response.json();
    } catch (error) {
        console.error('API Hatası:', error);
        return { basarili: false, hata: 'Bağlantı hatası' };
    }
}

// Bildirim göster
function bildirimGoster(mesaj, tip = 'success') {
    const notification = document.getElementById('notification');
    notification.textContent = mesaj;
    notification.className = `notification ${tip}`;
    notification.style.display = 'block';
    
    setTimeout(() => {
        notification.style.display = 'none';
    }, 3000);
}

// Modal işlemleri
function modalAc(modalId) {
    document.getElementById(modalId).style.display = 'block';
}

function modalKapat(modalId) {
    document.getElementById(modalId).style.display = 'none';
}

// Sayfa yüklendiğinde
let seciliSinifId = null;

document.addEventListener('DOMContentLoaded', function() {
    siniflariYukle();
    ogrencileriYukle();
    
    // Modal dışına tıklanınca kapat
    window.onclick = function(event) {
        if (event.target.classList.contains('modal')) {
            event.target.style.display = 'none';
        }
        
        // Dropdown dışına tıklanınca kapat
        if (!event.target.closest('.dropdown')) {
            document.querySelectorAll('.dropdown-content').forEach(dropdown => {
                dropdown.style.display = 'none';
            });
        }
    };
});

// Sınıfları yükle
async function siniflariYukle() {
    const sonuc = await apiCall('/api/siniflar');
    
    if (sonuc.basarili) {
        const siniflar = sonuc.siniflar;
        sinifFiltresiDoldur(siniflar);
        ogrenciSinifSecimiDoldur(siniflar);
        sinifListesiGoster(siniflar);
    }
}

// Sınıf filtresini doldur
function sinifFiltresiDoldur(siniflar) {
    const select = document.getElementById('sinifFiltresi');
    select.innerHTML = '<option value="">Tüm Sınıflar</option>';
    siniflar.forEach(sinif => {
        const option = document.createElement('option');
        option.value = sinif.id;
        option.textContent = sinif.ad;
        if (seciliSinifId == sinif.id) {
            option.selected = true;
        }
        select.appendChild(option);
    });
}

// Öğrenci ekleme modal'ındaki sınıf seçimini doldur
function ogrenciSinifSecimiDoldur(siniflar) {
    const select = document.getElementById('ogrenciSinifSecimi');
    select.innerHTML = '<option value="">Sınıf Seçin (Opsiyonel)</option>';
    siniflar.forEach(sinif => {
        const option = document.createElement('option');
        option.value = sinif.id;
        option.textContent = sinif.ad;
        select.appendChild(option);
    });
}

// Sınıf listesini göster
function sinifListesiGoster(siniflar) {
    const liste = document.getElementById('sinifListesi');
    if (siniflar.length === 0) {
        liste.innerHTML = '<p>Henüz sınıf eklenmemiş</p>';
        return;
    }
    
    liste.innerHTML = siniflar.map(sinif => `
        <div style="display: flex; justify-content: space-between; align-items: center; padding: 10px; border: 1px solid #ddd; border-radius: 5px; margin-bottom: 10px;">
            <span><strong>${sinif.ad}</strong></span>
            <button class="btn btn-icon btn-danger" onclick="sinifSil(${sinif.id}, '${sinif.ad}')">
                <i class="fas fa-trash"></i>
            </button>
        </div>
    `).join('');
}

// Sınıf filtrele
async function sinifFiltrele() {
    const select = document.getElementById('sinifFiltresi');
    seciliSinifId = select.value ? parseInt(select.value) : null;
    ogrencileriYukle();
}

// Öğrencileri yükle
async function ogrencileriYukle() {
    let url = '/api/ogrenciler';
    if (seciliSinifId) {
        url += `?sinif_id=${seciliSinifId}`;
    }
    const sonuc = await apiCall(url);
    
    if (sonuc.basarili) {
        const ogrenciler = sonuc.ogrenciler;
        ogrencileriGoster(ogrenciler);
        istatistikleriGuncelle(ogrenciler);
    } else {
        bildirimGoster('Öğrenciler yüklenemedi: ' + sonuc.hata, 'error');
    }
}

// Öğrencileri göster
function ogrencileriGoster(ogrenciler) {
    const liste = document.getElementById('ogrenciListesi');
    
    if (ogrenciler.length === 0) {
        liste.innerHTML = `
            <div class="empty-state">
                <i class="fas fa-users"></i>
                <h3>Henüz öğrenci eklenmemiş</h3>
                <p>Yeni öğrenci eklemek için "Yeni Öğrenci" butonuna tıklayın</p>
            </div>
        `;
        return;
    }
    
    liste.innerHTML = ogrenciler.map(ogrenci => `
        <div class="ogrenci-card" onclick="window.location.href='/ogrenci/${ogrenci.id}'">
            <div class="ogrenci-header">
                <div class="ogrenci-avatar">
                    <i class="fas fa-user-circle"></i>
                </div>
                <div class="ogrenci-info">
                    <h3>${ogrenci.tam_ad}</h3>
                    <p><i class="fas fa-id-card"></i> ${ogrenci.ogrenci_no}</p>
                    ${ogrenci.sinif_adi ? `<p><i class="fas fa-users"></i> ${ogrenci.sinif_adi}</p>` : ''}
                    ${ogrenci.telefon ? `<p><i class="fas fa-phone"></i> ${ogrenci.telefon}</p>` : ''}
                </div>
            </div>
            <div class="ogrenci-footer">
                <span class="badge badge-info">
                    <i class="fas fa-calendar"></i> ${new Date(ogrenci.kayit_tarihi).toLocaleDateString('tr-TR')}
                </span>
                <div class="ogrenci-actions" onclick="event.stopPropagation()">
                    <button class="btn btn-icon btn-danger" onclick="ogrenciSil(${ogrenci.id}, '${ogrenci.tam_ad}')">
                        <i class="fas fa-trash"></i>
                    </button>
                </div>
            </div>
        </div>
    `).join('');
}

// İstatistikleri güncelle
async function istatistikleriGuncelle(ogrenciler) {
    document.getElementById('toplamOgrenci').textContent = ogrenciler.length;
    
    let degerlendirilenler = 0;
    let toplamZiyaret = 0;
    
    for (const ogrenci of ogrenciler) {
        const detay = await apiCall(`/api/ogrenciler/${ogrenci.id}`);
        if (detay.basarili) {
            if (detay.degerlendirme && detay.degerlendirme.toplam > 0) {
                degerlendirilenler++;
            }
            toplamZiyaret += detay.ziyaretler.length;
        }
    }
    
    document.getElementById('degerlendirilenler').textContent = degerlendirilenler;
    document.getElementById('toplamZiyaret').textContent = toplamZiyaret;
}

// Yeni öğrenci modal
async function yeniOgrenciModal() {
    document.getElementById('yeniOgrenciForm').reset();
    siniflariYukle(); // Sınıfları güncelle
    modalAc('yeniOgrenciModal');
}

// Öğrenci ekle
async function ogrenciEkle(event) {
    event.preventDefault();
    
    const form = event.target;
    const formData = new FormData(form);
    const data = {
        ad: formData.get('ad'),
        soyad: formData.get('soyad'),
        ogrenci_no: formData.get('ogrenci_no'),
        telefon: formData.get('telefon'),
        sinif_id: formData.get('sinif_id') || null
    };
    
    const sonuc = await apiCall('/api/ogrenciler', 'POST', data);
    
    if (sonuc.basarili) {
        bildirimGoster('Öğrenci başarıyla eklendi!', 'success');
        modalKapat('yeniOgrenciModal');
        ogrencileriYukle();
    } else {
        bildirimGoster('Hata: ' + sonuc.hata, 'error');
    }
}

// Öğrenci sil
async function ogrenciSil(id, ad) {
    if (!confirm(`${ad} isimli öğrenciyi silmek istediğinize emin misiniz?`)) {
        return;
    }
    
    const sonuc = await apiCall(`/api/ogrenciler/${id}`, 'DELETE');
    
    if (sonuc.basarili) {
        bildirimGoster('Öğrenci başarıyla silindi', 'success');
        ogrencileriYukle();
    } else {
        bildirimGoster('Hata: ' + sonuc.hata, 'error');
    }
}

// Arama yap
function aramaYap() {
    const aramaMetni = document.getElementById('searchInput').value.toLowerCase();
    const kartlar = document.querySelectorAll('.ogrenci-card');
    
    kartlar.forEach(kart => {
        const metin = kart.textContent.toLowerCase();
        if (metin.includes(aramaMetni)) {
            kart.style.display = 'block';
        } else {
            kart.style.display = 'none';
        }
    });
}

// Excel export
async function excelExport() {
    try {
        let url = '/api/excel/export';
        if (seciliSinifId) {
            url += `?sinif_id=${seciliSinifId}`;
        }
        window.location.href = url;
        bildirimGoster('Excel dosyası indiriliyor...', 'success');
    } catch (error) {
        bildirimGoster('Excel indirme hatası', 'error');
    }
}

// Excel import modal
function excelImportModal() {
    document.getElementById('uploadSonuc').style.display = 'none';
    modalAc('excelImportModal');
    
    // Upload area click event
    document.getElementById('uploadArea').onclick = function() {
        document.getElementById('excelFile').click();
    };
}

// Excel import
async function excelImport() {
    const fileInput = document.getElementById('excelFile');
    const file = fileInput.files[0];
    
    if (!file) return;
    
    const formData = new FormData();
    formData.append('file', file);
    
    try {
        const response = await fetch('/api/excel/import', {
            method: 'POST',
            body: formData
        });
        
        const sonuc = await response.json();
        const sonucDiv = document.getElementById('uploadSonuc');
        
        if (sonuc.basarili) {
            sonucDiv.className = 'upload-sonuc success';
            sonucDiv.innerHTML = `
                <strong>✅ Başarılı!</strong><br>
                ${sonuc.eklenen} öğrenci eklendi.
                ${sonuc.hatalar.length > 0 ? `<br><br><strong>Hatalar:</strong><br>${sonuc.hatalar.join('<br>')}` : ''}
            `;
            sonucDiv.style.display = 'block';
            ogrencileriYukle();
        } else {
            sonucDiv.className = 'upload-sonuc error';
            sonucDiv.innerHTML = `<strong>❌ Hata!</strong><br>${sonuc.hata}`;
            sonucDiv.style.display = 'block';
        }
    } catch (error) {
        bildirimGoster('Excel yükleme hatası: ' + error.message, 'error');
    }
}

// Rapor dropdown toggle
function raporDropdownToggle(event) {
    event.stopPropagation();
    const dropdown = document.getElementById('raporDropdown');
    const isVisible = dropdown.style.display === 'block';
    
    // Diğer dropdown'ları kapat
    document.querySelectorAll('.dropdown-content').forEach(d => {
        if (d.id !== 'raporDropdown') {
            d.style.display = 'none';
        }
    });
    
    dropdown.style.display = isVisible ? 'none' : 'block';
}

// Rapor indir
async function raporIndir(tip) {
    try {
        let url = '';
        if (tip === 'staj') {
            url = '/api/excel/rapor';
        } else if (tip === 'normal-donem') {
            url = '/api/excel/rapor/normal-donem';
        } else {
            bildirimGoster('Geçersiz rapor tipi', 'error');
            return;
        }
        
        if (seciliSinifId) {
            url += `?sinif_id=${seciliSinifId}`;
        }
        
        // Dropdown'ı kapat
        document.getElementById('raporDropdown').style.display = 'none';
        
        window.location.href = url;
        bildirimGoster('Rapor indiriliyor...', 'success');
    } catch (error) {
        bildirimGoster('Rapor indirme hatası', 'error');
    }
}

// Sınıf yönetimi modal
async function sinifYonetimiModal() {
    siniflariYukle();
    modalAc('sinifYonetimiModal');
}

// Sınıf ekle
async function sinifEkle(event) {
    event.preventDefault();
    const input = document.getElementById('yeniSinifAd');
    const ad = input.value.trim();
    
    if (!ad) {
        bildirimGoster('Sınıf adı gerekli!', 'error');
        return;
    }
    
    const sonuc = await apiCall('/api/siniflar', 'POST', { ad: ad });
    
    if (sonuc.basarili) {
        bildirimGoster('Sınıf başarıyla eklendi!', 'success');
        input.value = '';
        siniflariYukle();
    } else {
        bildirimGoster('Hata: ' + sonuc.hata, 'error');
    }
}

// Sınıf sil
async function sinifSil(sinifId, sinifAd) {
    if (!confirm(`${sinifAd} sınıfını silmek istediğinize emin misiniz?`)) {
        return;
    }
    
    const sonuc = await apiCall(`/api/siniflar/${sinifId}`, 'DELETE');
    
    if (sonuc.basarili) {
        bildirimGoster('Sınıf başarıyla silindi', 'success');
        siniflariYukle();
        if (seciliSinifId == sinifId) {
            seciliSinifId = null;
            document.getElementById('sinifFiltresi').value = '';
            ogrencileriYukle();
        }
    } else {
        bildirimGoster('Hata: ' + sonuc.hata, 'error');
    }
}

