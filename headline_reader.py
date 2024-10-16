import requests
from bs4 import BeautifulSoup
from gtts import gTTS
import pygame
import os
import tempfile


def fetch_headlines(url, headers):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    return [link['href'] for link in soup.find_all(class_='exn3ah91')[:5]]


def fetch_article_headline(article_url, headers):
    response = requests.get(article_url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    return soup.find(name="h1").text


def text_to_speech(text, output_file):
    tts = gTTS(text=text, lang='en')
    tts.save(output_file)


def play_audio(file):
    pygame.mixer.music.load(file)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)


if __name__ == "__main__":
    pygame.mixer.init()
    try:
        URL = 'https://www.bbc.co.uk/news'
        header = {
            "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"
                          " AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
        }

        article_urls = fetch_headlines(URL, header)
        headlines = [fetch_article_headline(f'https://www.bbc.co.uk{article}', header) for article in article_urls]

        welcome_text = "Good morning Mister Murphy, here are today's headlines"
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
            text_to_speech(welcome_text, tmp_file.name)
            play_audio(tmp_file.name)

        for headline in headlines:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
                text_to_speech(headline, tmp_file.name)
                play_audio(tmp_file.name)

    except Exception as e:
        print(f"Error reading headline and converting to speech: {e}")
