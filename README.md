# NRB Chatbot - Nepal Rastra Bank Information Retrieval System

A multilingual chatbot system for retrieving and answering questions about Nepal Rastra Bank (NRB) policies and information using Retrieval-Augmented Generation (RAG) with LangChain.

## Features

- **Multilingual Support**: Handles English, Nepali, and Romanized Nepali (Romanized Nepali script)
- **RAG Pipeline**: Uses FAISS vector store with HuggingFace embeddings for efficient document retrieval
- **Advanced LLM**: Powered by Groq's Llama 3.3 70B model for accurate responses
- **FastAPI Backend**: RESTful API with CORS support for easy integration
- **Smart Translation**: Automatic language detection and translation between English and Nepali
- **Rule-Based Assistant**: Strictly adheres to provided context with no hallucinations

## Architecture

### Core Components

1. **main.py** - Main RAG pipeline setup
   - Document loading and chunking
   - FAISS vector store initialization
   - LLM configuration with Groq
   - Query processing and response generation

2. **app.py** - FastAPI server
   - REST endpoint for chat queries
   - CORS middleware for cross-origin requests
   - Error handling

3. **translator.py** - Language processing
   - Query preprocessing (language detection)
   - Romanized Nepali to Devanagari conversion
   - Output translation based on input language

4. **roman.py** - Romanization mappings
   - Roman to Nepali script dictionary
   - Text conversion utilities

## Installation

### Prerequisites
- Python 3.8+
- Tesseract OCR (for document processing)

### Setup

1. Clone or download the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   ```bash
   cp .env.example .env
   ```
   Add your Groq API key:
   ```
   GROQ_API_KEY=your_api_key_here
   ```

4. Prepare the knowledge base:
   - Place NRB documents/information in `output.txt`

## Dependencies

- **LangChain**: RAG framework and orchestration
- **FAISS**: Vector database for similarity search
- **HuggingFace**: Multilingual embeddings (intfloat/multilingual-e5-base)
- **Groq**: LLM provider (Llama 3.3 70B)
- **FastAPI**: Web framework
- **GoogleTranslate**: Language translation
- **deep-translator**: Alternative translation support
- **langdetect**: Language detection
- **PyPDF**: PDF document processing
- **Tesseract-OCR**: Optical character recognition

## Usage

### Run the API Server

```bash
uvicorn app:app --reload
```

The server will start at `http://localhost:8000`

### API Endpoint

**POST** `/chat`

Request:
```json
{
  "message": "NRB को नीति के हो?"
}
```

Response:
```json
{
  "message": "Response from the chatbot based on NRB context..."
}
```

### Example Queries

- **English**: "What is NRB's current policy?"
- **Nepali**: "NRB को नीति के हो?"
- **Romanized Nepali**: "NRB ko niti ke ho?"

## Key Features Explained

### Language Preprocessing
The system automatically detects input language and converts it:
- **English** → Translated to Nepali for processing, response translated back
- **Nepali** → Used directly for LLM processing
- **Roman Script** → Converted to Devanagari script Nepali

### RAG Pipeline
1. Documents are loaded and split into chunks (600 tokens with 50-token overlap)
2. Embeddings generated using multilingual model
3. Query embedded and matched against document vectors
4. Top 5 most relevant chunks retrieved using MMR search
5. LLM generates answer based on retrieved context

### Strict Context Adherence
The system is configured with strict guidelines:
- Only answers from provided context
- Returns "मलाई थाहा छैन" (I don't know) when information unavailable
- No external knowledge or assumptions

## Configuration

### Vector Store Settings
- **Chunk Size**: 600 tokens
- **Chunk Overlap**: 50 tokens
- **Search Type**: MMR (Maximal Marginal Relevance)
- **Top K Results**: 5
- **Lambda Multiplier**: 0.9

### Embedding Model
- **Model**: intfloat/multilingual-e5-base
- **Supports**: 95+ languages with multilingual understanding

### LLM Model
- **Provider**: Groq
- **Model**: Llama 3.3 70B Versatile

## File Structure

```
├── main.py              # RAG pipeline and chat logic
├── app.py               # FastAPI server
├── translator.py        # Language detection and translation
├── roman.py             # Romanization mappings
├── requirements.txt     # Python dependencies
├── output.txt           # Knowledge base (NRB documents)
├── index.html           # Frontend (optional)
└── README.md            # This file
```

## Development

### Adding More NRB Documents
1. Add documents to `output.txt`
2. Restart the server to rebuild the vector store
3. The system will automatically chunk and index new content

### Customizing Prompts
Edit the `prompt` template in `main.py` to modify chatbot behavior or add different response styles.

### Extending Language Support
Add more mappings to `roman.py` for additional romanization patterns.

## Troubleshooting

### No API Key Error
Ensure `.env` file exists with valid `GROQ_API_KEY`

### Poor Response Quality
- Check if knowledge base (`output.txt`) contains relevant content
- Verify embeddings are properly generated
- Adjust chunk size/overlap for better context

### Language Detection Issues
- For romanized Nepali, ensure text follows standard romanization patterns
- Manually specify language if auto-detection fails

## Environment Variables

Create a `.env` file in the project root:
```
GROQ_API_KEY=your_groq_api_key_here
```

## Notes

- This system is designed specifically for NRB (Nepal Rastra Bank) information
- Responses are strictly bound to provided context documents
- All processing supports multilingual Nepali-English workflows

## License

[Add your license here]

## Contact

For questions or contributions, please contact the project maintainer.
