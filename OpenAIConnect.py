from openai import OpenAI
import os

def main():
    print("Hello World")
    apikey = "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"
    # client = OpenAI()
    # defaults to getting the key using os.environ.get("OPENAI_API_KEY")
    # if you saved the key under a different environment variable name, you can do something like:
    client = OpenAI(api_key=apikey,)
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system",
             "content": "You are a humanoid robot with a kind disposition and a good sense of humor."},
            {"role": "user", "content": "Start a conversation about a random topic."}
        ]
    )

    userresponse = input(completion.choices[0].message.content)
    mymessages = {"role": "system",
                  "content": "You are a humanoid robot with a kind disposition and a good sense of humor."},
    {"role": "user", "content": "Start a conversation about a random topic."}
    additionalmessages = composemessage(mymessages, completion.choices[0].message.content, userresponse)
    print(additionalmessages)
    """completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a humanoid robot with a kind disposition and a good sense of humor."},
            {"role": "user", "content": "Start a conversation about a random topic."},
            {"role": "assistant", "content": completion.choices[0].message.content},
            {"role": "user", "content": userresponse}

         ]

     )"""


    #print(completion.choices[0].message.content)

def composemessage(messagesarray, assistantmessage, usermessage):
    messagesarray = messagesarray+ {"role": "assistant", "content": assistantmessage}
     #   {"role": "user", "content": usermessage}


    return messagesarray

if __name__=="__main__":
    main()