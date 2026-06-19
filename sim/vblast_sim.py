#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
V-BLAST Monte-Carlo simülasyonu (TOOLBOX'SIZ, sıfırdan).

Bu Python betiği, `matlab/` klasöründeki MATLAB kodunun BİREBİR AYNISIDIR;
sadece sunuma girecek grafikleri burada (numpy/matplotlib) üretiyoruz çünkü
bu makinede MATLAB yok. Algoritma, parametreler ve sonuçlar aynıdır.

Üretilen grafikler:
  SIM-1 : BLER & BER vs SNR  -> ZF nulling-only  vs  ZF V-BLAST (sıralı SIC)
  SIM-2 : BLER vs SNR        -> sıralı SIC  vs  sırasız (sabit) SIC
  SIM-3 : (a) MMSE vs ZF V-BLAST   (b) Alıcı anten sayısı N etkisi

Kanal: zengin saçılma -> H elemanları i.i.d. CN(0,1) (Rayleigh düz sönümleme).
Modülasyon: 16-QAM (Gray), birim ortalama enerjiye normalize.
SNR tanımı (makaledeki gibi): ortalama alınan SNR = (tüm M vericiden gelen
güç) / (gürültü gücü). Birim enerjili sembollerle -> N0 = M / 10^(SNR/10).
"""

import numpy as np
import argparse
import os

# ----------------------------------------------------------------------------
# 1) 16-QAM Gray takımyıldızı (toolbox yok — elle kuruluyor)
# ----------------------------------------------------------------------------
def make_qam16():
    """Birim ortalama enerjili, Gray-kodlu 16-QAM.
    Dönüş: const (16,) kompleks noktalar; bits (16,4) her noktanın bitleri."""
    # 2-bit Gray -> seviye eşlemesi: 00->-3, 01->-1, 11->+1, 10->+3
    g2l = {0b00: -3, 0b01: -1, 0b11: +1, 0b10: +3}
    const = np.zeros(16, dtype=complex)
    bits = np.zeros((16, 4), dtype=int)
    for s in range(16):
        b3, b2, b1, b0 = (s >> 3) & 1, (s >> 2) & 1, (s >> 1) & 1, s & 1
        I = g2l[(b3 << 1) | b2]     # I bileşeni üst 2 bitten
        Q = g2l[(b1 << 1) | b0]     # Q bileşeni alt 2 bitten
        const[s] = I + 1j * Q
        bits[s] = (b3, b2, b1, b0)
    const = const / np.sqrt(10.0)   # ortalama enerji 10 -> 1'e normalize
    return const, bits


def slice_qam16(y, const):
    """En yakın komşu dilimleme (slicing). y: (...,) kompleks dizi.
    Dönüş: idx (en yakın sembol indeksi), val (o sembolün değeri)."""
    d = np.abs(y[..., None] - const[None, :])   # mesafeler
    idx = np.argmin(d, axis=-1)
    return idx, const[idx]


# ----------------------------------------------------------------------------
# 2) Alıcılar (hepsi sıfırdan)
# ----------------------------------------------------------------------------
def detect_zf_linear(H, R, const):
    """Saf ZF nulling (iptal YOK). G = pinv(H), tüm akışları tek seferde çöz."""
    G = np.linalg.pinv(H)            # (M,N)
    Y = G @ R                        # (M,T)
    idx, _ = slice_qam16(Y, const)
    return idx                       # (M,T) tahmini sembol indeksleri


def detect_mmse_linear(H, R, const, N0):
    """Saf MMSE nulling (iptal YOK). W = (H^H H + N0 I)^{-1} H^H (birim enerji)."""
    M = H.shape[1]
    A = H.conj().T @ H + N0 * np.eye(M)
    G = np.linalg.solve(A, H.conj().T)   # (M,N)
    Y = G @ R
    idx, _ = slice_qam16(Y, const)
    return idx


def detect_sic(H, R, const, N0, criterion='zf', ordered=True):
    """Sıralı iptal (SIC) alıcısı.
    criterion : 'zf' veya 'mmse'
    ordered   : True -> her adımda en küçük normlu satır (V-BLAST optimal sırası)
                False -> sabit doğal sıra (1,2,...,M)  [karşılaştırma için]
    Not: ZF sıralaması yalnızca H'ye bağlıdır; bu yüzden nulling vektörlerini
    bir kez hesaplayıp T sembol-vektörünün hepsine uyguluyoruz (verimli)."""
    N, M = H.shape
    T = R.shape[1]
    Rcur = R.copy()
    est_idx = np.zeros((M, T), dtype=int)
    remaining = list(range(M))
    Hdef = H.copy().astype(complex)

    for _ in range(M):
        if criterion == 'zf':
            G = np.linalg.pinv(Hdef)                       # (M,N)
        else:  # mmse
            A = Hdef.conj().T @ Hdef + N0 * np.eye(M)
            G = np.linalg.solve(A, Hdef.conj().T)          # (M,N)

        rownorm = np.sum(np.abs(G) ** 2, axis=1)           # satır normları
        if ordered:
            k = min(remaining, key=lambda j: rownorm[j])   # en güçlü akış (min norm)
        else:
            k = remaining[0]                               # doğal sıra

        w = G[k, :]                                        # nulling vektörü (1,N)
        y = w @ Rcur                                       # (T,)
        idx, val = slice_qam16(y, const)
        est_idx[k, :] = idx

        Rcur = Rcur - np.outer(H[:, k], val)               # iptal (cancellation)
        remaining.remove(k)
        Hdef[:, k] = 0                                     # deflation (sönükleştirme)

    return est_idx


# ----------------------------------------------------------------------------
# 3) Tek bir deney: verilen modlar için BLER & BER vs SNR
# ----------------------------------------------------------------------------
def run_experiment(M, N, snr_db, modes, nbursts, T, seed=12345):
    """modes: ör. ['zf_linear','zf_sic_ordered','zf_sic_fixed','mmse_sic_ordered']
    Dönüş: results[mode] = {'bler':..., 'ber':...} (snr_db ile aynı boyda)."""
    rng = np.random.default_rng(seed)
    const, bits = make_qam16()
    nsnr = len(snr_db)
    N0_list = M / (10.0 ** (np.asarray(snr_db) / 10.0))

    # sayaçlar
    block_err = {m: np.zeros(nsnr) for m in modes}
    bit_err = {m: np.zeros(nsnr) for m in modes}
    blocks_tot = np.zeros(nsnr)
    bits_tot = np.zeros(nsnr)

    for _ in range(nbursts):
        # --- burst başına: kanal, semboller, taban gürültü (SNR'lar arası ortak) ---
        H = (rng.standard_normal((N, M)) + 1j * rng.standard_normal((N, M))) / np.sqrt(2.0)
        tx_idx = rng.integers(0, 16, size=(M, T))
        A = const[tx_idx]                                  # (M,T) gönderilen semboller
        Wn = (rng.standard_normal((N, T)) + 1j * rng.standard_normal((N, T))) / np.sqrt(2.0)
        tx_bits = bits[tx_idx]                             # (M,T,4)

        HA = H @ A                                         # (N,T) gürültüsüz alınan

        for si, N0 in enumerate(N0_list):
            R = HA + np.sqrt(N0) * Wn                      # alınan vektörler

            for m in modes:
                if m == 'zf_linear':
                    est = detect_zf_linear(H, R, const)
                elif m == 'mmse_linear':
                    est = detect_mmse_linear(H, R, const, N0)
                elif m == 'zf_sic_ordered':
                    est = detect_sic(H, R, const, N0, 'zf', ordered=True)
                elif m == 'zf_sic_fixed':
                    est = detect_sic(H, R, const, N0, 'zf', ordered=False)
                elif m == 'mmse_sic_ordered':
                    est = detect_sic(H, R, const, N0, 'mmse', ordered=True)
                else:
                    raise ValueError(m)

                sym_wrong = (est != tx_idx)
                if sym_wrong.any():
                    block_err[m][si] += 1
                est_bits = bits[est]
                bit_err[m][si] += np.sum(est_bits != tx_bits)

            blocks_tot[si] += 1
            bits_tot[si] += M * T * 4

    results = {}
    for m in modes:
        results[m] = {
            'bler': block_err[m] / np.maximum(blocks_tot, 1),
            'ber': bit_err[m] / np.maximum(bits_tot, 1),
        }
    return results


# ----------------------------------------------------------------------------
# 4) Grafikler
# ----------------------------------------------------------------------------
def _mask(x, f=1e-12):
    """Ölçülemeyen (0) noktaları NaN yap; log eksende çizilmez (dürüst)."""
    x = np.asarray(x, dtype=float).copy()
    x[x <= f] = np.nan
    return x


YLIM = (3e-4, 1.3)   # tüm BLER/BER grafiklerinde ortak y-ekseni


def plot_sim1(snr, res, outdir):
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(1, 2, figsize=(11, 4.3))
    # BLER
    ax[0].semilogy(snr, _mask(res['zf_linear']['bler']), 's-', color='#c0392b',
                   label='Sadece Nulling (ZF)', lw=2, ms=6)
    ax[0].semilogy(snr, _mask(res['zf_sic_ordered']['bler']), 'o-', color='#1a1a1a',
                   label='V-BLAST (sıralı SIC)', lw=2, ms=6)
    ax[0].set_xlabel('Ortalama alınan SNR (dB)'); ax[0].set_ylabel('BLER (blok hata oranı)')
    ax[0].set_title('BLER:  Nulling-only  vs  V-BLAST'); ax[0].grid(True, which='both', alpha=0.3)
    ax[0].set_ylim(*YLIM); ax[0].legend()
    # BER
    ax[1].semilogy(snr, _mask(res['zf_linear']['ber']), 's-', color='#c0392b',
                   label='Sadece Nulling (ZF)', lw=2, ms=6)
    ax[1].semilogy(snr, _mask(res['zf_sic_ordered']['ber']), 'o-', color='#1a1a1a',
                   label='V-BLAST (sıralı SIC)', lw=2, ms=6)
    ax[1].set_xlabel('Ortalama alınan SNR (dB)'); ax[1].set_ylabel('BER (bit hata oranı)')
    ax[1].set_title('BER:  Nulling-only  vs  V-BLAST'); ax[1].grid(True, which='both', alpha=0.3)
    ax[1].set_ylim(*YLIM); ax[1].legend()
    fig.suptitle('SIM-1 · M=8, N=12, 16-QAM · Nulling vs V-BLAST', fontweight='bold')
    fig.tight_layout()
    fig.savefig(os.path.join(outdir, 'SIM-1.png'), dpi=140)
    plt.close(fig)


def plot_sim2(snr, res, outdir):
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.semilogy(snr, _mask(res['zf_sic_fixed']['bler']), '^-', color='#e67e22',
                label='Sırasız SIC (sabit sıra)', lw=2, ms=7)
    ax.semilogy(snr, _mask(res['zf_sic_ordered']['bler']), 'o-', color='#1a1a1a',
                label='Sıralı SIC (V-BLAST, maximin)', lw=2, ms=7)
    ax.set_xlabel('Ortalama alınan SNR (dB)'); ax.set_ylabel('BLER (blok hata oranı)')
    ax.set_title('SIM-2 · Sıralamanın etkisi (M=8, N=12, 16-QAM)', fontweight='bold')
    ax.grid(True, which='both', alpha=0.3); ax.set_ylim(*YLIM); ax.legend()
    fig.tight_layout()
    fig.savefig(os.path.join(outdir, 'SIM-2.png'), dpi=140)
    plt.close(fig)


def plot_sim3(snr_sq, res_sq, snr_n, res_n, n_list, outdir):
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(1, 2, figsize=(11, 4.3))
    # (a) Alıcı tipi: ZF vs MMSE (kare sistem N=M=8; BER, farkı net göstermek için)
    ax[0].semilogy(snr_sq, _mask(res_sq['zf_linear']['ber']), 's-', color='#c0392b',
                   label='ZF lineer', lw=2, ms=6)
    ax[0].semilogy(snr_sq, _mask(res_sq['mmse_linear']['ber']), 'd-', color='#2980b9',
                   label='MMSE lineer', lw=2, ms=6)
    ax[0].set_xlabel('Ortalama alınan SNR (dB)'); ax[0].set_ylabel('BER (bit hata oranı)')
    ax[0].set_title('(a) ZF vs MMSE — N=M=8 (kare sistem)'); ax[0].grid(True, which='both', alpha=0.3)
    ax[0].set_ylim(*YLIM); ax[0].legend()
    # (b) N etkisi
    colors = ['#7f8c8d', '#16a085', '#8e44ad']
    for c, Nv in zip(colors, n_list):
        ax[1].semilogy(snr_n, _mask(res_n[Nv]['zf_sic_ordered']['bler']), 'o-',
                       color=c, label=f'N={Nv}', lw=2, ms=6)
    ax[1].set_xlabel('Ortalama alınan SNR (dB)'); ax[1].set_ylabel('BLER')
    ax[1].set_title('(b) Alıcı anten sayısı N etkisi (M=8)')
    ax[1].grid(True, which='both', alpha=0.3); ax[1].set_ylim(*YLIM); ax[1].legend()
    fig.suptitle('SIM-3 · Alıcı tipi (ZF/MMSE) & anten sayısı', fontweight='bold')
    fig.tight_layout()
    fig.savefig(os.path.join(outdir, 'SIM-3.png'), dpi=140)
    plt.close(fig)


# ----------------------------------------------------------------------------
# 5) Ana akış
# ----------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--quick', action='store_true', help='hızlı pilot (az burst)')
    ap.add_argument('--nbursts', type=int, default=0, help='burst sayısı (0=otomatik)')
    ap.add_argument('--outdir', default=os.path.join(os.path.dirname(__file__), 'figures'))
    args = ap.parse_args()

    os.makedirs(args.outdir, exist_ok=True)
    M, T = 8, 80

    if args.quick:
        snr = np.arange(10, 31, 4)           # pilot: kaba tarama
        nb = args.nbursts or 300
    else:
        snr = np.arange(10, 31, 2)           # tam: 10..30 dB
        nb = args.nbursts or 8000

    print(f'[*] M={M} N=12 T={T} nbursts={nb} snr={snr[0]}..{snr[-1]}dB')

    # --- Ana deney (N=12): tüm modlar tek seferde (H paylaşımı, ortak rastgele sayılar) ---
    modes = ['zf_linear', 'mmse_linear', 'zf_sic_ordered', 'zf_sic_fixed']
    print('[*] Deney A: N=12, tüm modlar...')
    resA = run_experiment(M, 12, snr, modes, nb, T, seed=1)
    plot_sim1(snr, resA, args.outdir)        # SIM-1: nulling vs V-BLAST
    plot_sim2(snr, resA, args.outdir)        # SIM-2: sıralı vs sırasız

    # --- SIM-3a: ZF vs MMSE kare sistemde (N=M=8) — ZF için en zorlu durum ---
    snr_sq = np.arange(14, 37, 3) if not args.quick else np.arange(14, 37, 6)
    print('[*] Deney kare: N=M=8, ZF vs MMSE lineer...')
    resSq = run_experiment(M, 8, snr_sq, ['zf_linear', 'mmse_linear'], nb, T, seed=4)

    # --- SIM-3b: N etkisi: N=12 (A'dan), N=16, N=20 ---
    n_list = [12, 16, 20]
    resN = {12: resA}
    for Nv in (16, 20):
        print(f'[*] Deney N={Nv}...')
        resN[Nv] = run_experiment(M, Nv, snr, ['zf_sic_ordered'], nb, T, seed=3)
    plot_sim3(snr_sq, resSq, snr, resN, n_list, args.outdir)   # SIM-3: ZF/MMSE + N

    # --- özet sayıları yazdır (scriptlerdeki ⟨...⟩ için) ---
    print('\n==== ÖZET (BLER) ====')
    def gap_db(snr, b1, b2, target=1e-2):
        """target BLER'e ulaşmak için gereken SNR farkı (b1 - b2), dB."""
        def snr_at(b):
            b = np.asarray(b)
            for i in range(len(b) - 1):
                if b[i] >= target >= b[i + 1] and b[i] > b[i + 1]:
                    # log-lineer interpolasyon
                    import math
                    x0, x1 = snr[i], snr[i + 1]
                    y0, y1 = math.log10(max(b[i], 1e-9)), math.log10(max(b[i + 1], 1e-9))
                    return x0 + (math.log10(target) - y0) * (x1 - x0) / (y1 - y0)
            return None
        s1, s2 = snr_at(b1), snr_at(b2)
        if s1 is None or s2 is None:
            return None
        return s1 - s2
    def report(name, b1, b2, target):
        g = gap_db(snr, b1, b2, target)
        s = f'{g:.1f} dB' if g is not None else 'aralık dışı'
        print(f'{name} @BLER={target:.0e}: {s}')
        return g
    report('SIM-1  V-BLAST kazancı (nulling-only - V-BLAST)',
           resA['zf_linear']['bler'], resA['zf_sic_ordered']['bler'], 1e-1)
    report('SIM-2  Sıralama kazancı (sırasız - sıralı)     ',
           resA['zf_sic_fixed']['bler'], resA['zf_sic_ordered']['bler'], 1e-1)
    g3 = gap_db(snr_sq, resSq['zf_linear']['ber'], resSq['mmse_linear']['ber'], 1e-2)
    print('SIM-3a MMSE kazancı, N=M=8 lineer (ZF - MMSE)   @BER =1e-02: '
          + (f'{g3:.1f} dB' if g3 is not None else 'aralık dışı'))
    print('SIM-3b N etkisi (BLER, seçili SNR):')
    for Nv in n_list:
        b = resN[Nv]['zf_sic_ordered']['bler']
        print('  N=%2d: ' % Nv + '  '.join(f'{s}dB={v:.1e}' for s, v in zip(snr, b)))
    print('[+] Grafikler:', args.outdir)


if __name__ == '__main__':
    main()
