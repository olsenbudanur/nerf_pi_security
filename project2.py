from gpiozero import AngularServo
from time import sleep
from picamera2 import Picamera2, Preview
import time
from twilio.rest import Client
import requests
import base64
import json
import socket

picam2 = Picamera2()
camera_config = picam2.create_still_configuration(main={"size": (1920, 1080)}, lores={"size": (640, 480)}, display="lores")
picam2.configure(camera_config)
picam2.start()

twilioAuth = "secret"
twilioSid = "secret"

myPhone = "+secret"
twilioPhone = "+secret"

imgurID = "secret"
imgurSecret = "secret"


def imgurUpload():
    with open("test.jpg", "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())

        url = "https://api.imgur.com/3/image"

        payload={'image': encoded_string}
        files=[

        ]
        headers = {'Authorization': 'Client-ID ' + imgurID}

        response = requests.request("POST", url, headers=headers, data=payload, files=files)

        response_data = json.loads(response.text)
        image_link = response_data['data']['link']
        return image_link


def send_mms():
    imageLink = imgurUpload()

    account_sid = twilioSid
    auth_token = twilioAuth
    client = Client(account_sid, auth_token)

    message = client.messages \
        .create(
            body='Intruder alert, nerf shots has been fired!!!!!!',
            media_url=[imageLink],
            from_= twilioPhone,
            to=myPhone
        )

    print(message.sid)


def fire():
    servo = AngularServo(18, min_pulse_width=0.0006, max_pulse_width=0.0023)
    servo.angle = -90
    sleep(2)
    servo.angle = 90
    sleep(2)


#
# Trigger this once intruder is found!
def intruderDetected():
    try:
        fire()
    except: 
        pass
    time.sleep(1)
    picam2.capture_file("test.jpg")
    time.sleep(1)
    try:
        send_mms()
    except: 
        pass

# get the hostname
hostname = socket.gethostname()

# get the IP address associated with the hostname
ip_address = socket.gethostbyname(hostname)

print(f"IP address of the machine running the listening program is: {ip_address}")

HOST = ''  
PORT = 12345

# create a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# bind the socket to a public host and a port
s.bind((HOST, PORT))

# start listening for incoming connections
s.listen(1)

print(f"Listening on port {PORT}...")

while True:
    # wait for a connection
    conn, addr = s.accept()
    print("Connected")
    intruderDetected()
    conn.close()
