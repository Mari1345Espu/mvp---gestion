import os

async def send_reset_password_email(email: str, reset_token: str):
    """Envía un correo con el enlace para restablecer la contraseña"""
    # Implementación temporal que solo imprime el mensaje
    print(f"Enviando correo de recuperación a {email}")
    print(f"Token: {reset_token}")
    return True

async def send_notification_email(email: str, subject: str, message: str):
    """Envía un correo de notificación"""
    # Implementación temporal que solo imprime el mensaje
    print(f"Enviando notificación a {email}")
    print(f"Asunto: {subject}")
    print(f"Mensaje: {message}")
    return True 