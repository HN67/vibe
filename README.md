# Vibe

A project to provide methods to unify different and unique
sensory experiences into cohesive collections.

## Django Site

### Setup

See <https://docs.djangoproject.com/en/3.2/intro/tutorial01/>

Create a Python virtual environment using `python -m venv .venv`,
and then activate according to platform.

The Django site was initially created using `django-admin startproject site`.

### Directory Structure

The root repository is `vibe`, which then contains a folder called `site`
which contains the Django site. This folder can be easily renamed.

The site itself is mostly within another folder named `vibe` in `site`,
this folder can not be so easily renamed.

The script `site/manage.py` is used for most Django configuration.

### Running

Running a debug server of the site can be done with `python manage.py runserver [port]`
which starts a server on localhost.

### Creating Apps

Apps (e.g. site components) can be bootstrapped with `python manage.py startapp [name]`,
and should be created sibling to the `vibe` folder in `site`.

### Example

I created an example `form` app that has two endpoints,
`http://localhost:8000/form/` and `http://localhost:8000/form/data`,
the later of which serves JSON.

The neccesary code to do this is in `form/views.py` for the actual logic,
and `form/urls.py` and `vibe/urls.py` for the routing information.
