# Simple Reporting Schema

This is a small Django application which contains models for a basic job accounting system. It also has a db seed script for generating example data.


# Setup

```sh
script/setup # Install dependencies, running migrations
python manage.py seed # Generate mock data
make # Install dependencies with yarn package
# if you use windows, run `make -f Makefile_windows` instead of `make`
```

# Runnin the Server

```sh
script/server
```
