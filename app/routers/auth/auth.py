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


@auth_router.post(
    "/login", status_code=200)
async def login(request: Request):
    """

    """
    good_pass = False

    try:
        mongo_bd = get_bd()
        user_collection = mongo_bd['users']

        form_data = await request.form()

        find_user = {'username': form_data.get('username')}
        user = await user_collection.find_one(find_user)
        if user:
            good_pass = verificar_usuario(form_data.get('password'), user['password'])
    except Exception as e:
        msg = 'error desconocido'
        log.error(str(traceback.format_exc()))
        res = dict(success=False, data=None, msg=msg)
        response = JSONResponse(content=res, status_code=500)
    else:
        if good_pass:
            token = create_access_token(user['username'])
            response = RedirectResponse("www.google.com", status_code=302)
            response.set_cookie(
                key=Sesion.cookie_name,
                value=token,
                expires=Sesion.expiracion_cookie,
            )

        else:
            response = RedirectResponse(
                "/auth/form-login" + f"?verificado=no",
                status_code=302)

    return response


@auth_router.get("/logout", status_code=200)
def logout() -> RedirectResponse:
    respuesta = RedirectResponse(
        "/auth/form-login",
        status_code=302)
    respuesta.delete_cookie(Sesion.cookie_name)

    return respuesta