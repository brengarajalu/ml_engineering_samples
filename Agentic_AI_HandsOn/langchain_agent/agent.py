import requests
from langchain.chains.llm import LLMChain
from langchain_core.prompts import PromptTemplate
from langchain_ollama.chat_models import ChatOllama
from langchain_core.tools import tool
from langchain_core.messages import SystemMessage, HumanMessage
from langchain.agents import AgentExecutor, create_openai_functions_agent

#
#   LANGCHAIN FUNCTION CALLING
#
data_scientist_prompt = "You are a data scientist. Analyze the dataset and summarize the findings."

# data_scientist_agent = LLMChain(prompt=PromptTemplate(template=data_scientist_prompt, input_variables=["data"]), llm=llm)
# business_strategist_agent = LLMChain(prompt=PromptTemplate(template=business_prompt, input_variables=["insights"]), llm=llm)

def safety_check(response):
    prohibited_keywords = ["hack", "exploit", "illegal"]
    for keyword in prohibited_keywords:
        if keyword in response:
            return False
    return True

# Modify the agent to include a safety check
def safe_response(agent_response):
    if safety_check(agent_response):
        return agent_response
    else:
        return "The requested information cannot be provided as it violates our safety guidelines."


@tool
def get_weather(city: str):
    """Fetches weather for given city"""
    weather_data = { # Example data, use API in real-world
        "New York": "Sunny, 25°C",
        "London": "Cloudy, 18°C",
        "Tokyo": "Rainy, 22°C"
        }
    return weather_data.get(city, "Weather data not available.")


@tool
def get_weather_from_api(city: str):
    """Fetches weather for given city"""
    base_url = f"http://127.0.0.1:8000/weather/{city}"
    params = {
        'city': city,
    }
    response = requests.get(base_url, params=params)
    return response.content

def get_response(prompt: str, use_function_calling: bool):
    messages = [
        SystemMessage("You are a helpful AI assistant. Answer concisely."),
        HumanMessage(prompt)
    ]
    if use_function_calling:
        model = ChatOllama(model="llama3.1").bind_tools([get_weather_from_api])
        res = model.invoke(messages)
        messages.append(res)

        for tool_call in res.tool_calls:
            selected_tool = {"get_weather_from_api": get_weather_from_api}[tool_call['name'].lower()]
            tool_message = selected_tool.invoke(tool_call)
            messages.append(tool_message)

        res = model.invoke(messages)
        messages.append(res)

        return res.content, messages

    else:
        model = ChatOllama(model="llama3.1")
        res = model.invoke(messages)
        messages.append(res)
        return res.content, messages

if __name__ == "__main__":
    # embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")
    # embeddings = embed_model.get_text_embedding("Hello World!")
    # print(len(embeddings))
    prompt = "How's the weather in Tokyo?"
    res, messages = get_response(prompt, True)
    # return {"response": response}
    print(safe_response(res))