---
proje: V-BLAST Sunum
dosya: Slayt planı + anlatım scriptleri
guncelleme: 2026-06-19
durum: TASLAK v2 — diversity + 3 simülasyon analizi eklendi (sim sayıları sonra netleşecek)
---

# 🎤 Sunum Planı & Anlatım Scriptleri (40 dk, ~23 slayt)

> Her slayt için: **(a)** başlık, **(b)** slaytta görünecek madde/görseller, **(c)** anlatım scripti (konuşmacının söyleyeceği). Scriptler `.pptx`'in speaker notes kısmına da eklenecek.
> `⟨...⟩` ile işaretli yerler simülasyon çalıştıktan sonra **gerçek sayılarla** doldurulacak.
> İlgili kavramların detayı için → `V-BLAST_Ogrenme_Dokumani.md` (bölüm numaraları parantezle verildi).

---

## Slayt 1 — Başlık
**Slaytta:** Başlık "V-BLAST: Zengin-Saçılımlı Kablosuz Kanalda Çok Yüksek Veri Hızları" · Makale: Wolniansky, Foschini, Golden, Valenzuela (Bell Labs, 1998) · Sunan: [İsim] · Tarih.

**Script:** "Herkese merhaba. Bugün kablosuz haberleşmenin kilometre taşı sayılan bir çalışmayı, Bell Labs'in V-BLAST mimarisini anlatacağım. Bu makale, aynı frekansı ve aynı zamanı paylaşan birden fazla anteni kullanarak, kablosuz spektral verimliliği o güne kadar görülmemiş seviyelere — 20 ila 40 bps/Hz'e — çıkarmayı başardı. Sunumun sonunda, hem yöntemin nasıl çalıştığını hem de bunu kendi MATLAB simülasyonumuzla nasıl doğruladığımızı göreceğiz. Önce en temelden, tek antenli sistemlerden başlayacağız; merak etmeyin, her kavramı sıfırdan kuracağız."

---

## Slayt 2 — Sunum Akışı
**Slaytta:** 1) Motivasyon & temel kavramlar 2) MIMO ve çok antenin amaçları 3) Uzamsal çoğullama 4) V-BLAST mimarisi 5) Alıcı: nulling + sıralı iptal 6) Optimal sıralama 7) Makale sonuçları 8) Kendi simülasyonumuz 9) Sonuç.

**Script:** "Yol haritamız şöyle: Önce neden yeni bir yönteme ihtiyaç duyulduğunu, kapasite sorununu konuşacağız. Ardından MIMO'nun ne olduğunu ve birden fazla anteni hangi amaçlarla kullanabileceğimizi göreceğiz. Buradan V-BLAST'e geçip alıcının kalbindeki iki fikri — nulling ve sıralı iptal — adım adım inceleyeceğiz. Makalenin laboratuvar sonuçlarını gördükten sonra, aynı ortamı MATLAB'de sıfırdan simüle edip kendi sonuçlarımızı sunacağım. Yaklaşık 40 dakika sürecek; sonunda sorularınız için zaman ayıracağım."

---

## Slayt 3 — Motivasyon: Veri Talebi & Spektrum Kıtlığı
**Slaytta:** • Kablosuz veri talebi katlanarak artıyor • Frekans spektrumu kıt ve pahalı • Daha fazla bant / daha fazla güç → sürdürülebilir değil • Soru: Aynı spektrumla daha çok bit nasıl?

**Script:** "Her yıl daha fazla cihaz, daha fazla veri istiyor. Ama kablosuz haberleşmenin hammaddesi olan frekans spektrumu kıt bir kaynak; lisansları milyarlarca dolar. İki klasik çözüm var: ya daha geniş bant kullanırsınız — ama bant yok — ya da daha fazla güç verirsiniz — ama birazdan göreceğimiz gibi bu çok verimsiz. Demek ki asıl soru şu: Elimizdeki aynı frekans bandından, gücü de çok artırmadan, nasıl çok daha fazla bit geçirebiliriz? V-BLAST'in cevabı, hiç beklenmedik bir yerden geliyor: çok yollu yayılımı, yani normalde baş belası saydığımız şeyi, bir avantaja çevirmekten."

---

## Slayt 4 — SISO & Kablosuz Kanal  (Doküman §1)
**Slaytta:** • SISO = tek verici, tek alıcı anten • Kanal: zayıflama + gürültü + multipath (çok yollu) • Multipath → fading (sönümlenme) • SISO'da multipath bir sorundur · [basit şema: TX→yansımalar→RX]

**Script:** "En basit sistemle başlayalım: SISO, yani tek verici ve tek alıcı anten. Sinyal antenden çıkıp havada yol alırken üç şey olur: mesafeyle zayıflar, alıcıda gürültüye karışır ve en önemlisi, duvarlara, eşyalara çarpıp birden fazla yoldan alıcıya ulaşır. Buna çok yollu yayılım, multipath diyoruz. Bu kopyalar bazen birbirini güçlendirir, bazen söndürür; sinyal gücü dalgalanır, buna sönümlenme yani fading denir. Tek antenli sistemlerde multipath tamamen bir baş belasıdır — sinyali bozar. Bu cümleyi aklınızda tutun, çünkü MIMO bu bakışı tam tersine çevirecek."

---

## Slayt 5 — Kapasite Sorunu  (Doküman §2)
**Slaytta:** • Shannon: $C = B\log_2(1+\mathrm{SNR})$ • Bant B kıt • SNR `log` içinde → güç 2× → kapasite az artar • Spektral verimlilik (bps/Hz) sınırlı

**Script:** "Bir kanaldan ne kadar hızlı veri geçirebileceğimizin teorik sınırını Shannon formülü verir: kapasite, bant genişliği çarpı log iki tabanında bir artı SNR. Buradaki acı gerçek şu: bant genişliğini artıramıyoruz çünkü spektrum kıt. SNR'ı artırmak için gücü iki katına çıkarsak bile, SNR logaritmanın içinde olduğu için kapasite sadece bir tık artar — yani güç pompalamak çok verimsiz. Sonuç olarak, birim banttan geçirdiğimiz bit sayısı, yani spektral verimlilik, geleneksel sistemlerde birkaç bps/Hz'de tıkanır. Peki bandı ve gücü artıramıyorsak ne yapacağız? Cevap: yepyeni bir boyut eklemek — uzayı."

---

## Slayt 6 — MIMO Nedir?  (Doküman §3)
**Slaytta:** • MIMO = M verici + N alıcı anten (M ≤ N) • Aynı frekans, aynı anda, çok akış • "Karışsınlar, yeter ki alıcıda ayıralım" • Kanal matrisi H'nin bağımsız sütunları → ayrıştırma mümkün • Benzetme: yankılı odada 4 konuşmacı, çok mikrofon

**Script:** "MIMO, çok girişli çok çıkışlı demek: vericide M, alıcıda N anten. Fikir cüretkâr: aynı frekansta, aynı anda birden fazla bağımsız veri akışı gönderelim. Geleneksel sezgi 'olmaz, karışırlar' der. MIMO ise 'karışsınlar, biz alıcıda geri ayırırız' der. Bunu mümkün kılan şey kanal matrisi H. Eğer ortamda bol yansıma varsa, her verici-alıcı çiftinin kanalı farklı olur ve H'nin sütunları doğrusal bağımsız olur; bu da denklemi çözülebilir kılar. Şöyle düşünün: yankılı bir odada dört kişi aynı anda konuşuyor; farklı yerlere koyduğunuz dört mikrofon, seslerin her birine farklı ulaşmasını kullanarak onları ayırabilir. MIMO tam olarak budur."

---

## Slayt 7 — Çok Antenin ÜÇ Amacı  (Doküman §4) ⭐YENİ
**Slaytta:** Üç sütunlu görsel — **1) Çeşitleme (Diversity):** güvenilirlik · RX (MRC) & TX (Alamouti) · aynı veri, farklı yollar. **2) Hüzmeleme (Beamforming):** SNR/kapsama · enerjiyi yönlendir. **3) Uzamsal Çoğullama (SM):** hız · farklı antenden farklı veri → **V-BLAST budur**. • Ödünleşim: ya hız ya güvenilirlik.

**Script:** "Önemli bir noktayı netleştirelim: 'birden fazla anten kullanmak' tek bir şey değildir; üç farklı amacı olabilir. Birincisi çeşitleme, yani diversity: aynı veriyi birden fazla bağımsız yoldan gönderip alırsınız; biri sönümlenmeye düşse bile diğeri sağlam kalır, böylece güvenilirlik artar. Bunu alıcıda yaparsanız RX diversity, vericide Alamouti gibi kodlarla yaparsanız TX diversity denir. İkincisi hüzmeleme, beamforming: antenleri birlikte kullanıp enerjiyi belirli bir yöne odaklarsınız, SNR ve kapsama artar. Üçüncüsü ise uzamsal çoğullama: farklı antenlerden farklı veriler gönderip hızı katlarsınız. İşte V-BLAST tam olarak bu üçüncüsünü hedefler. Ama dikkat: aynı antenleri ya hıza ya güvenilirliğe ayırırsınız; aralarında bir ödünleşim vardır. V-BLAST hıza odaklanır, ama birazdan göreceğimiz gibi alıcı anten fazlalığı sayesinde biraz da çeşitleme kazanır."

---

## Slayt 8 — Uzamsal Çoğullama & Kapasite Avantajı  (Doküman §5)
**Slaytta:** • 1 akışı M alt-akışa böl, ayrı antenlerden aynı anda gönder • $C_{MIMO} \approx M\cdot B\log_2(1+\mathrm{SNR})$ • Kapasite anten sayısıyla **doğrusal** büyür • Ekstra bant/güç YOK • V-BLAST = SM'nin pratik gerçeklemesi

**Script:** "Çoğullamanın gücünü biraz açalım. Tek bir hızlı akışı M parçaya bölüp her parçayı ayrı antenden, aynı frekansta, aynı anda gönderiyoruz. Sonuç dramatik: hatırlayın, SISO'da gücü iki katına çıkarmak kapasiteyi sadece logaritmik artırıyordu. MIMO'da ise kapasite, anten sayısı M ile doğrudan çarpılıyor — yani doğrusal büyüyor. Sekiz anten, kabaca sekiz kat kapasite, üstelik ne ekstra bant ne ekstra güç gerekmeden. Spektrumun altın değerinde olduğu bir dünyada bu bir devrim. V-BLAST işte bu fikrin gerçek donanımda çalışan pratik bir gerçeklemesi. Şimdi soru şu: bu karışmış akışları alıcıda nasıl ayıracağız?"

---

## Slayt 9 — BLAST Ailesi: D-BLAST vs V-BLAST  (Doküman §6)
**Slaytta:** Tablo — | | D-BLAST | V-BLAST | Kodlama: çapraz/karmaşık vs yok ; Performans: ~%90 Shannon vs biraz düşük ama yüksek ; Karmaşıklık: yüksek vs **gerçek zamanlı uygulandı**. • V-BLAST'in çözdüğü problem: pratik, basit, çalışan bir MIMO alıcısı.

**Script:** "BLAST, Bell Labs Layered Space-Time'ın kısaltması ve iki üyesi var. D-BLAST, yani çapraz BLAST, alt-akışlar arasında zekice bir çapraz kodlama kullanır; teorik olarak müthiş, Shannon kapasitesinin yüzde doksanına ulaşır. Ama o kadar karmaşık ki gerçek zamanlı donanımda uygulamak çok zor. V-BLAST, yani dikey BLAST, bu kodlamayı tamamen atar: sadece 'böl ve gönder'. Biraz teorik performanstan feragat eder ama karşılığında gerçek zamanlı çalışabilen, basit bir sistem sunar. Yani V-BLAST'in çözdüğü problem net: MIMO'nun yüksek verimliliğini, gerçekten çalışan pratik bir alıcıyla elde etmek. Vericide her şey basit; tüm zekâ alıcıda."

---

## Slayt 10 — V-BLAST Sistem Mimarisi  🖼️ Şekil 1  (Doküman §7)
**Slaytta:** **Şekil 1** (image_000000 — blok diyagram). • Vektör kodlayıcı → M verici (her biri sıradan QAM) • Zengin saçılma ortamı • N alıcı → V-BLAST işleme → veri • Toplam güç sabit (her TX 1/M güç).

**Script:** "Sistemin kuş bakışı görünümü bu. Soldan başlayalım: tek veri akışı vektör kodlayıcıda M alt-akışa bölünüyor. Her alt-akış sıradan bir QAM vericisine gidiyor — burada özel bir şey yok, klasik modülasyon. M verici aynı frekansta, senkronize, aynı anda yayın yapıyor; toplam güç sabit kalsın diye her biri 1/M güçle. Sinyaller zengin saçılma ortamından geçip karışarak N alıcı antene ulaşıyor. Bütün marifet sağdaki kutuda: V-BLAST sinyal işleme. Bu blok, karışmış sinyallerden orijinal akışları geri çıkarıyor. Sunumun geri kalanı esasen bu kutunun içini açmak olacak."

---

## Slayt 11 — Sistem Modeli & Varsayımlar  (Doküman §7)
**Slaytta:** • $r = Ha + \nu$ • a: gönderilen semboller (M×1) · H: kanal (N×M) · r: alınan (N×1) · ν: gürültü (σ²) • Flat fading, yarı-durağan kanal • H, eğitim dizisiyle (training) tahmin edilir.

**Script:** "Tüm problemi tek bir denkleme indirgeyelim: alınan vektör r eşittir kanal matrisi H çarpı gönderilen vektör a, artı gürültü nü. a bizim bulmak istediğimiz semboller, H kanal, r elimizdeki ölçüm. Birkaç makul varsayım yapıyoruz: kanal bir burst boyunca sabit kalıyor — buna yarı-durağan diyoruz — ve her burst'ün başına gömülü bir eğitim dizisiyle H'yi doğru biçimde tahmin ediyoruz. Yani alıcı H'yi biliyor kabul ediyoruz. Artık problem saf matematiğe indi: r ve H biliniyor, a'yı çöz. 'a eşittir H ters çarpı r' demek istiyorsunuz; doğru ama gürültü yüzünden iş o kadar basit değil — işte alıcı tasarımı burada devreye giriyor."

---

## Slayt 12 — Detection & Nulling (ZF / MMSE)  (Doküman §8a)
**Slaytta:** • Her akışı sırayla "istenen", gerisini "girişim" say • Ağırlık vektörü w ile bastır • ZF: $w_i^\top (H)_j = \delta_{ij}$ (diğerlerini sıfırla) • MMSE: gürültü+girişimi dengeler • Karar: $y_i = w_i^\top r$

**Script:** "Karışmış sinyalleri ayırmanın ilk yolu nulling, yani sıfırlama. Mantık şu: bir akışı 'istenen sinyal', diğerlerinin hepsini 'girişim' kabul ediyoruz. Sonra alınan sinyali öyle bir ağırlık vektörüyle çarpıyoruz ki istenen akış geçsin, diğerleri sıfırlansın. Zero-Forcing yönteminde bu koşul şu: ağırlık vektörü, istenen akışın kanal sütunuyla çarpınca bir, diğerleriyle çarpınca sıfır versin — formüldeki Kronecker delta tam bunu söylüyor. ZF basittir ama gürültüyü büyütebilir. Alternatifi MMSE, girişim ile gürültüyü birlikte dengeler ve genelde daha iyidir; bunu birazdan simülasyonda karşılaştıracağız. Makale sadelik için ZF üzerinden gider. Ama nulling tek başına en iyisi değil — bir adım daha var."

---

## Slayt 13 — Sembol İptali (SIC): Adım Adım  (Doküman §8b,c)
**Slaytta:** Akış şeması: **Nulling** → **Slice** $\hat{a}=Q(y)$ → **Cancel** $r_{i+1}=r_i-\hat{a}_{k_i}(H)_{k_i}$ → tekrarla. • Çözülen sembolü sinyalden çıkar → kalan girişim azalır • DFE'ye benzer

**Script:** "İşte V-BLAST'i güçlü kılan ikinci fikir: ardışık sembol iptali, yani SIC. Mantık çok sezgisel: bir sembolü çözdüysem, onun alınan sinyale kattığı katkıyı hesaplayıp geri çıkarabilirim. Böylece geriye bir girişim kaynağı daha az kalır. Döngü şöyle işliyor: önce nulling ile bir akışın kaba tahminini al; sonra slice et, yani en yakın geçerli QAM noktasına yuvarla; sonra bu tahmini kanal sütunuyla çarpıp alınan sinyalden çıkar — buna cancel diyoruz. Artık problem küçüldü, kalan akışlar için aynı döngüyü tekrarlıyoruz. Her turda iş kolaylaşıyor. Bu yaklaşım, ekolayzır tasarımındaki karar geri-beslemeli denkleştirmeye çok benzer. Peki bu neden saf nulling'den iyi?"

---

## Slayt 14 — Neden İptal Daha İyi?  (Doküman §8)
**Slaytta:** • Saf nulling: her w, M−1 akışa ortogonal olmalı (ağır kısıt) • İptal ile: w sadece **kalan** akışlara ortogonal • Cauchy-Schwarz: çok kısıt → büyük ‖w‖ • SNR: $\rho_{k_i} = \dfrac{\langle|a_{k_i}|^2\rangle}{\sigma^2\|w_{k_i}\|^2}$ → küçük norm = yüksek SNR

**Script:** "Cevap ağırlık vektörünün normunda gizli. Saf nulling'de her ağırlık vektörü, diğer bütün M eksi bir akışa birden ortogonal olmak zorunda — çok ağır bir kısıt. Ama iptal kullanınca, bir akışı çözüp çıkardıktan sonra, bir sonraki ağırlık vektörü artık sadece kalan, henüz çözülmemiş akışlara ortogonal olmak zorunda. Yani daha az kısıt. Burada Cauchy-Schwarz eşitsizliği devreye giriyor: bir vektör ne kadar çok şeye ortogonal olmaya zorlanırsa normu o kadar büyür. Ve şu kritik formüle bakın: detection sonrası SNR, ağırlık vektörünün normunun karesiyle ters orantılı. Küçük norm, yüksek SNR demek. İptal kısıtları azalttığı için norm küçülür, SNR yükselir, hata düşer. İşte iptalin saf nulling'i yenmesinin matematiksel sebebi bu."

---

## Slayt 15 — Optimal Sıralama: "En İyiyi Önce Al"  (Doküman §9)
**Slaytta:** • İptalde **sıra önemli** (saf nulling'de değil) • En zayıf akış hatayı belirler → maximin hedefi • **Sonuç:** her adımda en yüksek SNR'lı akışı seç → küresel optimum • Seçim: $k_i = \arg\min_j \|(G_i)_j\|^2$ • Hata yayılımını azaltır

**Script:** "İptal kullanınca yeni bir soru doğuyor: akışları hangi sırayla çözmeliyiz? Çünkü önce çözdüğümüz akış, sonrakileri etkiliyor. Tüm akışlar aynı takımyıldızı kullandığı için, sistemin hatasını en zayıf akış belirler. O halde mantıklı hedef, en kötü akışın SNR'ını mümkün olduğunca yükseltmek — buna maximin diyoruz. Makalenin zarif ve şaşırtıcı sonucu şu: her adımda sadece o anki en güçlü, en yüksek SNR'lı akışı seçip çözmek — yani basit bir açgözlü kural — küresel olarak en iyi sıralamayı garanti ediyor. Pratikte 'en güçlü akış', pseudoinverse matrisinin en küçük normlu satırına karşılık gelir. Bunun bir faydası daha var: en güvenilir kararı başta verdiğimiz için hata yayılımını da azaltıyoruz. Bu sezgisel kural yıllardır kullanılıyordu ama optimalliği ilk kez bu makalede ispatlandı."

---

## Slayt 16 — Tam Algoritma (Özyinelemeli) — Eq. (9)  (Doküman §10)
**Slaytta:** Başlangıç: $G_1=H^+$, $k_1=\arg\min_j\|(G_1)_j\|^2$. Özyineleme: $w_{k_i}=(G_i)_{k_i}$ → $y_{k_i}=w_{k_i}^\top r_i$ → $\hat{a}_{k_i}=Q(y_{k_i})$ → $r_{i+1}=r_i-\hat{a}_{k_i}(H)_{k_i}$ → $G_{i+1}=H_{\bar{k_i}}^+$ → $k_{i+1}=\arg\min\|(G_{i+1})_j\|^2$.

**Script:** "Bütün parçaları tek bir özyinelemeli algoritmada birleştirelim. Başlangıçta H'nin pseudoinverse'ini hesaplıyoruz ve en küçük normlu satırı bularak ilk çözeceğimiz akışı seçiyoruz. Sonra döngü: o akışın nulling vektörünü al, karar istatistiğini hesapla, slice et, tahmini sinyalden çıkar. Şimdi önemli adım: H'yi 'sönükleştiriyoruz' — çözdüğümüz akışın sütununu sıfırlayıp pseudoinverse'i yeniden hesaplıyoruz. Çünkü o akış artık yok; sistem bir antenle küçülmüş gibi davranıyor. Yeni matriste yine en küçük normlu satırı seçip bir sonraki akışa geçiyoruz. Bütün akışlar bitene kadar bu böyle sürüyor. Birkaç satır gibi görünse de, bu algoritma MIMO alıcısının kalbidir. Şimdi gerçekten çalışıyor mu, ona bakalım."

---

## Slayt 17 — Makale Laboratuvar Sonuçları  🖼️ Şekil 2 + 3  (Doküman §11)
**Slaytta:** **Şekil 2** (BLER vs SNR: null only vs null+iptal, ~4 dB fark) + **Şekil 3** (konuma göre gürbüzlük). • Prototip: 1.9 GHz, M=8/N=12, 16-QAM • **20–40 bps/Hz**, 621 kbps @ 30 kHz • İptal ~4 dB kazanç.

**Script:** "Makale sadece teori değil; gerçek bir laboratuvar prototipi kurulmuş. 1.9 gigahertz'de, sekiz verici on iki alıcı antenle, gerçek bir ofis ortamında çalıştırılmış. Soldaki Şekil 2'de blok hata oranı SNR'a karşı çiziliyor. Üstteki kötü eğri saf nulling, alttaki iyi eğri nulling artı optimal sıralı iptal. Aradaki fark yaklaşık dört desibel — bu da bu konfigürasyonda neredeyse on bps/Hz'lik bir verimlilik farkı demek. Sağdaki Şekil 3 ise vericiyi farklı konumlara taşıdıklarında performansın gürbüz kaldığını gösteriyor. Sonuç: 20 ila 40 bps/Hz spektral verimlilik, sadece 30 kilohertz bantta 621 kilobit. Aynı verimliliği tek antenle elde etmek için milyarlarca noktalı bir takımyıldız gerekirdi — yani imkânsız. Şimdi bunu kendimiz doğrulayalım."

---

## Slayt 18 — Bizim Simülasyonumuz: Kurulum  (Doküman §12)
**Slaytta:** • Makale ortamı **MATLAB'de, toolbox fonksiyonu KULLANMADAN** • M=8, N=12, 16-QAM, Rayleigh flat fading (H ~ i.i.d. CN(0,1)) • Sıfırdan: QAM mod/demod, kanal, gürültü, ZF/MMSE/SIC alıcı • Monte Carlo, BLER & BER vs SNR

**Script:** "Makaledeki ortamı doğrulamak için her şeyi MATLAB'de sıfırdan, hiçbir hazır toolbox fonksiyonu kullanmadan kodladık. Yani 16-QAM modülasyonunu, kanalı, gürültüyü, pseudoinverse'i, sıralı iptalli alıcıyı — hepsini elle yazdık. Parametreler makaleyle aynı: sekiz verici, on iki alıcı, 16-QAM, ve zengin saçılmayı temsil eden bağımsız Rayleigh sönümlemeli kanal. Her SNR noktasında binlerce rastgele burst üretip Monte Carlo yöntemiyle blok hata oranını ve bit hata oranını ölçtük. Sırasıyla dört şey göstereceğim: ana karşılaştırma, sıralamanın etkisi, alıcı tipinin etkisi ve anten sayısının etkisi. Sonuçlara bakalım."

---

## Slayt 19 — Simülasyon 1: BLER & BER (Nulling vs V-BLAST)  🖼️ SIM-1  (Doküman §11,12)
**Slaytta:** **SIM-1 grafiği** (BLER + BER vs SNR: nulling-only vs V-BLAST). • V-BLAST eğrisi **~4 dB** solda (daha iyi) • Makale Şekil 2 trendiyle uyumlu • Yüksek SNR'da V-BLAST eğimi daha dik

**Script:** "İşte ana sonucumuz, makaledeki Şekil 2'nin muadili. Yatay eksende ortalama SNR, dikey eksende hata oranı, logaritmik ölçekte. İki eğri var: üstteki saf nulling, alttaki V-BLAST, yani sıralı iptalli alıcı. Görüldüğü gibi V-BLAST eğrisi yaklaşık dört desibel solda; aynı hata oranına çok daha düşük SNR'da ulaşıyor. Ölçtüğümüz kazanç 4.4 desibel — makalenin bildirdiği yaklaşık dört desibellik farkla neredeyse birebir aynı. Dikkat edin, V-BLAST'in eğimi de daha dik — çünkü her doğru kararla bir girişim kaynağını temizleyip sonraki kararları kolaylaştırıyor. Yani makalenin ana iddiasını kendi kodumuzla, sıfırdan doğrulamış olduk."

---

## Slayt 20 — Simülasyon 2: Sıralamanın Etkisi (Sıralı vs Sırasız)  🖼️ SIM-2  (Doküman §9,12-B)
**Slaytta:** **SIM-2 grafiği** (sıralı SIC vs sabit sıralı SIC). • Sıralı (maximin) **~3 dB** daha iyi • Makalenin ana teorik katkısının deneysel kanıtı • Hata yayılımı azalır

**Script:** "İkinci grafik, makalenin en zarif teorik sonucunu test ediyor: sıralama gerçekten önemli mi? Burada iki iptal stratejisini karşılaştırıyoruz. Üstteki eğri, akışları gelişigüzel, sabit bir sırayla çözen sürüm. Alttaki eğri ise V-BLAST'in optimal sıralaması: her adımda en güçlü akışı önce çöz. Aradaki fark yaklaşık üç desibel. Bu, 'en iyiyi önce al' kuralının neden değerli olduğunun doğrudan kanıtı: en güvenilir kararları başta verince hata yayılımı azalıyor ve en zayıf akışın SNR'ı yükseliyor. Makalenin matematiksel olarak ispatladığı maximin optimalliğini, biz burada deneysel olarak görüyoruz."

---

## Slayt 21 — Simülasyon 3: Alıcı Tipi & Anten Sayısı  🖼️ SIM-3  (Doküman §12-A,C)
**Slaytta:** **SIM-3 grafiği (iki panel):** (sol) ZF vs MMSE — **N=M=8 kare sistemde** MMSE **~3 dB** iyi (BER); (sağ) N=12/16/20 — N↑ → performans↑. • MMSE: gürültü+girişim dengesi • Fazla alıcı anten = çeşitleme kazancı

**Script:** "Son simülasyonumuzda iki tasarım sorusuna bakıyoruz. Solda alıcı tipini karşılaştırıyoruz. Burada özellikle zorlu bir durumu seçtim: alıcı anten sayısı verici sayısına eşit, yani N eşittir M eşittir sekiz — kare sistem. Bu durumda kanal kötü koşullu olur ve ZF girişimi sıfırlarken gürültüyü ciddi biçimde büyütür. Grafikte görüldüğü gibi MMSE, bit hata oranında ZF'ten yaklaşık üç desibel daha iyi; çünkü MMSE girişim ile gürültüyü birlikte dengeler. Sağda ise alıcı anten sayısının etkisini görüyoruz: M sekiz sabitken N'i on ikiden yirmiye çıkardığımızda performans belirgin iyileşiyor. Sebep, başta konuştuğumuz çeşitleme: fazladan her alıcı anten ekstra serbestlik derecesi ve sönümlenmeye karşı dayanıklılık getiriyor. Bu da V-BLAST'in neden N'i M'den büyük tuttuğunu açıklıyor."

---

## Slayt 22 — Sonuçlar, Önem & Kapanış  (Doküman §11,13)
**Slaytta:** • V-BLAST: basit verici + akıllı alıcı (nulling + sıralı iptal + optimal sıra) • 20–40 bps/Hz — eşi görülmemiş • Multipath'i fırsata çevirdi • Simülasyonumuz makaleyi doğruladı (V-BLAST > nulling, sıralı > sırasız, MMSE > ZF, N↑) • **Bugün: Wi-Fi (802.11n/ac/ax), 4G LTE, 5G MIMO'sunun temeli**

**Script:** "Toparlayalım. V-BLAST'in dehası, vericiyi olabildiğince basit tutup tüm zekâyı alıcıya yüklemesinde: nulling ile sinyalleri ayır, sıralı iptal ile birbirini temizle, ve her zaman en güçlü akışı önce çöz. Bu yöntemle, normalde düşmanımız olan çok yollu yayılımı bir avantaja çevirip 20 ila 40 bps/Hz gibi o güne dek görülmemiş verimliliklere ulaşıldı. Kendi sıfırdan yazdığımız MATLAB simülasyonumuz da bütün ana sonuçları doğruladı: V-BLAST saf nulling'i, sıralı iptal sırasızı, MMSE ZF'i yendi ve anten sayısı arttıkça performans iyileşti. Ve bu akademik bir merak değil: bugün evimizdeki Wi-Fi'da, telefonumuzdaki 4G ve 5G'de kullanılan MIMO teknolojisinin doğrudan temeli bu çalışma. Beni dinlediğiniz için teşekkürler — sorularınızı almaktan memnuniyet duyarım."

---

## Slayt 23 — Kaynaklar & Sorular
**Slaytta:** • Ana kaynak: Wolniansky et al., V-BLAST (1998) • Foschini, Layered Space-Time (1996) • Foschini & Gans (1998) • "Sorular?" • İletişim.

**Script:** "Bu slaytta ana kaynakları görüyorsunuz; özellikle Foschini'nin 1996'daki temel makalesi ve elimizdeki V-BLAST çalışması. Sorularınız için buradayım."

> **Hazır Q&A (öğrenme dokümanı §13):** V-BLAST vs D-BLAST · nulling vs iptal · sıralama neden önemli · ZF vs MMSE · hata yayılımı · zengin saçılma neden gerekli · M ≤ N koşulu · çok antenin amaçları · V-BLAST diversity kazanır mı.

---

## Notlar
- ✅ Simülasyon sayıları işlendi (FAZ 1 tamam): SIM-1 ~4.4 dB, SIM-2 ~3 dB, SIM-3a ~3 dB (N=M=8), SIM-3b N↑ iyileşme.
- Scriptler ortalama 130-170 kelime → slayt başına ~1.5-2.5 dk → 23 slayt ≈ ~40 dk.
- Tüm scriptler `.pptx` speaker notes'a kopyalanacak (FAZ 2).
- Görsel eşleşmeleri: Şekil 1→S10, Şekil 2+3→S17, SIM-1→S19, SIM-2→S20, SIM-3→S21.
- Grafik dosyaları: `sim/figures/SIM-1.png`, `SIM-2.png`, `SIM-3.png`.
