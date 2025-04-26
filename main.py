import streamlit as st
from openai import OpenAI
from streamlit_js_eval import streamlit_js_eval
from system_prompt_generator import system_prompt
from data_loader import load_data

st.set_page_config(layout="wide")

st.markdown("<h1 style='text-align: center;'>Talk to Text</h1>", unsafe_allow_html=True)

text_col, spacer, chat_col = st.columns([5, 1, 5])

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

if "context" not in st.session_state:
    st.session_state.context = ""

if "query" not in st.session_state:
    st.session_state.query = ""
    

# Text Section
with text_col:
    st.header("📝 Paste or Type Text")
    with st.form("my_form"):
        text = st.text_area("Enter text")
        submitted = st.form_submit_button("Submit", type="primary")
    
    if submitted:
        with st.spinner("🧠 Processing your text... Please wait"):
            st.session_state.context = text
            load_data()
            st.success("Your text was uploaded successfully. Start chatting!")
        

    reset=st.button("Reset")
    if reset:
        st.session_state.vector_store = None
        st.session_state.messages = []
        st.session_state.context = ""
        st.session_state.query = ""
        streamlit_js_eval(js_expressions="parent.window.location.reload()")

        
# Chat Section
with chat_col:
    st.header("💬 Chat Window")

    if st.session_state.context:
        # st.session_state.messages = [
        #             {"role": "system", "content": system_prompt()}
        #         ]
        # print(system_prompt())

        # Set OpenAI API key from Streamlit secrets
        # client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
        client = OpenAI(
            api_key=st.secrets["GOOGLE_API_KEY"],
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
        )

        # Display chat messages from history on app rerun
        for i in range(1, len(st.session_state.messages)):
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
        prompt = st.chat_input("What is up?")
        try:
            if prompt:
                st.session_state.query = prompt

                # Display user message in chat message container
                with st.chat_message("user"):
                    st.markdown(prompt)

            # Display assistant response in chat message container
            # try:
                with st.chat_message("assistant"):
                    with st.spinner("✍️ Generating response..."):
                        stream = client.chat.completions.create(
                            model='gemini-2.0-flash',
                            messages=[
                                {"role": "system", "content": system_prompt()},
                                {"role": "user", "content": st.session_state.query},
                            ],
                            stream=True,
                        )
                        response = st.write_stream(stream)
        except Exception as e:
            st.warning(f"⚠️ Error: {e}. Please try again later.")