from fastapi import APIRouter, Request, Depends, Response
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from config import get_log

import traceback

from utils.user import hash_password, verificar_usuario
from utils.auth import create_access_token
from metadata.sesion import Sesion
from config import get_bd


log = get_log()
auth_router = APIRouter(prefix='/auth', tags=['auth_router'])


templates = Jinja2Templates(directory='./public/static/html')


@auth_router.get(
    "/form-login", status_code=200)
async def form_login(request: Request, verificado: str = 'si'):
    """

    """

    respuesta = templates.TemplateResponse('auth/login.html',
                                           {'request': request, 'verificado': verificado})

    return respuesta



@auth_router.get(
    "/reserva", status_code=200)
async def form_login(request: Request):
    """

    """

    respuesta = templates.TemplateResponse('reserva/index.html',
                                           {'request': request})

    return respuesta


@auth_router.post(
    "/login", status_code=200)
async def login(request: Request):
    """

    """
    response = RedirectResponse(
        "/auth/reserva",
        status_code=302)

    return response


@auth_router.get("/logout", status_code=200)
def logout() -> RedirectResponse:
    respuesta = RedirectResponse(
        "/auth/form-login",
        status_code=302)
    respuesta.delete_cookie(Sesion.cookie_name)

    return respuesta