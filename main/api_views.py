"""
API на Django REST Framework: JWT проверяется заголовком Authorization: Bearer <access>.
"""

from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


class MeView(APIView):
    """Пример защищённого эндпоинта: только с валидным access-токеном."""

    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary='Текущий пользователь',
        description='Нужен валидный access JWT (кнопка Authorize в Swagger).',
        tags=['auth'],
    )
    def get(self, request):
        u = request.user
        return Response(
            {
                'id': u.id,
                'username': u.username,
                'email': u.email or '',
                'first_name': u.first_name or '',
                'last_name': u.last_name or '',
            }
        )
