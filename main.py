import streamlit as st
from openai import OpenAI
from streamlit_js_eval import streamlit_js_eval
from system_prompt_generator import system_prompt
from data_loader import load_data

st.set_page_config(layout="wide")

st.title("Talk to Text")

text_col, chat_col = st.columns(2)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

if "context" not in st.session_state:
    st.session_state.context = ""

if "query" not in st.session_state:
    st.session_state.query = ""
    

# Text Section
with text_col:
    st.header("Enter your text here")
    with st.form("my_form"):
        text = st.text_area("Enter text")
        submitted = st.form_submit_button("Submit", type="primary")
    
    if submitted:
        with st.spinner("Loading data ..."):
            st.session_state.context = text
            load_data()
            st.success("You text is uploaded successfully. You can start chating")
        

    reset=st.button("Reset")
    if reset:
        st.session_state.vector_store = None
        st.session_state.messages = []
        st.session_state.context = ""
        st.session_state.query = ""
        streamlit_js_eval(js_expressions="parent.window.location.reload()")

        
# Chat Section
with chat_col:
    st.header("Chat Section")

    if st.session_state.context:
        # st.session_state.messages = [
        #             {"role": "system", "content": system_prompt()}
        #         ]
        # print(system_prompt())

        # Set OpenAI API key from Streamlit secrets
        client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

        # Display chat messages from history on app rerun
        for i in range(len(st.session_state.messages)):
            message = st.session_state.messages[i]
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # # Accept user input.
        # if prompt := st.chat_input("What is up?"):
        #     # Add user message to chat history
        #     st.session_state.messages.append({"role": "user", "content": prompt})
        #     # Display user message in chat message container
        #     with st.chat_message("user"):
        #         st.markdown(prompt)

        # Accept user input.
        if prompt := st.chat_input("What is up?"):
            st.session_state.query = prompt

            # Display user message in chat message container
            with st.chat_message("user"):
                st.markdown(prompt)

        # Display assistant response in chat message container
        # try:
        with st.chat_message("assistant"):
            stream = client.chat.completions.create(
                model='gpt-4.1-mini',
                messages=[
                    {"role": "system", "content": system_prompt()},
                    {"role": "user", "content": st.session_state.query},
                ],
                stream=True,
            )
            response = st.write_stream(stream)
            # print(stream.choices[0].message.content)
        # except:
        #     st.warning("Sorry! Unable to generate response due to high traffic")