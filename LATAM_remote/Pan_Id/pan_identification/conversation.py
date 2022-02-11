class Conversation:
    conversation_id = ''
    authors = []
    messages = []
    has_abuser = False

    def __init__(self, id):
        self.conversation_id = str(id)
    
    def add_author(self, author):
        self.authors.append(author)

    def add_message(self, message):
        self.messages.append(message)

    def set_authors(self, author):
        self.authors =  author

    def set_messages(self, message):
        self.messages =  message
    
    def set_has_abusers(self, has_abuser):
        self.has_abuser =  has_abuser
    def __str__(self):
        b = '1' if self.has_abuser else '0'
        return self.conversation_id + ';' + ','.join(str(e) for e in self.authors) + ';' + b + ';' + '|'.join(str(e).rstrip() for e in self.messages)