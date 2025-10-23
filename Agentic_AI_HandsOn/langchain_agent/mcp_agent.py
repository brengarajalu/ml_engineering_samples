import asyncio

import langchain_mcp_adapters

from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_react_agent
from langchain_ollama import ChatOllama
from mcp import stdio_client, ClientSession, StdioServerParameters
from langchain_mcp_adapters.tools import load_mcp_tools

client = MultiServerMCPClient(
    {
        "math": {
            "transport": "stdio",  # Local subprocess communication
            "command": "python",
            # Absolute path to your math_server.py file
            "args": ["/path/to/math_server.py"],
        },
        "weather": {
            "transport": "streamable_http",  # HTTP-based remote server
            # Ensure you start your weather server on port 8000
            "url": "http://localhost:6274/mcp",
        }
    }
)
model = ChatOllama(model="llama3.1", base_url="http://localhost:11434")

async def run_agent():
    async with client.session("weather") as session:
        # Initialize the connection
        await session.initialize()

        # Get tools
        tools = await load_mcp_tools(session)

        # Create and run the agent
        agent = create_react_agent(model, tools)
        agent_response = await agent.ainvoke({"messages": "what's (3 + 5) x 12?"})
        return agent_response


# Run the async function
if __name__ == "__main__":
    result = asyncio.run(run_agent())
    print(result)