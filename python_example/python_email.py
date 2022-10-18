import os
import re
import smtplib
import socket
import sys
from email import encoders
from bs4 import BeautifulSoup
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.utils import COMMASPACE, formatdate


class Email:
    def __init__(self, sender, receiver):
        self.enabled = True
        self.sender = sender
        self.receiver = receiver
        self.mail_host = 'a_good_maile_host.com'
        if self.receiver is None:
            self.enabled = False
        self.text = ""
        self.title = ""
        self.mime_images = []
        self.attachment_list = []

    def setReceiver(self, receiver_list):
        self.receiver = ";".join(receiver_list)
        self.enabled = True

    def setMainText(self, text):
        self.text = text

    def loadMainTextFromFile(self, file):
        with open(file, "r") as f:
            self.text = f.read()

    def replaceTagById(self, tag_attrs):
        """
        tag_attrs must have key: id, tag
        """
        id = tag_attrs.get("id", None)
        tag = tag_attrs.pop("tag", None)
        tag_string = tag_attrs.pop("text", "")
        if id is None or tag is None:
            return
        soup = BeautifulSoup(self.text, 'lxml')
        new_tag = soup.new_tag(tag)
        new_tag.string = tag_string
        elements_by_id = soup.select('#{}'.format(id))
        if len(elements_by_id) > 0:
            elements_by_id[0].replace_with(new_tag)
        self.text = soup.prettify()

    def replaceContentById(self, content_dict):
        """
        replace element text by id with content in content_dict
        key of dict is id
        """
        soup = BeautifulSoup(self.text, 'lxml')
        for key, value in content_dict.items():
            elements_by_id = soup.select('#{}'.format(key))
            if len(elements_by_id) > 0:
                elements_by_id[0].string = content_dict[key]
        self.text = soup.prettify()

    def addImageById(self, id, image_path):
        imagetype = 'svg+xml'
        if os.path.isfile(image_path):
            pass
        else:
            print("Failed to add image: file {} not exist!".format(image_path))
            return
        with open(image_path, 'rb') as fp:
            mail_image = MIMEImage(fp.read())
        mail_image.add_header('Content-ID', "<{}>".format(id))
        self.mime_images.append(mail_image)

    def addAttachment(self, file):
        self.attachment_list.append(file)

    def setTitle(self, title):
        self.title = title

    def send(self, text=None, attachments=None):
        if self.enabled is False:
            print("WARNING: No receiver found, email sending aborted")
            return

        if text:
            self.text = text
        if attachments:
            self.attachment_list.extend(attachments.split(';'))

        self.text, num = re.subn(r"^(?!\s\s)", "  ", self.text, flags=re.M)

        receivers = self.receiver.split(';')

        msg = MIMEMultipart()
        msg['From'] = self.sender
        msg['To'] = COMMASPACE.join(receivers)
        msg['Subject'] = self.title
        msg['Date'] = formatdate(localtime=True)
        msg.attach(MIMEText(self.text, 'html', 'utf-8'))

        for file in self.attachment_list:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(open(file, 'rb').read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(file))
            msg.attach(part)

        for mime_image in self.mime_images:
            msg.attach(mime_image)

        try:
            smtpobj = smtplib.SMTP(self.mail_host)
            smtpobj.ehlo()
            smtpobj.starttls()
            smtpobj.ehlo()
            smtpobj.sendmail(self.sender, receivers, msg.as_string())
            print("INFO:Email has been sent to %s" % (self.receiver))
            return True
        except smtplib.SMTPException:
            print("ERROR:Failed to send email.")
            return False


if __name__ == "__main__":
    print("ok")
    test_mail = Email('zenghui0_0@163.com', '784515773@qq.com')
    mail_msg = """
<p>Python test email sender...</p>
<p><a href="http://baidu.com/">click to go baidu</a></p>
"""
    test_mail.setMainText(mail_msg)
    test_mail.send()
