class Duty:
    def __init__(self, identifier, description):
        self.identifier = identifier
        self.description = description
    
    def has_identifier(self, identifier: str) -> bool:
        if len(self.identifier) > 0:
            return self.identifier == identifier
        else:
            return False
        
    def has_description(self, description: str) -> bool:
        if len(self.description) > 0:
            return self.description == description
        else:
            return False
        
    def matches(self, identifier, description):
        return self.identifier == identifier and self.description == description
