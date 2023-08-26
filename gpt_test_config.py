import os
import re

import dotenv
import nest_asyncio
import openai
import json

nest_asyncio.apply()

os.environ["OPENAI_API_KEY"] = dotenv.dotenv_values()["OPENAI_API_KEY"]

openai.api_key = os.environ["OPENAI_API_KEY"]



def test_query(my_text: str) -> str:
    prompt = f"""
    Using the provided text:

    "{my_text}"

     you are an expert in creating tests. I am giving you a text for constructing questions and with an answer. generate questions without asking unnecessary questions,
    just generate questions and return it as a list of objects based on the given text, Generate 5 choice questions taking this as an example of response format:

    [
    {{
          "question": "Sample question?",
          "options": {{
                "A": "Option A",
                "B": "Option B",
                "C": "Option C",
                "D": "Option D"
          }},
    "correct_answer": "A"
   }},
        
    {{
        "question": "Sample question 2?",
        "options": {{
                    "A": "Option A",
                    "B": "Option B",
                    "C": "Option C",
                    "D": "Option D"
              }},
    "correct_answer": "C"
  }}
  ]
    
    """
    response = openai.Completion.create(engine="text-davinci-003", prompt=prompt, max_tokens=500)

    response_text = response.choices[0].text

    print("responnse: ", response_text)

    try:
        list_of_dicts = json.loads(response_text)
        return list_of_dicts
    except json.JSONDecodeError:
        print("Invalid JSON string")



