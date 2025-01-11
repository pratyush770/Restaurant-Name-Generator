# import streamlit as st
from secret_key import sec_key
from langchain_huggingface import HuggingFaceEndpoint
from langchain_core.prompts import PromptTemplate
from langchain.schema.runnable import RunnableSequence
import os
import random
import json

# sec_key = st.secrets["HUGGINGFACEHUB_API_TOKEN"]
os.environ['HUGGINGFACEHUB_API_TOKEN'] = sec_key

repo_id = "mistralai/Mistral-7B-Instruct-v0.3"
llm = HuggingFaceEndpoint(
    repo_id=repo_id, temperature=0.6,
    model_kwargs={"max_length": 128, "token": sec_key}
)


def get_rest_name_and_items(cuisine):
    themes = ["fast food", "family style", "buffet", "cafe", "bar", "eco-friendly"]  # randomly choose a theme
    random_theme = random.choice(themes)
    question = f"Suggest a restaurant name for {cuisine} food and list some popular dishes."
    template = """
    Question: {question}
    Provide the output strictly in the following JSON format without any extra text or indentation issues. The restaurant name and dishes should align with the given theme: {random_theme}. Give 8 menu_items:
    {{
        "rest_name": "Themed restaurant name here",
        "menu_items": ["Themed Dish 1", "Themed Dish 2", "Themed Dish 3"]
    }}
    """
    prompt = PromptTemplate(template=template, input_variables=["question", "random_theme"])
    sequence = RunnableSequence(first=prompt, last=llm)
    response = sequence.invoke({"question": question, "random_theme": random_theme})

    try:
        response_dict = json.loads(response)  # convert the JSON response into a Python dict
        return response_dict
    except json.JSONDecodeError as e:
        print(f"JSON parsing error: {e}")
        print(f"Raw response: {response}")
        return {"rest_name": "Unknown", "menu_items": []}


if __name__ == "__main__":
    print(get_rest_name_and_items("Indian"))
