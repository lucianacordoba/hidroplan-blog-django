# HidroPlan Blog — Proyecto Final Python/Django

Aplicación web estilo blog desarrollada en **Django**, como entrega final individual del curso.
Temática: noticias y artículos sobre gestión hídrica, cuencas y aprovechamiento sustentable del
agua, en línea con el proyecto HidroPlan IA.

## Video de presentación

📹 _[Agregar aquí el link al video de YouTube/Drive una vez grabado]_

## Demo / credenciales de prueba

| Rol | Usuario | Contraseña |
|---|---|---|
| Administrador | `admin` | `hidroplan2026` |

> Podés crear tu propio usuario desde **Signup** para probar el flujo completo de registro.

## Tecnologías utilizadas

- Python 3.9
- Django 4.2 (LTS)
- django-ckeditor (editor de texto enriquecido)
- Pillow (manejo de imágenes)
- SQLite (base de datos de desarrollo)
- HTML5 / CSS3 (sin frameworks de frontend)

## Estructura del proyecto

```
Proyecto_Final_Python_Django/
├── hidroplan_blog/     # Configuración del proyecto (settings, urls raíz)
├── blog/               # App principal: Home, About, CRUD de páginas (Articulo)
├── accounts/           # App de autenticación: signup, login, logout, perfil
├── mensajeria/         # App de mensajería privada entre usuarios
├── templates/          # Templates HTML (herencia desde base.html)
├── static/             # CSS propio del proyecto
├── media/              # Imágenes subidas por usuarios (no versionado)
├── requirements.txt
└── manage.py
```

## Apps y modelos

### `blog`
- **Modelo principal:** `Articulo`
  - `titulo` (CharField)
  - `resumen` (CharField)
  - `contenido` (RichTextField vía ckeditor)
  - `imagen` (ImageField)
  - `fecha_publicacion` (DateField, autogenerada)
  - `autor` (FK a User)
- Vistas: `HomeView`, `AboutView`, `ArticuloListView` (con buscador por título y
  mensaje de "No hay páginas aún" cuando corresponde), `ArticuloDetailView`,
  `ArticuloCreateView`, `ArticuloUpdateView` (con `LoginRequiredMixin` +
  `UserPassesTestMixin`, solo el autor puede editar), y `articulo_delete`
  (vista basada en función con decorador `@login_required`).

### `accounts`
- **Modelo:** `Perfil` (OneToOne con `User`): `avatar`, `biografia`, `link`,
  `fecha_nacimiento`. Se crea automáticamente vía signal al registrar un usuario.
- Vistas: registro (`signup`, solicita username/email/password), login, logout,
  perfil (muestra nombre, apellido, email, avatar y biografía), edición de
  perfil y cambio de contraseña.

### `mensajeria`
- **Modelo:** `Mensaje` (emisor, receptor, contenido, fecha_envio, leído).
- Vistas: bandeja de entrada (lista de conversaciones + usuarios disponibles
  para iniciar una nueva) y vista de conversación 1 a 1.

Todos los modelos están registrados en el panel de **Admin** de Django.

## Requisitos base cubiertos

- Rutas `about/` y `pages/` visibles desde la barra de navegación.
- Listado de páginas con "Leer más" → detalle en `pages/<id>/`.
- Mensaje "No hay páginas aún" cuando no existen registros (o sin resultados de búsqueda).
- Edición y borrado de páginas solo disponible para usuarios logueados (y autores).
- Herencia de templates (`base.html` con `<nav>` común a todo el sitio).
- Mínimo 2 CBVs (`ListView`, `DetailView`, `CreateView`, `UpdateView`) +
  1 mixin (`LoginRequiredMixin` / `UserPassesTestMixin`) + 1 decorador
  (`@login_required` en `articulo_delete` y en las vistas de `accounts`/`mensajeria`).
- Formularios con imágenes adaptados en template (`enctype="multipart/form-data"`) y vista.
- App independiente (`accounts`) para autenticación y perfil.
- App independiente (`mensajeria`) para mensajería entre usuarios.

## Instalación y puesta en marcha local

```bash
# 1. Clonar el repositorio
git clone <url-del-repo>
cd Proyecto_Final_Python_Django

# 2. Crear y activar entorno virtual
python3 -m venv venv
source venv/bin/activate      # En Windows: venv\Scripts\activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Aplicar migraciones
python manage.py migrate

# 5. Crear un superusuario (opcional, para acceder al admin)
python manage.py createsuperuser

# 6. Levantar el servidor de desarrollo
python manage.py runserver
```

Luego abrir [http://127.0.0.1:8000/](http://127.0.0.1:8000/) en el navegador.

> **Nota:** el archivo `db.sqlite3` y la carpeta `media/` no se incluyen en el
> repositorio (ver `.gitignore`). Al correr las migraciones se genera una base
> de datos vacía; hay que registrar un usuario y crear páginas de prueba.

## Autor

Luciana Córdoba — Proyecto Final individual, curso Python/Django.
