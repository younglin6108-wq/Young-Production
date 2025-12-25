import notion_client
from notion_client import Client
import inspect

print(f"File: {notion_client.__file__}")
print(dir(notion_client))

client = Client(auth="secret_fake")
print(f"Client dir: {dir(client)}")
print(f"Databases dir: {dir(client.databases)}")
