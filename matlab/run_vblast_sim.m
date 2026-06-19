function run_vblast_sim()
%RUN_VBLAST_SIM  V-BLAST Monte-Carlo simulasyonu (TOOLBOX YOK).
%
%   Bu betik, sim/vblast_sim.py'nin BIREBIR AYNISIDIR. Makaledeki ortami
%   (M=8, N=12, 16-QAM, zengin sacilma = i.i.d. Rayleigh) sifirdan simule
%   eder ve 3 grafik uretir:
%       SIM-1 : BLER & BER vs SNR  -> ZF nulling-only vs V-BLAST (sirali SIC)
%       SIM-2 : BLER vs SNR        -> sirali vs sirasiz SIC
%       SIM-3 : (a) ZF vs MMSE (N=M=8, BER)   (b) anten sayisi N etkisi
%
%   Calistirmak icin: bu klasorde >> run_vblast_sim
%   (qam16_const.m, qam16_mod.m, qam16_demod.m, vblast_detect.m ayni klasorde)
%
%   NOT: nbursts'i artirmak egrileri duzlestirir ama yavaslatir.
%   Python referansinda nbursts=8000 kullanildi; MATLAB'de hizli deneme icin
%   2000 yeterlidir.

    rng(1);                          % tekrarlanabilirlik
    M = 8;  T = 80;  nbursts = 2000;
    snr   = 10:2:30;                 % ana tarama (dB)
    snrSq = 14:3:36;                 % kare sistem (N=M=8) taramasi

    fprintf('[*] M=%d, T=%d, nbursts=%d\n', M, T, nbursts);

    % --- Deney A (N=12): tum modlar ---
    fprintf('[*] Deney A: N=12 ...\n');
    modesA = {'zf_linear','mmse_linear','zf_sic_ordered','zf_sic_fixed'};
    A = run_experiment(M, 12, snr, modesA, nbursts, T);

    % --- Kare sistem (N=M=8): ZF vs MMSE lineer ---
    fprintf('[*] Deney kare: N=M=8 ...\n');
    Sq = run_experiment(M, 8, snrSq, {'zf_linear','mmse_linear'}, nbursts, T);

    % --- N etkisi: N=12 (A'dan), 16, 20 ---
    Nlist = [12 16 20];
    resN = struct(); resN.n12 = A;
    fprintf('[*] Deney N=16 ...\n'); resN.n16 = run_experiment(M, 16, snr, {'zf_sic_ordered'}, nbursts, T);
    fprintf('[*] Deney N=20 ...\n'); resN.n20 = run_experiment(M, 20, snr, {'zf_sic_ordered'}, nbursts, T);

    % ====================== GRAFIKLER ======================
    % SIM-1
    figure('Name','SIM-1','Color','w','Position',[100 100 1000 400]);
    subplot(1,2,1);
    semilogy(snr, mask(A.zf_linear.bler), 'rs-', 'LineWidth',2,'MarkerSize',7); hold on;
    semilogy(snr, mask(A.zf_sic_ordered.bler), 'ko-', 'LineWidth',2,'MarkerSize',7);
    grid on; xlabel('Ortalama alinan SNR (dB)'); ylabel('BLER');
    title('BLER: Nulling-only vs V-BLAST'); ylim([3e-4 1.3]);
    legend('Sadece Nulling (ZF)','V-BLAST (sirali SIC)','Location','southwest');
    subplot(1,2,2);
    semilogy(snr, mask(A.zf_linear.ber), 'rs-', 'LineWidth',2,'MarkerSize',7); hold on;
    semilogy(snr, mask(A.zf_sic_ordered.ber), 'ko-', 'LineWidth',2,'MarkerSize',7);
    grid on; xlabel('Ortalama alinan SNR (dB)'); ylabel('BER');
    title('BER: Nulling-only vs V-BLAST'); ylim([3e-4 1.3]);
    legend('Sadece Nulling (ZF)','V-BLAST (sirali SIC)','Location','southwest');
    sgtitle('SIM-1 \cdot M=8, N=12, 16-QAM');

    % SIM-2
    figure('Name','SIM-2','Color','w','Position',[120 120 700 500]);
    semilogy(snr, mask(A.zf_sic_fixed.bler), '^-','Color',[0.9 0.5 0.13],'LineWidth',2,'MarkerSize',8); hold on;
    semilogy(snr, mask(A.zf_sic_ordered.bler), 'ko-','LineWidth',2,'MarkerSize',8);
    grid on; xlabel('Ortalama alinan SNR (dB)'); ylabel('BLER'); ylim([3e-4 1.3]);
    title('SIM-2 \cdot Siralamanin etkisi (M=8, N=12)');
    legend('Sirasiz SIC (sabit sira)','Sirali SIC (V-BLAST, maximin)','Location','southwest');

    % SIM-3
    figure('Name','SIM-3','Color','w','Position',[140 140 1000 400]);
    subplot(1,2,1);
    semilogy(snrSq, mask(Sq.zf_linear.ber), 'rs-','LineWidth',2,'MarkerSize',7); hold on;
    semilogy(snrSq, mask(Sq.mmse_linear.ber), 'd-','Color',[0.16 0.5 0.72],'LineWidth',2,'MarkerSize',7);
    grid on; xlabel('Ortalama alinan SNR (dB)'); ylabel('BER'); ylim([3e-4 1.3]);
    title('(a) ZF vs MMSE - N=M=8 (kare sistem)');
    legend('ZF lineer','MMSE lineer','Location','southwest');
    subplot(1,2,2);
    cols = [0.5 0.5 0.5; 0.09 0.63 0.52; 0.56 0.27 0.68];
    semilogy(snr, mask(resN.n12.zf_sic_ordered.bler),'o-','Color',cols(1,:),'LineWidth',2,'MarkerSize',7); hold on;
    semilogy(snr, mask(resN.n16.zf_sic_ordered.bler),'o-','Color',cols(2,:),'LineWidth',2,'MarkerSize',7);
    semilogy(snr, mask(resN.n20.zf_sic_ordered.bler),'o-','Color',cols(3,:),'LineWidth',2,'MarkerSize',7);
    grid on; xlabel('Ortalama alinan SNR (dB)'); ylabel('BLER'); ylim([3e-4 1.3]);
    title('(b) Alici anten sayisi N etkisi (M=8)');
    legend('N=12','N=16','N=20','Location','southwest');
    sgtitle('SIM-3 \cdot Alici tipi (ZF/MMSE) & anten sayisi');

    fprintf('[+] Bitti. 3 figur uretildi.\n');
end

% ========================================================================
function res = run_experiment(M, N, snr_db, modes, nbursts, T)
%RUN_EXPERIMENT  Verilen modlar icin BLER & BER vs SNR (ortak rastgele sayilar).
    [const, bits] = qam16_const();
    nsnr = numel(snr_db);
    N0list = M ./ (10.^(snr_db/10));

    blockErr = zeros(nsnr, numel(modes));
    bitErr   = zeros(nsnr, numel(modes));
    blocksTot = zeros(nsnr,1);
    bitsTot   = zeros(nsnr,1);

    for b = 1:nbursts
        H  = (randn(N,M) + 1i*randn(N,M))/sqrt(2);
        txIdx = randi(16, M, T);
        Asym  = const(txIdx);                                % MxT
        Wn = (randn(N,T) + 1i*randn(N,T))/sqrt(2);
        HA = H * Asym;
        txBits = bits(txIdx(:), :);                          % (M*T)x4

        for si = 1:nsnr
            N0 = N0list(si);
            R = HA + sqrt(N0)*Wn;
            for mi = 1:numel(modes)
                est = vblast_detect(H, R, modes{mi}, N0);
                if any(est(:) ~= txIdx(:))
                    blockErr(si,mi) = blockErr(si,mi) + 1;
                end
                estBits = bits(est(:), :);
                bitErr(si,mi) = bitErr(si,mi) + sum(estBits(:) ~= txBits(:));
            end
            blocksTot(si) = blocksTot(si) + 1;
            bitsTot(si)   = bitsTot(si) + M*T*4;
        end
    end

    res = struct();
    for mi = 1:numel(modes)
        res.(modes{mi}).bler = (blockErr(:,mi) ./ blocksTot).';
        res.(modes{mi}).ber  = (bitErr(:,mi)   ./ bitsTot).';
    end
end

% ========================================================================
function y = mask(x)
%MASK  Olculemeyen (0) noktalari NaN yap (log eksende cizilmez).
    y = x; y(y <= 0) = NaN;
end
