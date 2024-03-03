from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from exceptions import EmailNotValid
from routers import users, books, category
from fastapi import status
from auth import authentication
app = FastAPI()
app.include_router(users.router, tags=['users'])
app.include_router(books.router, tags=['books'])
app.include_router(category.router, tags=['categories'])
app.include_router(authentication.router, tags=['auth'])




@app.exception_handler(EmailNotValid)
def email_not_valid(request: Request, exc: EmailNotValid):
    return JSONResponse(content=str(exc), status_code=status.HTTP_400_BAD_REQUEST)