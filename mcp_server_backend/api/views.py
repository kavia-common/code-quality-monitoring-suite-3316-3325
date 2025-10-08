from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

# PUBLIC_INTERFACE
@api_view(["GET"])
@permission_classes([AllowAny])
def health(request):
    """
    Health check endpoint.

    Returns 200 OK with a basic message to confirm the server is responsive.
    """
    return Response({"message": "Server is up!"})
