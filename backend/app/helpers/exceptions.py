from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
import traceback

class HTTPException(Exception):

    def __init__(self, *, status_code: int = 400):
        self.status_code = status_code

    def __str__(self):
        return self.__class__.__name__


def initialize_exception_handler(app):

    @app.exception_handler(HTTPException)
    async def unicorn_exception_handler(request: Request, exc: HTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                'error': exc.__class__.__name__
            }
        )

    @app.exception_handler(AssertionError)
    async def assertion_error_handler(request: Request, exc: AssertionError):
        traceback.print_exc()
        return JSONResponse(
            status_code=400,
            content={'error': str(exc)},
        )

    @app.exception_handler(ValueError)
    async def value_error_handler(request: Request, exc: ValueError):
        traceback.print_exc()
        return JSONResponse(
            status_code=400,
            content={'error': str(exc)},
        )

    @app.exception_handler(RequestValidationError)
    async def request_validation_error_handler(request: Request, exc: RequestValidationError):
        traceback.print_exc()
        invalid_fields = []
        # attempt to reconstruct the error
        try:
            e_list = exc.errors()
            for e in e_list:
                loc = e.get('loc', None)
                invalid_fields.append(loc[len(loc) - 1])
            error = f'Invalid values: {", ".join(invalid_fields)}'
        except:
            error = exc

        return JSONResponse(
            status_code=400,
            content={'error': error},
        )