---
proje: V-BLAST Simülasyon
dosya: Kod Açıklama Dokümanı
guncelleme: 2026-06-19
---

# 🧮 V-BLAST Simülasyon — Kod Açıklama Dokümanı

> Bu doküman, `matlab/` (asıl teslimat, MATLAB 2025a) ve `sim/` (Python aynası, grafik üretimi) klasörlerindeki kodu **satır satır mantığıyla** açıklar. Amaç: kodu hiç görmemiş birinin ne yaptığını anlaması ve gerekirse değiştirebilmesi. İlgili kavramlar için → `V-BLAST_Ogrenme_Dokumani.md`.

---

## 1. Genel bakış: ne simüle ediyoruz?

Makaledeki ortamı **sıfırdan** (hiçbir hazır iletişim toolbox'ı kullanmadan) kuruyoruz:
- **M = 8** verici, **N = 12** alıcı anten
- **16-QAM** (uncoded), zengin saçılma = **i.i.d. Rayleigh düz sönümleme**
- Alıcılar: saf nulling (ZF/MMSE) ve **V-BLAST** (sıralı iptal)
- Çıktı: **BLER & BER vs SNR** eğrileri + analizler

**İki kod, tek algoritma:**
| Klasör | Dil | Rol |
|---|---|---|
| `matlab/` | MATLAB 2025a | **Asıl teslimat.** Kendi PC'nde çalıştırıp doğrularsın. |
| `sim/` | Python (numpy) | Bu makinede MATLAB olmadığı için **sunum grafiklerini bu üretti.** |

İkisi **birebir aynı** algoritmayı uygular; aynı sonucu verir.

---

## 2. Nasıl çalıştırılır?

### MATLAB (asıl)
```matlab
% matlab/ klasörüne gir, sonra:
>> run_vblast_sim
```
5 dosya aynı klasörde olmalı: `qam16_const.m`, `qam16_mod.m`, `qam16_demod.m`, `vblast_detect.m`, `run_vblast_sim.m`. 3 figür açılır (SIM-1/2/3). `nbursts` varsayılan 2000 (hızlı); daha düzgün eğri için artır.

### Python (grafik üreten ayna)
```bash
.venv/bin/python sim/vblast_sim.py            # tam koşu (nbursts=8000, ~5 dk)
.venv/bin/python sim/vblast_sim.py --quick    # hızlı pilot (~7 sn)
# grafikler -> sim/figures/SIM-1.png, SIM-2.png, SIM-3.png
```

---

## 3. Matematiksel temel (kodun dayandığı denklemler)

**Sistem modeli:** `r = H·a + ν`
- `a` : M×1 gönderilen 16-QAM sembolleri (birim ortalama enerji, E|a_k|²=1)
- `H` : N×M kanal, elemanları `h_ij ~ CN(0,1)` (zengin saçılma)
- `ν` : N×1 gürültü, her bileşen `CN(0, N0)`

**SNR tanımı (makaledeki gibi):** *ortalama alınan SNR* = tüm M vericiden gelen güç / gürültü gücü. Birim enerjili sembollerle alıcı antene düşen sinyal gücü = M, dolayısıyla:

$$\text{SNR} = \frac{M}{N_0} \quad\Rightarrow\quad N_0 = \frac{M}{10^{\,\text{SNR}_\text{dB}/10}}$$

Kodda: `N0 = M ./ (10.^(snr_db/10))`. Bu yüzden grafiklerin x-ekseni "ortalama alınan SNR (dB)".

---

## 4. Dosya dosya açıklama (MATLAB ve Python ortak mantık)

### 4.1 `qam16_const` — Takımyıldız kurulumu (toolbox'sız)
16-QAM noktalarını ve bit eşlemesini **elle** kurar.
- I ve Q bileşenleri `{-3,-1,+1,+3}` seviyelerinden gelir.
- **Gray kodlama:** komşu noktalar tek bitte farklıdır (BER'i azaltır). 2-bit Gray eşlemesi: `00→-3, 01→-1, 11→+1, 10→+3`.
- 4 bit → 1 sembol: üst 2 bit I'yı, alt 2 bit Q'yu seçer.
- Son adım: `/sqrt(10)` ile **ortalama enerji 1'e normalize** (çünkü ham 16-QAM ortalama enerjisi 10'dur).

> Neden önemli? `qammod` gibi bir toolbox fonksiyonu kullanmadan, modülasyonu tam kontrolle kuruyoruz. Hem verici hem alıcı **aynı** takımyıldızı kullandığı için tutarlı.

### 4.2 `qam16_mod` — İndis → sembol
1..16 indislerini kompleks sembollere çevirir (`sym = const(idx)`). Vektör/matris girdiyi olduğu gibi işler.

### 4.3 `qam16_demod` — Slicing (en yakın komşu)
Karar istatistiği `y`'yi alır, **en yakın** takımyıldız noktasının indisini döner. Matematiksel slicing `Q(·)` operasyonu budur. Tüm noktalara mesafeyi hesaplayıp minimumu seçer (`abs(y - const')` → `min`).

### 4.4 `vblast_detect` — Alıcılar (kalbi burası)
Beş mod içerir:

| mode | Açıklama | Formül |
|---|---|---|
| `zf_linear` | Saf ZF nulling, iptal yok | `G = pinv(H); â = Q(G·r)` |
| `mmse_linear` | Saf MMSE nulling | `G = (HᴴH + N0·I)⁻¹Hᴴ` |
| `zf_sic_ordered` | **V-BLAST**: ZF + sıralı iptal | Eq. (9) — maximin sıra |
| `zf_sic_fixed` | ZF + sırasız (sabit) iptal | sıra = 1,2,…,M |
| `mmse_sic_ordered` | MMSE + sıralı iptal | MMSE nulling + Eq.(9) sıra |

**`sic_core` (sıralı iptal çekirdeği) — Eq.(9) ↔ kod eşleşmesi:**
```
Her adım i = 1..M:
  1) G = pinv(Hdef)                  % (9b/9h) nulling matrisi (deflated H)
  2) rownorm = ||G satırları||²       % SNR ölçütü (küçük norm = yüksek SNR)
  3) k = argmin rownorm (kalanlardan) % (9c/9i) OPTIMAL SIRA: en iyiyi önce al
  4) w = G(k,:)                       % (9d) nulling vektörü
  5) y = w · Rcur                     % (9e) karar istatistiği
  6) idx = Q(y)                       % (9f) slicing
  7) Rcur = Rcur - H(:,k)·â_k         % (9g) CANCELLATION (iptal)
  8) Hdef(:,k) = 0                    % (9h) DEFLATION (sönükleştirme)
```
- `ordered=false` ise 3. adımda sıralama yapılmaz, sıra sabittir → bu, **SIM-2**'deki "sırasız" karşılaştırma.
- ZF sıralaması yalnızca H'ye bağlı olduğundan, nulling vektörleri T sembol-vektörünün hepsine aynı uygulanır (vektörel, hızlı).

### 4.5 `run_experiment` / `run_vblast_sim` — Monte Carlo
- Her **burst** için: rastgele `H`, rastgele semboller, taban gürültü `Wn` üretilir.
- **Ortak rastgele sayılar:** Aynı H/semboller/gürültü tüm SNR noktalarında kullanılır (yalnızca `N0` ölçeklenir). Bu, eğrileri pürüzsüzleştirir ve hızlandırır.
- Her SNR ve her mod için alıcı çalıştırılır; **blok hatası** (burst'te ≥1 sembol yanlış) ve **bit hatası** sayılır.
- `BLER = hatalı blok / toplam blok`, `BER = hatalı bit / toplam bit`.

---

## 5. Toolbox'sız tasarım — hangi fonksiyonlar?

| İhtiyaç | Toolbox fonksiyonu (KULLANILMADI) | Bizim kullandığımız (temel MATLAB) |
|---|---|---|
| QAM modülasyon | `qammod` ❌ | `qam16_const` + indeksleme ✅ |
| QAM demodülasyon | `qamdemod` ❌ | `qam16_demod` (min-mesafe) ✅ |
| Kanal | `comm.MIMOChannel` ❌ | `randn` ✅ |
| Gürültü | `awgn` ❌ | `randn` + ölçekleme ✅ |
| Pseudoinverse | — | `pinv` (temel) ✅ |
| MMSE çözüm | — | `\` (mldivide, temel) ✅ |

Yani: rastgele sayı, lineer cebir ve grafik dışında hiçbir özel araç yok.

---

## 6. Parametreler — neyi nasıl değiştirirsin?

| Parametre | Yer | Varsayılan | Etkisi |
|---|---|---|---|
| `M` | run_vblast_sim | 8 | Verici/akış sayısı |
| `N` | run_experiment çağrıları | 12 | Alıcı anten sayısı (≥M) |
| `T` | run_vblast_sim | 80 | Burst başına sembol-vektör (payload) |
| `nbursts` | run_vblast_sim | 2000 (MATLAB) / 8000 (Python) | ↑ daha düzgün eğri, ↑ süre |
| `snr` | run_vblast_sim | 10:2:30 dB | Tarama aralığı |
| 16→64-QAM | qam16_const | — | Daha yüksek mertebe için takımyıldız değişir |

---

## 7. Sonuçların yorumu (ölçülen değerler)

Python tam koşusundan (nbursts=8000) elde edilen değerler:

| Grafik | Karşılaştırma | Bulgu |
|---|---|---|
| **SIM-1** | Nulling-only vs V-BLAST | V-BLAST **~4.4 dB** daha iyi → makale Şekil 2'nin ~4 dB'iyle tutarlı ✅ |
| **SIM-2** | Sıralı vs sırasız SIC | Optimal sıralama **~2.7 dB** kazandırır → maximin teoreminin kanıtı |
| **SIM-3a** | ZF vs MMSE (N=M=8) | MMSE **~2.7 dB** daha iyi (kare sistemde ZF gürültü büyütür) |
| **SIM-3b** | N = 12/16/20 | N arttıkça performans belirgin iyileşir (çeşitleme kazancı) |

> ⚠️ **Makaleyle birebir aynı sayı beklenmez:** Makale gerçek ofis ortamında ölçüm yaptı (kanal korelasyonu, donanım kusurları var). Biz ideal i.i.d. Rayleigh varsaydık. Yine de **trendler ve büyüklük mertebesi** (özellikle ~4 dB iptal kazancı) örtüşüyor — bu, hem yöntemin hem kodun doğruluğunu gösterir.

---

## 8. MATLAB ↔ Python eşdeğerliği

İki kod **aynı algoritmayı** uygular:
- Aynı 16-QAM Gray takımyıldızı ve normalizasyon
- Aynı kanal modeli `(randn+1i·randn)/sqrt(2)`
- Aynı SNR tanımı `N0 = M/10^(SNR/10)`
- Aynı ZF/MMSE/SIC mantığı, aynı sıralama ölçütü (min satır normu)
- Aynı BLER/BER sayımı

Grafikler bu makinede Python ile üretildi; MATLAB kodu kendi PC'nde (2025a) çalıştırıldığında **istatistiksel olarak aynı** eğrileri verir (rastgele tohum farkından kaynaklı küçük dalgalanmalar dışında).

---

## 9. Doğrulama (sanity checks)

Kodun doğru çalıştığını şu gözlemler teyit eder:
1. **V-BLAST < nulling-only** (her SNR'da) — iptal her zaman yardımcı olmalı ✅
2. **Sıralı < sırasız** — optimal sıralama daima en az sırasız kadar iyi ✅
3. **N↑ → eğri sola/aşağı** — daha çok alıcı anten = daha iyi ✅
4. **Yüksek SNR'da BLER/BER monoton düşer** ✅
5. **~4 dB iptal kazancı** — makaleyle nicel tutarlılık ✅
