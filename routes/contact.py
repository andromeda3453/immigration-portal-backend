from fastapi import APIRouter, HTTPException
from schemas import ContactMessage
import smtplib, os
from email.mime.text import MIMEText

router = APIRouter()

@router.post("/contact")
async def contact(msg: ContactMessage):
    sender = os.getenv("EMAIL_USER")
    recipient = "info@applicationtracker.id"
    password = os.getenv("EMAIL_PASS")

    email_body = f"""
    Name: {msg.name}
    Email: {msg.email}
    Message:
    {msg.message}
    """

    email = msg.email

    msg = MIMEText(email_body)
    msg['Subject'] = 'Contact Form Submission'
    msg['From'] = sender
    msg['To'] = recipient
    msg['Reply-To'] = email

    try:
        server = smtplib.SMTP(os.getenv("SMTP_SERVER"), int(os.getenv("SMTP_PORT")))
        server.starttls()
        server.login(sender, password)
        server.sendmail(sender, recipient, msg.as_string())
        server.quit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Email failed: {str(e)}")

    return {"message": "Message sent successfully!"}
