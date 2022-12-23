from fastapi import FastAPI, Response


app = FastAPI(title="Wobot Technologies Todo API")

from .routers import user_auth, todo_route
app.include_router(user_auth.user_auth)
app.include_router(todo_route.todos)

@app.get("/")
async def get_doc():
    data = """
    <html>
        <head>
            <style>
                a:link, a:visited {
                background-color: #f44336;
                color: white;
                padding: 14px 25px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                }

                a:hover, a:active {
                background-color: red;
                }
                </style>
            <title>Wobot Todo</title>
        </head>
        <body>
            <a href="./docs">Swagger Documentation</a>
            <a href="./redoc">OpenAPI Documentation</a>
        </body>
    </html>
    """
    return Response(content=data, media_type="text")