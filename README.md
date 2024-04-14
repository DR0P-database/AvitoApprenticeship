# Avito test assignment
This is a service that allows you to show banners to users, depending on the required fic and tag of the user, as well as manage banners and their associated tags and fic. The service uses PostgreSql, FastAPI, Redis (stores data about user banners for 5 minutes).

## Setup

    $ git clone https://github.com/DR0P-database/AvitoApprenticeship.git
    $ cd AvitoApprenticeship
    $ docker compose build
    $ docker compose up

If run without docker:

    $ git clone https://github.com/DR0P-database/AvitoApprenticeship.git
    $ cd AvitoApprenticeship
    $ python -m venv .venv
    $ source .venv/bin/activate
    $ pip install -r requirements.txt
    $ python main.py

## Usage
### X-Token and users
If you make a request without a token in the header or the token is not equal to `"user_token"` and `"admin_token"`, the application will return errors:

    { "detail": "Пользователь не авторизован" }

    { "detail": "Пользователь не имеет доступа" }

### Add banner
    $ curl -X 'POST' 'http://127.0.0.1:8000/banner/' -H 'accept: application/json' -H 'x-token: admin_token' -H 'Content-Type: application/json' -d '{
        "tag_ids": [
          5,6
        ],
        "feature_id": 7,
        "content": {"text":"qwerty"},
        "is_active": true
      }'
<img width="1149" alt="image" src="https://github.com/DR0P-database/AvitoApprenticeship/assets/159697952/7e1dcac3-107a-4784-b585-87d79152cfe4">

All parametrs required and list of tag_ids must be `not empty`, token must be `"admin_token"`

If all right response will be with status `code 201`:

    { "banner_id": 1 }
    
If same banner already exists will be returned status `code 400`:

    { "detail": "Похожий баннер уже есть" }

### Uncorrect data type in requests
If you enter an invalid data type in the query, you will get an `error 400`:

    { "error": "Некорректные данные" }

### Get banner by feature/tag
    $ curl -X 'GET' 'http://127.0.0.1:8000/banner/?feature_id=7&tag_id=1' -H 'accept: application/json' -H 'x-token: admin_token'

<img width="1146" alt="image" src="https://github.com/DR0P-database/AvitoApprenticeship/assets/159697952/e41d3489-794d-4dfe-82a3-71a73e80950a">

Respnse will be with `status 200`:
<img width="1144" alt="image" src="https://github.com/DR0P-database/AvitoApprenticeship/assets/159697952/7a6752ec-5ec4-4acd-9d33-8886f92a166b">

### Get user_banner
    $ curl -X 'GET' 'http://127.0.0.1:8000/user_banner/?feature_id=1&tag_id=7&use_last_revision=true' -H 'accept: application/json' -H 'x-token: user_token'

"feature_id" and "tag_id" is `required`

Response will be with status `code 200`:

<img width="1147" alt="image" src="https://github.com/DR0P-database/AvitoApprenticeship/assets/159697952/49b0c907-3d85-4ce8-ab27-2d604d255435">

If banner not found return `code 404`:

    { "detail": "Баннер для не найден" }

### Patch banner
Use method `PATCH` and url 'http://127.0.0.1:8000/banner/{id}' where id is int banner id when add banner

<img width="1148" alt="image" src="https://github.com/DR0P-database/AvitoApprenticeship/assets/159697952/c0d604c4-7991-42f0-bedf-74faf6865af2">

All fields `required`, tag_ids must be `not_empty`

If all right response will be with `status 200`:

    { "detail": "OK" }

If same banner already exists return will be `code 400`:

    { "detail": "Похожий баннер уже есть" }

### Delete banner
Use method `DELETE` and url 'http://127.0.0.1:8000/banner/{id}' where id is int banner id when add banner

    $ curl -X 'DELETE' 'http://127.0.0.1:8000/banner/1' -H 'x-token: admin_token'

If all right response will be `status 204`:

Else `status or 404`:

    { "detail": "Баннер для тэга не найден" }

## Issues and solutions
1. You cannot add a new banner with a feature and a tag if such a banner with a feature and a tag from the list already exists. For example, there is a banner with a feature 2 tags [1,2,3], then it will not be possible to add a banner with feature 2 and tags [1,5,6] or [1,2] or [3,4,5]. You will only be able to add a banner with an existing feature that has tags that do not overlap.
Also in PATCH method of banner.

2. Does a banner have to have at least one tag? -- On the service, when creating and patching a banner, the list of tags should not be empty.

3. What if requests are from a token that is not a 'user_token' or 'admin_token' -- the Application thinks it is not authorized.
