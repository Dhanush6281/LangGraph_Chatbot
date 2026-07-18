from app.database import db

db.save_message("user", "Hello")
db.save_message("assistant", "Hi Dhanush!")

messages = db.get_messages()

for role, message in messages:
    print(role, ":", message)