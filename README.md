# COSC 310 Software Engineering

## StackSquad

Make sure to `cd` into your `venv`. Whenever you add a new library to to the code to work with, add it to `requirements.txt`, and make sure to update your `venv` every now and then to avoid missing libraries.

### Running Project

If wanting to test us `PyTest`, make sure all imports from within the project are imported using namespace `backend.app.module` and not just `app.module`.

When running `fastapi dev app/main.py`, make sure all imports are imported with no addtional namespace 'backend.app.' etc.
