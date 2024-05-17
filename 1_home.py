import streamlit as st
import os
import openai
from dotenv import load_dotenv
load_dotenv()


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


def pagina_principal():
  
  if not 'messages' in st.session_state:
    st.session_state['messages'] = []
  
  messages = st.session_state['messages']
  
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


pagina_principal()