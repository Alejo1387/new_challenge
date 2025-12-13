import uuid

def create_unique():
    return uuid.uuid7().hex[:12]