<div style="display: flex; justify-content: center; align-items: center;">
  <img src="./staticfiles/img/zalon_design_logo.png" alt="zalon design logo" width="250"/>
</div>

Plataforma de exposición y ventas de los packs de las líneas de Zalon Design. Con un backoffice para poder cargar packs y tener info de rendimiento.

## Tech stack
- Django
- Bulma CSS Framework

### We're also using these other styling libraries for a more enjoyable experience
- Font Awesome: for icons
- Animate.css: for animations
- Hover.css: for hover effects


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