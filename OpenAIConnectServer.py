"""
Thosha Moodley
    This code provides an http server which connects to OpenAI GPT
    It also converts wav files to text using OpenAI
    The purpose is to provide OpenAI GPT conversational functionality
    to a Java program which initiates a conversation via the Aldebaran
    Nao robot. The wav files are user speech responses recorded by Nao.
"""

import urllib.parse
from http.server import BaseHTTPRequestHandler, HTTPServer
from openai import OpenAI
import os
import glob
import base64
import requests

#create an OpenAI client
OpenAIclient = OpenAI()

# create the initial prompt for GPT


#HTTP server which runs waiting for java code to contact it
#connects to GPT for responses to user conversation input
class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    #the standard Python HTTP handler

    mymessages = [{"role": "system",
                   "content": "You are a humanoid robot with a kind disposition and a good sense of humor who always replies in 20 words or less. Start your conversation with 'I would like to talk about'"},
                  {"role": "user", "content": "Start a conversation about a random topic."}]

    #handle GET request
    def do_GET(self):
        # respond to GET request from Java client

        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        #get an array of url parameters passed by Java code
        params = urllib.parse.parse_qs(self.path.lstrip("/?"))

        #if there are parameters, handle them
        if len(params.values())>0:
            #if this is the first call from Java code, initialse the conversation
            if params['action'][0] == 'init':
                #setup the conversation parameters using the messages array
                #get GPT invitation to converse

                completion = OpenAIclient.chat.completions.create(
                    model="gpt-4-turbo",
                    messages=self.mymessages
                )

                gptresponse = completion.choices[0].message.content
                #send GPT response to HTTP response
                self.wfile.write(bytes(gptresponse,"utf-8"))

            #if this is not the first call, "convo" will be used in the action parameter
            elif params['action'][0] == 'convo':
                # use OpenAI library to convert user speech wav file to text to be used in prompt
                userresponse = speechtotext()

                # create a cumulative prompt with user response from the robot
                self.mymessages.append({"role": "user", "content": userresponse})
                print(self.mymessages)
                # contact GPT to get a new context related response to the user input
                completion = OpenAIclient.chat.completions.create(
                    model="gpt-4o",
                    messages=self.mymessages
                )
                gptresponsetext = completion.choices[0].message.content

                self.mymessages = self.mymessages.append({"role": "assistant", "content": gptresponsetext})
                self.wfile.write(bytes(gptresponsetext, "utf-8"))

            # use image input and have a conversation about it, separate from the chatbot functionality
            elif params['action'][0] == 'vision':
                # get file location from environmental variables
                filelocation = os.environ['FILEDIR']
                print(filelocation)

                list_of_files = glob.glob(filelocation + '/*.jpg')
                latest_file = max(list_of_files, key=os.path.getctime)
                print(latest_file)
                # Path to your image
                image_path = latest_file

                # Getting the base64 string
                base64_image = encode_image(image_path)
                vision_prompt_text = "the image is from the camera of a humanoid robot. what would the robot say about the image to start a conversation? you don't have to identify or make assumptions about people in images."

                response = OpenAIclient.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {"type": "text", "text": vision_prompt_text},
                                {
                                    "type": "image_url",
                                    "image_url": {
                                        "url": f"data:image/jpeg;base64,{base64_image}"
                                    },
                                },
                            ],
                        }
                    ],
                    max_tokens=300,
                )

                print(response.choices[0])
                gptresponsetext = response.choices[0].message.content

                self.mymessages = self.mymessages.append({"role": "assistant", "content": gptresponsetext})
                self.wfile.write(bytes(gptresponsetext, "utf-8"))
        else:
            self.wfile.write(b'no data')
# Function to encode the image
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

def run(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler, port=8001):
    # starts the HTTP server
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Server listening on port {port}")
    httpd.serve_forever()

def speechtotext():
    # retrieves the audiofile written by Java client and sends to OpenAI to convert to text. Returns the text

    # get file location from environmental variables
    filelocation = os.environ['FILEDIR']
    print(filelocation)

    list_of_files = glob.glob(filelocation + '/*.wav')
    latest_file = max(list_of_files, key=os.path.getctime)
    print(latest_file)

    # open the wav file from file location on disk
    audio_file = open(latest_file, "rb")

    # send the file to OpenAI for transcription
    transcription = OpenAIclient.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file
    )

    print(transcription.text)

    return transcription.text

if __name__ == '__main__':
    run()
