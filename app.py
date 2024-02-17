import streamlit as st
from dotenv import load_dotenv
import os
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi

#loads all environment variables
load_dotenv()

#prompt
prompt = "You are an intelligent youtube video summarizer. Make use of professional words and explain in detailed manner . You will take the transcript text and summarize the entire video and provide important and helpful summary in paragraph and points format within 300 words. Please provide the summary here : "

genai.configure(api_key=os.getenv("Google_API_KEY"))


def extract_transcript(youtube_video_url):
    try:
        video_id = youtube_video_url.split("=")[1]
        print(video_id)  # "=" splits the url into index 0 and 1 . This index identifies the video id that is located at index 1
        transcript_text = YouTubeTranscriptApi.get_transcript(video_id)
        transcript = ""
        for i in transcript_text:
            transcript += "." + i["text"]
        return transcript
    
    except Exception as e:
        raise e
    

def generate_gemini_content(transcript_text, prompt):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt+transcript_text)
    return response.text

st.title("Youtube Video Summarizer")
youtube_link = st.text_input("Youtube Video Link : ")
#to get the video thumbnail
if youtube_link:
    video_id = youtube_link.split("=")[1]
    print(video_id)
    st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True) #default thumbnail url for youtube
if st.button("Summarize"):
    transcript_text = extract_transcript(youtube_link)  

    if transcript_text:
           summary = generate_gemini_content(transcript_text, prompt)
           st.markdown("summary : ")
           st.write(summary)