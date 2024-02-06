import assemblyai as aai
import streamlit as st
from openai import OpenAI
from st_clickable_images import clickable_images
import pandas as pd
from pytube import YouTube
import os
import requests
from time import sleep

OPENAI_API_KEY = "sk-____________________"
aai.settings.api_key = "________________"

# Input YouTube video URL
video_url = st.text_input('Enter YouTube video URL', '')  # Creates a text input box in Streamlit

if video_url:  # Checks if the input box is not empty
    # Initialize a YouTube object with the URL
    yt = YouTube(video_url)

    # Select the audio stream
    audio_stream = yt.streams.filter(only_audio=True).first()

    # Set the destination path for the audio file
    destination = '________________________________'  # Replace this with your desired path

    # Download the audio stream
    audio_stream.download(output_path=destination, filename=f"{yt.title}.mp3")

    st.write(f"Audio from '{yt.title}' has been successfully downloaded.")
    FILE_URL=f"{yt.title}.mp3"
    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(FILE_URL)
    st.audio(FILE_URL)

    ans = transcript.text
    st.write(f"This is all the captions:-")
    st.write(f"{ans}")

    from openai import OpenAI

    client = OpenAI(api_key=OPENAI_API_KEY)
    def abstract_summary_extraction(transcription):
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a highly skilled AI trained in language comprehension and summarization."},
                {"role": "user", "content": transcription}
            ],
            temperature=0,
            max_tokens=150,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )
        return response.choices[0].message.content

    final = abstract_summary_extraction(ans)
    st.write(f"This is the summary:-")
    st.write(f"{final}")
        

else:
    st.write("Please enter a YouTube video URL.")



