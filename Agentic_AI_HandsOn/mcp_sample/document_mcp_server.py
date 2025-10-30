from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.prompts import base
from markitdown import MarkItDown
import os
import logging

# Configure logging for production monitoring
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

mcp = FastMCP("DocumentReader", dependencies=["markitdown[all]"])
md = MarkItDown()

# File size limit (10MB) for production safety
MAX_FILE_SIZE = 10 * 1024 * 1024


def validate_file(file_path: str, allowed_extensions: list) -> tuple[bool, str]:
    """Validate file existence, size, and type."""
    try:
        expanded_path = os.path.expanduser(file_path)

        # Check if file exists
        if not os.path.exists(expanded_path):
            return False, f"File not found: {file_path}"

        # Check file size
        file_size = os.path.getsize(expanded_path)
        if file_size > MAX_FILE_SIZE:
            return False, f"File too large: {file_size / 1024 / 1024:.1f}MB (max 10MB)"

        # Check file extension
        file_ext = os.path.splitext(expanded_path)[1].lower()
        if file_ext not in allowed_extensions:
            return False, f"Unsupported file type: {file_ext}"

        return True, expanded_path

    except Exception as e:
        return False, f"File validation error: {str(e)}"


@mcp.tool(
    annotations={
        "title": "Read PDF Document",
        "readOnlyHint": True,
        "openWorldHint": False
    }
)
def read_pdf(file_path: str) -> str:
    """Extract text content from PDF files for AI analysis.

    Processes PDF documents and returns clean text content suitable for
    language model analysis. Handles both text-based and scanned PDFs.

    Args:
        file_path: Path to the PDF file (supports ~ for home directory)

    Returns:
        Extracted text content or error message
    """
    try:
        # Validate file before processing
        is_valid, result = validate_file(file_path, ['.pdf'])
        if not is_valid:
            return f"Error: {result}"

        logger.info(f"Processing PDF: {file_path}")

        # Extract text using markitdown
        content = md.convert(result).text_content

        # Basic content validation
        if not content.strip():
            return "Warning: PDF appears to be empty or contains only images"

        logger.info(f"Successfully processed PDF: {len(content)} characters extracted")
        return content

    except Exception as e:
        error_msg = f"Error reading PDF: {str(e)}"
        logger.error(error_msg)
        return error_msg


@mcp.tool(
    annotations={
        "title": "Read Word Document",
        "readOnlyHint": True,
        "openWorldHint": False
    }
)
def read_docx(file_path: str) -> str:
    """Extract text content from Word documents for AI analysis.

    Processes DOCX files and returns formatted text content while preserving
    document structure for better language model understanding.

    Args:
        file_path: Path to the Word document (supports ~ for home directory)

    Returns:
        Extracted text content or error message
    """
    try:
        # Validate file before processing
        is_valid, result = validate_file(file_path, ['.docx', '.doc'])
        if not is_valid:
            return f"Error: {result}"

        logger.info(f"Processing DOCX: {file_path}")

        # Extract text using markitdown
        content = md.convert(result).text_content

        if not content.strip():
            return "Warning: Document appears to be empty"

        logger.info(f"Successfully processed DOCX: {len(content)} characters extracted")
        return content

    except Exception as e:
        error_msg = f"Error reading DOCX: {str(e)}"
        logger.error(error_msg)
        return error_msg


@mcp.resource("file://document/pdf-example")
def provide_example_pdf():
    """Provide sample PDF content for demonstration and testing.

    This resource makes example document content available to help users
    understand the server's capabilities and expected output format.
    """
    try:
        # Use absolute path for reliability
        pdf_path = os.path.expanduser("~/Documents/example.pdf")

        if not os.path.exists(pdf_path):
            return "Example PDF not available. Please add ~/Documents/example.pdf"

        return md.convert(pdf_path).text_content

    except Exception as e:
        return f"Error providing example PDF: {str(e)}"


@mcp.resource("file://document/recent/{filename}")
def provide_recent_document(filename: str):
    """Access recently used documents dynamically.

    Provides quick access to documents in a designated recent files folder,
    enabling efficient workflows for frequently referenced materials.

    Args:
        filename: Name of the file in the recent documents folder
    """
    try:
        # Construct safe path
        recent_docs_folder = os.path.expanduser("~/Documents/Recent")
        file_path = os.path.join(recent_docs_folder, filename)

        # Security check - ensure path is within allowed directory
        if not os.path.commonpath([recent_docs_folder, file_path]) == recent_docs_folder:
            return "Error: Invalid file path"

        is_valid, result = validate_file(file_path, ['.pdf', '.docx', '.doc', '.txt'])
        if not is_valid:
            return f"Error: {result}"

        return md.convert(result).text_content

    except Exception as e:
        return f"Error accessing document: {str(e)}"