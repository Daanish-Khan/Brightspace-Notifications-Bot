"""email_listener: Listen in an email folder and process incoming emails."""
import email
import html2text
from imapclient import IMAPClient
import os
import time
import datetime

from helpers import (
    calc_timeout,
    get_time,
)

t1 = get_time()
print(t1)
print(datetime.datetime.utcnow().timestamp())

t2 = datetime.datetime.now()
dt = datetime.datetime.fromtimestamp(t2.timestamp())
delta = datetime.timedelta(minutes=10)
print(t2)
print(dt)
print(t2 + delta)


