# Learning Management System (LMS)

Sistema de gestión de aprendizaje completo construido con Django 5.2 y Django REST Framework. Esta plataforma permite a instructores crear y gestionar cursos, mientras que los estudiantes pueden inscribirse, acceder al contenido y dejar reseñas. El proyecto incluye una API REST completa con documentación interactiva mediante Swagger/ReDoc, autenticación con Django Allauth (incluyendo OAuth2 con Google), y una interfaz web funcional.

## Características

### Para estudiantes
- **Exploración de cursos**: Navega por todos los cursos disponibles con información detallada
- **Inscripciones**: Inscríbete en cursos con un solo clic
- **Mis cursos**: Panel personalizado para ver todos tus cursos inscritos
- **Reseñas y calificaciones**: Deja reseñas y califica cursos (1-5 estrellas)
- **Progreso de aprendizaje**: Rastrea tu progreso en cada curso

### Para instructores
- **Gestión de cursos**: Crea, edita y publica cursos con descripciones, precios y miniaturas
- **Lecciones**: Organiza el contenido del curso en lecciones ordenadas
- **Videos**: Soporte para videos mediante URLs externas
- **Control de visibilidad**: Publica o mantén cursos en borrador
- **Estadísticas**: Visualiza el número de inscripciones por curso

### Funcionalidades técnicas
- **API REST completa**: Endpoints para cursos, lecciones, inscripciones y reseñas
- **Documentación interactiva**: Swagger UI y ReDoc para explorar la API
- **Autenticación flexible**: 
  - Registro e inicio de sesión tradicional
  - OAuth2 con Google
  - Verificación de email obligatoria
- **Filtrado y búsqueda**: Búsqueda avanzada y filtros en la API
- **Paginación**: Respuestas paginadas para mejor rendimiento
- **Subida de archivos**: Gestión de imágenes para miniaturas de cursos
- **Base de datos PostgreSQL**: Configuración lista para producción

## 🛠️ Stack tecnológico

- **Backend**: Django 5.2.6
- **API**: Django REST Framework 3.16.1
- **Base de datos**: PostgreSQL 15
- **Autenticación**: Django Allauth 65.12.0
- **Documentación API**: drf-yasg 1.21.7
- **Filtros**: django-filter 24.2
- **Procesamiento de imágenes**: Pillow 11.3.0
- **Contenedorización**: Docker & Docker Compose

## Requisitos

### Opción A — Docker (recomendada)
- Docker Desktop 4.x o superior
- Docker Compose (incluido en Docker Desktop)

### Opción B — Entorno local
- Python 3.11 o superior
- PostgreSQL 15 (o usar SQLite para desarrollo)
- `git`
- Virtualenv (`python -m venv`)

## Configuración

### Variables de entorno

Sigue el .env.example

> **Nota**: Para Gmail, necesitarás generar una "Contraseña de aplicación" en la configuración de tu cuenta de Google. No uses tu contraseña normal.

## Instalación y ejecución

### Opción A: Con Docker (recomendada)

1. **Clona el repositorio**:
```bash
git clone https://github.com/daduke1/rest-django.git
cd rest-django
```

2. **Crea el archivo `.env`**

3. **Construye y levanta los servicios**:
```bash
docker compose up --build
```

4. **En otra terminal, aplica las migraciones y crea un superusuario**:
```bash
docker compose exec web python manage.py migrate
docker compose exec web python manage.py createsuperuser
```

5. **Accede a la aplicación**:
   - **Aplicación web**: http://localhost:8500/
   - **Panel de administración**: http://localhost:8500/admin/
   - **API Swagger**: http://localhost:8500/swagger/
   - **API ReDoc**: http://localhost:8500/redoc/

6. **Para detener los servicios**:
```bash
docker compose down
```

7. **Para reconstruir las imágenes** (después de cambios en `requirements.txt`):
```bash
docker compose build --no-cache
docker compose up
```

### Opción B: Sin Docker (entorno local)

1. **Clona el repositorio**:
```bash
git clone https://github.com/daduke1/rest-django.git
cd rest-django
git checkout api
```

2. **Crea y activa un entorno virtual**:
```bash
# Crear entorno virtual
python -m venv venv

# Activar (Windows)
venv\Scripts\activate

# Activar (macOS/Linux)
source venv/bin/activate
```

3. **Instala las dependencias**:
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

4. **Configura la base de datos**:

   **Opción SQLite (simple para desarrollo)**:
   - Modifica `project/settings.py` para usar SQLite en lugar de PostgreSQL
   - Cambia la configuración de `DATABASES` a:
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.sqlite3',
           'NAME': BASE_DIR / 'db.sqlite3',
       }
   }
   ```

   **Opción PostgreSQL (recomendada)**:
   - Asegúrate de tener PostgreSQL instalado y corriendo
   - Crea una base de datos:
   ```bash
   createdb mydatabase
   ```
   - Ajusta las variables de entorno `POSTGRES_*` en tu `.env` o directamente en `settings.py`

5. **Aplica las migraciones y crea un superusuario**:
```bash
python manage.py migrate
python manage.py createsuperuser
```

6. **Ejecuta el servidor de desarrollo**:
```bash
python manage.py runserver
```

7. **Accede a la aplicación**:
   - **Aplicación web**: http://127.0.0.1:8000/
   - **Panel de administración**: http://127.0.0.1:8000/admin/
   - **API Swagger**: http://127.0.0.1:8000/swagger/
   - **API ReDoc**: http://127.0.0.1:8000/redoc/

## 📂 Estructura del proyecto

```
rest-django/
│
├── project/              # Configuración global de Django
│   ├── settings.py       # Configuración principal (apps, middleware, BD, etc.)
│   ├── urls.py          # URLs principales del proyecto
│   ├── wsgi.py          # WSGI config para despliegue
│   └── asgi.py          # ASGI config para despliegue
│
├── lms/                 # Aplicación principal del LMS
│   ├── models.py        # Modelos: Course, Lesson, Enrollment, Review
│   ├── views.py         # Vistas (funciones y ViewSets para API)
│   ├── serializers.py   # Serializers para la API REST
│   ├── urls.py          # URLs de la API
│   ├── forms.py         # Formularios Django
│   ├── admin.py         # Configuración del panel de administración
│   ├── signals.py       # Señales de Django
│   ├── templates/       # Plantillas HTML
│   │   ├── index.html
│   │   ├── course_detail.html
│   │   ├── my_courses.html
│   │   └── account/     # Templates de autenticación
│   └── migrations/      # Migraciones de base de datos
│
├── polls/               # Aplicación de ejemplo (demo de Django)
│   ├── models.py
│   ├── views.py
│   └── templates/
│
├── media/               # Archivos subidos por usuarios (imágenes, etc.)
│   └── courses/
│       └── thumbnails/  # Miniaturas de cursos
│
├── manage.py           # CLI de Django
├── requirements.txt    # Dependencias de Python
├── Dockerfile          # Configuración de Docker
├── docker-compose.yaml # Orquestación de servicios
└── README.md          # Este archivo
```

## API REST

El proyecto expone una API REST completa bajo el prefijo `/api/`. Todos los endpoints requieren autenticación excepto las operaciones de lectura (GET) en cursos y lecciones.

### Endpoints principales

- **`/api/courses/`** - CRUD de cursos
  - `GET /api/courses/` - Lista todos los cursos (con filtros y búsqueda)
  - `POST /api/courses/` - Crea un nuevo curso (requiere autenticación)
  - `GET /api/courses/{id}/` - Detalles de un curso
  - `PUT/PATCH /api/courses/{id}/` - Actualiza un curso
  - `DELETE /api/courses/{id}/` - Elimina un curso

- **`/api/lessons/`** - CRUD de lecciones
  - Similar estructura a cursos
  - Filtrable por curso: `/api/lessons/?course={course_id}`

- **`/api/enrollments/`** - Gestión de inscripciones
  - `GET /api/enrollments/` - Lista tus inscripciones
  - `POST /api/enrollments/` - Inscríbete en un curso

- **`/api/reviews/`** - Reseñas y calificaciones
  - `GET /api/reviews/` - Lista reseñas (filtrable por curso)
  - `POST /api/reviews/` - Crea una reseña (requiere autenticación)

### Autenticación en la API

La API soporta dos métodos de autenticación:

1. **Session Authentication**: Para uso desde el navegador
2. **Token Authentication**: Para aplicaciones cliente
   - Obtén un token en: `/api-auth/login/`
   - Usa el header: `Authorization: Token <tu-token>`

### Documentación interactiva

- **Swagger UI**: http://localhost:8500/swagger/
- **ReDoc**: http://localhost:8500/redoc/
- **Schema JSON**: http://localhost:8500/swagger.json
- **Schema YAML**: http://localhost:8500/swagger.yaml

## 🎯 Funcionalidades web

### Rutas principales

- **`/`** - Página de inicio con listado de cursos
- **`/course/<slug>/`** - Detalle de un curso (información, lecciones, reseñas)
- **`/course/<slug>/enroll/`** - Inscripción en un curso (POST)
- **`/my-courses/`** - Panel personal de cursos inscritos
- **`/accounts/login/`** - Inicio de sesión
- **`/accounts/signup/`** - Registro de nuevo usuario
- **`/accounts/google/login/`** - Inicio de sesión con Google
- **`/admin/`** - Panel de administración de Django

### Autenticación

El sistema utiliza **Django Allauth** para la autenticación, lo que proporciona:

- Registro con verificación de email obligatoria
- Inicio de sesión tradicional
- OAuth2 con Google
- Recuperación de contraseña
- Gestión de sesiones

> **Importante**: Para que funcione el login con Google, necesitas configurar las credenciales OAuth2 en el panel de administración de Django (Social Applications).

## Comandos útiles

### Gestión de base de datos

```bash
# Crear migraciones después de cambios en modelos
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Ver el SQL de una migración
python manage.py sqlmigrate lms 0001
```

### Usuarios y permisos

```bash
# Crear superusuario
python manage.py createsuperuser

# Cambiar contraseña de usuario
python manage.py changepassword <username>
```

### Desarrollo

```bash
# Ejecutar servidor de desarrollo
python manage.py runserver

# Ejecutar con puerto específico
python manage.py runserver 0.0.0.0:8500

# Ejecutar tests
python manage.py test

# Ejecutar tests de una app específica
python manage.py test lms
```

### Docker

```bash
# Ver logs
docker compose logs -f web

# Ejecutar comando en el contenedor
docker compose exec web python manage.py <comando>

# Acceder al shell de Django
docker compose exec web python manage.py shell

# Reconstruir sin caché
docker compose build --no-cache
```

## Solución de problemas

### 1. Error de Docker en Windows con WSL2

Si encuentras errores relacionados con `overlayfs` o `snapshots`:

```bash
# Reinicia WSL2
wsl --shutdown

# Reabre Docker Desktop y luego:
docker compose up --build
```

Si persiste el problema:

```bash
# Limpia el sistema de Docker
docker builder prune -f
docker system prune -f

# Elimina el volumen de PostgreSQL (¡cuidado, perderás datos!)
docker volume rm django_docker_postgres_data

# Reconstruye todo
docker compose build --no-cache
docker compose up
```

### 2. Error "relation does not exist" en PostgreSQL

Asegúrate de haber aplicado las migraciones:

```bash
# Con Docker
docker compose exec web python manage.py migrate

# Localmente
python manage.py migrate
```

Si cambiaste los modelos, también necesitas crear las migraciones:

```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. Variables de entorno no se leen

- Verifica que el archivo `.env` esté en la raíz del proyecto
- Asegúrate de que `settings.py` use `os.getenv()` para leer las variables
- Si usas Docker, verifica que `docker-compose.yaml` tenga `env_file: .env` en el servicio web

### 4. Error de conexión a la base de datos

**Con Docker**:
- Verifica que el servicio `db` esté corriendo: `docker compose ps`
- Revisa los logs: `docker compose logs db`
- Asegúrate de que `POSTGRES_HOST=db` en tu `.env`

**Localmente**:
- Verifica que PostgreSQL esté corriendo
- Confirma las credenciales en `settings.py` o `.env`
- Prueba la conexión: `psql -U user -d mydatabase`

### 5. Error al subir imágenes

- Verifica que la carpeta `media/` exista y tenga permisos de escritura
- En producción, configura correctamente `MEDIA_ROOT` y `MEDIA_URL` en `settings.py`
- Con Docker, asegúrate de que el volumen esté montado correctamente

### 6. Email de verificación no se envía

- Verifica las credenciales de email en `.env` (`EMAIL_HOST_USER` y `EMAIL_HOST_PASSWORD`)
- Para Gmail, usa una "Contraseña de aplicación", no tu contraseña normal
- Revisa los logs del servidor para ver errores de SMTP
- En desarrollo, puedes usar el backend de consola: `EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'`

## Modelos de datos

### Course (Curso)
- `title`: Título del curso
- `slug`: URL amigable (generado automáticamente)
- `description`: Descripción completa
- `short_description`: Descripción breve
- `instructor`: Usuario que crea el curso
- `thumbnail`: Imagen miniatura
- `price`: Precio del curso
- `is_published`: Si está publicado o en borrador
- `created_at`, `updated_at`: Fechas de creación y actualización

### Lesson (Lección)
- `course`: Curso al que pertenece
- `title`: Título de la lección
- `content`: Contenido de texto
- `video_url`: URL del video (opcional)
- `duration_minutes`: Duración en minutos
- `order`: Orden de la lección en el curso

### Enrollment (Inscripción)
- `user`: Usuario inscrito
- `course`: Curso en el que está inscrito
- `enrolled_at`: Fecha de inscripción
- `is_completed`: Si completó el curso

### Review (Reseña)
- `course`: Curso reseñado
- `user`: Usuario que hace la reseña
- `comment`: Comentario de la reseña
- `rating`: Calificación de 1 a 5 estrellas
- `published_at`: Fecha de publicación

## Seguridad

> **⚠️ Importante para producción**:
> - Cambia `DJANGO_SECRET_KEY` por una clave segura
> - Establece `DEBUG=False`
> - Configura `ALLOWED_HOSTS` correctamente
> - Usa HTTPS
> - Configura variables de entorno de forma segura
> - Revisa los permisos de archivos y directorios

**Desarrollado con ❤️ usando Django y Django REST Framework**
