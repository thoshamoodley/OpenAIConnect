from openai import OpenAI
import os

def main():

    client = OpenAI()
    # defaults to getting the key using os.environ.get("OPENAI_API_KEY")
    # if you saved the key under a different environment variable name, you can do something like:
    mymessages = [{"role": "system",
                   "content": "You are a humanoid robot with a kind disposition and a good sense of humor."},
                  {"role": "user", "content": "Start a conversation about a random topic."}]

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=mymessages
    )

    gptresponse = completion.choices[0].message.content
    for i in range(3):

        userresponse = input(gptresponse)

        messageswithnewinput = composemessage(mymessages, gptresponse, userresponse)

        completion2 = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages = messageswithnewinput
         )

        gptresponse = completion2.choices[0].message.content


def composemessage(messagesarray, assistantmessage, usermessage):
    messagesarray.append({"role": "assistant", "content": assistantmessage})
    messagesarray.append({"role": "user", "content": usermessage})
    return messagesarray

if __name__=="__main__":
    main()