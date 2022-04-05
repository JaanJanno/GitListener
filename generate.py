import uuid
token = uuid.uuid4()
with open('token.cfg', 'w', encoding = 'utf-8') as file:
    file.write(str(token))