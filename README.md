# Document management

Run `python -m pip install -r requirements.txt`, then `python manage.py migrate` and
`python manage.py runserver`.

The JSON API uses Django session authentication:

- `GET` / `POST` `/documents/` (JSON, or multipart with an optional `file` field)
- `GET` / `PUT` / `PATCH` / `DELETE` `/documents/<document_id>/`
- `GET` `/admin/documents/` (staff users only)

Every detail lookup scopes `Document` by both its ID and `get_current_user(request).id`.

For example, upload a file with:

```sh
curl -b cookies.txt -F 'title=My document' -F 'file=@./notes.pdf' \
  http://localhost:8000/documents/
```

Uploaded files are stored under `media/documents/` in development. Configure a
production storage backend before deploying.
