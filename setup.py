from distutils.core import setup
import setuptools

setup(
    name='wishlist',
    version='0.1.0',
    author='Patrick Clements',
    author_email='patrick.clements@gmail.com',
    packages=[
        'wishlist',
        'wishlist_app',
        'wishlist_app.forms',
        'wishlist_app.middleware',
        'wishlist_app.migrations',
        'wishlist_app.views'
    ],
    description='A Django app for managing wishlists in a group',
    install_requires=[
        "Django==1.8.4",
        "django-bootstrap3==6.2.2",
        # "django-registration==1.0",
        "psycopg2==2.6.1",
    ],
)