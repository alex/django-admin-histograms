from setuptools import setup, find_packages

setup(
    name = "django-admin-histograms",
    version = __import__("django_histograms").__version__,
    author = "Alex Gaynor",
    author_email = "alex.gaynor@gmail.com",
    description = "A library for simple histograms in Django's admin.",
    long_description = open("README").read(),
    license = "BSD",
    url = "http://github.com/alex/django-admin-histograms",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=['django'],
    classifiers = [
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Framework :: Django",
    ]
)
 

