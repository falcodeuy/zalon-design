<div style="display: flex; justify-content: center; align-items: center;">
  <img src="./staticfiles/img/zalon_design_logo.png" alt="zalon design logo" width="250"/>
</div>

Plataforma de exposición y ventas de los packs de las líneas de Zalon Design. Con un backoffice para poder cargar packs y tener info de rendimiento.

## Tech stack
- **Backend:**
  - [Django](https://www.djangoproject.com/)
    - [Django CKEditor](https://django-ckeditor.readthedocs.io/): for rich text editing
- **Frontend:**
  - Django Templates
  - JavaScript (yep just vanilla JS)
  - CSS for styling (we're not using SASS as we don't want to compile anything)
    - [Bulma CSS Framework](https://bulma.io/): for general styling
    - [Font Awesome](https://fontawesome.com/): for icons
    - [Animate.css](https://animate.style/): for animations
    - [Hover.css](http://ianlunn.github.io/Hover/): for hover effects


## Run the project
```bash
docker compose up
```
You'll get the app running on `http://localhost:8000`

## Make and apply migrations
```bash
docker compose exec web python manage.py makemigrations
docker compose exec web python manage.py migrate
```

> You can see more about the way we work in Falcode [here](http://docs.falcode.dev/django/)

<div style="display: flex; justify-content: center; align-items: center;">
  <img src="./staticfiles/img/falcode_logo.svg" alt="falcode logo" width="200"/>
</div>