# Text Streaming Service

A FastAPI-based service that implements a text streaming API which generates real-time text completions using the GPT-2 model. It leverages FastAPI for the web server, Redis for task queue management, and ModelQ for distributed task processing. The service streams text responses in real-time using Server-Sent Events (SSE).

## Features

- Real-time text streaming using Server-Sent Events (SSE)
- GPT-2 model integration for text generation
- Distributed task processing with ModelQ
- Redis-based task queue management
- FastAPI web server implementation

## Prerequisites

- Python 3.7+
- Redis server running locally
- CUDA-capable GPU (recommended for better performance)

## Installation

1. Clone the repository
2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the required dependencies:
```bash
pip install -r requirements.txt
```

4. Copy the environment example file and configure it:
```bash
cp .env.example .env
# Edit .env with your configuration
```

## Project Structure

```
text-streaming-service/
├── app.py              # FastAPI application and endpoints
├── tasks.py            # ModelQ tasks and model initialization
├── runner.py           # Worker process runner
├── requirements.txt    # Python dependencies
├── .env.example        # Example environment configuration
├── .gitignore         # Git ignore rules
└── README.md          
```

## Usage

1. Start the Redis server:
```bash
redis-server
```

2. Start the worker process:
```bash
python runner.py
```

3. Start the FastAPI server:
```bash
uvicorn app:app --reload
```

4. Access the API endpoint:
```
GET /completion/{question}
```

The service will stream the generated text response in real-time.

## API Endpoints

### Text Completion

- **Endpoint**: `/completion/{question}`
- **Method**: GET
- **Response**: Server-Sent Events (SSE) stream of generated text
- **Media Type**: `text/event-stream`

## Configuration

The service uses the following default configurations (configurable via .env file):
- Redis host: localhost
- Redis port: 6379
- Redis database: 0
- Model: GPT-2 (openai-community/gpt2)
- Generation parameters: max_new_tokens=20

## Dependencies

- FastAPI
- ModelQ
- Redis
- PyTorch
- Transformers
- NumPy

## Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

Please ensure your PR includes:
- Clear description of changes
- Updated documentation if needed