# Günlük teklif akışı

Teklif ekranı üç adımlıdır: Belgeler ve talep → Taslak ve fiyat → Teklif ve onay. Adımlar serbestçe değiştirilebilir; adım değiştirmek alanları silmez veya onayı değiştirmez. Kaydet düğmesi her adımda kullanılabilir.

Alternatifin toplam fiyatı ve eksik hesap uyarısı kapalı maliyet bölümü dışında görünür. Kalıp dış ölçüleri/maça notları, ek alternatif işlemleri, malzeme hesabı ve maliyet dökümü ayrı açılır bölümlerdedir. Teknik 3D inceleme düğmesi görünür kalır. Teklif tarihleri ve koşulları çıktı adımında açılır; onay işlemleri de burada bulunur. Belgelerin paket indirme ve görsel düzenleme seçenekleri belge adımındaki ek bölümde korunur.

Eksik bilgi bağlantıları hedefin bulunduğu adıma geçer ve üstteki kapalı ayrıntıları açar. Tüm alanlar DOM içinde tutulur; gizlenen alanlar kayıt/hesaplama dışında bırakılmaz. Sadeleştirme veri formatını, fiyat formüllerini, yetenekleri veya kayıtlı teklifleri değiştirmez.

Doğrulama: tarayıcıda üç adım geçişi, kapalı bölümün açılması, manuel ölçünün adım değiştirdikten sonra kaydedilmesi, alternatif eklenmesi, eksiklerle ön izleme ve eksik alan yönlendirmesi; mevcut V4 hesap/ayar/yedek/onay kontrolleri.

## Son fiyat kontrolü

Üçüncü adımda her dahil alternatif için malzeme, işçilik ve hırdavat/piston oranları ayrı düzenlenir. Bunlar V4'teki maliyet üzerine kâr oranlarıdır; satıştan yüzde düşme hesabı değildir. Son kontrol ile maliyet ayrıntısındaki alanlar aynı hesap verisini kullanır. Manuel satış seçiliyse oran değişikliği bu fiyatı ezmez; kullanıcıya uyarı ve oranlarla hesaplama seçeneği gösterilir. Son onaydan önceki ön izleme taslaktır. Nihai onay düğmesi “Fiyatları onayla ve teklif oluştur” adını taşır; geçerli onay sonrasında mevcut çıktı oluşturma/kayıt akışı çalışır.
