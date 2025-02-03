from fastapi import FastAPI
from starlette.responses import RedirectResponse
import models
from database import engine, session_local
from routers import todos, auth, admin


def setup_database():
    models.Base.metadata.create_all(bind=engine)

# Dependency to get the database session
def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()



app = FastAPI()
app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
setup_database()


@app.get("/", include_in_schema=False)
async def redirect_to_docs():
    return RedirectResponse(url="/docs")