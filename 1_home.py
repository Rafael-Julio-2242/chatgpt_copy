import streamlit as st
from utils_openai import get_model_response

from utils_files import *


def initialize():
  if not 'messages' in st.session_state:
    st.session_state['messages'] = []
  if not 'current_chat' in st.session_state:
    st.session_state['current_chat'] = ''
  if not 'model' in st.session_state:
      st.session_state['model'] = 'gpt-3.5-turbo'
  if not 'api_key' in st.session_state:
      st.session_state['api_key'] = load_key()


def tab_conversas(tab):
  tab.button('➕ Nova Conversa', key='nova_conversa', on_click=select_message, args=('',), use_container_width=True)
  tab.markdown('')
  conversas = listar_conversas()
  
  for conversa in conversas:
    message_name = desconvert_name_message(conversa).capitalize()
    if len(message_name) == 30:
      message_name += '...'
    tab.button(
      desconvert_name_message(conversa).capitalize(), 
      key=conversa, 
      on_click=select_message, 
      args=(conversa,),
      disabled=conversa==st.session_state['current_chat'],
      use_container_width=True
      )

def tab_config(tab):
  choosen_model = tab.selectbox(
      'Select Model', 
      ['gpt-3.5-turbo', 'gpt-4']
    )
  st.session_state['model'] = choosen_model
  
  key = tab.text_input('Add your OpenAI API Key', value=st.session_state['api_key'])
  if key != st.session_state['api_key']:
    st.session_state['api_key'] = key
    save_key(key)
    tab.success('Key saved successfully!')

def select_message(file_name):
  if file_name == '':
    st.session_state['messages'] = []
  else:
    messages = read_message_by_file_name(file_name)
    st.session_state['messages'] = messages
  st.session_state['current_chat'] = file_name

def pagina_principal():
  messages = read_messages(st.session_state['messages'])
  
  st.header('GPT Chatbot Training Copy')
  
  for message in messages:
    chat = st.chat_message(message['role'])
    chat.markdown(message['content'])
  
  prompt = st.chat_input('Enter your message')
  
  if prompt:
    if st.session_state['api_key'] == '':
      st.error('ADD the API KEY FIRST!')
    else:
      new_message = {'role': 'user', 'content': prompt}
      chat = st.chat_message(new_message['role'])
      chat.markdown(new_message['content'])
      messages.append(new_message)
      
      
      chat = st.chat_message('assistant')
      placeholder = chat.empty()
      full_response = ''
      placeholder.markdown('▌')
      responses = get_model_response(messages, open_ai_key=st.session_state['api_key'] ,stream=True, model=st.session_state['model'])
      
      for response in responses:
        full_response += response.choices[0].delta.get('content', '')
        placeholder.markdown(full_response + "▌")
      placeholder.markdown(full_response)
      
      new_response = {'role': 'assistant', 'content': full_response}
      messages.append(new_response)
      
      st.session_state['messages'] = messages
      save_messages(messages)

def main():
  initialize()
  pagina_principal()
  tab1, tab2 = st.sidebar.tabs(['Conversas','Configurações'])
  tab_conversas(tab1)
  tab_config(tab2)

if __name__ == '__main__':
  main()