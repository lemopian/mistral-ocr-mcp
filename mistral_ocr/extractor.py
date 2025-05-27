"""Document extraction functionality using Mistral OCR."""

import base64
from typing import Dict, Any, Optional
import os
from pathlib import Path
from dotenv import load_dotenv
from mistralai import Mistral


class MistralOCR:
    """Extract content from documents using Mistral OCR."""

    def __init__(
        self, api_key: Optional[str] = None, model_name: str = "mistral-ocr-latest"
    ):
        """Initialize the extractor.

        Args:
            api_key: Mistral API key. If not provided, reads from MISTRAL_API_KEY env var.
            model_name: OCR model to use.
        """
        load_dotenv()
        self.api_key = api_key or os.environ.get("MISTRAL_API_KEY")
        if not self.api_key:
            raise ValueError("MISTRAL_API_KEY must be set in environment or provided")

        self.client = Mistral(api_key=self.api_key)
        self.model_name = model_name

    def _encode_file_to_base64(self, file_path: str) -> str:
        """Encode file to base64 string."""
        try:
            with open(file_path, "rb") as file:
                return base64.b64encode(file.read()).decode("utf-8")
        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {file_path}")
        except Exception as e:
            raise Exception(f"Error encoding file: {e}")

    def _get_mime_type(self, file_path: str) -> str:
        """Get MIME type based on file extension."""
        extension = Path(file_path).suffix.lower()
        mime_types = {
            ".pdf": "application/pdf",
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".png": "image/png",
            ".tiff": "image/tiff",
            ".bmp": "image/bmp",
        }
        return mime_types.get(extension, "image/jpeg")

    def _process_ocr_response(self, ocr_response, file_path: str) -> Dict[str, Any]:
        """Process OCR response into standardized format."""
        pages_content = []
        full_text = ""

        for page in ocr_response.pages:
            page_text = page.markdown
            pages_content.append(page_text)
            full_text += page_text + "\n\n"

        return {
            "source": file_path,
            "pages": pages_content,
            "total_pages": len(pages_content),
            "full_text": full_text.strip(),
            "metadata": {
                "processed_at": os.path.getmtime(file_path),
                "file_size": os.path.getsize(file_path),
            },
        }

    def process_file(self, file_path: str) -> Dict[str, Any]:
        """Process a file and extract text content.

        Args:
            file_path: Path to PDF or image file

        Returns:
            Dictionary with extracted content and metadata
        """
        file_path = str(file_path)

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        extension = Path(file_path).suffix.lower()
        supported_formats = {".pdf", ".jpg", ".jpeg", ".png", ".tiff", ".bmp"}

        if extension not in supported_formats:
            raise ValueError(f"Unsupported format: {extension}")

        base64_content = self._encode_file_to_base64(file_path)
        mime_type = self._get_mime_type(file_path)

        if extension == ".pdf":
            document_config = {
                "type": "document_url",
                "document_url": f"data:{mime_type};base64,{base64_content}",
            }
        else:
            document_config = {
                "type": "image_url",
                "image_url": f"data:{mime_type};base64,{base64_content}",
            }

        ocr_response = self.client.ocr.process(
            model=self.model_name,
            document=document_config,
            include_image_base64=False,
        )

        return self._process_ocr_response(ocr_response, file_path)
