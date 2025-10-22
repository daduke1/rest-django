# rest-django

Pequeño proyecto **Django + Django REST Framework** con apps de ejemplo y configuración lista para correr localmente o con Docker Compose.

> Estructura principal del repositorio (rama `api`): `lms/`, `polls/`, `project/`, `manage.py`, `requirements.txt`, `Dockerfile`, `docker-compose.yaml`.

---

## 🧩 Requisitos

### Opción A — Docker (recomendada)
- Docker Desktop 4.x+
- Docker Compose (incluido en Docker Desktop)

### Opción B — Local (sin Docker)
- Python 3.11+ (recomendado)
- `git`
- (Windows) PowerShell o Git Bash; (macOS/Linux) bash/zsh
- Virtualenv (`python -m venv`)

> Este proyecto usa **Django REST Framework** para exponer una API web navegable.

---

## ⚙️ Variables de entorno

Crea un archivo **`.env`** en la raíz del repo (mismo nivel que `docker-compose.yaml` y `manage.py`) con valores como:

```ini
# Django
DJANGO_DEBUG=1
DJANGO_SECRET_KEY=dev-secret-change-me
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1

# Base de datos (Docker usa estos por defecto)
POSTGRES_DB=appdb
POSTGRES_USER=appuser
POSTGRES_PASSWORD=apppass
POSTGRES_HOST=db
POSTGRES_PORT=5432
```
A) Con Docker (recomendado)

1️⃣ Clona y entra al proyecto:
```
git clone https://github.com/daduke1/rest-django.git
cd rest-django
git checkout api
```

2️⃣ Crea el archivo .env (ver sección anterior).

3️⃣ Levanta los servicios (con build inicial):
```
docker compose up --build
```

4️⃣ Aplica migraciones y crea superusuario (en otra terminal):
```
docker compose exec web python manage.py migrate
docker compose exec web python manage.py createsuperuser
```

5️⃣ Navega:

App/API: http://localhost:8500/

Admin: http://localhost:8500/admin/

Para apagar:
```
docker compose down
```

Para reconstruir imágenes después de cambios en dependencias:
```
docker compose build --no-cache
```
B) Sin Docker (entorno local)

1️⃣ Clona y entra al proyecto:
```
git clone https://github.com/daduke1/rest-django.git
cd rest-django
git checkout api
```

2️⃣ Crea y activa un entorno virtual:
```
python -m venv .venv
# Windows
. .venv/Scripts/activate
# macOS/Linux
source .venv/bin/activate
```

3️⃣ Instala dependencias:
```
pip install --upgrade pip
pip install -r requirements.txt
```

4️⃣ Configura tu .env:

Opción SQLite (simple): ajusta settings.py para usar SQLite en modo DEBUG.

Opción Postgres local: exporta las variables POSTGRES_* según tu configuración.

5️⃣ Migraciones y superusuario:
```
python manage.py migrate
python manage.py createsuperuser
```

6️⃣ Ejecuta el servidor:
```
python manage.py runserver
```

Visita:

App/API: http://127.0.0.1:8500/

Admin: http://127.0.0.1:8500/admin/

🔧 Comandos útiles
# Aplicar migraciones
```
python manage.py makemigrations
python manage.py migrate
```
# Crear superusuario
```
python manage.py createsuperuser
```
# Correr tests (si existieran)
```
python manage.py test
```

📂 Estructura del proyecto
rest-django/
│
├── project/           # Configuración global de Django (settings, urls, wsgi)
├── lms/               # App principal (modelos, vistas, serializers)
├── polls/             # App de ejemplo (similar a la clásica demo de Django)
├── manage.py          # CLI de Django
├── requirements.txt   # Dependencias
├── Dockerfile
└── docker-compose.yaml


Confirma en project/urls.py los endpoints expuestos (por ejemplo, /, /admin/, /api/).

🧰 Troubleshooting
1️⃣ Error de Docker en Windows con WSL2 (overlayfs)

Si ves algo como:

failed to stat parent: ... snapshots/.../fs: no such file or directory


Prueba:
```
wsl --shutdown
# Reabre Docker Desktop
docker compose up --build
```

Si persiste:
```
docker builder prune -f
docker system prune -f
docker volume rm django_docker_postgres_data
docker compose build --no-cache
docker compose up
```
2️⃣ Migraciones: “relation does not exist”

Asegúrate de correr migrate dentro del contenedor:

docker compose exec web python manage.py migrate


Si cambiaste modelos, corre también makemigrations.

3️⃣ Variables de entorno no leídas

Asegúrate de que .env esté en la raíz.

Verifica que settings.py use os.getenv().

Si usas Docker, revisa que el servicio web cargue env_file: .env.
