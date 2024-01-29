class Sesion:
    """Variables relacionadas con la sesión del usuario."""

    expiracion_token = 5
    """Tiempo en horas de expiración del token."""

    expiracion_cookie = expiracion_token * 3600
    """Tiempo en segundos que tiene validez una cookie"""

    cookie_name = 'Authorization_pepe'
