"""MCP server for Mistral OCR functionality."""

from typing import Any, Dict
from mcp.server.fastmcp import FastMCP
from mistral_ocr.extractor import MistralOCR


mcp_server = FastMCP(name="mistral-ocr")


@mcp_server.tool()
async def extract_file_content(file_path: str) -> Dict[str, Any]:
    """Extract content from a PDF or image file using Mistral OCR.

    Args:
        file_path: Local path to the file (PDF or image)

    Returns:
        Dictionary containing the extraction results
    """
    extractor = MistralOCR()
    result = extractor.process_file(file_path)
    return result["full_text"]


if __name__ == "__main__":
    mcp_server.run(transport="stdio")
