# ✅ schemas.py (for drf-spectacular)


from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework import status

register_schema = extend_schema(
    responses={
        status.HTTP_201_CREATED: OpenApiResponse(description="User registered successfully."),
        status.HTTP_400_BAD_REQUEST: OpenApiResponse(description="Bad Request."),
    }
)
