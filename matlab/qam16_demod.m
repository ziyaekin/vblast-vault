function idx = qam16_demod(y)
%QAM16_DEMOD  En yakin komsu dilimleme (slicing). TOOLBOX YOK (qamdemod yok).
%   idx = qam16_demod(y)
%   y   : kompleks karar istatistigi (skaler/vektor/matris)
%   idx : ayni boyutta, en yakin takimyildiz noktasinin indisi (1..16)

    const = qam16_const();          % 16x1
    yv = y(:);                       % sutun vektor
    d  = abs(yv - const.');           % (numel x 16) mesafe matrisi
    [~, k] = min(d, [], 2);           % her ornek icin en yakin indis
    idx = reshape(k, size(y));
end
