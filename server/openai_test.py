
import openai
import apikeys
openai.api_key = apikeys.openai_apikey
from config import app, db, api
from models import User, StoryInput, ChatGptResponse, DallEResponse





full_test = "Illustrate this image in the style of digital art smooth. The illustation is for a children's book about a child named Jenna, 13 years old, Native American, with brown eyes, long black hair in a braid, wearing a tanktop (use seed 0 for generating Jenna). The illustation should go with the following text: Jenna was a 13 year-old girl who lived in Florida. She loved the sunshine, the sea, and the sand. But what she loved most of all was sailing. When she caught the wind, white sails billowing, and saw the blue horizon ahead of her, she felt alive with excitement. Jenna was determined to be the best sailor she could possibly be."
#  style “digital art smooth”


#  Solution: Adding faceless as a descriptor to the subject or use the word abstract. Just spend more credits and re-render till you get a good face.

#  Solution: Add more objects or details about the background, such as “next to a tree”, “with the sunset in the background”, “with the universe in the background”. These create complexities in the drawing and forces Dall-E to move away from drawing one big image.


# Grab a chatGPTresponse to test out with Dall-E

test_text01 = "Jenna was a 13 year-old girl who lived in Florida. She loved the sunshine, the sea, and the sand. But what she loved most of all was sailing. When she caught the wind, white sails billowing, and saw the blue horizon ahead of her, she felt alive with excitement. Jenna was determined to be the best sailor she could possibly be."

# prompt="Illustrate this image in the style of digital art smooth. The illustation is for a children's book about a child named Jenna, 13 years old, Native American, with brown eyes, long black hair in a braid, wearing a tanktop (use seed=0 for generating Jenna). The setting is the Florida Keys - please include this in the background and make Jenna take up only about one-tenth of the image. The illustation should go with the following text: Jenna was a 13 year-old girl who lived in Florida. She loved the sunshine, the sea, and the sand. But what she loved most of all was sailing. When she caught the wind, white sails billowing, and saw the blue horizon ahead of her, she felt alive with excitement. Jenna was determined to be the best sailor she could possibly be.",


# Illustrate this image in the style of digital art smooth. Please make Jenna take up only a small amount of the image, around one-eight of the image size, with the rest being items that fit the following story: Jenna was a 13 year-old girl who lived in Florida. She loved the sunshine, the sea, and the sand. But what she loved most of all was sailing. When she caught the wind, white sails billowing, and saw the blue horizon ahead of her, she felt alive with excitement. Jenna was determined to be the best sailor she could possibly be.



# Suggestions based on Chat-GPT
# "Digital art illustration of a Florida beach scene with bright sunshine and sparkling sea. On one side, occupying about an eighth of the image, is Jenna, a 13-year-old girl with a determined look on her face. In the background, there's a sailboat with white sails billowing against the blue horizon. The sand is golden, and there are seashells scattered around. The essence of the image should capture Jenna's love for sailing and her ambition to be the best sailor."

# "Digital art depiction of a vast ocean with the sun reflecting on its surface. On the far left, Jenna, a 13-year-old girl, stands looking out at the sea, taking up approximately one-eighth of the image. Nearby, there's a sailboat with white sails catching the wind, conveying the thrill and excitement of sailing. The horizon is clear blue, symbolizing Jenna's endless possibilities as a sailor."

# "Smooth digital art showcasing a coastal scene from Florida. In the bottom right corner, Jenna, a young 13-year-old, is seen holding a miniature sailboat, representing her dreams. The majority of the image is filled with a beautiful seascape: white sails of distant boats billow in the wind, the sun casts a golden hue on the sand, and the waves gently touch the shoreline."

# "Digital art of a picturesque Florida setting with a focus on sailing. In a small section, Jenna, a 13-year-old girl with a passion for sailing, is depicted holding a compass or a map, symbolizing her determination. The rest of the image is dominated by the vast sea, with several sailboats, their white sails full from the wind, racing towards the blue horizon. The ambiance should evoke a sense of adventure and aspiration."

response_dalle = openai.Image.create(
  prompt="Digital art illustration of a children's park in New York City. In the centre of the image, occupying about one-eighth of the image size, is Lydia, a 2-year-old child wearing a pink dress, with Asian features, and wavy brown hair. Her parents and other children can be seen in the background, playing on the swings or having a picnic in the park. All characters should be faceless or shown looking away from us. The essence of the image should capture Lydia's joy and happiness on a family outing.",
  n=1,
  size="1024x1024"
)
image_url = response_dalle['data'][0]['url']
print(image_url)


# "child_age": "13",
# "child_clothing": "a tank top",
# "child_eyecolor": "brown",
# "child_hairstyle": "long black hair in a braid",
# "child_interests": "sailing",
# "child_location": "Florida",
# "child_name": "Jenna",
# "child_other_features": "",
# "child_race": "Native American",
# "id": 16,
# "story_setting": "the Florida Keys",
# "user_id": 1







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