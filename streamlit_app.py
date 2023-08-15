#Install necessary dependencies
import streamlit as st
import pprint
import google.generativeai as palm
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.llms import VertexAI
from langchain import PromptTemplate, LLMChain
from gtts import gTTS
from io import BytesIO
import tempfile

#Mention your api key here provided to you by https://makersuite.google.com/app
palm.configure(api_key=st.secrets['PALM-API-KEY'])
models = [m for m in palm.list_models() if 'generateText' in m.supported_generation_methods]
model = models[0].name

#Title of application
st.title("A chatbot with the capabilities of PalmAI 🤖")

#Setting up the prompt area of app
prompt = st.text_input("Enter your question here..")
if prompt:
    completion = palm.generate_text(
        model=model,
        prompt=prompt,
        temperature=0.7,
        # The maximum length of the response
        max_output_tokens=800
)
    st.write(completion.result)
    #Using google-text-to-speech library
    tts = gTTS(completion.result, lang='en')

# Save audio to temporary file
    with tempfile.NamedTemporaryFile(delete=False) as fp:
        tts.save(fp.name)
        audio_path = fp.name

# Read the audio file
    with open(audio_path, 'rb') as f:
        audio_bytes = f.read()

# Play the audio
    st.audio(audio_bytes, format='audio/mp3')
else:
    st.write("type something and hit enter...")
