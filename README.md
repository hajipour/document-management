# Document management

Run `python -m pip install -r requirements.txt`, then `python manage.py migrate` and
`python manage.py runserver`.

The JSON API uses Django session authentication:

- `GET` / `POST` `/documents/`
- `GET` / `PUT` / `PATCH` / `DELETE` `/documents/<document_id>/`
- `GET` `/admin/documents/` (staff users only)

Every detail lookup scopes `Document` by both its ID and `get_current_user(request).id`.
