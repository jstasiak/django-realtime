
from setuptools import setup, find_packages


setup(
    name = "django-realtime",
    version = __import__("realtime").__version__,
    author = "Jakub Stasiak",
    author_email = "kuba.stasiak@gmail.com",
    description = ("Django application that simplifies usage of socket.io in Django projects"),
    long_description = open('README.rest').read(),
    url = "http://github.com/jstasiak/django-realtime",
    py_modules=["realtime",],
    install_requires=["gevent-socketio", "gevent-websocket"],
    zip_safe = False,
    include_package_data = True,
    packages = find_packages(),
    classifiers = [
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: POSIX",
        "Programming Language :: Python",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: HTTP Servers",
        "Topic :: Internet :: WWW/HTTP :: WSGI",
    ]
)
