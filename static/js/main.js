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
document.addEventListener('DOMContentLoaded', function() {
    ogrencileriYukle();
    harfNotuGrafigiCiz();
    
    // Modal dışına tıklanınca kapat
    window.onclick = function(event) {
        if (event.target.classList.contains('modal')) {
            event.target.style.display = 'none';
        }
    };
});

// Öğrencileri yükle
async function ogrencileriYukle() {
    const sonuc = await apiCall('/api/ogrenciler');
    
    if (sonuc.basarili) {
        const ogrenciler = sonuc.ogrenciler;
        ogrencileriGoster(ogrenciler);
        istatistikleriGuncelle(ogrenciler);
        harfNotuGrafigiCiz(); // Grafiği güncelle
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
function yeniOgrenciModal() {
    document.getElementById('yeniOgrenciForm').reset();
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
        telefon: formData.get('telefon')
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
        window.location.href = '/api/excel/export';
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

// Rapor indir
async function raporIndir() {
    try {
        window.location.href = '/api/excel/rapor';
        bildirimGoster('Rapor indiriliyor...', 'success');
    } catch (error) {
        bildirimGoster('Rapor indirme hatası', 'error');
    }
}

// Harf notu pasta grafiği çiz
let harfNotuGrafik = null;

async function harfNotuGrafigiCiz() {
    const sonuc = await apiCall('/api/istatistikler/harf-notlari');
    
    if (!sonuc.basarili || Object.keys(sonuc.harf_notlari).length === 0) {
        // Veri yoksa grafiği gizle
        const chartContainer = document.querySelector('.chart-container');
        if (chartContainer) {
            chartContainer.style.display = 'none';
        }
        return;
    }
    
    const harfNotlari = sonuc.harf_notlari;
    
    // Harf notlarını sırala (AA, BA, BB, CB, CC, DC, DD, FD, FF)
    const harfNotuSirasi = ['AA', 'BA', 'BB', 'CB', 'CC', 'DC', 'DD', 'FD', 'FF'];
    const labels = [];
    const data = [];
    
    harfNotuSirasi.forEach(harf => {
        if (harfNotlari[harf]) {
            labels.push(harf);
            data.push(harfNotlari[harf]);
        }
    });
    
    // Renkler - her harf notu için farklı renk
    const colors = [
        '#2ecc71', // AA - Yeşil
        '#3498db', // BA - Mavi
        '#1abc9c', // BB - Turkuaz
        '#f39c12', // CB - Turuncu
        '#e67e22', // CC - Koyu Turuncu
        '#e74c3c', // DC - Kırmızı
        '#c0392b', // DD - Koyu Kırmızı
        '#95a5a6', // FD - Gri
        '#34495e'  // FF - Koyu Gri
    ];
    
    const ctx = document.getElementById('harfNotuGrafik');
    
    // Eski grafiği temizle
    if (harfNotuGrafik) {
        harfNotuGrafik.destroy();
    }
    
    // Yeni grafik oluştur
    harfNotuGrafik = new Chart(ctx, {
        type: 'pie',
        data: {
            labels: labels,
            datasets: [{
                label: 'Öğrenci Sayısı',
                data: data,
                backgroundColor: colors.slice(0, labels.length),
                borderWidth: 2,
                borderColor: '#ffffff'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        padding: 15,
                        font: {
                            size: 14,
                            weight: 'bold'
                        }
                    }
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            const label = context.label || '';
                            const value = context.parsed || 0;
                            const total = context.dataset.data.reduce((a, b) => a + b, 0);
                            const percentage = ((value / total) * 100).toFixed(1);
                            return `${label}: ${value} öğrenci (${percentage}%)`;
                        }
                    },
                    backgroundColor: 'rgba(0, 0, 0, 0.8)',
                    titleFont: {
                        size: 14,
                        weight: 'bold'
                    },
                    bodyFont: {
                        size: 13
                    },
                    padding: 12,
                    cornerRadius: 8
                }
            }
        }
    });
}

