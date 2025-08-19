from fastapi_mail import FastMail, ConnectionConfig, MessageSchema, MessageType
from app.core.config import settings
from pathlib import Path
from app.core.errors import EmailSendingError

config = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_STARTTLS=settings.MAIL_STARTTLS,
    MAIL_SSL_TLS=settings.MAIL_SSL_TLS,
    TEMPLATE_FOLDER= Path("app/templates")
)


class EmailService : 

    def __init__(self) -> None:
        self.fastMail = FastMail(config)

    async def send_email(
            self,
            recipients : list[str], 
            subject : str, 
            template_body : dict[str,str],
            template_name : str
        ):

        message  = MessageSchema(
            recipients=recipients, 
            subject= subject, 
            template_body=template_body,
            subtype= MessageType.html
        )
        try:
            await self.fastMail.send_message(message, template_name= template_name)
        except : 
            raise EmailSendingError('Email sending failed')
    

    