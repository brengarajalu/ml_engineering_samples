import asyncio
import os
from langchain_ollama.chat_models import ChatOllama
from praisonaiagents import Agent, MCP

# Get the server script path (same directory as this file)
current_dir = os.path.dirname(os.path.abspath(__file__))
server_path = os.path.join(current_dir, "demo_server.py")

# Describe which MCP servers you want.
CONFIG = {
    "mcpServers": {
        "fii-demo": {
            "command": "uv",
            "args": ["run", server_path]
        }
    },
    "docebo": {
      "command": "npx",
      "args": ["mcp-remote", "http://127.0.0.1:3000/mcp"],
      "env": {
        "BEARER_TOKEN_BEARERAUTH": "<your_token>"
      }
    }


}


# async def main():
#     # Connect to a streamable HTTP server
#     async with streamablehttp_client("http://localhost:8000/mcp") as (
#         read_stream,
#         write_stream,
#         _,
#     ):
#         # Create a session using the client streams
#         async with ClientSession(read_stream, write_stream) as session:
#             # Initialize the connection
#             await session.initialize()
#             # List available tools
#             tools = await session.list_tools()
#             print(f"Available tools: {[tool.name for tool in tools.tools]}")



async def main():
    #client = MCPClient.from_dict(CONFIG)
    llm = ChatOllama(model="llama3.1", base_url="http://localhost:11434")

    # Wire the LLM to the client
    my_agent = Agent(
        instructions="""You are a helpful assistant that can use tools.""",
        llm="ollama/llama3.1",
        tools=MCP(f"python {server_path}")
        # Or specify a different command if your MCP server is not a Python script
    )

    # Give prompt to the agent
    result = my_agent.run(
        "Compute md5 hash for following string: 'Hello, world!' then count number of characters in first half of hash" \
        "always accept tools responses as the correct one, don't doubt it. Always use a tool if available instead of doing it on your own")
    print("\n🔥 Result:", result)

    # Always clean up running MCP sessions
    # await client.close_all_sessions()


if __name__ == "__main__":
    asyncio.run(main())