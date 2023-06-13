import cv2
import pillow
import customtkinter
import mediapipe as mp
import numpy
import pyttsx3
import speech_recognition as sr
import threading
import spotipy as sp
from spotipy.oauth2 import SpotifyOAuth
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

import asyncio
from spHelper import *
from telegramHelper import *
from telethon import TelegramClient, events
from telethon.errors import SessionPasswordNeededError
from telethon.tl.functions.account import UpdateProfileRequest

# Volume Control

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)

volLevel = volume.GetMasterVolumeLevel()
volRange = volume.GetVolumeRange()
#

###### GUI #######

gui = customtkinter.CTk()
pillow.
##################

###### SPOTIFY #######
client_id = '6c4b59e22bfc46b58f157861dfd37001'
client_secret = '895ba7f8590747f08c45a5b3cc1a29c9'
redirect_uri = 'https://example.com/callback/'
scope = 'user-read-private user-read-playback-state user-modify-playback-state'
username = '31eu65rpsquz2q64ca5r43j3sczm'

auth_manager = SpotifyOAuth(
    client_id=client_id,
    client_secret=client_secret,
    redirect_uri=redirect_uri,
    scope=scope,
    username=username)

spotify = sp.Spotify(auth_manager=auth_manager)
##################

######## TELEGRAM #######
api_id = 20692913
api_hash = '678f824b2a57342c53810dcbba19dfcb'

client = TelegramClient('new', api_id, api_hash)
###########################


cap = cv2.VideoCapture(0)

mpHands = mp.solutions.hands
hands = mpHands.Hands(min_tracking_confidence=0.8)
mpDraw = mp.solutions.drawing_utils

cTime = 0
pTime = 0

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')

engine.setProperty('voice', voices[1].id)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def getCmd():
    r = sr.Recognizer()

    with sr.Microphone(0) as source:
        print('Listening...')
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source=source)
        audio = r.listen(source)

    try:
        print('Recognizing...')
        query = r.recognize_google(audio, language='en-in')
        print('User said ' + query)

    except Exception as e:
        # print(e)
        print("Say that again please...")
        return "None"
    return query

def setVolLevel(vol):
    volume.SetMasterVolumeLevel(vol, None)

def trackHand():
    while True:
        success, img = cap.read()
        img = cv2.flip(img, 1)
        results = hands.process(img)

        if results.multi_hand_landmarks:
            for handLms in results.multi_hand_landmarks:
                for id, lm in enumerate(handLms.landmark):

                    h, w, c = img.shape
                    # print(h, w, c)

                    cx, cy = int(lm.x * w), int(lm.y * h)

                    if id == 4:
                        cv2.circle(img, (cx, cy), 10, (255, 255, 255), cv2.FILLED)

                    if id == 8:
                        cv2.circle(img, (cx, cy), 10, (255, 255, 255), cv2.FILLED)

                x0, y0 = int(handLms.landmark[4].x * 640), int(handLms.landmark[4].y * 480)
                x1, y1 = int(handLms.landmark[8].x * 640), int(handLms.landmark[8].y * 480)

                cx, cy = (x0 + x1)//2, (y0 + y1)//2

                cv2.line(img, (x0, y0), (x1, y1), (0, 0, 100), 1)
                cv2.circle(img, (cx, cy), 5, (0, 10, 0), cv2.FILLED)

                length = int(numpy.hypot(x1-x0, y1-y0))

                #print(length)

                if length <= 50:
                    cv2.circle(img, (cx, cy), 5, (0, 255, 0), cv2.FILLED)
                    #os.open()

                vol = numpy.interp(length, [50, 200], [volRange[0], volRange[1]])
                #print(vol)
                setVolLevel(vol)

                #mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

        cv2.imshow("Image", img)
        cv2.waitKey(1)


def ondestroy():
    # TODO : All code that we want to destroy at end
    client.disconnect()

#if __name__ == "__main__":
def run_assistant():

    while True:
        query = getCmd().lower()

        if 'vini' in query:
            label.configure(text="Listening...", text_color="white")

            speak('hello sir! how can i help you today')
            query = getCmd().lower()

            if 'play song' in query:
                speak('Which song would you like me to play')
                song = getCmd().lower()
                trackUri = searchSongUri(spotify, song)
                if trackUri is not None:
                    #TODO : Label stays only for a sec then goes back to "Asleep"
                    label.configure(text=f"Playing Song {song}", text_color="white")
                    play_track(spotify, trackUri)

            if 'play artist' in query:
                speak('Which artist would you like me to play')
                artist = getCmd().lower()
                artistUri = searchArtist(spotify, artist)
                if artistUri is not None:
                    play_artist(spotify, artist)

            if 'play album' in query:
                speak('Which album would you like me to play')
                album = getCmd().lower()
                albumUri = searchArtist(spotify, album)
                if albumUri is not None:
                    play_album(spotify, albumUri)

            elif 'set volume' in query:
                speak('is it too much?')
                ans = getCmd().lower()

                # if 'lower volume' in query:
                #     volLevel -= 10
                #     volume.SetMasterVolumeLevel(volLevel, None)
                #
                # elif 'increase volume' in query:
                #     volLevel += 10
                #     volume.SetMasterVolumeLevel(volLevel, None)

            elif 'track my hand' in query:
                speak('tracking your hand')
                trackHand()

            if 'send message' in query:
                speak('what would you like me to send?')
                msg = getCmd().lower()

                label.configure(text=msg+'. would like me to send this msg?')

                ans = getCmd().lower()

                if 'yes' in ans:
                    await sendmsgto(ans)
                else:
                    break

        if 'close' in query:
            ondestroy()
            exit()

        label.configure(text="Asleep", text_color="gray")

async def main():

    # TODO : Convert this function to work with the rest of the speech recognition

    entity = await getinputentity()

    await sendmsgto(entity, 'hi')


# def drawGui():
if __name__ == "__main__":

    await connectToTelegram()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

    gui.geometry('300x100')
    gui.title('Vinnie')

    customtkinter.set_default_color_theme("dark-blue")
    customtkinter.set_appearance_mode("dark")

    img = customtkinter.CTkImage()
    label = customtkinter.CTkLabel(master=gui, text='Asleep', text_color='gray')
    label.pack(pady=10, padx=20)

    threading.Thread(target=run_assistant).start()

    gui.mainloop()