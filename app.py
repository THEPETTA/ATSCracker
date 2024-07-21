import json
from openai import OpenAI
from dotenv import load_dotenv
import os
import subprocess
from instructions import prompts



def readInput():
    try:
        with open('input.json', 'r') as file:
            data = json.load(file)
            return data
        
    except FileNotFoundError:
        print("Error: The file does not exist.")
        exit()

    except json.JSONDecodeError:
        print("Error: The file is not a valid JSON.")
        exit()


def openAISetup():
    load_dotenv()
    client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    )
    return client

def createFile(s):
    try:
        filename = "temp.py"
        with open(filename, 'w') as file:
            file.write(s)
        subprocess.run(['python', filename], check=True)
        os.remove(filename)
        return "Successful"
    except Exception as e:
        print(e)
        exit()


def getResponse(client, data):
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            prompts[0],
            {"role": "user", "content": str(data)},
            prompts[1]
        ],
        temperature = 0.8,
        n=1
        )
    s = completion.choices[0].message.content[10:len(completion.choices[0].message.content)-3]
    return createFile(s)

def main():
    data = readInput()
    client = openAISetup()
    return getResponse(client, data)

print(main())