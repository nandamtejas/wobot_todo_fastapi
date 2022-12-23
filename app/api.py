from fastapi import FastAPI


app = FastAPI(title="Wobot Technologies Todo API")

from .routers import user_auth, todo_route
app.include_router(user_auth.user_auth)
app.include_router(todo_route.todos)