import streamlit as st
from openai import OpenAI
from streamlit_js_eval import streamlit_js_eval
from system_prompt_generator import system_prompt
from data_loader import load_data
from langchain_community.document_loaders import PyPDFLoader
import PyPDF2

st.set_page_config(
    page_title="Talk to PDF",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="collapsed"
)


st.markdown("<h1 style='text-align: center;'>Talk to PDF</h1>", unsafe_allow_html=True)

pdf_col, spacer, chat_col = st.columns([5, 1, 5])

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

if "context" not in st.session_state:
    st.session_state.context = ""

if "query" not in st.session_state:
    st.session_state.query = ""
    

# Text Section
with pdf_col:
    st.header("📝 Upload your PDF")

    # PDF Uploader
    uploaded_pdf = st.file_uploader('📄 Select your PDF file:', type="pdf")
    print(uploaded_pdf)
    if uploaded_pdf is not None:
        # Read the PDF file
        pdf_reader = PyPDF2.PdfReader(uploaded_pdf)
        # Extract the content
        content = ""
        for page in range(len(pdf_reader.pages)):
            content += pdf_reader.pages[page].extract_text()
        # progress = st.progress(0)
        # for idx, page in enumerate(pdf_reader.pages):
        #     content += page.extract_text()
        #     progress.progress((idx+1)/len(pdf_reader.pages))
        # # Display the content
        # st.write(content)

    submitted = st.button("Upload", type="primary", disabled=(uploaded_pdf is None))
    
    if submitted:
        with st.spinner("🧠 Processing your PDF... Please wait"):
            st.session_state.context = content
            load_data()
            st.success("Your PDF was uploaded successfully. Start chatting!")
        

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
        # Set OpenAI API key from Streamlit secrets
        # client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
        # client = OpenAI(
        #     api_key=st.secrets["GOOGLE_API_KEY"],
        #     base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
        # )
        client = OpenAI(
            base_url="https://models.github.ai/inference",
            api_key=st.secrets["GITHUB_TOKEN"],
        )

        # Display chat messages from history on app rerun
        for i in range(1, len(st.session_state.messages)):
            message = st.session_state.messages[i]
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Accept user input.
        prompt = st.chat_input("What is up?")
        try:
            if prompt:
                st.session_state.query = prompt

                # Display user message in chat message container
                with st.chat_message("user"):
                    st.markdown(prompt)

            # Display assistant response in chat message container
                with st.chat_message("assistant"):
                    with st.spinner("✍️ Generating response..."):
                        stream = client.chat.completions.create(
                            model="openai/gpt-4.1-mini",
                            messages=[
                                {"role": "system", "content": system_prompt()},
                                {"role": "user", "content": st.session_state.query},
                            ],
                            stream=True,
                        )
                        response = st.write_stream(stream)
        except Exception as e:
            st.warning(f"⚠️ Error: {e}. Please try again later.")