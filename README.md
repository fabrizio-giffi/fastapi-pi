# fastapi-pi

## How to run the application

### Development

`uvicorn main:app --reload`

from the docs:

Remember to remove the --reload option if you were using it.<br>
The --reload option consumes much more resources, is more unstable, etc.<br>
It helps a lot during development, but you shouldn't use it in production.

### Running the server

`uvicorn main:app --host 0.0.0.0 --port 1312`