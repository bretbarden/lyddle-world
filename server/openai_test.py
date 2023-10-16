
import openai
import apikeys
openai.api_key = apikeys.openai_apikey

# Test Chat GPT calldfc

response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Who won the world series in 2020?"},
        {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
        {"role": "user", "content": "Where was it played?"}
    ]
)



print(response)



response2 = openai.Completion.create(
  engine="text-davinci-003",
  prompt="What is the oldest known use of the concept of the number zero?",
  max_tokens=60
)

print(response2.choices[0].text.strip())



# Test Dall-E API call

response3 = openai.Image.create(
  prompt="A two year old girl who is part white, part asia, with wavy hair jsut past her shoulders and a great smile, wearing a bright colorful dress, smiling and riding a bulbasaur",
  n=1,
  size="1024x1024"
)
image_url = response3['data'][0]['url']
print(image_url)