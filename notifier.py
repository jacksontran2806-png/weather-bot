import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import EMAIL_PASSWORD

def send_email(subject, body, to_email):
    """Send email via Gmail SMTP"""
    
    # Gmail SMTP settings
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    from_email = "em.sun2019@gmail.com"  # Replace with your Gmail
    
    # Create message
    message = MIMEMultipart()
    message["From"] = from_email
    message["To"] = to_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))
    
    try:
        # Connect to Gmail
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Secure the connection
        server.login(from_email, EMAIL_PASSWORD)
        
        # Send email
        server.send_message(message)
        server.quit()
        
        print(f"✅ Email sent to {to_email}")
        return True
        
    except Exception as e:
        print(f"❌ Failed to send email: {e}")
        return False

if __name__ == "__main__":
    # Test email
    send_email(
        subject="Test Email",
        body="If you're reading this, the email system works!",
        to_email="em.sun2019@gmail.com"  # Send to yourself for testing
    )