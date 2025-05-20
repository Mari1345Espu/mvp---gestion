from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from pathlib import Path
from typing import List
import os
from dotenv import load_dotenv

load_dotenv()

# Configuración del servidor de correo
conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv("MAIL_USERNAME", "tu_correo@gmail.com"),
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD", "tu_contraseña"),
    MAIL_FROM=os.getenv("MAIL_FROM", "tu_correo@gmail.com"),
    MAIL_PORT=int(os.getenv("MAIL_PORT", 587)),
    MAIL_SERVER=os.getenv("MAIL_SERVER", "smtp.gmail.com"),
    MAIL_FROM_NAME=os.getenv("MAIL_FROM_NAME", "Sistema de Gestión de Proyectos"),
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    TEMPLATE_FOLDER=Path(__file__).parent.parent / 'templates' / 'email'
)

fastmail = FastMail(conf)

async def send_reset_password_email(email: str, reset_token: str):
    """Envía un correo con el enlace para restablecer la contraseña"""
    reset_link = f"http://localhost:8000/reset-password?token={reset_token}"
    
    message = MessageSchema(
        subject="Recuperación de Contraseña",
        recipients=[email],
        body=f"""
        <html>
            <body>
                <h2>Recuperación de Contraseña</h2>
                <p>Has solicitado restablecer tu contraseña. Haz clic en el siguiente enlace para crear una nueva contraseña:</p>
                <p><a href="{reset_link}">Restablecer Contraseña</a></p>
                <p>Si no solicitaste este cambio, puedes ignorar este correo.</p>
                <p>El enlace expirará en 1 hora.</p>
            </body>
        </html>
        """,
        subtype="html"
    )
    
    await fastmail.send_message(message)

async def send_notification_email(email: str, subject: str, message: str):
    """Envía un correo de notificación"""
    message = MessageSchema(
        subject=subject,
        recipients=[email],
        body=f"""
        <html>
            <body>
                <h2>{subject}</h2>
                <p>{message}</p>
            </body>
        </html>
        """,
        subtype="html"
    )
    
    await fastmail.send_message(message) 