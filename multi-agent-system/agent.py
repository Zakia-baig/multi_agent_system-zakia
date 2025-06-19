from dotenv import load_dotenv
from openai import AsyncOpenAI
from agents import Agent, Runner, OpenAIChatCompletionsModel,set_tracing_disabled
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
    name= "Web developer",
    instructions= "Build responsive and performant website s using modern frameworks.",
    model=model,
    handoff_description="handoff to web developer if the task isrelated to web development."
)
mobile_dev = Agent(
    name="Mobile App Developer Expert",
    instructions="Develop cross-platform mobile apps for iOS and Android.",
    model=model,
    handoff_description="handoff to mobile app developer if the task is related to mobile apps."
)
marketing = Agent(
    name="Marketing Expert Agent",
    instructions="Create and execute marketing strategies for product launches.",
    model=model,
    handoff_description="handoff to marketing agent if the task is related to marketing."
)
async def myAgent(user_input):
    manager = Agent(
        name="Manager",
        instructions="You will chat with the user and delegate tasks to specialized agents based on their requests.",
        model=model,
        handoffs=[web_dev, mobile_dev, marketing]
)
    response = await Runner.run(
        manager,
        input = user_input,
)
    return response.final_output