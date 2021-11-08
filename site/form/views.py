"""Views logic."""

from django import http


def index(request: http.HttpRequest) -> http.HttpResponse:
    """Main index page."""
    return http.HttpResponse("Hello world.")


def data(request: http.HttpRequest) -> http.HttpResponse:
    """Test JSON data endpoint."""
    return http.JsonResponse({"x": 3, "y": 4})
