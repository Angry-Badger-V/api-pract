import psycopg2
import fastapi
import src.models.events as events
import src.models.users as users
import db.connection as db_connection
import src.exceptions.handlers as exception_handlers

app = fastapi.FastAPI()

app.add_exception_handler(
    fastapi.exceptions.RequestValidationError,
    exception_handlers.validation_exception_handler
)

@app.get("/api/events")
def get_events():
    events = events.select_all_events()
    return {"events": events}

@app.get("/api/events/{id}")
def get_events(id: int):
    event = events.select_event(id)
    return {"event": event}

@app.post("/api/auth/login")
def get_hash(user_auth: users.UserAuth):
    token = users.authorise_user(user_auth)
    if token is None:
        raise fastapi.HTTPException(
                status_code=401,
                detail="Invalid email or password")
    return {"token": token}

#@app.post("api/auth/register")
#def do_register(user_reg: UserReg):
#    user = register_user(user_reg)
#    if user is None:
#        raise HTTPException
#    return {"user": user}
