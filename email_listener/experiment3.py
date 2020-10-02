"""email_listener: Listen in an email folder and process incoming emails."""
import email
import html2text
from imapclient import IMAPClient
import os
import time
from email_listener.__init__ import EmailListener

email = os.environ['EL_EMAIL']
app_password = os.environ['EL_APW']
# Read from the folder 'email_listener'
folder = "email_listener"
# Save attachments to a dir saved in env
attachment_dir = os.environ['EL_FOLDER']
el = EmailListener(email, app_password, folder, attachment_dir)
print("el: {}".format(el.scrape(None)))

