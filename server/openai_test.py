
import openai
import apikeys
openai.api_key = apikeys.openai_apikey
from config import app, db, api
from models import User, StoryInput, ChatGptResponse, DallEResponse


# Grad the first story input as an example
def example_input():
    example = StoryInput.query.filter(StoryInput.id == 1).first()
    print(example.to_dict())
    return example

example_input()



# prompt = "Please write a 10-page children's book about a child provided in the context using parameteres provided in the context. The child should overcome "
# response = openai.Completion.create(
#   engine="davinci-003",
#   prompt=prompt,
#   max_tokens=50
# )

# generated_text = response.choices[0].text.strip()
# print(generated_text)



# text = "Whisper is an automatic speech recognition (ASR) system trained on 680,000 hours of multilingual and multitask supervised data collected from the web. We show that the use of such a large and diverse dataset leads to improved robustness to accents, background noise and technical language. Moreover, it enables transcription in multiple languages, as well as translation from those languages into English. We are open-sourcing models and inference code to serve as a foundation for building useful applications and for further research on robust speech processing."
# response = openai.Completion.create(
#   engine="davinci",
#   prompt=f"Summarize:\n{text}",
#   max_tokens=50
# )

# summary = response.choices[0].text.strip()
# print(summary)




# response2 = openai.Completion.create(
#   engine="text-davinci-003",
#   prompt="Write me a 10 page children's book about a girl named Sally who likes animals.",
#   max_tokens=4000
# )

# print(response2.choices[0].text.strip())




# response = openai.ChatCompletion.create(
#     model="gpt-3.5-turbo",
#     messages=[
#         {"role": "system", "content": "You are a helpful assistant."},
#         {"role": "user", "content": "Who won the world series in 2020?"},
#         {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
#         {"role": "user", "content": "Where was it played?"}
#     ]
# )

# print(response)





# # Test Dall-E API call

# response3 = openai.Image.create(
#   prompt="A two year old girl who is part white, part asia, with wavy hair jsut past her shoulders and a great smile, wearing a bright colorful dress, smiling and riding a bulbasaur",
#   n=1,
#   size="1024x1024"
# )
# image_url = response3['data'][0]['url']
# print(image_url)