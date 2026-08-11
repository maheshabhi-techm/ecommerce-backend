from fastapi_mail import FastMail, MessageSchema
from ..security.config import conf

mail = FastMail(conf)


async def send_otp(email: str, otp: str):

    html = f"""
        <html>
            <body>
                <h2>Welcome to Ecommerce App</h2>

                <p>Thank you for registering.</p>

                <p>Your email verification code is:</p>

                <h1>{otp}</h1>

                <p>
                    This OTP expires in <b>10 minutes</b>.
                </p>

                <br>

                <p>
                    If you did not create this account,
                    please ignore this email.
                </p>

                <hr>

                <small>
                    Ecommerce App Team
                </small>
            </body>
        </html>
        """

    message = MessageSchema(
        subject="Verify your account",
        recipients=[email],
        body=html,
        # f"""
        # Hello
        # Your verification otp is
        # {otp}
        # It expires in 10 minutes""",
        subtype="html",  # add 'plain' in type is text
    )

    await mail.send_message(message)


async def send_email(email: str, subject: str, html: str):
    message = MessageSchema(
        subject=subject, recipients=[email], body=html, subtype="html"
    )
    await mail.send_message(message)
