class Duty:
    def __init__(self, identifier, description):
        self.identifier = identifier
        self.description = description

    def get_identifier(self):
        return self.identifier
    
    def get_description(self):
        return self.description