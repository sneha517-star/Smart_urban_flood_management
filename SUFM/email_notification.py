import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

SMTP_SERVER = "smtp.gmail.com" 
SMTP_PORT = 587  

SENDER_EMAIL = os.getenv("SENDER_EMAIL", "snehamurugesan517@gmail.com")  
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD", "hbhc tnvg wwxu otpv")  

def send_progress_email(recipient, student_name, progress_data):
    """Sends a progress report email with details."""
    
    subject = f"📊 Progress Report for {student_name}"
    
    body = f"""
    <html>
        <body>
            <h2>📊 Progress Report for {student_name}</h2>
            <table border="1" cellpadding="5" cellspacing="0" style="border-collapse: collapse; width: 60%;">
                <tr>
                    <th>Attempt</th>
                    <th>Score</th>
                    <th>Correct</th>
                    <th>Difficulty Level</th>
                </tr>
    """
    
    for attempt, (score, correct, difficulty) in enumerate(progress_data, start=1):
        body += f"""
                <tr>
                    <td>{attempt}</td>
                    <td>{score}</td>
                    <td>{'✅' if correct else '❌'}</td>
                    <td>{difficulty}</td>
                </tr>
        """
    
    body += """
            </table>
            <p>Keep up the good work! 🚀</p>
        </body>
    </html>
    """
    
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = recipient
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'html'))  
    
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()  
            server.login(SENDER_EMAIL, SENDER_PASSWORD)  
            server.sendmail(SENDER_EMAIL, recipient, msg.as_string())  
            print(f"✅ Progress report sent successfully to {recipient}!")
    
    except Exception as e:
        print(f"❌ Failed to send email: {str(e)}")

recipient_email = "vishnupriyamanikandan235@gmail.com"  
student_name = "Vishnu Priya"

progress_data = [
    (85, True, "Medium"),
    (72, False, "Easy"),
    (90, True, "Hard"),
    (65, False, "Medium"),
    (88, True, "Hard"),
]

send_progress_email(recipient_email, student_name, progress_data)

