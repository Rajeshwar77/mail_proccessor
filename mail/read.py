class EmailProcessor:
    def __init__(self, provider):
        self.provider = provider

    def process_emails(self, email):
        self.provider.fetch_emails()

    def mark_as_read(self, email_id):
        self.provider.mark_as_read(email_id)

    def move_message(self, email_id, folder):
        self.provider.move_message(email_id, folder)
