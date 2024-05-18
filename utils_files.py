import re
import pickle
from pathlib import Path
from unidecode import unidecode


CONFIG_FOLDER=Path(__file__).parent / 'config'
CONFIG_FOLDER.mkdir(exist_ok=True)

MESSAGES_FOLDER=Path(__file__).parent / 'messages'
MESSAGES_FOLDER.mkdir(exist_ok=True)
DISCONVERT_CACHE = {}


def get_chat_name(messages):
  message_name = ''
  for message in messages:
    if message['role'] == 'user':
      message_name = message['content'][:30]
      break
  return message_name
def save_messages(messages):
  if len(messages) <= 0:
    return False
  message_name = get_chat_name(messages)
  file_name = convert_name_message(message_name)
  file_to_save = {
                  'message_name': message_name, 
                  'file_name': file_name,
                  'messages': messages
                }
  with open(MESSAGES_FOLDER / file_name, 'wb') as f:
    pickle.dump(file_to_save, f)
def convert_name_message(message_name):
    file_name = unidecode(message_name)
    file_name = re.sub('\W+', '', file_name).lower()
    return file_name
def desconvert_name_message(file_name):
  if not file_name in DISCONVERT_CACHE:
    message_name = read_message_by_file_name(file_name, key='message_name')
    DISCONVERT_CACHE[file_name] = message_name
  return DISCONVERT_CACHE[file_name]
def read_message_by_file_name(file_name, key='messages'):
  with open(MESSAGES_FOLDER / file_name, 'rb') as f:
    messages = pickle.load(f)
  return messages[key]
def read_messages(messages, key='messages'):
  if len(messages) <= 0:
    return []
  message_name = get_chat_name(messages)
  file_name = convert_name_message(message_name)
  with open(MESSAGES_FOLDER / file_name, 'rb') as f:
    messages = pickle.load(f)
  return messages[key]
def listar_conversas():
  conversas = list(MESSAGES_FOLDER.glob('*'))
  conversas = sorted(conversas, key=lambda item: item.stat().st_mtime_ns, reverse=True)
  return [c.stem for c in conversas]
def save_key(key):
  with open(CONFIG_FOLDER / 'key', 'wb') as f:
    pickle.dump(key, f)
def load_key():
  if (CONFIG_FOLDER / 'key').exists():
      with open(CONFIG_FOLDER / 'key', 'rb') as f:
        return pickle.load(f)
  else:
    return ''