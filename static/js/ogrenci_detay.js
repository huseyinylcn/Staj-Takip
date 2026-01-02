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
    ogrenciDetayYukle();
    
    // Modal dışına tıklanınca kapat
    window.onclick = function(event) {
        if (event.target.classList.contains('modal')) {
            event.target.style.display = 'none';
        }
    };
});

// Öğrenci detaylarını yükle
async function ogrenciDetayYukle() {
    const sonuc = await apiCall(`/api/ogrenciler/${ogrenciId}`);
    
    if (sonuc.basarili) {
        ogrenciBilgileriGoster(sonuc.ogrenci);
        ziyaretleriGoster(sonuc.ziyaretler);
        degerlendirmeGoster(sonuc.degerlendirme);
        normalDonemGoster(sonuc.normal_donem);
    } else {
        bildirimGoster('Öğrenci bilgileri yüklenemedi: ' + sonuc.hata, 'error');
    }
}

// Öğrenci bilgilerini göster
function ogrenciBilgileriGoster(ogrenci) {
    document.getElementById('ogrenciBaslik').textContent = ogrenci.tam_ad;
    
    document.getElementById('ogrenciBilgi').innerHTML = `
        <h2>${ogrenci.tam_ad}</h2>
        <p><i class="fas fa-id-card"></i> <strong>Öğrenci No:</strong> ${ogrenci.ogrenci_no}</p>
        ${ogrenci.telefon ? `<p><i class="fas fa-phone"></i> <strong>Telefon:</strong> ${ogrenci.telefon}</p>` : ''}
        <p><i class="fas fa-calendar"></i> <strong>Kayıt Tarihi:</strong> ${new Date(ogrenci.kayit_tarihi).toLocaleDateString('tr-TR')}</p>
    `;
}

// Tab değiştir
function tabDegistir(tabId) {
    // Tüm tab butonlarını ve içerikleri pasif yap
    document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
    document.querySelectorAll('.tab-content').forEach(content => content.classList.remove('active'));
    
    // Seçili tab'ı aktif yap
    event.target.closest('.tab-btn').classList.add('active');
    document.getElementById(tabId).classList.add('active');
}

// Ziyaretleri göster
function ziyaretleriGoster(ziyaretler) {
    const liste = document.getElementById('ziyaretListesi');
    
    if (ziyaretler.length === 0) {
        liste.innerHTML = `
            <div class="empty-state">
                <i class="fas fa-notes-medical"></i>
                <h3>Henüz ziyaret notu eklenmemiş</h3>
                <p>Yeni ziyaret notu eklemek için "Yeni Not Ekle" butonuna tıklayın</p>
            </div>
        `;
        return;
    }
    
    liste.innerHTML = ziyaretler.map(ziyaret => `
        <div class="ziyaret-item">
            <div class="ziyaret-header">
                <strong>${ziyaret.ogretmen_adi || 'Öğretmen'}</strong>
                <div>
                    <small>${new Date(ziyaret.tarih).toLocaleString('tr-TR')}</small>
                    <button class="btn btn-icon btn-danger" onclick="ziyaretSil(${ziyaret.id})">
                        <i class="fas fa-trash"></i>
                    </button>
                </div>
            </div>
            <div class="ziyaret-text">${ziyaret.not_metni}</div>
        </div>
    `).join('');
}

// Ziyaret notu modal
function ziyaretNotuModal() {
    document.getElementById('ziyaretForm').reset();
    modalAc('ziyaretNotuModal');
}

// Ziyaret notu ekle
async function ziyaretNotuEkle(event) {
    event.preventDefault();
    
    const form = event.target;
    const formData = new FormData(form);
    const data = {
        ogrenci_id: ogrenciId,
        ogretmen_adi: formData.get('ogretmen_adi'),
        not_metni: formData.get('not_metni')
    };
    
    const sonuc = await apiCall('/api/ziyaretler', 'POST', data);
    
    if (sonuc.basarili) {
        bildirimGoster('Ziyaret notu başarıyla eklendi!', 'success');
        modalKapat('ziyaretNotuModal');
        ogrenciDetayYukle();
    } else {
        bildirimGoster('Hata: ' + sonuc.hata, 'error');
    }
}

// Ziyaret sil
async function ziyaretSil(ziyaretId) {
    if (!confirm('Bu ziyaret notunu silmek istediğinize emin misiniz?')) {
        return;
    }
    
    const sonuc = await apiCall(`/api/ziyaretler/${ziyaretId}`, 'DELETE');
    
    if (sonuc.basarili) {
        bildirimGoster('Ziyaret notu silindi', 'success');
        ogrenciDetayYukle();
    } else {
        bildirimGoster('Hata: ' + sonuc.hata, 'error');
    }
}

// Değerlendirmeyi göster
function degerlendirmeGoster(degerlendirme) {
    if (!degerlendirme) return;
    
    const form = document.getElementById('degerlendirmeForm');
    
    // Form alanlarını doldur
    form.isyeren_notu.value = degerlendirme.isyeren_notu || 0;
    form.icindekiler.value = degerlendirme.icindekiler || 0;
    form.firma_bilgisi.value = degerlendirme.firma_bilgisi || 0;
    form.yazim_duzeni.value = degerlendirme.yazim_duzeni || 0;
    form.resim_sekil.value = degerlendirme.resim_sekil || 0;
    form.dil_kullanimi.value = degerlendirme.dil_kullanimi || 0;
    form.sonuc_bolumu.value = degerlendirme.sonuc_bolumu || 0;
    form.defter_duzeni_mulakat.value = degerlendirme.defter_duzeni_mulakat || 0;
    
    // Toplam ve harf notunu göster
    document.getElementById('toplamPuan').textContent = degerlendirme.toplam.toFixed(1);
    document.getElementById('harfNotu').textContent = degerlendirme.harf_notu || '-';
}

// Toplam hesapla
function toplamHesapla() {
    const form = document.getElementById('degerlendirmeForm');
    
    const toplam = 
        parseFloat(form.isyeren_notu.value || 0) +
        parseFloat(form.icindekiler.value || 0) +
        parseFloat(form.firma_bilgisi.value || 0) +
        parseFloat(form.yazim_duzeni.value || 0) +
        parseFloat(form.resim_sekil.value || 0) +
        parseFloat(form.dil_kullanimi.value || 0) +
        parseFloat(form.sonuc_bolumu.value || 0) +
        parseFloat(form.defter_duzeni_mulakat.value || 0);
    
    document.getElementById('toplamPuan').textContent = toplam.toFixed(1);
    
    // Harf notunu hesapla
    let harfNotu = '-';
    if (toplam >= 90) harfNotu = 'AA';
    else if (toplam >= 85) harfNotu = 'BA';
    else if (toplam >= 80) harfNotu = 'BB';
    else if (toplam >= 75) harfNotu = 'CB';
    else if (toplam >= 70) harfNotu = 'CC';
    else if (toplam >= 65) harfNotu = 'DC';
    else if (toplam >= 60) harfNotu = 'DD';
    else if (toplam >= 50) harfNotu = 'FD';
    else if (toplam > 0) harfNotu = 'FF';
    
    document.getElementById('harfNotu').textContent = harfNotu;
}

// Değerlendirme kaydet
async function degerlendirmeKaydet(event) {
    event.preventDefault();
    
    const form = event.target;
    const formData = new FormData(form);
    
    const data = {
        isyeren_notu: parseFloat(formData.get('isyeren_notu')),
        icindekiler: parseFloat(formData.get('icindekiler')),
        firma_bilgisi: parseFloat(formData.get('firma_bilgisi')),
        yazim_duzeni: parseFloat(formData.get('yazim_duzeni')),
        resim_sekil: parseFloat(formData.get('resim_sekil')),
        dil_kullanimi: parseFloat(formData.get('dil_kullanimi')),
        sonuc_bolumu: parseFloat(formData.get('sonuc_bolumu')),
        defter_duzeni_mulakat: parseFloat(formData.get('defter_duzeni_mulakat'))
    };
    
    const sonuc = await apiCall(`/api/degerlendirme/${ogrenciId}`, 'POST', data);
    
    if (sonuc.basarili) {
        bildirimGoster('Değerlendirme başarıyla kaydedildi!', 'success');
        degerlendirmeGoster(sonuc.degerlendirme);
    } else {
        bildirimGoster('Hata: ' + sonuc.hata, 'error');
    }
}

// Normal dönem değerlendirmesini göster
function normalDonemGoster(normalDonem) {
    if (!normalDonem) return;
    
    const form = document.getElementById('normalDonemForm');
    
    // Form alanlarını doldur
    form.vize_notu.value = normalDonem.vize_notu || 0;
    form.vize_odev_puani.value = normalDonem.vize_odev_puani || '';
    form.vize_odev_yuzdesi.value = normalDonem.vize_odev_yuzdesi || 0;
    
    form.final_notu.value = normalDonem.final_notu || 0;
    form.final_odev_puani.value = normalDonem.final_odev_puani || '';
    form.final_odev_yuzdesi.value = normalDonem.final_odev_yuzdesi || 0;
    
    form.devamsizlik_durumu.checked = normalDonem.devamsizlik_durumu || false;
    
    form.butunleme_notu.value = normalDonem.butunleme_notu || '';
    form.butunleme_odev_puani.value = normalDonem.butunleme_odev_puani || '';
    form.butunleme_odev_yuzdesi.value = normalDonem.butunleme_odev_yuzdesi || 0;
    
    // Hesaplanmış değerleri göster
    document.getElementById('vizeToplam').textContent = (normalDonem.vize_toplam || 0).toFixed(2);
    document.getElementById('finalToplam').textContent = (normalDonem.final_toplam || 0).toFixed(2);
    document.getElementById('butunlemeToplam').textContent = normalDonem.butunleme_toplam !== null ? normalDonem.butunleme_toplam.toFixed(2) : '-';
    document.getElementById('genelToplam').textContent = (normalDonem.genel_toplam || 0).toFixed(2);
    document.getElementById('normalDonemHarfNotu').textContent = normalDonem.harf_notu || '-';
}

// Normal dönem hesapla
function normalDonemHesapla() {
    const form = document.getElementById('normalDonemForm');
    
    // Vize hesaplama
    let vize = parseFloat(form.vize_notu.value || 0);
    let vizeOdev = form.vize_odev_puani.value ? parseFloat(form.vize_odev_puani.value) : null;
    let vizeOdevYuzdesi = parseFloat(form.vize_odev_yuzdesi.value || 0);
    
    let vizeToplam = vize;
    if (vizeOdev !== null && vizeOdevYuzdesi > 0) {
        let vizeAgirlik = (100 - vizeOdevYuzdesi) / 100;
        let odevAgirlik = vizeOdevYuzdesi / 100;
        vizeToplam = (vize * vizeAgirlik) + (vizeOdev * odevAgirlik);
    }
    document.getElementById('vizeToplam').textContent = vizeToplam.toFixed(2);
    
    // Final hesaplama
    let final = parseFloat(form.final_notu.value || 0);
    let finalOdev = form.final_odev_puani.value ? parseFloat(form.final_odev_puani.value) : null;
    let finalOdevYuzdesi = parseFloat(form.final_odev_yuzdesi.value || 0);
    
    let finalToplam = final;
    if (finalOdev !== null && finalOdevYuzdesi > 0) {
        let finalAgirlik = (100 - finalOdevYuzdesi) / 100;
        let odevAgirlik = finalOdevYuzdesi / 100;
        finalToplam = (final * finalAgirlik) + (finalOdev * odevAgirlik);
    }
    document.getElementById('finalToplam').textContent = finalToplam.toFixed(2);
    
    // Bütünleme hesaplama
    let butunleme = form.butunleme_notu.value ? parseFloat(form.butunleme_notu.value) : null;
    let butOdev = form.butunleme_odev_puani.value ? parseFloat(form.butunleme_odev_puani.value) : null;
    let butOdevYuzdesi = parseFloat(form.butunleme_odev_yuzdesi.value || 0);
    
    let butunlemeToplam = null;
    if (butunleme !== null) {
        butunlemeToplam = butunleme;
        if (butOdev !== null && butOdevYuzdesi > 0) {
            let butAgirlik = (100 - butOdevYuzdesi) / 100;
            let odevAgirlik = butOdevYuzdesi / 100;
            butunlemeToplam = (butunleme * butAgirlik) + (butOdev * odevAgirlik);
        }
        document.getElementById('butunlemeToplam').textContent = butunlemeToplam.toFixed(2);
    } else {
        document.getElementById('butunlemeToplam').textContent = '-';
    }
    
    // Devamsızlık kontrolü
    let devamsizlikDurumu = form.devamsizlik_durumu.checked;
    
    // Genel toplam hesaplama
    let genelToplam = 0;
    let harfNotu = '-';
    
    if (!devamsizlikDurumu) {
        genelToplam = 0;
        harfNotu = 'FF';
    } else {
        // Bütünleme varsa onu kullan, yoksa vize+final
        if (butunlemeToplam !== null) {
            genelToplam = butunlemeToplam;
        } else {
            // Vize %40, Final %60
            genelToplam = (vizeToplam * 0.4) + (finalToplam * 0.6);
        }
        
        // Harf notunu hesapla (resimdeki ölçek)
        if (genelToplam >= 82) harfNotu = 'AA';
        else if (genelToplam >= 74) harfNotu = 'BA';
        else if (genelToplam >= 65) harfNotu = 'BB';
        else if (genelToplam >= 58) harfNotu = 'CB';
        else if (genelToplam >= 50) harfNotu = 'CC';
        else if (genelToplam >= 40) harfNotu = 'DC';
        else if (genelToplam >= 35) harfNotu = 'DD';
        else if (genelToplam >= 25) harfNotu = 'FD';
        else harfNotu = 'FF';
    }
    
    document.getElementById('genelToplam').textContent = genelToplam.toFixed(2);
    document.getElementById('normalDonemHarfNotu').textContent = harfNotu;
}

// Normal dönem kaydet
async function normalDonemKaydet(event) {
    event.preventDefault();
    
    const form = event.target;
    const formData = new FormData(form);
    
    const data = {
        vize_notu: parseFloat(formData.get('vize_notu') || 0),
        vize_odev_puani: formData.get('vize_odev_puani') ? parseFloat(formData.get('vize_odev_puani')) : null,
        vize_odev_yuzdesi: parseFloat(formData.get('vize_odev_yuzdesi') || 0),
        final_notu: parseFloat(formData.get('final_notu') || 0),
        final_odev_puani: formData.get('final_odev_puani') ? parseFloat(formData.get('final_odev_puani')) : null,
        final_odev_yuzdesi: parseFloat(formData.get('final_odev_yuzdesi') || 0),
        devamsizlik_durumu: formData.get('devamsizlik_durumu') === 'on',
        butunleme_notu: formData.get('butunleme_notu') ? parseFloat(formData.get('butunleme_notu')) : null,
        butunleme_odev_puani: formData.get('butunleme_odev_puani') ? parseFloat(formData.get('butunleme_odev_puani')) : null,
        butunleme_odev_yuzdesi: parseFloat(formData.get('butunleme_odev_yuzdesi') || 0)
    };
    
    const sonuc = await apiCall(`/api/normal-donem/${ogrenciId}`, 'POST', data);
    
    if (sonuc.basarili) {
        bildirimGoster('Normal dönem notları başarıyla kaydedildi!', 'success');
        normalDonemGoster(sonuc.degerlendirme);
    } else {
        bildirimGoster('Hata: ' + sonuc.hata, 'error');
    }
}

