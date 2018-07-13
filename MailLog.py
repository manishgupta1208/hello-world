
import zipfile
import glob
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE,formatdate
import smtplib
from os.path import basename
import os

def zip_files():
    zf = zipfile.ZipFile('/var/log/supervisor/logfiles.zip',mode='a')
    try:
        for logfile in glob.glob("/var/log/supervisor/*BIB*.log*"):
            print(logfile)
            zf.write(logfile,compress_type=zipfile.ZIP_DEFLATED)
    except Exception as e:
        print(e)
    finally:
        zf.close

def send_files(source_glob):
    try:
        files = []
        for file in glob.glob(source_glob):
            files.append(file)
            send_mail("bearsremoterpi@gmail.com",files)

        for logfile in glob.glob(source_glob):
            os.remove(logfile)
    except Exception as e:
        print(e)

def send_mail(address,data):
    print("Sending mail")
    try:
        msg = MIMEMultipart()
        msg['From'] = address
        msg['To'] = address
        msg['Date'] = formatdate(localtime=True)
        msg['Subject'] = "Log files"

        msg.attach(MIMEText("Files for your reference"))
        for f in data:
            with open(f,"rb") as fil:
                part = MIMEApplication(
                    fil.read(),
                    Name=basename(f)
                    )
                part['Content-Disposition']='attachment;filename="%s"' % basename(f)
                msg.attach(part)

        server = smtplib.SMTP_SSL(host='smtp.gmail.com',port=465,timeout=15)
        server.ehlo()
        server.login("bearsremoterpi@gmail.com","b3ar5@1234")
        server.sendmail(address,address,msg.as_string())
        print("File sent")
        server.close()
    except Exception as e:
        print(e)
          
def main():
    print("Zipping files")
    zip_files()
    send_files("/var/log/supervisor/logfiles.zip")
    
if __name__ == "__main__":
    main()
