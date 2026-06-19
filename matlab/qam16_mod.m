function sym = qam16_mod(idx)
%QAM16_MOD  16-QAM sembol uretimi (indis -> kompleks sembol). TOOLBOX YOK.
%   sym = qam16_mod(idx)
%   idx : 1..16 arasi indis dizisi (skaler/vektor/matris olabilir)
%   sym : ayni boyutta kompleks 16-QAM sembolleri (birim enerji)

    const = qam16_const();
    sym = const(idx);          % MATLAB indeksleme idx ile ayni boyutu dondurur
end
