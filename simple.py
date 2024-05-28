import streamlit as st
from openai import OpenAI

client = OpenAI(api_key=st.secrets["openai_api_key"])
import json

# Set up OpenAI API key

# Load the context as a configuration
with open("chunks.txt", "r") as f:
    context = f.read()

# Define the prompt template
prompt_template = """
Given the following context:
{context}
Generate a workflow in JSON format based on the user input: {user_input}
NOTE: Refer to the section named example in the context to see how final workflows are formed. make sure to not generate unusable one. remember apply may mean New state with create event and some other have their correspondings. for example Free means that the payment_pending is not need as there is no need for pay event. when there is a assign_office that means it may have return for actions, approve and reject all of those are added on level's you can refer to the examples in context to know how it's done.
NOTE: NO EXPLAINATIONS. JUST PURE WORKFLOW. NO SUGEESTIONS
NOTE: RETURN IT AS JSON NOT MARKDOWN
"""

def generate_workflow(user_input):
    prompt = prompt_template.format(context=context, user_input=user_input)
    response = client.chat.completions.create(model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt}
    ],
    max_tokens=1000,
    temperature=0.7)

    workflow = response.choices[0].message.content.strip()
    return workflow

def main():
    st.title("Workflow Generator")

    user_input = st.text_input("Enter the events for the workflow (e.g., APPLY-PAY)")

    if st.button("Generate Workflow"):
        workflow = generate_workflow(user_input)
        st.code(workflow, language="json")

if __name__ == "__main__":
    main()
