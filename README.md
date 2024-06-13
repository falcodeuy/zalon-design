<div style="display: flex; justify-content: center; align-items: center;">
  <img src="./staticfiles/img/zalon_design_logo.png" alt="zalon design logo" width="250"/>
</div>

Plataforma de exposición y ventas de los packs de las líneas de Zalon Design.
Con un backoffice para poder cargar packs y tener info de rendimiento.

[Website here](https://design.zalon.app/)

## Tech stack

- **Backend:**
  - [Django](https://www.djangoproject.com/)
    - [Django CKEditor 5](https://pypi.org/project/django-ckeditor-5/): for rich
      text editing
- **Frontend:**
  - Django Templates
  - JavaScript
    - [Splide.js](https://splidejs.com/): for carousels.
  - CSS for styling
    - [Bulma CSS Framework](https://bulma.io/): for general styling - We use
      Bulma with the help of
      [django-simple-bulma](https://github.com/lemonsaurus/django-simple-bulma)
      (Better than django-bulma in our opinion)
    - [Lineicons](https://lineicons.com/): for icons
    - Some CSS files for custom styling. One for general rules directly in
      _staticfiles_ and another others in every app directory that needs it.

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

## Run collectstatic

```bash
docker compose exec web python manage.py collectstatic
```

> You can see more about the way we work in Falcode
> [here](http://docs.falcode.dev/django/)

<div style="display: flex; justify-content: center; align-items: center;">
  <img src="./staticfiles/img/falcode_logo.svg" alt="falcode logo" width="200"/>
</div>
