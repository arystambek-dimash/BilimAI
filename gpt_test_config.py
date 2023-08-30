import os
import dotenv
import openai
import json


os.environ["OPENAI_API_KEY"] = dotenv.dotenv_values()["OPENAI_API_KEY"]

openai.api_key = os.environ["OPENAI_API_KEY"]


def test_query(my_text: str) -> str:
    prompt = f"""
    Using the provided text:

        "{my_text}"
    
         you are an expert in creating tests. I am giving you a text for constructing questions and with an answer. 
         generate questions without asking unnecessary questions, just generate questions and return it as a list of 
         objects based on the given text, this is example of response format:
    
        [
        {{
        {{
              "question": "Sample question?",
              "options": {{
                    "A": "Option A",
                    "B": "Option B",
                    "C": "Option C",
                    "D": "Option D"
              }},
       }},
    
        {{
            "question": "Sample question 2?",
            "options": {{
                        "A": "Option A",
                        "B": "Option B",
                        "C": "Option C",
                        "D": "Option D"
                  }},
      }} 
      }}
      ]
    just send the list at json questions without any words and and completely write the list to the end.

    warning: The correct answer should always be on option A    
    """
    response = openai.Completion.create(engine="text-davinci-003", prompt=prompt, max_tokens=500,n=5,stop=None)

    response_text = response.choices[0]["text"]
    try:
        list_of_dicts = json.loads(str(response_text).strip())
        return list_of_dicts
    except json.JSONDecodeError:
        print("Invalid JSON string")
