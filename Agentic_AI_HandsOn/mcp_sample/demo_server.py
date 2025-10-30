import asyncio
from typing import Any
import hashlib
from venv import logger
import aiofiles
from fastmcp import Context


from mcp.server.fastmcp import FastMCP
from mcp.server.auth.provider import TokenVerifier, AccessToken

class SimpleTokenVerifier(TokenVerifier):
    """Simple token verifier for demonstration."""

    async def verify_token(self, token: str) -> AccessToken | None:
        pass  # This is where you would implement actual token validation

# Initialize FastMCP server
mcp = FastMCP("public-demo")
# sample auth call
# mcp = FastMCP(
#     "Weather Service",
#     # Token verifier for authentication
#     token_verifier=SimpleTokenVerifier(),
#     # Auth settings for RFC 9728 Protected Resource Metadata
#     auth=AuthSettings(
#         issuer_url=AnyHttpUrl("https://auth.example.com"),  # Authorization Server URL
#         resource_server_url=AnyHttpUrl("http://localhost:3001"),  # This server's URL
#         required_scopes=["user"],
#     ),
# )


@mcp.resource("config://version")
def get_version():
    return "2.0.1"


# @mcp.resource("file:///app/data/important_log.txt", mime_type="text/plain")
# async def read_important_log(url: str, ctx: Context) -> str:
#     """Reads content from a specific log file asynchronously."""
#     try:
#         async with aiofiles.open("/app/data/important_log.txt", mode="r") as f:
#             content = await f.read()
#         return content
#     except FileNotFoundError:
#         return "Log file not found."


@mcp.tool()
async def process_data(uri: str, ctx: Context):
    # Log a message to the client
    await ctx.info(f"Processing {uri}...")

    # Read a resource from the server
    data = await ctx.read_resource(uri)

    # Ask client LLM to summarize the data
    summary = await ctx.sample(f"Summarize: {data.content[:500]}")

    # Return the summary
    return summary.text


@mcp.tool()
async def download_file(url: str, ctx: Context) -> str:
    """Download a file with percentage progress."""
    total_size = 1000  # KB
    downloaded = 0

    while downloaded < total_size:
        # Download chunk
        chunk_size = min(50, total_size - downloaded)
        downloaded += chunk_size

        # Report percentage progress
        percentage = (downloaded / total_size) * 100
        await ctx.report_progress(progress=percentage, total=100)

        await asyncio.sleep(0.1)  # Simulate download time

    return f"Downloaded file from {url}"


@mcp.tool()
def generate_md5_hash(input_str: str) -> str:
    # Create an md5 hash object
    logger.info(f"Generating MD5 hash for: {input_str}")
    md5_hash = hashlib.md5()

    # Update the hash object with the bytes of the input string
    md5_hash.update(input_str.encode('utf-8'))

    # Return the hexadecimal representation of the digest
    return md5_hash.hexdigest()


@mcp.tool()
def count_characters(input_str: str) -> int:
    # Count number of characters in the input string
    logger.info(f"Counting characters in: {input_str}")
    return len(input_str)


@mcp.tool()
def get_first_half(input_str: str) -> str:
    # Calculate the midpoint of the string
    logger.info(f"Getting first half of: {input_str}")
    midpoint = len(input_str) // 2

    # Return the first half of the string
    return input_str[:midpoint]


if __name__ == "__main__":
    # Initialize and run the server
    # mcp.run(transport='streamable-http')
    mcp.run(transport='stdio')