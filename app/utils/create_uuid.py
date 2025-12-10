import uuid

def create_unique():
    return uuid.uuid4().hex[:12]