# Kararsızım 🤔 — Proje Planı ve Claude Code Rehberi

> Bu dosya projenin tek doğruluk kaynağıdır. Repo köküne `CLAUDE.md` adıyla konulmalıdır.
> Claude Code her oturumda önce bu dosyayı okur, sonra yalnızca **istenen fazı** uygular.

---

## 1. Proje Özeti

**Kararsızım**, kararsız kalan kullanıcıların diğer kullanıcılara danışmak için hızlıca anket açtığı bir web uygulamasıdır.

Örnek: *"Bugün sinemaya mı gitsem, tiyatroya mı?"* → Seçenekler: `Sinema`, `Tiyatro`

### Temel kurallar

| Kural | Açıklama |
|---|---|
| Seçenek sayısı | Her ankette **en az 2, en fazla 5** seçenek olur. |
| Takip sistemi | **Yok.** Kullanıcılar birbirini takip etmez, akış herkes için aynıdır. |
| Görüntüleme | Herkes (üye olsun olmasın) tüm anketleri görebilir. |
| Oy verme | Herkes (üye olsun olmasın) tüm anketlere oy verebilir. Her kişi bir ankete **1 kez** oy verir. |
| Anket oluşturma | **Sadece üyeler.** Üye olmayan kullanıcı "Anket Oluştur"a basarsa giriş/kayıt sayfasına yönlendirilir. |
| Kayıt | E-posta + kullanıcı adı + parola. |
| Gizlilik | Anketlerde **yalnızca kullanıcı adı** görünür. E-posta hiçbir sayfada, HTML'de veya JSON yanıtında **asla** gösterilmez. |

### Hedef

İlk hedef **çalışan bir prototip**. Karmaşık teknolojilerden kaçınılır, proje fazlar halinde adım adım ilerler.

---

## 2. Teknoloji Yığını

| Katman | Teknoloji | Not |
|---|---|---|
| Dil | Python 3.12 | |
| Backend | Django 5.2 (LTS) | Django şablonları ile sunucu taraflı render |
| Veritabanı | Supabase (PostgreSQL) | Django ORM ile doğrudan bağlantı. **Supabase Auth kullanılmaz**, kimlik doğrulama Django'nun kendi sistemiyle yapılır. |
| Frontend | Saf HTML + CSS + JavaScript | Aynı repo içinde, `templates/` ve `static/` klasörlerinde. React/Vue/Tailwind vb. **yok**. |
| Statik dosyalar | WhiteNoise | Vercel üzerinde CSS/JS servis etmek için |
| Deployment | Vercel | `@vercel/python` runtime |

### `requirements.txt`

```
Django>=5.2,<6.0
psycopg[binary]>=3.2
dj-database-url>=2.2
whitenoise>=6.7
python-dotenv>=1.0
```

Bunların dışında paket eklenmez. Ek paket gerekirse önce kullanıcıya sorulur.

---

## 3. Claude Code İçin Çalışma Kuralları

1. **Sadece istenen fazı uygula.** Sonraki fazların işine girme, "hazır yapmışken" ekleme yapma.
2. Her fazın sonunda **Kabul Kriterleri** listesini tek tek kontrol et ve sonucu raporla.
3. Yeni bağımlılık, framework veya build aracı ekleme (npm, webpack, Tailwind vb. yasak).
4. Gizli bilgileri (SECRET_KEY, veritabanı şifresi) asla koda yazma; `.env` kullan, `.env` dosyasını `.gitignore`'a ekle.
5. Arayüz metinleri **Türkçe**, kod (değişken, fonksiyon, sınıf adları) **İngilizce**.
6. Kodu sade tut: class-based view gerekmiyorsa function-based view kullan.
7. Her model değişikliğinden sonra migration oluştur.
8. Her faz sonunda çalıştırılacak komutları (`migrate`, `runserver`, `test`) kullanıcıya listele.

---

## 4. Klasör Yapısı

```
kararsizim/
├── CLAUDE.md
├── README.md
├── manage.py
├── requirements.txt
├── vercel.json
├── .env.example
├── .gitignore
├── config/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── accounts/
│   ├── models.py          # Custom User
│   ├── forms.py           # SignupForm, LoginForm
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   └── tests.py
├── polls/
│   ├── models.py          # Poll, Option, Vote
│   ├── forms.py           # PollCreateForm
│   ├── views.py
│   ├── urls.py
│   ├── voter.py           # Anonim seçmen kimliği (cookie) yardımcıları
│   ├── admin.py
│   └── tests.py
├── templates/
│   ├── base.html
│   ├── partials/
│   │   ├── navbar.html
│   │   ├── messages.html
│   │   └── poll_card.html
│   ├── accounts/
│   │   ├── signup.html
│   │   └── login.html
│   └── polls/
│       ├── home.html
│       ├── detail.html
│       ├── create.html
│       └── my_polls.html
└── static/
    ├── css/
    │   └── main.css
    └── js/
        ├── main.js         # Genel (mobil menü, mesaj kapatma)
        ├── create_poll.js  # Seçenek ekle/çıkar
        └── vote.js         # Oy verme + sonuç çubukları
```

---

## 5. Veri Modeli

### 5.1 `accounts.User` (Custom User Model)

> ⚠️ **Custom user model ilk migration'dan ÖNCE tanımlanmalıdır.** Sonradan değiştirmek çok zordur.

`AbstractUser`'dan türetilir.

| Alan | Tip | Kurallar |
|---|---|---|
| `email` | EmailField | `unique=True`, zorunlu, küçük harfe çevrilerek kaydedilir |
| `username` | CharField(20) | `unique=True`, 3–20 karakter, sadece `a-z A-Z 0-9 _`. Büyük/küçük harf duyarsız benzersizlik (`Ali` varken `ali` alınamaz) |
| `password` | (Django) | Django'nun varsayılan parola doğrulayıcıları, minimum 8 karakter |

- `USERNAME_FIELD = "email"` → giriş e-posta ile yapılır.
- `REQUIRED_FIELDS = ["username"]`
- `first_name`, `last_name` kullanılmaz.

### 5.2 `polls.Poll`

| Alan | Tip | Kurallar |
|---|---|---|
| `author` | FK → User | `on_delete=CASCADE`, `related_name="polls"` |
| `question` | CharField(150) | Zorunlu. Örn: "Bugün sinemaya mı gitsem, tiyatroya mı?" |
| `description` | TextField | İsteğe bağlı, max 500 karakter |
| `is_closed` | BooleanField | Varsayılan `False`. Kapalı ankete oy verilemez (Faz 5) |
| `created_at` | DateTimeField | `auto_now_add=True` |

- Varsayılan sıralama: `-created_at`
- `__str__`: soru metni

### 5.3 `polls.Option`

| Alan | Tip | Kurallar |
|---|---|---|
| `poll` | FK → Poll | `on_delete=CASCADE`, `related_name="options"` |
| `text` | CharField(80) | Zorunlu |
| `order` | PositiveSmallIntegerField | 0–4, seçeneklerin görünme sırası ve renk eşleşmesi için |

- Sıralama: `order`
- Bir ankette aynı metinli iki seçenek olamaz (büyük/küçük harf duyarsız, form seviyesinde kontrol).

### 5.4 `polls.Vote`

| Alan | Tip | Kurallar |
|---|---|---|
| `poll` | FK → Poll | `on_delete=CASCADE`, `related_name="votes"` |
| `option` | FK → Option | `on_delete=CASCADE`, `related_name="votes"` |
| `user` | FK → User | `null=True, blank=True`, `on_delete=SET_NULL` |
| `voter_token` | UUIDField | `null=True, blank=True`, anonim/çerez kimliği |
| `created_at` | DateTimeField | `auto_now_add=True` |

**Veritabanı kısıtları (Meta.constraints):**

- `UniqueConstraint(fields=["poll", "user"], condition=Q(user__isnull=False))` → bir üye bir ankete bir kez oy verir.
- `UniqueConstraint(fields=["poll", "voter_token"], condition=Q(voter_token__isnull=False))` → bir tarayıcı bir ankete bir kez oy verir.
- `CheckConstraint`: `user` veya `voter_token` alanlarından en az biri dolu olmalı.

**Uygulama seviyesi kontrol:** `option.poll_id == poll.id` olmalı (başka anketin seçeneğine oy verilemez).

### 5.5 Seçmen Kimliği Mantığı (`polls/voter.py`)

Üye olmayanların tekrar oy vermesini engellemek için basit çerez yöntemi:

- Çerez adı: `kararsizim_voter`
- Değer: UUID4, süre 1 yıl, `httponly=True`, `samesite="Lax"`, production'da `secure=True`
- Çerez yoksa ilk ziyarette/oy anında oluşturulur.
- **Üye giriş yapmışsa:** Oy kaydına hem `user` hem `voter_token` yazılır. "Daha önce oy verdi mi?" kontrolü `user` **veya** `voter_token` eşleşmesine bakar. (Böylece anonim oy verip sonra giriş yapan kişi aynı ankete ikinci kez oy veremez.)
- **Üye değilse:** sadece `voter_token` ile kontrol edilir.

> Not: Çerez silinerek tekrar oy verilebilir. Prototip için bu kabul edilebilir; ileride IP/hız sınırlama eklenebilir.

### 5.6 Oy Kuralları

- Oy **değiştirilemez ve geri alınamaz** (prototip için sade tutuyoruz).
- Anket sahibi kendi anketine oy verebilir.
- Oy verdikten sonra sonuçlar (yüzde + oy sayısı) gösterilir.
- Oy vermemiş kullanıcı sonuçları görmez; sadece toplam oy sayısını görür. (Böylece kişi sonuçlardan etkilenmeden oy verir.)

---

## 6. Sayfalar ve URL'ler

| URL | View | Erişim | Açıklama |
|---|---|---|---|
| `/` | `home` | Herkes | Anket akışı. 12'li sayfalama. `?sirala=yeni` (varsayılan) veya `?sirala=populer` (oy sayısına göre) |
| `/anket/<int:pk>/` | `poll_detail` | Herkes | Anket detayı, oy verme / sonuçlar |
| `/anket/olustur/` | `poll_create` | Sadece üye | Üye değilse `/giris/?next=/anket/olustur/` adresine yönlenir ve "Anket oluşturmak için giriş yapmalı ya da üye olmalısın" mesajı gösterilir |
| `/anket/<int:pk>/oy/` | `poll_vote` | Herkes | Sadece POST. JSON döner |
| `/anket/<int:pk>/sil/` | `poll_delete` | Sadece anket sahibi | Sadece POST. Onay JS `confirm()` ile |
| `/anket/<int:pk>/kapat/` | `poll_close` | Sadece anket sahibi | Sadece POST (Faz 5) |
| `/anketlerim/` | `my_polls` | Sadece üye | Kullanıcının kendi anketleri |
| `/kayit/` | `signup` | Sadece misafir | Kayıt sonrası otomatik giriş + ana sayfaya yönlendirme |
| `/giris/` | `login` | Sadece misafir | E-posta + parola |
| `/cikis/` | `logout` | Üye | **POST** ile (Django 5 gereği), navbar'da küçük bir form butonu |
| `/admin/` | Django admin | Superuser | |

### 6.1 Oy Endpoint'i Sözleşmesi

**İstek:** `POST /anket/<pk>/oy/`, header'da `X-CSRFToken`, gövde: `{"option_id": 12}`

**Başarılı yanıt (200):**
```json
{
  "ok": true,
  "total_votes": 37,
  "voted_option_id": 12,
  "results": [
    {"id": 12, "text": "Sinema", "votes": 22, "percent": 59},
    {"id": 13, "text": "Tiyatro", "votes": 15, "percent": 41}
  ]
}
```

**Hata yanıtları:**
- `400` → `{"ok": false, "error": "Geçersiz seçenek."}`
- `403` → `{"ok": false, "error": "Bu anket oylamaya kapalı."}`
- `409` → `{"ok": false, "error": "Bu ankete zaten oy verdin."}` + mevcut sonuçlar

Yanıtta **hiçbir kullanıcı e-postası** bulunmaz. Yüzdeler tam sayıya yuvarlanır. Oy sayısı 0 iken yüzde 0 olur (sıfıra bölme hatası olmamalı).

Aynı anda gelen iki istekte unique constraint `IntegrityError` fırlatırsa 409 döndürülür.

---

## 7. Formlar ve Doğrulama

### 7.1 Kayıt Formu (`SignupForm`)
- Alanlar: Kullanıcı adı, E-posta, Parola, Parola (tekrar)
- E-posta benzersiz (büyük/küçük harf duyarsız) → hata: "Bu e-posta zaten kayıtlı."
- Kullanıcı adı benzersiz (büyük/küçük harf duyarsız) → hata: "Bu kullanıcı adı alınmış."
- Kullanıcı adı formatı → hata: "Kullanıcı adı 3-20 karakter olmalı; sadece harf, rakam ve alt çizgi içerebilir."
- Parolalar eşleşmeli, Django doğrulayıcılarından geçmeli. Hata mesajları Türkçe (`LANGUAGE_CODE = "tr"`).
- Formun altında bilgi notu: "E-postan kimseyle paylaşılmaz, anketlerde sadece kullanıcı adın görünür."

### 7.2 Giriş Formu
- E-posta + Parola. Hatalı girişte: "E-posta veya parola hatalı."

### 7.3 Anket Oluşturma Formu (`PollCreateForm`)
- Soru (zorunlu, max 150), Açıklama (isteğe bağlı, max 500)
- Seçenekler: `option_1` … `option_5` alanları, her biri max 80 karakter.
- **Sunucu tarafı doğrulama (asıl güvence):**
  - Boşlukları kırpılmış, dolu seçenek sayısı 2–5 arası olmalı → "En az 2, en fazla 5 seçenek eklemelisin."
  - Aynı seçenek iki kez yazılamaz → "Aynı seçeneği iki kez ekleyemezsin."
- **İstemci tarafı (`create_poll.js`):** Sayfa 2 seçenek kutusuyla açılır. "+ Seçenek ekle" butonu 5'e ulaşınca gizlenir. Her seçeneğin yanında "×" butonu vardır, 2 seçenek kalınca kaldırma butonları devre dışı olur. Karakter sayacı (örn. `45/150`).
- Kayıt işlemi `transaction.atomic()` içinde yapılır (anket + seçenekler birlikte).
- Başarılı oluşturma sonrası anket detay sayfasına yönlendirme + "Anketin yayında! 🎉" mesajı.

---

## 8. Arayüz Tasarımı

### 8.1 Tasarım Yönü
Gençlere hitap eden, **açık arka planlı, canlı renklerin yumuşak tonlarıyla süslenmiş, temiz** bir arayüz. Ferah boşluklar, yuvarlak köşeler, hafif gölgeler. Kalabalık değil, eğlenceli ama okunaklı.

- **Arka plan:** Kırık beyaz zemin (`#FBFAFF`), köşelerinde çok soluk renkli büyük bulanık lekeler (`radial-gradient` ile mor, pembe ve turkuaz tonlar, opaklık düşük). Bu "üstüne ton koyulmuş" hissini verir.
- **Kartlar:** Beyaz yüzey, 20px köşe yarıçapı, çok hafif renkli gölge, hover'da 2px yukarı kalkma.
- **Ana buton:** Mordan pembeye gradyan (`#7C3AED → #EC4899`), beyaz yazı, tam yuvarlak (pill) form.
- **Yazı tipi:** Google Fonts `Plus Jakarta Sans` (400, 500, 700, 800), yedek: `system-ui, -apple-system, "Segoe UI", sans-serif`.
- **Mobil öncelikli** tasarım; kartlar mobilde tek sütun, tablette 2, masaüstünde 3 sütun (CSS Grid).

### 8.2 Renk Paleti (CSS değişkenleri, `:root` içinde)

```css
:root {
  --bg: #FBFAFF;
  --surface: #FFFFFF;
  --text: #1E1B2E;
  --text-muted: #6B6880;
  --border: #ECE8F5;

  --primary: #7C3AED;
  --primary-tint: #F1EAFF;
  --accent: #EC4899;
  --gradient: linear-gradient(135deg, #7C3AED 0%, #EC4899 100%);

  /* Seçenek renkleri: maksimum 5 seçenek = 5 renk */
  --opt-1: #7C3AED; --opt-1-tint: #F1EAFF;  /* mor */
  --opt-2: #EC4899; --opt-2-tint: #FDE7F3;  /* pembe */
  --opt-3: #F97316; --opt-3-tint: #FFEEDD;  /* turuncu */
  --opt-4: #14B8A6; --opt-4-tint: #DDF7F3;  /* turkuaz */
  --opt-5: #3B82F6; --opt-5-tint: #E3EEFF;  /* mavi */

  --success: #16A34A;
  --danger: #DC2626;
  --radius: 20px;
  --shadow: 0 8px 24px rgba(124, 58, 237, 0.08);
}
```

Her seçenek `order` değerine göre kendi rengini alır (1. seçenek mor, 2. pembe ...). Seçenek butonları tint arka planlı, sınırı ve harf rengi ana renkte olur.

### 8.3 Bileşenler

- **Navbar:** Solda logo "Kararsızım 🤔" (gradyan yazı), sağda: misafir için "Giriş Yap" (metin buton) + "Üye Ol" (gradyan buton); üye için "Anket Oluştur", "Anketlerim", `@kullaniciadi` ve "Çıkış". Mobilde hamburger menü.
- **Hero (sadece ana sayfa):** Büyük başlık "Kararsız mı kaldın? Sor, gitsin! ✨", alt metin "Seçeneklerini yaz, herkes oy versin, kararını ver." ve "Anket Oluştur" butonu.
- **Sıralama sekmeleri:** "🆕 En Yeni" / "🔥 Popüler" — pill şeklinde, aktif olan dolu renkli.
- **Anket kartı (`poll_card.html`):** Soru (kalın), `@kullaniciadi · 2 saat önce` (Django `timesince`), seçeneklerin renkli küçük etiketleri (chip), alt kısımda "🗳️ 37 oy" ve "Oy ver →" bağlantısı.
- **Anket detay sayfası:**
  - Oy verilmemişse: seçenekler büyük, tıklanabilir renkli butonlar olarak listelenir. Tıklayınca seçilir, "Oyumu Ver" butonu aktifleşir.
  - Oy verildikten sonra: her seçenek için sonuç çubuğu. Çubuk seçeneğin renginde, genişliği yüzde kadar, 0'dan animasyonla dolar (`transition: width .6s ease`). Kullanıcının seçtiği seçeneğin yanında "✓ Senin oyun" etiketi. En çok oy alan seçenekte "👑" işareti.
  - Sayfa yenilemeden çalışır (`vote.js` → `fetch`). JS kapalıysa normal form POST'u da çalışır ve sayfa yeniden yüklenir (progressive enhancement).
  - Anket sahibine "Sil" butonu (ve Faz 5'te "Oylamayı Kapat").
  - "🔗 Bağlantıyı Kopyala" butonu (`navigator.clipboard`).
- **Mesajlar:** Django messages framework, sayfanın üstünde renkli tint kutular, 4 saniye sonra kaybolur ve "×" ile kapatılabilir.
- **Boş durum:** Hiç anket yoksa sevimli bir mesaj: "Henüz anket yok. İlk kararsız sen ol! 😄" + buton.
- **Formlar:** Geniş girdi kutuları, odakta mor halka (`outline` / `box-shadow`), hatalar kutunun altında kırmızı küçük metin.

### 8.4 Erişilebilirlik
- Tüm girdi kutularında `<label>`.
- Klavye ile odak görünür (`:focus-visible`).
- Renk tek başına anlam taşımaz; sonuçlarda yüzde ve oy sayısı metin olarak da yazılır.
- Metin/arka plan kontrastı en az WCAG AA.
- `prefers-reduced-motion` ayarında animasyonlar kapatılır.

---

## 9. Ayarlar ve Ortam Değişkenleri

### `.env.example`
```
SECRET_KEY=degistir-beni
DEBUG=True
DATABASE_URL=postgresql://postgres.PROJE_ID:SIFRE@aws-0-REGION.pooler.supabase.com:6543/postgres
ALLOWED_HOSTS=localhost,127.0.0.1,.vercel.app
CSRF_TRUSTED_ORIGINS=https://*.vercel.app
```

### `settings.py` önemli noktalar
- `python-dotenv` ile `.env` okunur.
- `DATABASE_URL` yoksa yerel geliştirme için **SQLite**'a düşülür (Faz 0'da Supabase olmadan da çalışabilmek için).
- `AUTH_USER_MODEL = "accounts.User"`
- `LANGUAGE_CODE = "tr"`, `TIME_ZONE = "Europe/Istanbul"`, `USE_TZ = True`
- `LOGIN_URL = "/giris/"`, `LOGIN_REDIRECT_URL = "/"`, `LOGOUT_REDIRECT_URL = "/"`
- `TEMPLATES` → `DIRS: [BASE_DIR / "templates"]`
- `STATIC_URL = "/static/"`, `STATICFILES_DIRS = [BASE_DIR / "static"]`, `STATIC_ROOT = BASE_DIR / "staticfiles"`
- WhiteNoise middleware `SecurityMiddleware`'den hemen sonra.
- Production'da (`DEBUG=False`): `SESSION_COOKIE_SECURE`, `CSRF_COOKIE_SECURE`, `SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")`.

### Supabase bağlantısı (önemli)
Vercel serverless çalıştığı için Supabase'in **Transaction Pooler** bağlantısı (port **6543**) kullanılır. Bunun için:

```python
DATABASES = {"default": dj_database_url.config(conn_max_age=0, ssl_require=True)}
DATABASES["default"]["DISABLE_SERVER_SIDE_CURSORS"] = True
DATABASES["default"].setdefault("OPTIONS", {})["prepare_threshold"] = None  # pgbouncer/supavisor uyumu
```

(SQLite'a düşüldüğünde bu Postgres'e özgü ayarlar uygulanmaz.)

### Supabase güvenlik notu
Supabase, `public` şemasındaki tabloları otomatik REST API ile dışarı açar. Django tablolarının bu API üzerinden okunmasını engellemek için **tüm tablolarda Row Level Security (RLS) açılır, hiç policy eklenmez.** Django `postgres` rolüyle bağlandığı için RLS'den etkilenmez. Bu işlem bir veri migration'ı (`RunSQL`) veya Supabase SQL Editor'den tek seferlik bir sorguyla yapılır (Faz 4).

---

## 10. Fazlar

Her faz bağımsız bir Claude Code oturumunda verilebilir. Bir faz bitip kullanıcı onaylamadan sonrakine geçilmez.

---

### FAZ 0 — Proje İskeleti ve Kurulum

**Amaç:** Çalışan boş bir Django projesi, custom user modeli ve temel şablon.

**Görevler:**
1. `config` adlı Django projesi, `accounts` ve `polls` uygulamaları.
2. `requirements.txt`, `.env.example`, `.gitignore` (`.env`, `__pycache__`, `*.sqlite3`, `staticfiles/`, `.venv/`, `.vercel/`).
3. `settings.py` → Bölüm 9'daki tüm ayarlar (SQLite yedeği dahil).
4. `accounts.User` custom user modeli (Bölüm 5.1). **İlk migration bu modelle yapılır.**
5. `base.html` (navbar ve mesaj partial'larıyla), `static/css/main.css` içinde CSS değişkenleri, arka plan tonları ve temel tipografi.
6. Ana sayfada geçici bir hero bölümü.
7. Django admin'e User kaydı.
8. `README.md`: kurulum adımları (venv, `pip install`, `.env`, `migrate`, `createsuperuser`, `runserver`).

**Kabul Kriterleri:**
- [ ] `python manage.py runserver` hatasız açılıyor, ana sayfa yeni tasarım renkleriyle görünüyor.
- [ ] `AUTH_USER_MODEL` ayarlı ve ilk migration custom user ile oluşturulmuş.
- [ ] `.env` olmadan SQLite ile çalışıyor; `DATABASE_URL` verilince Supabase'e bağlanıyor.
- [ ] Admin paneline giriş yapılabiliyor.

**Claude Code promptu:**
```
CLAUDE.md dosyasını baştan sona oku. Şimdi sadece FAZ 0'ı uygula.
Bölüm 2, 4, 5.1, 8.2 ve 9'a uy. Sonraki fazlara ait hiçbir şey yazma.
Bitince kabul kriterlerini tek tek kontrol et ve çalıştırmam gereken komutları listele.
```

---

### FAZ 1 — Üyelik Sistemi

**Amaç:** Kayıt ol, giriş yap, çıkış yap.

**Görevler:**
1. `SignupForm` ve giriş formu (Bölüm 7.1, 7.2), e-posta ve kullanıcı adı için büyük/küçük harf duyarsız benzersizlik.
2. `/kayit/`, `/giris/`, `/cikis/` view'ları ve URL'leri. Giriş yapmış kullanıcı kayıt/giriş sayfasına girerse ana sayfaya yönlenir.
3. Kayıt sonrası otomatik giriş.
4. `signup.html`, `login.html`: ortalanmış kart tasarımı, Türkçe hata mesajları, "Hesabın yok mu? Üye ol" / "Zaten üye misin? Giriş yap" bağlantıları.
5. Navbar'ın misafir ve üye durumuna göre değişmesi; çıkış POST formu ile.
6. `?next=` parametresinin giriş ve kayıt sonrası doğru çalışması (güvenli yönlendirme için `url_has_allowed_host_and_scheme`).
7. `accounts/tests.py`: kayıt, mükerrer e-posta, mükerrer kullanıcı adı (`Ali`/`ali`), geçersiz kullanıcı adı, giriş testleri.

**Kabul Kriterleri:**
- [ ] Kayıt → otomatik giriş → navbar'da `@kullaniciadi` görünüyor.
- [ ] Aynı e-posta veya kullanıcı adı (harf büyüklüğü farklı olsa bile) ikinci kez alınamıyor.
- [ ] E-posta navbar dahil hiçbir yerde görünmüyor.
- [ ] Çıkış POST ile çalışıyor.
- [ ] `python manage.py test accounts` geçiyor.

**Claude Code promptu:**
```
CLAUDE.md'yi oku. FAZ 0 tamamlandı. Şimdi sadece FAZ 1'i uygula (Bölüm 5.1, 6, 7.1, 7.2, 8.3).
Anket modellerine dokunma. Bitince kabul kriterlerini kontrol et ve testleri çalıştır.
```

---

### FAZ 2 — Anket Oluşturma, Listeleme ve Detay

**Amaç:** Üyeler anket oluşturur, herkes anketleri görür.

**Görevler:**
1. `Poll` ve `Option` modelleri (Bölüm 5.2, 5.3) + migration + admin kaydı (Option, Poll içinde inline).
2. `PollCreateForm` ve sunucu tarafı doğrulama (Bölüm 7.3).
3. `create_poll.js`: dinamik seçenek ekleme/çıkarma (2–5), karakter sayaçları.
4. `/anket/olustur/` → `login_required`; misafir yönlendirildiğinde bilgi mesajı.
5. `/` ana sayfa: hero, sıralama sekmeleri (Popüler sıralaması Faz 3'te oylar gelince anlam kazanır; şimdilik `Count("votes")` yerine yeni→eski sıralama kullanılabilir, sekme yine görünür), 12'li sayfalama, anket kartları, boş durum.
6. `/anket/<pk>/` detay sayfası: soru, açıklama, `@kullaniciadi`, tarih, seçenekler renkli olarak (oy butonları henüz pasif/görsel).
7. `/anketlerim/` sayfası.
8. `/anket/<pk>/sil/` → sadece sahibi, POST, `confirm()` onayı. Başkası denerse 403.
9. Sorgu verimliliği: listede `select_related("author")`, `prefetch_related("options")`.
10. `polls/tests.py`: 1 seçenek reddedilir, 6 seçenek reddedilir, tekrar eden seçenek reddedilir, misafir oluşturma sayfasında login'e yönlenir, başkasının anketi silinemez.

**Kabul Kriterleri:**
- [ ] Misafir "Anket Oluştur"a basınca girişe yönleniyor ve mesaj görüyor.
- [ ] Üye 2–5 seçenekli anket oluşturabiliyor; kurallar hem JS hem sunucu tarafında uygulanıyor.
- [ ] Ana sayfada ve detayda sadece kullanıcı adı görünüyor (HTML kaynağında da e-posta yok).
- [ ] Mobil, tablet ve masaüstünde kart ızgarası düzgün.
- [ ] `python manage.py test` geçiyor.

**Claude Code promptu:**
```
CLAUDE.md'yi oku. FAZ 0 ve 1 tamamlandı. Şimdi sadece FAZ 2'yi uygula
(Bölüm 5.2, 5.3, 6, 7.3, 8). Vote modelini ve oy verme mantığını henüz yazma.
Bitince kabul kriterlerini kontrol et ve testleri çalıştır.
```

---

### FAZ 3 — Oylama ve Sonuçlar

**Amaç:** Herkes (üye/misafir) her ankete bir kez oy verebilir, sonuçları görür.

**Görevler:**
1. `Vote` modeli ve kısıtları (Bölüm 5.4) + migration.
2. `polls/voter.py`: çerez tabanlı seçmen kimliği (Bölüm 5.5) — `get_or_create_voter_token(request)`, `has_voted(request, poll)`, `get_user_vote(request, poll)`.
3. `/anket/<pk>/oy/` endpoint'i (Bölüm 6.1): JSON sözleşmesi, `IntegrityError` → 409, çerezi yanıtta ayarlama.
4. JS kapalıyken form POST desteği (aynı view, `Accept`/istek türüne göre JSON veya redirect döner).
5. `vote.js`: seçenek seçme, `fetch` ile oy gönderme (`X-CSRFToken` çerezden okunur), sonuç çubuklarını animasyonla çizme, "✓ Senin oyun" ve "👑" işaretleri, hata mesajlarını gösterme, gönderim sırasında butonu kilitleme.
6. Detay sayfası: oy verilmişse sayfa doğrudan sonuçlarla açılır (sunucu tarafında hesaplanmış).
7. Kartlarda ve detayda toplam oy sayısı (`annotate(vote_count=Count("votes"))`); ana sayfada "Popüler" sıralaması oy sayısına göre.
8. "🔗 Bağlantıyı Kopyala" butonu.
9. Testler: misafir oy verebilir, aynı çerezle ikinci oy 409, üye ikinci kez oy veremez, anonim oy verip giriş yapan kişi tekrar oy veremez, başka anketin seçeneğiyle oy 400, JSON yanıtında e-posta yok, 0 oyda yüzde hesaplaması hatasız.

**Kabul Kriterleri:**
- [ ] Misafir ve üye oy verebiliyor; sayfa yenilenmeden sonuçlar animasyonla görünüyor.
- [ ] Aynı kişi aynı ankete ikinci kez oy veremiyor.
- [ ] Sayfa yenilenince kişi sonuç görünümünü görüyor.
- [ ] Oy vermemiş kişi sadece toplam oy sayısını görüyor.
- [ ] "Popüler" sekmesi oy sayısına göre sıralıyor.
- [ ] `python manage.py test` geçiyor.

**Claude Code promptu:**
```
CLAUDE.md'yi oku. FAZ 0, 1 ve 2 tamamlandı. Şimdi sadece FAZ 3'ü uygula
(Bölüm 5.4, 5.5, 5.6, 6.1, 8.3). Bitince kabul kriterlerini kontrol et ve testleri çalıştır.
```

---

### FAZ 4 — Supabase + Vercel Deployment

**Amaç:** Prototipi internete çıkarmak.

**Görevler:**
1. Supabase projesinin bağlantı ayarlarını doğrula (Bölüm 9, Transaction Pooler, port 6543).
2. RLS'yi tüm uygulama ve Django tablolarında açan bir migration (`RunSQL`, sadece PostgreSQL'de çalışacak şekilde; SQLite'ta atlanır). Policy eklenmez.
3. `config/wsgi.py` içinde Vercel için `app = application` satırı.
4. `vercel.json`:
   ```json
   {
     "builds": [{ "src": "config/wsgi.py", "use": "@vercel/python" }],
     "routes": [{ "src": "/(.*)", "dest": "config/wsgi.py" }]
   }
   ```
   > Claude Code: Vercel'in Python/Django desteği zamanla değişebiliyor. Bu yapılandırmayı uygulamadan önce Vercel'in güncel Python runtime dokümantasyonunu kontrol et; daha sade bir resmi yöntem varsa onu öner ve kullanıcıya sor.
5. Statik dosyalar: WhiteNoise ile servis. Prototip için `collectstatic` build adımı gerektirmeyen yaklaşım: `WHITENOISE_USE_FINDERS = True`. (Kalıcı çözüm olarak build adımında `collectstatic` ileride eklenebilir.)
6. Migration'lar Vercel'de **çalıştırılmaz**; yerel makineden Supabase'e karşı `python manage.py migrate` ile yapılır. README'ye yaz.
7. README'ye deployment rehberi: Vercel'de ortam değişkenleri (`SECRET_KEY`, `DEBUG=False`, `DATABASE_URL`, `ALLOWED_HOSTS`, `CSRF_TRUSTED_ORIGINS`), GitHub reposu bağlama, ilk deploy.
8. `python manage.py check --deploy` uyarılarını gözden geçir, prototip için gerekli olanları düzelt.

**Kabul Kriterleri:**
- [ ] Vercel adresinde site açılıyor, CSS/JS yükleniyor.
- [ ] Kayıt, giriş, anket oluşturma ve oy verme canlıda çalışıyor.
- [ ] Supabase tablolarında RLS açık; veriler Supabase REST API'den anon key ile okunamıyor.
- [ ] Hiçbir gizli bilgi repoda yok.

**Claude Code promptu:**
```
CLAUDE.md'yi oku. FAZ 0–3 tamamlandı. Şimdi sadece FAZ 4'ü uygula (Bölüm 9 ve Faz 4 görevleri).
vercel.json'u yazmadan önce Vercel'in güncel Python dokümantasyonunu kontrol et.
Benim manuel yapmam gereken adımları (Supabase panelinde, Vercel panelinde) ayrıca numaralı liste olarak yaz.
```

---

### FAZ 5 — Cila ve Küçük Eklemeler (isteğe bağlı)

Prototip çalıştıktan sonra, kullanıcı hangilerini isterse:

- Anket sahibinin oylamayı kapatması (`is_closed`, `/anket/<pk>/kapat/`), kapalı anketlerde "🔒 Oylama kapandı" rozeti.
- Ana sayfada basit arama (soru metninde `icontains`).
- Özel 404 ve 500 sayfaları (tasarıma uygun, eğlenceli metinlerle).
- Sosyal paylaşım için `<meta>` Open Graph etiketleri (anket sorusu başlık olarak).
- Basit hız sınırlama (aynı çerezden dakikada X oy) — ek paket olmadan, Django cache ile.
- Favicon ve logo SVG'si.

**Claude Code promptu:**
```
CLAUDE.md'yi oku. FAZ 0–4 tamamlandı. FAZ 5 listesinden sadece şunları uygula: [buraya seçtiklerini yaz].
```

---

## 11. Kapsam Dışı (Prototipte YOK)

- Takip etme / takipçi sistemi
- Yorumlar, beğeniler, bildirimler
- Profil fotoğrafı, kullanıcı profili sayfası
- E-posta doğrulama ve şifre sıfırlama (ileride eklenebilir)
- Sosyal medya ile giriş
- Oy değiştirme / geri alma
- Anketlere görsel ekleme
- Anket bitiş süresi (zamanlayıcı)
- Frontend framework'leri, npm, build araçları

---

## 12. Sözlük (Arayüz Metinleri)

| Anahtar | Metin |
|---|---|
| Uygulama adı | Kararsızım |
| Slogan | Kararsız mı kaldın? Sor, gitsin! ✨ |
| Ana buton | Anket Oluştur |
| Oy butonu | Oyumu Ver |
| Oy sonrası | Teşekkürler! İşte sonuçlar 👇 |
| Zaten oy verdi | Bu ankete zaten oy verdin. |
| Misafir uyarısı | Anket oluşturmak için giriş yapmalı ya da üye olmalısın. |
| Anket yayında | Anketin yayında! 🎉 |
| Silme onayı | Bu anketi silmek istediğine emin misin? Bu işlem geri alınamaz. |
| Boş liste | Henüz anket yok. İlk kararsız sen ol! 😄 |
| Gizlilik notu | E-postan kimseyle paylaşılmaz, anketlerde sadece kullanıcı adın görünür. |
