# COSC 310 Software Engineering

## StackSquad

Make sure to `cd` into your `venv`. Whenever you add a new library to to the code to work with, add it to `requirements.txt`, and make sure to update your `venv` every now and then to avoid missing libraries. Do this using `pip install -r requirements.txt`

### Running FastAPI & PyTest

Make sure that your working directory is the project root before you start FastAPI or use PyTest otherwise it will not work (An example of root: `Users/user/COSC 310/Project/COSC_310_Lab`) <br>
&nbsp;&nbsp; To run FastApi: `fastapi dev backend/app/main.py`<br>
&nbsp;&nbsp; To use PyTest: `pytest backend/test/unit/...` or `pytest backend/test/integration/...` (whichever you want to test)

### Testing with PyTest

When testing, test from project root: `/root/to/project/root` (etc: `Users/user/COSC 310/Project/COSC_310_Lab`) <br>
&nbsp;&nbsp; Use `pytest backend/test/unit/...` or `pytest backend/test/integration/...`

To get a coverage report run: `pytest --cov=backend --cov-report=term`

### Using PyLint

In the terminal, run `pylint path-to-file` to run PyLint on specific file

### Running project with Docker

1. Make sure your Docker engine is running
2. Change working directory to project root `cd ~/COSC_310_Lab` or whever you saved it to
3. Run `docker-compose up --build`
4. For Backend: Open http://localhost:8000 for "site", http://localhost:8000/docs for endpoints via SwaggerUI, or http://localhost:8000/redoc for endpoint documentation
5. For Frontend: Open http://localhost:3000 for UI