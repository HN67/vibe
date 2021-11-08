"""Views logic."""

import random
import typing as t

from django import http


def index(request: http.HttpRequest) -> http.HttpResponse:
    """Main index page."""
    return http.HttpResponse("Hello world.")


def get_data(name: t.Optional[str] = None) -> t.Mapping[str, int]:
    """Retrieve data from *somewhere* (e.g. a database)."""
    if name is None:
        return {"x": random.randint(1, 4), "y": random.randint(1, 4)}
    return {f"{name}_x": random.randint(1, 4), f"{name}_y": random.randint(1, 4)}


def data(request: http.HttpRequest, name: t.Optional[str] = None) -> http.HttpResponse:
    """Test JSON data endpoint."""
    return http.JsonResponse(get_data(name))
