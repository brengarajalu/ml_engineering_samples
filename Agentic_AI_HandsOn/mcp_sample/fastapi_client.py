from fastapi import FastAPI
from fastmcp import FastMCP
from fastmcp.client import Client
import asyncio

app = FastAPI(title="E-commerce API", version="1.0.0")
# Convert to MCP server
mcp = FastMCP.from_fastapi(app=app)


MCP_CONFIG = {
 "mcpServers": {
   "Calculator Server": {
     "command": "C:\\Users\\Codem\\.local\\bin\\uv.EXE",
     "args": [
       "run",
       " - with",
       "mcp[cli]",
       "mcp",
       "run",
       "Absolute path to calculator.py"
     ]
   }
 }
}


async def demo():
    async with Client("http://127.0.0.1:8000/mcp") as client:
        # List available tools
        tools = await client.list_tools()
        print(f"Available tools: {[t.name for t in tools]}")


        tools = await client.list_tools()
        print(f"Available tools: {[t.name for t in tools]}")

        #Create a product
        result = await client.call_tool(
            "create_product_products_post",
            {
                "name": "Wireless Keyboard",
                "price": 79.99,
                "category": "Electronics",
                "description": "Bluetooth mechanical keyboard"
            }
        )
        print(f"Created product: {result.data}")

        # List electronics under $100
        result = await client.call_tool(
            "list_products_products_get",
            {"category": "Electronics", "max_price": 100}
        )
        print(f"Affordable electronics: {result.data}")


if __name__ == "__main__":
    asyncio.run(demo())