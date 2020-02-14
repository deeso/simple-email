# Adam Pridgen
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

from . standard_logger import Logger
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.encoders import encode_base64
from os.path import basename
from .consts import *
from .config import Config
from .util import FileUtil

# from simplified_email import *
# host = 'smtp.gmail.com'
# port = 587
# password = PASSWORD
# user = 'adam.pridgen@thecoverofnight.com'
# recipient = 'adam.pridgen.phd@gmail.com'
# sender = 'dso@thecoverofnight.com'

# body = "test"
# subject = "test send"
# body_content_type = 'text'

# s = SendEmail(host, port, user, password)

# s.send_mime_message(sender, recipient, subject=subject,
#                     body_content_type=body_content_type,
#                     body=body)


class SendEmail(object):
    logger = Logger('ulm-sendemail')

    DEFAULT_VALUES = {
        SMTP_HOST: '127.0.0.1',
        SMTP_PORT: 25,
        SMTP_USERNAME: None,
        SMTP_PASSWORD: None,
        SMTP_USE_TLS: False,
        SMTP_LEVEL: 0,
    }

    def __init__(self, **kwargs):

        for k, v in self.DEFAULT_VALUES.items():
            if k in kwargs:
                setattr(self, k, kwargs.get(k, v))


    @classmethod
    def from_config(cls, **kwargs):
        kwargs = {}
        for k, dv in cls.DEFAULT_VALUES.items():
            v = Config.get_value(k, dv)
            if k not in kwargs:
                kwargs[k] = v
        return cls(**kwargs)

    def send_email(self, sender, recipients, message):
        x = "Connecting to server"
        self.logger.action('sendemail.send_mime_messages', sender, x)
        server = smtplib.SMTP(self.smtp_host, self.smtp_port)
        server.set_debuglevel(self.smtp_level)

        if self.smtp_use_tls:
            x = "starting TLS"
            self.logger.action('sendemail.send_email', sender, x)
            server.starttls()

        if self.smtp_username is not None and self.smtp_password is not None:
            x = "authenticating as: %s"% self.user
            self.logger.action('sendemail.send_email', sender, x)
            server.login(self.smtp_username, self.smtp_password)

        elif self.smtp_password is not None:
            x = "authenticating as: %s"% sender
            self.logger.action('sendemail.send_email', sender, x)

            server.login(sender, self.smtp_password)

        x = "Sending email as %s to %d recipients"% (sender, len(recipients))
        self.logger.action('sendemail.send_email', sender, x)

        server.sendmail(sender, recipients, message)
        x = "email send completed"
        self.logger.action('sendemail.send_email', sender, x)

        server.quit()

    def send(self, sender, recipient, message, cc=[], bcc=[]):

        recipients = [recipient, ] + cc + bcc
        if message is None:
            x = "Message must be a string or a MIMEmultipart instance"
            self.logger.action('sendemail.send_email', sender, x)
            raise Exception(x)
        msg_str = message

        if not isinstance(message, str):
            msg_str = message.as_string()

        return self.send_email(sender, recipients, msg_str)

    def add_attachments(self, message, attachment_name=None, attachment=None, filenames_contents=[]):
        filenames_contents = [ i for i in filenames_contents]
        if attachment_name is not None and attachment is not None:
            filenames_contents.append({FILENAME: attachment_name, BUFFERED_CONTENT: attachment})

        for filename_content in filenames_contents:
            filename = filename_content[FILENAME]
            content = filename_content[BUFFERED_CONTENT]
            application, subtype = FileUtil.buffer_mime_type(content).split('/')
            a_content = MIMEBase(application, subtype)
            a_content.set_payload(content)
            encode_base64(a_content)
            a_content.add_header('Content-Disposition', 'attachment; filename="{}"'.format(basename(filename)))
            x = "adding mime attachment (%s) to email len=%d"% (filename, len(content))
            self.logger.action('sendemail.add_attachments', 'email_sender', x)
            message.attach(a_content)

    def send_mime_message(self, sender, recipient, cc=[], bcc=[],
                           subject='', encoding='us-ascii',
                           body_content_type='plain', body='',
                           attachment_name=None, attachment=None, filenames_contents=[]):

        x = "Building mime message to: %s"% (recipient)
        self.logger.action('sendemail.send_mime_message', sender, x)
        message = MIMEMultipart()
        message['From'] = sender
        message['To'] = recipient
        message['Subject'] = subject
        message['Cc'] = ",".join(cc)
        message['Bcc'] = ",".join(bcc)
        bcontent = MIMEText(body, body_content_type)
        message.attach(bcontent)
        self.add_attachments(message, attachment_name=attachment_name,
                             attachment=attachment,
                             filenames_contents=filenames_contents)

        return self.send(sender, recipient, message, cc=cc, bcc=bcc)

    def send_mime_zip(self, sender, recipient, cc=[], bcc=[], subject='', encoding='us-ascii',
                      body_content_type='plain', body='', attachment_name=None,
                      attachment=None, attachment_content_type=None, filenames_contents=[], zip_files=[]):
        # ref: https://stackoverflow.com/questions/45618222/adding-to-an-email-a-zip-file
        if zip_files is None or len(zip_files) == 0:
            return self.send_mime_message(sender, recipient, cc, bcc, subject,
                                          encoding, body_content_type, body,
                                          attachment_name, attachment,
                                          attachment_content_type)

        x = "Building mime message to: %s"% (recipient)
        self.logger.action('sendemail.send_mime_zips', sender, x)
        message = MIMEMultipart()
        message['From'] = sender
        message['To'] = recipient
        message['Subject'] = subject
        message['Cc'] = ",".join(cc)
        message['Bcc'] = ",".join(bcc)
        content = MIMEText(body, body_content_type)
        message.attach(content)

        filenames_contents = [ i for i in filenames_contents]
        for zf in zip_files:
            filenames_contents.append({FILENAME:zf, BUFFERED_CONTENT: open(zf, 'rb').read()})

        self.add_attachments(message, attachment_name=attachment_name,
                             attachment=attachment,
                             filenames_contents=filenames_contents)

        return self.send(sender, recipient, message, cc=cc, bcc=bcc)
