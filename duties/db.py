_database = []

def call_database(action="SELECT", data=None):
    if action == "INSERT" and data is not None:
        _database.append(data)
    return _database