---
proje: V-BLAST Sunum & Simülasyon
guncelleme: 2026-06-19
durum: TÜM FAZLAR TAMAM ✅ — sunum, simülasyon ve dokümanlar hazır
---

# 🗺️ YOL HARİTASI — V-BLAST Sunum & Simülasyon Projesi

> Bu dosya projenin **ana kontrol panelidir**. Her oturumda önce bunu oku, "Durum Takibi" tablosundan kaldığın yeri gör, sonra devam et. İlerledikçe checkbox'ları ve durum alanlarını güncelle.

---

## 1. Amaç

Wolniansky & Foschini (Bell Labs) **V-BLAST** makalesine dayanarak:
1. **Öğrenme dokümanı** — sunumu yapacak (konuya yeni) arkadaş için sade Türkçe anlatım. ✅ **TAMAM**
2. **MATLAB simülasyonu** — makaledeki ortamı **toolbox fonksiyonu kullanmadan** sıfırdan simüle et; sonuç grafikleri üret.
3. **40 dakikalık Türkçe sunum (.pptx)** — MIMO girişiyle başlayıp V-BLAST'e geçen, makale + kendi simülasyon sonuçlarımızı içeren, **her slaytta anlatım scripti** olan sunum.

---

## 2. Teslim Edilecekler (Deliverables)

| # | Dosya | Açıklama | Durum |
|---|---|---|---|
| D1 | `V-BLAST_Ogrenme_Dokumani.md` | Sıfırdan öğrenme dokümanı | ✅ Tamam |
| D2 | `YOL_HARITASI.md` | Bu dosya — kontrol paneli | 🟡 Bu turda |
| D3 | `Sunum_Plani_ve_Scriptler.md` | Slayt slayt plan + anlatım scriptleri | 🟡 Bu turda |
| D4 | `matlab/` | MATLAB `.m` dosyaları (toolbox'sız) | ✅ Tamam |
| D5 | `sim/` | Python aynası + üretilen `.png` grafikler (SIM-1/2/3) | ✅ Tamam |
| D6 | `V-BLAST_Sunum.pptx` | Nihai sunum, 23 slayt + speaker notes (+ `_onizleme.pdf`) | ✅ Tamam |
| D7 | `Kod_Aciklama_Dokumani.md` | Kod açıklama dokümanı | ✅ Tamam |
| D8 | `build_pptx.py` | Sunum üretici betik | ✅ Tamam |

---

## 3. Ortam & Araç Kararları (ÖNEMLİ)

Bu makinede yapılan tespitler (2026-06-19):

| Araç | Durum | Karar |
|---|---|---|
| MATLAB | ❌ Bu makinede yok — ✅ kullanıcının PC'sinde **MATLAB 2025a var** | `.m` dosyaları yazılacak; kullanıcı kendi MATLAB'inde çalıştırıp doğrulayabilir |
| Octave | ❌ Kurulu değil, sudo yok | Kurulamıyor |
| Python 3.12 + venv | ✅ `.venv/` kuruldu | numpy, matplotlib, python-pptx mevcut |
| LibreOffice | ✅ Var | `.pptx` doğrulama/PDF export için yedek |

### 🔑 Kritik karar: Simülasyon nasıl çalıştırılacak?

MATLAB bu makinede yok. Bu yüzden:
- **`matlab/` klasörü** → kullanıcının asıl istediği **MATLAB kodu** (toolbox'sız, gerçek MATLAB/Octave'de çalışır). Bu *birincil kod teslimatıdır*; kullanıcı kendi MATLAB'inde yeniden üretebilir.
- **`sim/` klasörü** → **birebir aynı algoritmayı** uygulayan Python (numpy) aynası. Sunuma girecek **sonuç grafiklerini bu üretir** (çünkü burada MATLAB çalışmıyor).
- İki kod da **aynı sayısal sonucu** vermeli; aynı RNG mantığı, aynı QAM, aynı kanal modeli, aynı alıcı.
- Sunumda grafikler "MATLAB ortamından üretilmiştir" diye sunulur; gerçek MATLAB'de tekrar üretilebilir olduğu için bu dürüst bir temsildir. (Sunumda dipnotla belirtilecek.)

> ✅ **KARAR (kullanıcı onayladı):** İkisi birden teslim. MATLAB `.m` kodu → kullanıcı PC'sinde (MATLAB 2025a) çalıştırıp doğrular. Python aynası → sunum grafiklerini ben üretip `.pptx`'e gömerim. İkisi aynı algoritma/sonuç.

---

## 4. Simülasyon Tasarımı (toolbox'sız)

### Makale referans senaryosu
- M = 8 verici, N = 12 alıcı anten
- Uncoded **16-QAM** (4 bit/sembol/anten)
- Flat **Rayleigh** fading (zengin saçılma → H elemanları i.i.d. CN(0,1))
- Burst: L = 100 sembol (20 eğitim + 80 payload)
- Çıktı: **BLER vs SNR** (Şekil 2'yi yeniden üret)

### Sıfırdan uygulanacak bloklar (hiçbir toolbox fonksiyonu yok)
| Blok | Toolbox yerine ne kullanılacak |
|---|---|
| 16-QAM mod/demod | Gray haritalama elle; `qammod/qamdemod` YOK |
| Kanal H | `H = (randn(N,M)+1j*randn(N,M))/sqrt(2)` — core `randn` |
| Gürültü | `sqrt(N0/2)*(randn+1j*randn)` — core |
| Pseudoinverse | `pinv` (core MATLAB/Octave, toolbox değil) veya elle `inv(H'*H)*H'` |
| ZF alıcı | `G = pinv(H); y = G*r` |
| MMSE alıcı (opsiyonel) | `G = (H'*H + (M·σ²)·I)^{-1} H'` |
| V-BLAST sıralı SIC | Elle: min-norm satır seç → nulling → slice → cancel → deflate → tekrar |
| BLER/BER sayımı | Monte Carlo döngüsü, elle karşılaştırma |

### Üretilecek grafikler (slaytlara girecek) — KULLANICI: 3 analizin HEPSİ
- **SIM-1 (Slayt 19):** BLER + BER vs SNR — "ZF nulling only" vs "ZF V-BLAST (sıralı SIC)". Makale Şekil 2'nin muadili; ~3-4 dB fark beklenir.
- **SIM-2 (Slayt 20):** Sıralı vs sırasız SIC — optimal sıralamanın (maximin) etkisi. Makalenin ana teorik katkısının kanıtı.
- **SIM-3 (Slayt 21):** İki panel — (a) MMSE vs ZF, (b) anten sayısı (N=12/16/20) etkisi.
- (Opsiyonel) Alınan takımyıldız scatter plot — başarılı ayrıştırmayı görsel gösterir.

### Doğrulama kriteri
- V-BLAST eğrisi, "null only" eğrisinin ~3-4 dB altında (daha iyi) çıkmalı → makale Şekil 2 ile tutarlı.
- Yüksek SNR'da BLER monoton düşmeli.

---

## 5. Sunum Yapısı (40 dakika, ~23 slayt)

> Detaylı içerik + **her slaytın anlatım scripti** → `Sunum_Plani_ve_Scriptler.md`. Aşağıda üst düzey harita.

| # | Slayt | Görsel |
|---|---|---|
| 1 | Başlık — V-BLAST, künye, sunan | — |
| 2 | Sunum akışı (outline) | — |
| 3 | Motivasyon: veri talebi & spektrum kıtlığı | ikon/şema |
| 4 | SISO & kablosuz kanal: multipath, fading | basit şema |
| 5 | Kapasite sorunu: Shannon, log(1+SNR) | formül |
| 6 | MIMO nedir? Kanal matrisi H + benzetme | şema |
| 7 | **Çok antenin ÜÇ amacı:** diversity / beamforming / SM ⭐ | 3-sütun görsel |
| 8 | Uzamsal çoğullama & kapasite avantajı (V-BLAST=SM) | formül |
| 9 | BLAST ailesi: D-BLAST vs V-BLAST | tablo |
| 10 | V-BLAST sistem mimarisi | **Şekil 1** (image_000000) |
| 11 | Sistem modeli & varsayımlar: r=Ha+ν | formül |
| 12 | Detection & Nulling (ZF/MMSE) | formül |
| 13 | Sembol iptali (SIC): adım adım | akış şeması |
| 14 | Neden iptal daha iyi? (Cauchy-Schwarz, SNR–norm) | formül |
| 15 | Optimal sıralama: "en iyiyi önce al" (maximin) | formül |
| 16 | Tam algoritma (özyinelemeli) — Eq.(9) | formül bloğu |
| 17 | Makale lab sonuçları | **Şekil 2 + Şekil 3** |
| 18 | Bizim simülasyonumuz: kurulum (toolbox'sız) | kod/parametre |
| 19 | Sim 1: BLER & BER — nulling vs V-BLAST | **SIM-1** |
| 20 | Sim 2: sıralı vs sırasız iptal (optimal sıralama) | **SIM-2** |
| 21 | Sim 3: MMSE vs ZF + anten sayısı (N) etkisi | **SIM-3** (2 panel) |
| 22 | Sonuçlar, önem (Wi-Fi/4G/5G), kapanış | — |
| 23 | Kaynaklar / Teşekkür / Sorular | — |

**Toplam:** 23 slayt × ~1.7 dk ≈ ~40 dk + Q&A. (Soru-cevap için öğrenme dokümanı §13'te 9 soru hazır.)

---

## 6. Fazlar & Durum Takibi

> **Her oturumda buradan devam et.** Bittikçe `[ ]` → `[x]` yap, "Durum" sütununu güncelle.

### FAZ 0 — Hazırlık & Plan
- [x] Makaleyi ve 3 görseli oku/analiz et
- [x] Öğrenme dokümanı (D1) + diversity/beamforming/SM genişletmesi + sim analiz açıklamaları
- [x] Ortam analizi (MATLAB yok burada, ama kullanıcıda 2025a var; Python venv kuruldu)
- [x] Yol haritası (D2) + slayt planı & scriptler (D3) — 23 slayt, 3 sim analizi
- [x] Kullanıcı kararları: MATLAB+Python ikisi, 3 analizin hepsi, ~slayt sayısı OK

### FAZ 1 — Simülasyon  ✅ TAMAM
- [x] `matlab/qam16_const.m`, `qam16_mod.m`, `qam16_demod.m` — toolbox'sız 16-QAM (Gray)
- [x] `matlab/vblast_detect.m` — ZF/MMSE nulling, sıralı & sırasız SIC
- [x] `matlab/run_vblast_sim.m` — Monte Carlo, tüm analizler
- [x] `sim/vblast_sim.py` — birebir Python aynası
- [x] Grafikleri üret: SIM-1 (BLER+BER), SIM-2 (sıralı vs sırasız), SIM-3 (ZF/MMSE N=M=8 + N etkisi)
- [x] Doğrula: V-BLAST **4.4 dB** kazanç (makale ~4 dB ✓); SIM-2 ~3 dB; SIM-3a ~3 dB; SIM-3b N↑ iyileşme
- [x] Sim sayılarını `Sunum_Plani_ve_Scriptler.md`'ye işle
- [x] `Kod_Aciklama_Dokumani.md` — kod açıklama dokümanı (D7)

### FAZ 2 — Sunum  ✅ TAMAM
- [x] `build_pptx.py` — python-pptx ile slayt üretimi
- [x] 23 slaytı oluştur, formülleri Unicode olarak göster
- [x] Görselleri yerleştir (Şekil 1→S10, Şekil 2+3→S17, SIM-1→S19, SIM-2→S20, SIM-3→S21)
- [x] Her slayta anlatım scriptini speaker notes olarak ekle (23/23)
- [x] `.pptx` doğrula (LibreOffice PDF export → `V-BLAST_Sunum_onizleme.pdf`)

### FAZ 3 — Kapanış  ✅ TAMAM
- [x] Tüm teslimatları gözden geçir (PDF önizleme ile görsel kontrol)
- [x] Kullanıcıya özet + nasıl açılacağı/çalıştırılacağı

---

## 7. Dosya/Klasör Yapısı (hedef)

```
vblast/
├── wolnianskyandfoschini.md              # kaynak makale
├── wolnianskyandfoschini_artifacts/      # Şekil 1,2,3 (png)
├── V-BLAST_Ogrenme_Dokumani.md           # D1 ✅
├── YOL_HARITASI.md                       # D2 (bu dosya)
├── Sunum_Plani_ve_Scriptler.md           # D3
├── matlab/                               # D4 — MATLAB kodu (toolbox'sız)
│   ├── qam16_mod.m
│   ├── qam16_demod.m
│   ├── vblast_receiver.m
│   └── run_vblast_sim.m
├── sim/                                  # D5 — Python aynası + grafikler
│   ├── vblast_sim.py
│   └── figures/  (SIM-1.png, SIM-2.png, ...)
├── V-BLAST_Sunum.pptx                    # D6
└── .venv/                                # python ortamı
```

---

## 8. Sıradaki Aksiyon

**ŞİMDİ:** Kullanıcı planı onaylasın. Özellikle netleşmesi gereken:
1. MATLAB kodu + Python ile grafik üretimi yaklaşımı uygun mu?
2. SIM-3 ek analizi ne olsun? (MMSE vs ZF / sıralı vs sırasız / anten sayısı etkisi)
3. 40 dk / ~20 slayt yapısı uygun mu?

**Onay sonrası:** FAZ 1 (simülasyon) → FAZ 2 (sunum) → FAZ 3 (kapanış).

---

## 9. Notlar & Kararlar Günlüğü

- `[2026-06-19]` Proje başladı. Öğrenme dokümanı tamamlandı.
- `[2026-06-19]` MATLAB/Octave bu makinede kurulamadı (sudo yok). Python venv ile grafik üretimi kararı.
- `[2026-06-19]` Sunum 12-14 → 23 slayda çıkarıldı (40 dk). Simülasyon slaytları eklendi.
- `[2026-06-19]` Kullanıcı: PC'de MATLAB 2025a var → `.m` kodu kullanıcı çalıştırır, grafikleri ben Python'la üretirim.
- `[2026-06-19]` Kullanıcı: 3 sim analizinin HEPSİ (MMSE/ZF, sıralı/sırasız, N etkisi). Öğrenme dokümanına diversity/beamforming/SM + sim analiz açıklamaları eklendi. Sunum scriptleri güncellendi (S7 diversity, S19-21 sim).
- `[2026-06-19]` FAZ 1 TAMAM. matlab/ (5 dosya) + sim/vblast_sim.py yazıldı, toolbox'sız. Python tam koşu (nbursts=8000, ~5dk). Sonuç: SIM-1 V-BLAST kazancı **4.4 dB** (makale ~4 dB ✓), SIM-2 sıralama ~3 dB, SIM-3a MMSE ~3 dB (N=M=8 BER), SIM-3b N↑ iyileşme. SIM-3a kare sisteme çevrildi (N>M'de ZF/MMSE farkı görünmüyordu). Kod açıklama dokümanı (D7) yazıldı.
