import streamlit as st
from openai import OpenAI
import json



client = OpenAI()

language = st.selectbox(
    "Select reply language",
    ["English", "Italian", "German"]
)

def process_email(email, language):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": f"Classify the email (work/personal/spam), summarize it, and suggest a reply in {language}. Return JSON with keys: category, summary, reply."
            },
            {"role": "user", "content": email}
        ]
    )
    return response.choices[0].message.content

st.title("AI Email Assistant")

email_input = st.text_area("Paste your email here:")

if st.button("Process"):
    if email_input:
        result = process_email(email_input, language)
        result_dict = json.loads(result)
        st.subheader("Result")
        st.subheader("Category")
        st.write(result_dict["category"])

        st.subheader("Summary")
        st.write(result_dict["summary"])

        st.subheader("Reply")
        st.text_area("Generated Reply", result_dict["reply"], height=200)

        st.button("Copy manually: select and CTRL+C")
    else:
        st.warning("Please enter an email.")