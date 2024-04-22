import json

# from generate_panels import generate_panels
# from stability_ai import text_to_image
# from add_text import add_text_to_panel
# from create_strip import create_strip

from stability_ai import text_to_image
from add_text import add_text_to_panel
from create_strip import create_strip

from openai import OpenAI
client = OpenAI(api_key='XXXXX')

template = """
You are a cartoon creator.

You will be given a short scenario, you must split it in 6 parts.
Each part will be a different cartoon panel.
For each cartoon panel, you will write a description of it with:
 - the characters in the panel, they must be described precisely each time
 - the background of the panel
The description should be only word or group of word delimited by a comma, no sentence.
Make sure the description of characters are the same across all panels. VERY IMPORTANT.
You must use the same characters description for all panels.
You will also write the text of the panel.
The text should not be more than 1 small sentences.

Example input:
Write a story about two girls playing catch

Example output:

{'1':{'description': '2 girls, one wearing glasses, one wearing hat, sitting at the office, with computers',
    'text': 'Catch the ball! This is fun.'} }

# end

Short Scenario:
{scenario}

Split the scenario in 6 parts:
"""


def create_storyline(prompt, STYLE):

  response = client.chat.completions.create(
    model="gpt-4-1106-preview",
    messages=[
      {"role": "system", "content": "{}.Your response should be in JSON format.".format(template)},
      {"role": "user", "content": "{}".format(prompt)}
    ],
    response_format={"type": "json_object"}
  )

  response_json=eval(response.choices[0].message.content)
  print(response_json)

  return response_json

  # SCENARIO = """
  # Characters: Peter is a tall guy with blond hair. Steven is a small guy with black hair.
  # Peter and Steven walk together in new york when aliens attack the city. They are afraid and try to run for their lives. The army arrive and save them.
  # """


def create_comic(response_json, style):
  panel_images = []
  print(response_json)
  for key in response_json.keys():
      print(key)
      panel_prompt=response_json[key]['description'] + ", cartoon box, " + style  

      panel_image = text_to_image(panel_prompt, int(key))
      panel_image_with_text = add_text_to_panel(response_json[key]["text"], panel_image)
      panel_image_with_text.save(f"output/panel-{key}.png")
      

      panel_images.append(panel_image_with_text)
  #create_strip(panel_images)
  return create_strip(panel_images)
  
  