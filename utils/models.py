class Email:
    def __init__(self, user_id, sender, receiver, subject, message, received_at, message_id, history_id):
        self.user_id = user_id
        self.sender = sender
        self.receiver = receiver
        self.subject = subject
        self.message = message
        self.received_at = received_at
        self.message_id = message_id
        self.history_id = history_id    

class OAuthCredentials:
    def __init__(self, email, provider, client_id, project_id, client_secret):
        self.email = email
        self.provider = provider
        self.client_id = client_id
        self.project_id = project_id
        self.client_secret = client_secret

