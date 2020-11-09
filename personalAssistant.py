import pyttsx3
import speech_recognition as sr  # Install brew -> install portaudio -> pip3 install PyAudio
import random
import time
import requests
import wikipedia
import smtplib
from Google import places_details, distance


name = "Karen" # Name it however you want!


def speak(data=f"Hey, I am {name}. How can I help you ?"):
    engine = pyttsx3.init()
    """VOICE"""
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[33].id)
    engine.say(data)
    engine.runAndWait()


def listen():
    # obtain audio from the microphone
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("I am listening...")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
        response = ""
        try:
            response = r.recognize_google(audio)
            print("You said: " + response)
        except sr.UnknownValueError:
            speak("Sorry I did not get it. Please try again")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service. Check for Internet connection."
                  " Error message: {0}".format(e))

        return response


def voice_assistant(response):
    if "how are you" in response:
        speak("I am fine, thank you")

    if "what is your name" == response:
        speak("My name is Galaxy, the one and only")

    if "what time is it" in response:
        t = time.localtime()
        current_time = time.strftime("%H:%M:%S", t)
        print(current_time)
        speak(current_time)

    if "how far is the Moon" == response:
        speak("the moon is 384,400 km away")

    if "how far is the Sun" == response:
        speak("the Sun is 150 million kilometers away")

    if "b****" in response:
        speak("Please speak nicely next time. Beach")

    if "f*****" in response:
        speak("Please speak nicely next time")

    if "stop the program" in response:
        speak("Ok,I hope to see you soon!")
        exit()

    if "close the program" in response:
        speak("Ok,I hope to see you soon!")
        exit()

    if "exit the program" in response:
        speak("Ok,I hope to see you soon!")
        exit()

    if "tell me a joke" == response:
        joke_list = [
            "Never criticize someone until you've walked a mile in their shoes. That way, when you criticize them, "
            "they won't be able to hear you from that far away. Plus, you'll have their shoes.",
            "Two fish are in a tank. One says to the other, Do you know how to drive this thing?",
            "Can a kangaroo jump higher than a house?. Of course, a house doesn't jump at all",
            "The doctor is saying. I'm sorry but you suffer from a terminal illness and have only 10 to live. "
            "The patient replies.What do you mean, 10?. 10 what?, 10 Months? 10 Weeks? 10 days? .Then the doctor is "
            "saying, Nine. Eight. Seven."]
        speak("Here is one")
        speak(random.choice(joke_list))
        speak("Funny, right? ha ha ha ha")

    if "what is the weather" in response:
        city = response.split("what is the weather in")
        city = " ".join(city)  # "Gets only the city name"
        city = city.strip()
        weather(city)
    
    if "is the weather" in response:
        city = response.split("is the weather in")
        city = " ".join(city)  # "Gets only the city name"
        city = city.strip()
        weather(city)

    if "who is" in response:
        search = response.split('is')
        search = search[1]
        search = search.strip()
        print(search + ":")
        wiki(search)

    if "who was" in response:
        search = response.split('was')
        search = search[1]
        search = search.strip()
        print(search + ":")
        wiki(search)
     
    if "what was" in response:
        search = response.split('was')
        search = search[1]
        search = search.strip()
        print(search + ":")
        wiki(search)

    if "what is" in response:
        search = response.split('is')
        search = search[1]
        search = search.strip()
        print(search + ":")
        wiki(search)


    if "send email" in response:
        speak("Please enter the receiver email address")
        receiver_mail_address = input("Receiver email address:")
        speak("Please record your message:")
        print("Wait...")
        message = listen()
        email(message, receiver_mail_address)

    if "show me places nearby" in response:
        place = response.split("show me places nearby")
        place = " ".join(place)  # "Gets only the city name"
        speak("sure. which kinds of places? Bars? , restaurants? , coffee?")
        answer = listen()
        speak(f"Here is a list of the best {answer}  in {place} their address and your estimated time to get there")
        places_details(place, answer)

    if "how long it will take me get to" in response:
        place = response.split("how long it will take me get to")
        place = " ".join(place)  # "Gets only the city name"
        speak(f"It will take you {distance('current', place)}")

    if "how long will it take me to get to" in response:
        place = response.split("how long will it take me to get to")
        place = " ".join(place)  # "Gets only the city name"
        speak(f"It will take you {distance('current', place)} to get to {place}")


def weather(city="Tel Aviv", unit="c"):
    api_key = keys.weather_api_key()
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={api_key}'
    # print(url)
    json_data = requests.get(url).json()
    # print(json_data)
    weather_state = (json_data['weather'][0]['main'])
    tempC = (json_data['main']['temp'])
    tempF = celsius_to_fahrenheit(json_data['main']['temp'])
    hum = (json_data['main']['humidity'])
    if unit == "c":
        speak(f"The weather in {city} is {weather_state}, the temperature is {tempC} celsius "
              f"and the humidity is {hum} percent")
    else:
        speak(f"The weather is {weather_state}, the temperature is {tempF} fahrenheit and the humidity is {hum}")


def wiki(search="Track and Field", sentences=2):
    try:
        search_result = wikipedia.summary(search, sentences=sentences)
    # If she can not find the wiki value
    except:
        speak(f"I am sorry, I don't now who is {search} but here is a link that might help:")
        print(google_search(search))
    else:
        url = wikipedia.page(search).url
        speak(f"{search_result}, for more, click the following link:")
        print(url)


def email(email_content="Hey!", receiver_email='Enters your email here for testing, otherwise leave as None'):
    """
    This is the simple email sending syntax for GMAIL USERS:
    """
    my_email = 'your_email'
    email_password = 'your_email password'
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()

        smtp.login(my_email, email_password)
        subject = "This email was sent through my personal assistant!"
        body = email_content

        msg = f'Subject: {subject}\n\n{body}'

        smtp.sendmail(my_email, receiver_email, msg)
        speak("Email was successfully sent")


def google_search(search):
    search = search.split(" ")
    search = '+'.join(search)
    return f'https://www.google.com/search?sxsrf=ALeKk03EEoudq6N9VEyh7yXFkzzQj4aMDQ%3A1604338782086&ei=XkSgX6LbBKGNlwS_' \
           f'2JNI&q={search}'


def celsius_to_fahrenheit(c):
    return round((c * 9 / 5) + 32)


if __name__ == "__main__":
    speak()
    while 1:
        response = listen()
        voice_assistant(response)
