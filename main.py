import fastapi

from src.routes import events, auth, user
from src.exceptions import handlers as exception_handlers

app = fastapi.FastAPI()

app.add_exception_handler(
    fastapi.exceptions.RequestValidationError,
    exception_handlers.validation_exception_handler
)

app.include_router(events.router)
app.include_router(auth.router)
app.include_router(user.router)
