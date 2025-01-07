from secret_key import sec_key
from langchain_huggingface import HuggingFaceEndpoint
from langchain_core.prompts import PromptTemplate
from langchain.schema.runnable import RunnableSequence
import os

sec_key = st.secrets["HUGGINGFACEHUB_API_TOKEN"]
os.environ['HUGGINGFACEHUB_API_TOKEN'] = sec_key

repo_id = "mistralai/Mistral-7B-Instruct-v0.3"
llm = HuggingFaceEndpoint(
    repo_id=repo_id, temperature=0.6,
    model_kwargs={"max_length": 128, "token": sec_key}
)


def get_rest_name_and_items(cuisine):
    question = f"Suggest a restaurant name for {cuisine} food and list some popular dishes."
    template = """
    Question: {question}
    Provide the output strictly in the following JSON format without any extra text or indentation issues and give 8 menu_items:
    {{
        "rest_name": "Your restaurant name here",
        "menu_items": ["Dish 1", "Dish 2", "Dish 3"]
    }}
    """
    prompt = PromptTemplate(template=template, input_variables=["question"])
    sequence = RunnableSequence(first=prompt, last=llm)
    response = sequence.invoke({"question": question})
    try:
        # Parse the response into a dictionary
        import json
        response_dict = json.loads(response)  # convert the json response into python dict
        return response_dict
    except json.JSONDecodeError as e:
        print(f"JSON parsing error: {e}")
        print(f"Raw response: {response}")
        return {"rest_name": "Unknown", "menu_items": []}


if __name__ == "__main__":
    print(get_rest_name_and_items("Indian"))
