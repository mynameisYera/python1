from datetime import datetime, timezone

from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods, require_POST
from pydantic import ValidationError as PydanticValidationError
from sqlalchemy import select

from .db import SessionLocal
from .sa_models import Item
from .schemas import ItemCreate, ItemUpdate, RegisterBody


def index(request):
    return HttpResponse('main app works — дальше: модели → миграции → API или шаблоны.')


def favicon(request):
    # Browser requests /favicon.ico; 204 avoids noisy 404 in runserver logs until you add a real icon.
    return HttpResponse(status=204)


def hello(request):
    return HttpResponse('Hello')


def users_list(request):
    rows = User.objects.order_by('id').values(
        'id',
        'username',
        'email',
        'first_name',
        'last_name',
        'is_active',
        'is_staff',
        'date_joined',
    )
    return JsonResponse(list(rows), safe=False)


@csrf_exempt
@require_POST
def register(request):
    """Создание пользователя. JSON валидируется моделью RegisterBody (Pydantic)."""
    try:
        body = RegisterBody.model_validate_json(request.body)
    except PydanticValidationError as exc:
        return JsonResponse({'error': exc.errors(include_url=False)}, status=422)

    if User.objects.filter(username__iexact=body.username).exists():
        return JsonResponse({'error': 'username already taken'}, status=409)

    try:
        validate_password(body.password)
    except ValidationError as exc:
        return JsonResponse({'error': exc.messages}, status=400)

    user = User.objects.create_user(
        username=body.username,
        password=body.password,
        email=body.email,
        first_name=body.first_name,
        last_name=body.last_name,
    )
    return JsonResponse(
        {"message": "User created"},
        status=201,
    )


def _item_to_dict(item: Item):
    return {
        'id': item.id,
        'title': item.title,
        'content': item.content,
        'created_at': item.created_at.isoformat() if item.created_at else None,
        'updated_at': item.updated_at.isoformat() if item.updated_at else None,
    }


@csrf_exempt
@require_http_methods(['GET', 'POST'])
def items_collection(request):
    """GET — список; POST — создать (Create)."""
    if request.method == 'GET':
        with SessionLocal() as session:
            rows = session.scalars(select(Item).order_by(Item.id)).all()
            payload = [_item_to_dict(i) for i in rows]
        return JsonResponse(payload, safe=False)

    try:
        body = ItemCreate.model_validate_json(request.body)
    except PydanticValidationError as exc:
        return JsonResponse({'error': exc.errors(include_url=False)}, status=422)

    with SessionLocal() as session:
        row = Item(title=body.title, content=body.content)
        session.add(row)
        session.commit()
        session.refresh(row)
        out = _item_to_dict(row)
    return JsonResponse(out, status=201)


@csrf_exempt
@require_http_methods(['GET', 'PATCH', 'DELETE'])
def items_detail(request, pk: int):
    """GET — одна запись (Read); PATCH — обновить (Update); DELETE — удалить (Delete)."""
    with SessionLocal() as session:
        row = session.get(Item, pk)
        if row is None:
            return JsonResponse({'error': 'not found'}, status=404)

        if request.method == 'GET':
            return JsonResponse(_item_to_dict(row))

        if request.method == 'DELETE':
            session.delete(row)
            session.commit()
            return JsonResponse({'ok': True})

        try:
            body = ItemUpdate.model_validate_json(request.body)
        except PydanticValidationError as exc:
            return JsonResponse({'error': exc.errors(include_url=False)}, status=422)

        if body.title is not None:
            row.title = body.title
        if body.content is not None:
            row.content = body.content
        row.updated_at = datetime.now(timezone.utc)
        session.commit()
        session.refresh(row)
        return JsonResponse(_item_to_dict(row))
