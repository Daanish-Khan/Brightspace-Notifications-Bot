import email_listener


class gmail_reader:

    def __init__(self, email, password, folder):
        self.EMAIL = email
        self.PASSWORD = password
        self.folder = folder

    def login(self):
        self.listener = email_listener.EmailListener(self.EMAIL, self.PASSWORD, self.folder, "C:\\Users\\khand\\Desktop\\Projects\\Brightspace Bot\\Attachments")
        self.listener.login()

    def listen_to_messages(self, timeout, h):
        self.listener.listen(h=h, timeout=timeout, process_func=email_listener.email_processing.write_json_file)

    def logout(self):
        self.listener.logout()
