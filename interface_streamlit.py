import streamlit as st
from langchain_mistralai import ChatMistralAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

st.title("Dispute Resolution Chatbot")

st.write(
    """
    This chatbot facilitates resolution generation by reducing conflict between 
    two parties through constructive feedback, delivered via text or voice, after 
    both parties have presented their arguments.
    """
)

mistral_api_key = st.text_input("Mistral API Key", type="password")

if st.button("Submit API Key"):
    if mistral_api_key:
        st.success("API Key submitted successfully!")

def generate_resolution(first_party_prompt, second_party_prompt):

    llm = ChatMistralAI(
        model="mistral-large-latest",
        max_retries=2,
        api_key=mistral_api_key or st.secrets["MISTRAL_API_KEY"],
    )

    prompt_template = PromptTemplate(
        input_variables=["first_party", "second_party"],
        template="""
        You are a dispute resolution assistant. Your goal is to reduce conflict between two parties by providing constructive feedback and suggesting a resolution.

        First Party Argument: {first_party}
        Second Party Argument: {second_party}

        Analyze the arguments, identify the main conflict, and suggest a resolution. Ensure the response is concise, comprehensive, and neutral.
        """
    )

    chain = LLMChain(llm=llm, prompt=prompt_template)
    response = chain.run(first_party=first_party_prompt, second_party=second_party_prompt)
    return response


with st.form("dispute_form"):
    first_party_prompt = st.text_area("Argument from First Party:")
    second_party_prompt = st.text_area("Argument from Second Party:")
    submitted = st.form_submit_button("Submit")

    if submitted:
        if first_party_prompt.strip() and second_party_prompt.strip():

            st.write("Generating resolution...")
            resolution = generate_resolution(first_party_prompt, second_party_prompt)
            st.success("Resolution Generated:")
            st.write(resolution)

        else:
            st.error("Please provide arguments from both parties.")