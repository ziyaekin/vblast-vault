function est = vblast_detect(H, R, mode, N0)
%VBLAST_DETECT  V-BLAST / lineer MIMO alicilari (hepsi sifirdan). TOOLBOX YOK.
%   est = vblast_detect(H, R, mode, N0)
%
%   H    : NxM kanal matrisi
%   R    : NxT alinan vektorler (T = sembol-vektor sayisi)
%   mode : 'zf_linear'        - saf ZF nulling (iptal yok)
%          'mmse_linear'      - saf MMSE nulling (iptal yok)
%          'zf_sic_ordered'   - V-BLAST: ZF nulling + SIRALI iptal (maximin)
%          'zf_sic_fixed'     - ZF nulling + SIRASIZ (sabit) iptal
%          'mmse_sic_ordered' - MMSE nulling + sirali iptal
%   N0   : gurultu varyansi (MMSE ve raporlama icin)
%
%   est  : MxT tahmini sembol indisleri (1..16)
%
%   Kullanilan cekirdek fonksiyonlar: pinv, mldivide (\), min, abs - hepsi
%   temel MATLAB; hicbir toolbox fonksiyonu kullanilmaz.

    const = qam16_const();
    [N, M] = size(H); %#ok<ASGLU>

    switch mode
        case 'zf_linear'
            G = pinv(H);                 % MxN
            est = qam16_demod(G * R);

        case 'mmse_linear'
            G = (H'*H + N0*eye(M)) \ H';  % MxN  (birim enerji: N0/Es, Es=1)
            est = qam16_demod(G * R);

        case {'zf_sic_ordered', 'zf_sic_fixed', 'mmse_sic_ordered'}
            ordered = ~strcmp(mode, 'zf_sic_fixed');
            if strcmp(mode, 'mmse_sic_ordered'), crit = 'mmse'; else, crit = 'zf'; end
            est = sic_core(H, R, const, N0, crit, ordered);

        otherwise
            error('Bilinmeyen mode: %s', mode);
    end
end

% ------------------------------------------------------------------------
function est = sic_core(H, R, const, N0, crit, ordered)
%SIC_CORE  Sirali/sirasiz iptal cekirdegi (Eq.(9) ozyinelemesi).
    [~, M] = size(H);
    T = size(R, 2);
    Rcur = R;
    est = zeros(M, T);
    remaining = 1:M;
    Hdef = H;                          % "soluklestirilen" (deflated) kanal

    for step = 1:M %#ok<*NASGU>
        % --- nulling matrisi G_i ---
        if strcmp(crit, 'zf')
            G = pinv(Hdef);
        else
            G = (Hdef'*Hdef + N0*eye(M)) \ Hdef';
        end

        % --- siralama: en kucuk normlu (=en yuksek SNR'li) satiri sec ---
        rownorm = sum(abs(G).^2, 2);
        if ordered
            rn = rownorm;
            rn(setdiff(1:M, remaining)) = inf;   % cozulenleri disla
            [~, k] = min(rn);
        else
            k = remaining(1);                    % sabit dogal sira
        end

        % --- nulling -> karar -> iptal (cancellation) ---
        w = G(k, :);                    % 1xN nulling vektoru
        y = w * Rcur;                   % 1xT karar istatistigi
        idx = qam16_demod(y);           % 1xT
        est(k, :) = idx;
        val = const(idx);               % 1xT tahmini semboller
        Rcur = Rcur - H(:, k) * val;    % NxT: bu akisi sinyalden cikar

        % --- deflation: cozulen sutunu sifirla, sonraki tura gec ---
        remaining(remaining == k) = [];
        Hdef(:, k) = 0;
    end
end
