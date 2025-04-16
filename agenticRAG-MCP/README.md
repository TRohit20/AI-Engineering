# Agentic RAG with Model Context Protocol (MCP)

A sophisticated automated book writing system powered by AI agents, combining web scraping, vector database storage, and intelligent context processing through MCP.

## Overview

This project implements an advanced Retrieval Augmented Generation (RAG) system that:
- Uses [Bright Data](https://brdta.com/dailydoseofds) for intelligent web scraping
- Leverages Qdrant as a local vector database for efficient information storage and retrieval
- Integrates with Cursor IDE through Model Context Protocol (MCP) for enhanced context understanding

## Features

- **Intelligent Web Scraping**: Automated data collection from web sources using Bright Data's SERP API
- **Vector Database Storage**: Efficient storage and retrieval of embeddings using Qdrant
- **MCP Integration**: Seamless interaction with Cursor IDE for enhanced context processing
- **Hybrid Search**: Combines semantic search with traditional search methods for optimal results

## Prerequisites

- Python 3.11 or later
- Docker (for running Qdrant)
- Cursor IDE
- Bright Data account
- Sufficient storage space for vector database

## Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/LLM-engineering/agenticRAG-MCP.git
   cd agenticRAG-MCP
   ```

2. **Install Dependencies**
   ```bash
   pip install mcp qdrant-client
   ```

3. **Configure Bright Data**
   - Sign up at [Bright Data](https://brdta.com/dailydoseofds)
   - Create a new SERP API with "Native proxy-based access"
   - Copy your credentials and create a `.env` file:
     ```
     BRIGHDATA_USERNAME="your_username"
     BRIGHDATA_PASSWORD="your_password"
     ```

## Setup

1. **Start Qdrant Database**
   ```bash
   docker run -p 6333:6333 -p 6334:6334 \
   -v $(pwd)/qdrant_storage:/qdrant/storage:z \
   qdrant/qdrant
   ```

2. **Initialize Vector Database**
   - Open `notebook.ipynb`
   - Follow the instructions to create and configure your collection

3. **Configure MCP Server**
   - Open Cursor IDE settings
   - Navigate to MCP section
   - Add a new global MCP server with the following configuration:
     ```json
     {
       "mcpServers": {
           "mcp-rag-app": {
               "command": "python",
               "args": ["/absolute/path/to/server.py"],
               "host": "127.0.0.1",
               "port": 8080,
               "timeout": 30000
           }
       }
     }
     ```

## Usage

The system provides two main functionalities:
1. **Vector Database Queries**: Search and retrieve information from your local knowledge base
2. **Web Search Fallback**: Automatically fall back to web search when local data is insufficient

## Contributing

Contributions are welcome! Please follow these steps:
1. Raise relevant issue explaining the issue/suggestion along with solution.
2. Fork the repository.
3. Create a feature branch.
4. Commit your changes.
5. Push to the branch.
6. Submit a pull request.

## Disclaimer

This tool is provided as-is, without any warranties. Users are responsible for complying with all applicable laws and regulations regarding web scraping and data usage.

## Support

For issues, questions, or contributions, please:
1. Check existing issues in the repository
2. Create a new issue if needed

---