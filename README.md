# Document Extractor Service

A powerful document extraction service that uses OCR (Tesseract) and LLMs (Groq) to intelligently extract structured data from PDF documents and images.

## Features

- **Multi-Format Support**: Handles both PDF files and standard image formats (JPG, PNG).
- **Intelligent Extraction**: Uses Llama 3 via Groq for high-accuracy data extraction based on custom schemas.
- **Robust OCR**: Integrates Tesseract OCR for reliable text detection.
- **FastAPI Powered**: built on a modern, fast, and high-performance web framework.

## Prerequisites

Before running the application, ensure you have the following installed:

1.  **Python 3.8+**
2.  **Tesseract OCR**
    *   **Windows**: [Download Installer](https://github.com/UB-Mannheim/tesseract/wiki) (Add to PATH)
    *   **Linux**: `sudo apt install tesseract-ocr`
    *   **Mac**: `brew install tesseract`
3.  **Poppler** (Required for PDF processing)
    *   **Windows**: [Download Binary](https://github.com/oschwartz10612/poppler-windows/releases/), extract, and add `bin` folder to your PATH.
    *   **Linux**: `sudo apt install poppler-utils`
    *   **Mac**: `brew install poppler`
4.  **Ollama** (Required for local LLM inference)
    *   **All Platforms**: Download from [ollama.com](https://ollama.com)
    *   **Pull Model**: Run `ollama pull phi3` to download the default model.


## Installation

1.  **Clone the repository** (if you haven't already):
    ```bash
    git clone <your-repo-url>
    cd Document_Extracter
    ```


2.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## Configuration

1.  Create a `.env` file in the root directory.
2.  Add your Groq API Key:
    ```env
    GROQ_API_KEY=gsk_your_actual_api_key_here
    # Optional: Enable debug mode to save artifacts to /debug_output
    GROQ_API_KEY=gsk_your_actual_api_key_here
    # Optional: Enable debug mode to save artifacts to /debug_output
    DEBUG=True
    # Optional: Ollama URL (Defaults to http://localhost:11434/api/generate)
    OLLAMA_URL=http://localhost:11434/api/generate
    ```


## Running the Server

You can run the server using `uvicorn` or python module:

**Option 1: Python Module (Recommended)**
```bash
python -m app.main
```

**Option 2: Direct Uvicorn**
```bash
uvicorn app.main:app --host 0.0.0.0 --port 3000 --reload
```

The server will start at `http://localhost:3000`.

## JSON Schema Format

The extraction engine expects a valid JSON schema to define the fields you want to extract.

**Example Schema:**
```json
{
  "carrier_name": null,
  "shipper_name": null,
  "shipper_address": null,
  "consignee_name": null,
  "consignee_address": null,
  "notify_party_address":null,
  "vessel_name": null,
  "voyage_number": null,
  "port_of_loading": null,
  "port_of_discharge": null,
  "container_number": null,
  "goods_details":null,
  "seal_number": null,
  "gross_weight_kgs": null,
  "net_weight_kgs": null,
  "hs_code": null,
  "freight_terms": null,
  "issue_date": null,
  "issue_place":null
}
```

## Usage Example

You can test the API using `curl` or Postman.

**Endpoint:** `POST /extract`

**Curl Command:**
```bash
curl -X POST "http://localhost:3000/extract" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@/path/to/your/document.pdf" \
  -F "schema={\"invoice_number\": \"string\", \"total_amount\": \"number\"}" \
  -F "debug=true"
```

**Parameters:**
*   `file`: The PDF or image file you want to process.
*   `schema`: A JSON string defining the structure of data you want to extract.
*   `debug` (Optional): Set to `true` to save intermediate images and OCR text to the `debug_output` folder.

## Project Structure

```
Document_Extracter/
├── app/
│   ├── api/            # API Routes
│   ├── core/           # Core config and debug logic
│   ├── extractor_engine/ # LLM Integration (Groq)
│   ├── ocr/            # Tesseract OCR wrapper
│   ├── preprocess/     # Image/PDF preprocessing
│   └── main.py         # App entry point
├── debug_output/       # Generated artifacts (if debug=True)
├── .env                # Environment variables
├── .gitignore          # Git ignore rules
└── requirements.txt    # Python dependencies
```
