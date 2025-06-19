For initialize system we use these command

1- uv init .

2- uv venv

3-.venv\scripts\activate

4- Make a seperate file which name is .env

5- put secret key in .env file

6- add 3 dependencies like   

a) uv add openai-agents

b) uv add dotenv

c)  uv add chainlit

7- make a file which name is agent.py

8- run command in final for output

  uv run chainlit run main.py




          Build a Multi-Agent AI System using Handoffs  
�
�
 What is Handoff in AI Agents? 
Simple alfaaz mein: 
Handoff ka matlab hai ek agent doosre expert agent ko kaam assign karna. 
Jaise: 
● Agar user bole: "Mujhe mobile app chahiye" 
Toh Manager Agent yeh kaam Mobile App Developer Agent ko dega, Q ke yeh 
uska expert agent hai. 
Yeh bilkul waise hi hai jaise real life mein ek project manager team members ko kaam 
assign karta hai. 
�
�
 Aapka Task Kya Hai? 
Aap ne ek Multi-Agent AI System banana hai Python mein — jisme: 
● Ek Manager Agent hoga 
● Aur 3 expert agents: 
○ Web Developer 
○ Mobile Developer 
○ Marketing Agent 
Manager agent user se baat karega aur jo kaam hoga, usko relevant expert agent ko handoff 
karega. 
1 Project Setup 
● uv project initialize karo 
● Virtual env (venv) activate karo 
● Dependencies install karo: 
uv add  openai-agents dotenv 
2 .env file banao 
Isme apna GEMINI_API_KEY rakho 
3 Code Likho 
Import aur Setup 
(same) 
Expert Agents Banao 
Web Developer 
web_dev = Agent( 
name="Web Developer Expert", 
instructions="Build responsive and performant websites using modern frameworks.", 
model=model, 
development." 
) 
handoff_description="handoff to web developer if the task is related to web 
Mobile App Developer 
mobile_dev = Agent( 
    name="Mobile App Developer Expert", 
    instructions="Develop cross-platform mobile apps for iOS and Android.", 
    model=model, 
    handoff_description="handoff to mobile app developer if the task is related to 
mobile apps." 
) 
 
Marketing Agent 
marketing = Agent( 
    name="Marketing Expert Agent", 
    instructions="Create and execute marketing strategies for product launches.", 
    model=model, 
    handoff_description="handoff to marketing agent if the task is related to 
marketing." 
) 
 
 
Manager Agent aur Run Function 
(same) 
 
Chainlit Integration (Chat Interface) 
(same) 
 
�
�
 Expert Agents Pehle Kyun? 
Isliye ke Manager ko pehle se pata hona chahiye ke kisko kaam dena hai. 
Agar pehle Manager banaoge, aur uske handoffs mein agents undefined honge — to error aa 
jayega. 
Jaise ek project manager ko apni team ka pata hona chahiye pehle. 
 
�
�
 Aapka Kaam 
✅
 Yeh sara code apne IDE ya Google Colab mein likho 
✅
 Agents ke naam aur instructions apne interest ke hisaab se badlo (jaise Designer Expert, Writer
 Expert etc.) 
✅
 Test karo ke handoff sahi kaam kar raha hai 
✅
 Output ka screenshot leke submit karo 
�
�
 Summary 
Ek multi-agent system banaya jata hai jisme: 
● Manager agent user se baat karta hai 
● Task ko relevant expert agent ko handoff karta hai 
● Expert agent us task ka jawab deta hai 
Manager ko pehle hi apne team members ka pata hona chahiye. 
�
�
 Prompts for Testing  
�
�
 For Mobile App Developer Expert Agent: 
Prompt: 
I want a mobile app that works on both iOS and Android. 
�
�
 For Web Developer Expert Agent: 
Prompt: 
Build me a website that is responsive and fast. 
�
�
 For Marketing Expert Agent: 
Prompt: 
I need a marketing plan for my product. 
😈
 Extra test (which should not match any agent) 
Prompt: 
 Write me a poetry. 
Bas ab is final version se system run kar lo — aur dekh lo expert agents kis tarah kaam karte hain. 
Final code 
main.py 
from chatbot import myAgent 
import chainlit as cl 
import asyncio 
 
@cl.on_chat_start 
async def on_chat_start(): 
    await cl.Message( 
        content="Welcome to the Multi-Agent System! How can I assist you 
today?" 
    ).send() 
 
@cl.on_message 
async def main(message: cl.Message): 
    user_input = message.content 
    response = asyncio.run(myAgent(user_input)) 
    await cl.Message( 
        content=f"{response}" 
    ).send() 
 
 
chatbot.py 
from dotenv import load_dotenv 
from openai import AsyncOpenAI 
from agents import Agent, Runner, OpenAIChatCompletionsModel, 
set_tracing_disabled 
import os 
 
load_dotenv() 
set_tracing_disabled(True) 
 
provider = AsyncOpenAI( 
    api_key=os.getenv("GEMINI_API_KEY"), 
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/" 
) 
 
model = OpenAIChatCompletionsModel( 
    model="gemini-2.0-flash-exp", 
    openai_client=provider, 
) 
 
web_dev = Agent( 
    name="Web Developer", 
    instructions="Build responsive and performant websites using modern 
frameworks.", 
    model=model, 
    handoff_description="handoff to web developer if the task is related to 
web development." 
) 
mobile_dev = Agent( 
    name="Mobile App Developer", 
    instructions="Develop cross-platform mobile apps for iOS and Android.", 
    model=model, 
    handoff_description="handoff to mobile app developer if the task is 
related to mobile apps." 
) 
 
marketing = Agent( 
    name="Marketing Agent", 
    instructions="Create and execute marketing strategies for product 
launches.", 
    model=model, 
    handoff_description="handoff to marketing agent if the task is related to 
marketing." 
) 
async def myAgent(user_input): 
    manager = Agent( 
        name="Manager", 
        instructions="You will chat with the user and delegate tasks to
        specialized agents based on their requests.", 
        model=model, 
        handoffs=[web_dev, mobile_dev, marketing] 
    ) 
 
    response = await Runner.run( 
        manager, 
        input=user_input, 
    ) 
 
    return response.final_output 