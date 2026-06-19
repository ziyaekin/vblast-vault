function [const, bits] = qam16_const()
%QAM16_CONST  Birim ortalama enerjili, Gray-kodlu 16-QAM takimyildizi.
%   [const, bits] = qam16_const()
%   const : 16x1 kompleks noktalar (1..16 indisli), ortalama enerji = 1
%   bits  : 16x4 her noktanin bit gosterimi [b3 b2 b1 b0]
%
%   TOOLBOX YOK - tamamen elle kurulur. (qammod kullanilmaz.)
%   2-bit Gray -> seviye eslemesi: 00->-3, 01->-1, 11->+1, 10->+3

    lev = [-3, -1, 3, 1];          % key = 2*b_hi + b_lo  ->  seviye
    const = zeros(16, 1);
    bits  = zeros(16, 4);
    for s = 0:15
        b3 = bitget(s, 4); b2 = bitget(s, 3);   % I icin ust 2 bit
        b1 = bitget(s, 2); b0 = bitget(s, 1);   % Q icin alt 2 bit
        I = lev(2*b3 + b2 + 1);
        Q = lev(2*b1 + b0 + 1);
        const(s+1) = I + 1i*Q;
        bits(s+1, :) = [b3 b2 b1 b0];
    end
    const = const / sqrt(10);      % ortalama enerji 10 -> 1'e normalize
end
