import streamlit as st
import os
import openai
import re
from unidecode import unidecode
import pickle
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()

MESSAGES_FOLDER=Path(__file__).parent / 'messages'
MESSAGES_FOLDER.mkdir(exist_ok=True)
openai.api_key = os.environ['OPENAI_API_KEY']
def get_model_response(
  messages,
  model='gpt-3.5-turbo-0125',
  temperature=0,
  stream=False
):
  response = openai.ChatCompletion.create(
    model=model,
    messages=messages,
    temperature=temperature,
    stream=stream
  )
  return response

def convert_name_message(message_name):
    file_name = unidecode(message_name)
    file_name = re.sub('\W+', '', file_name).lower()
    return file_name

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

def read_messages(messages, key='messages'):
  if len(messages) <= 0:
    return []
  message_name = get_chat_name(messages)
  file_name = convert_name_message(message_name)
  with open(MESSAGES_FOLDER / file_name, 'rb') as f:
    messages = pickle.load(f)
  return messages[key]

def pagina_principal():
  
  if not 'messages' in st.session_state:
    st.session_state['messages'] = []
  
  messages = read_messages(st.session_state['messages'])
  
  st.header('GPT Chatbot Training Copy')
  
  for message in messages:
    chat = st.chat_message(message['role'])
    chat.markdown(message['content'])
  
  prompt = st.chat_input('Enter your message')
  
  if prompt:
    new_message = {'role': 'user', 'content': prompt}
    chat = st.chat_message(new_message['role'])
    chat.markdown(new_message['content'])
    messages.append(new_message)
    
    
    chat = st.chat_message('assistant')
    placeholder = chat.empty()
    full_response = ''
    placeholder.markdown('▌')
    responses = get_model_response(messages, stream=True)
    
    for response in responses:
      full_response += response.choices[0].delta.get('content', '')
      placeholder.markdown(full_response + "▌")
    placeholder.markdown(full_response)
    
    new_response = {'role': 'assistant', 'content': full_response}
    messages.append(new_response)
    
    st.session_state['messages'] = messages
    save_messages(messages)


pagina_principal()