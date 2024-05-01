import email.message
import smtplib
import os;

EMAIL_PASSWORD= os.getenv('EMAIL_PASSWORD');
EMAIL= os.getenv('EMAIL');
SMTP_HOST= os.getenv('SMTP_HOST');
SMTP_PORT= os.getenv('SMTP_PORT');
TO_EMAIL= os.getenv('SEND_EMAIL');

def sendCustomEmail(CONTENT,SUBJECT):
    try: 
        msg = email.message.Message()
        msg['Subject'] = f'{SUBJECT}'
        msg['From'] = EMAIL
        msg['To'] = TO_EMAIL
        msg.add_header('Content-Type','text/html')
        msg.set_payload(f'{CONTENT}')

        smtp = smtplib.SMTP(SMTP_HOST,SMTP_PORT)
        smtp.starttls()
        smtp.login(EMAIL,EMAIL_PASSWORD)
        smtp.sendmail(msg['From'], [msg['To']], msg.as_string())
        smtp.quit()
        print("Succesfully send")
    except Exception as ex: 
        print("Something went wrong....",ex);
