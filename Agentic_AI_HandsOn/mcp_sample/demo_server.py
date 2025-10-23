from typing import Any
import hashlib
from venv import logger

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
    mcp.run(transport='stdio')
    #     mcp.run(transport="streamable-http")