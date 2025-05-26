# Mistral OCR MCP Server

A Model Context Protocol (MCP) server that provides OCR (Optical Character Recognition) functionality using Mistral's OCR API. This server allows you to extract text content from PDF files and images through MCP-compatible clients like Cursor and Claude Desktop.

## Flowchart

```mermaid
---
config:
  theme: mc
  look: neo
id: ea72b068-989a-4066-9d14-cd30d6ccdb81
---
flowchart LR
    A["**Image** or **PDF** of handwritten notes"] --> B@{ label: "<img src=\"data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAQsAAAC9CAMAAACTb6i8AAAAsVBMVEX////hBQD/ggX/rwD6UA//2AD/jhb/sQj/qwDtgoH+fhj6RAD6ThL/fwD/rQD/1gD/4a7/nVTrQCr/yyD/ewD/++P/+dz/4mH/5Gr/9uP/89z/8eT/7Nz+7OX6SgD/0YT/mEb7hGX9uqj7jW79xbXvl5b/9vX/1pb/yQD/4KvrPCP/0Uz/7c7/1Ij/2Zr/iQD/kiz+hir/kUD6NgDte3fsUkPthoXzl471oZjrcW/ujo5VP/1mAAACWElEQVR4nO3aR1KCYRQFUcwBxYgZcwBzwLj/hTlsqxxwq3wFWnYv4N3vP0xpNJLaS1NBm9GtyraSZy1tlG5qQVqQFqQFaUFakBakBWlBWpAWpAVpQVqQFqQFaUFakBakBWlBWpAWpAVpQVqQFqQFaUFakBakBWlBWpAW1E42f6vFVK3Fdnct6Go5qHcdLV73kmNXybO67VqL2VbQbNRBtHiRHYuetVNsMVFVbFG3qAWLWrCoBYtasKgFi1qwqAWLWrCoBYtasKgFi1qwqAWLWrCoBYtasKgFi1qwqAWLWrCoBYtasKgFi1qwqAWLWrCoBYtasKgFi1qwqAWLWrCoBYtasFhs0ZqpauImWrytW2zVWuzeTZd1f5h0Xzd4t1drsT5e1mJW3eD677UYelqQFqQFaUFakBakBWlBWpAWpAVpQVqQFqQFaUFakBakBWlBWpAWpAVpQVqQFqQFaUFakBakBWlBWtBoLCr/fFR3q9xiPuhhJekxOTX/GN16SE4VW3SaC4PbP4punSa3msfRrZP95FbnJ5/+rU5zcnCxRXArtkhuaaGFFlpo8TUtSAvSgrQgLUgL0oK0IC1IC9KCtCAtSAvSgrQgLUgL0oK0IC1IC9KCtCAtSAvSgrQgLejPWzw1B/c0Eou5pP7latDzS3Lr9TTpLTn18pw867IffeJ5ozE27PrRT3Q29HdpQVqQFqQFaUFakBakBWlBWpAWpAVpQVqQFqQFaUFakBakBWlBWpAWpAVpQVqQFqQFaUFakBakBWlBWpAWNAqL98jiY+jvOo/e9V/6BKKquLLdyJ1kAAAAAElFTkSuQmCC\" width=\"1000\"> **OCR** Processing - Created MistralAI MCP server" }
    B --> C("Notion Page Creation - Official Notion MCP server")
    C --> D@{ label: "<img src=\"https://upload.wikimedia.org/wikipedia/commons/e/e9/Notion-logo.svg\" width=\"30\"> Notes saved in Notion page" }
    A@{ shape: doc}
    B@{ shape: rounded}
    D@{ shape: rect}
```

## Features

- Extract text from PDF files and images (JPG, JPEG, PNG, TIFF, BMP)
- Returns structured content with page-by-page breakdown
- Integrates seamlessly with MCP clients
- Built with FastMCP for optimal performance

## Prerequisites

- Python 3.10.1 or higher (but less than 3.13)
- [uv](https://docs.astral.sh/uv/) package manager
- Mistral API : [https://console.mistral.ai/api-keys](https://console.mistral.ai/api-keys)

## Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd mistral-ocr-mcp
   ```

2. **Install dependencies using uv:**
   ```bash
   uv sync
   ```

3. **Set up environment variables:**
   Create a `.env` file in the project root:
   ```bash
   echo "MISTRAL_API_KEY=your_mistral_api_key_here" > .env
   ```

## Configuration for MCP Clients

### Claude Desktop

Add the following configuration to your Claude Desktop config file:

**Location:** `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS)

```json
{
  "mcpServers": {
    "mistral-ocr": {
      "command": "/Users/yourusername/.local/bin/uv",
      "args": [
        "--directory",
        "/path/to/mistral-ocr-mcp",
        "run",
        "server.py"
      ]
    }
  }
}
```

**Important:** Replace `/path/to/mistral-ocr-mcp` with the actual path to your cloned repository.

### Cursor

For Cursor, add similar configuration to your MCP settings. The exact location may vary depending on your Cursor setup.

## Usage

Once configured, the server provides the following tool:

### `extract_file_content`

Extracts text content from PDF files and images.

**Parameters:**
- `file_path` (string): Local path to the PDF or image file

**Returns:**
- Extracted text content as a string

**Supported formats:**
- PDF files (`.pdf`)
- Image files (`.jpg`, `.jpeg`, `.png`, `.tiff`, `.bmp`)

**Example usage in Claude Desktop:**
```
Please extract the text from this document: /path/to/your/document.pdf
```

## Development

### Running the server directly

```bash
uv run server.py
```

### Project structure

```
mistral-ocr-mcp/
├── server.py          # MCP server implementation
├── extractor.py       # Mistral OCR functionality
├── pyproject.toml     # Project dependencies
├── .env              # Environment variables (create this)
└── README.md         # This file
```

## Environment Variables

- `MISTRAL_API_KEY`: Your Mistral API key (required)

## Troubleshooting

1. **"MISTRAL_API_KEY must be set" error:**
   - Ensure you've created a `.env` file with your Mistral API key
   - Verify the API key is valid

2. **"File not found" error:**
   - Check that the file path is correct and accessible
   - Ensure the file format is supported

3. **MCP connection issues:**
   - Verify the path to `uv` is correct in your MCP configuration
   - Ensure the repository path is absolute and correct
   - Check that all dependencies are installed with `uv sync`
