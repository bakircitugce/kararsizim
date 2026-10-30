# Kararsızım

Kararsız kalan kullanıcıların seçeneklerini paylaşarak diğer kullanıcılara danışabildiği Django web uygulaması.

## Yerel kurulum

Python 3.12 ve Git kurulu olmalıdır.

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

`.env` dosyasındaki `DATABASE_URL` boş bırakılırsa yerel SQLite kullanılır. Supabase bağlantısı için bu değişkeni transaction pooler adresiyle doldurun.

## Kontrol komutları

```powershell
python manage.py check
python manage.py test
```

Proje fazları, veri modeli ve kabul kriterleri için [CLAUDE.md](./CLAUDE.md) dosyasına bakın.
