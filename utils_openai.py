import openai

def get_model_response(
    messages,
    open_ai_key,
    model='gpt-3.5-turbo-0125',
    temperature=0,
    stream=False
):
    openai.api_key = open_ai_key
    response = openai.ChatCompletion.create(
    model=model,
    messages=messages,
    temperature=temperature,
    stream=stream
    )
    return response