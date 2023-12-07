from flask import Flask, request, jsonify
from flask_cors import CORS
import smtplib
import os
from email.mime.text import MIMEText
from ftplib import FTP
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
CORS(app)

FTP_USERNAME = os.getenv('FTP_USERNAME')
FTP_PASSWORD = os.getenv('FTP_PASSWORD')
FTP_SERVER = os.getenv('FTP_SERVER')
FTP_BASE_DIR = os.getenv('FTP_BASE_DIR')
FTP_UPLOAD_DIR = os.getenv('FTP_UPLOAD_DIR')

SMTP_SERVER = os.getenv('SMTP_SERVER')
SMTP_PORT = os.getenv('SMTP_PORT')
SMTP_EMAIL = os.getenv('SMTP_EMAIL')
SMTP_PASS = os.getenv('SMTP_PASS')

@app.route('/api/email', methods=['POST'])
def send_email():
    try:
        email = request.form.get('email')
        subject = request.form.get('subject')
        message_body = request.form.get('message')
        attachment = request.files.get('attachment')

        if attachment is not None: 
          send_attachment(attachment)
          ftp_link = f'ftp://{FTP_USERNAME}:{FTP_PASSWORD}@{FTP_SERVER}/{FTP_UPLOAD_DIR}/{attachment.filename}'
          message_body += f'\n\nAttachment: {ftp_link}'

        message = MIMEText(message_body)
        message['Subject'] = subject
        message['From'] = SMTP_EMAIL 
        message['To'] = email

        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
            server.login(SMTP_EMAIL, SMTP_PASS)
            server.sendmail(SMTP_EMAIL, email, message.as_string())

        return jsonify({'status': 'success', 'message': 'Email sent successfully'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

def send_attachment(attachment):
  ftp = FTP(FTP_SERVER) 
  ftp.login(user = FTP_USERNAME, passwd = FTP_PASSWORD)
  ftp.cwd(FTP_BASE_DIR + '/' + FTP_UPLOAD_DIR)

  filename = os.path.basename(attachment.filename)

  with attachment.stream as f:
    ftp.storbinary("STOR " + filename, f)
    
  file_list = ftp.nlst()
  print(file_list)

  ftp.quit()  

if __name__ == '__main__':
  app.run(debug=True)