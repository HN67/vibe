"""URL routing."""

# path constructor
from django.urls import path

# imports our views module
# containing our default views
from . import views

# connects url patterns to functions
urlpatterns = [
    path("", views.index, name="index"),
    path("data/", views.data, name="data"),
    path("data/<name>/", views.data),
]
