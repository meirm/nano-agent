# Complete Guide: Developing MCP Servers with FastMCP

## Table of Contents
1. [Introduction](#introduction)
2. [Installation & Setup](#installation--setup)
3. [Core Concepts](#core-concepts)
4. [Building Your First Server](#building-your-first-server)
5. [Tools - Adding Actions](#tools---adding-actions)
6. [Resources - Exposing Data](#resources---exposing-data)
7. [Prompts - Guiding Interactions](#prompts---guiding-interactions)
8. [Context & Advanced Features](#context--advanced-features)
9. [Running & Deployment](#running--deployment)
10. [Testing & Debugging](#testing--debugging)
11. [Real-World Examples](#real-world-examples)

## Introduction

FastMCP is a high-level Python framework that simplifies building Model Context Protocol (MCP) servers. MCP is a standardized way for AI assistants (like Claude, Cursor, etc.) to interact with external data sources and tools - think of it as "the USB-C port for AI".

### Why FastMCP?

- **Minimal Boilerplate**: Create fully functional MCP servers with just a few lines of code
- **Pythonic Design**: Uses familiar decorator patterns similar to Flask/FastAPI
- **Automatic Schema Generation**: Generates MCP schemas from type hints and docstrings
- **Production Ready**: Includes authentication, deployment tools, and testing frameworks

## Installation & Setup

### Prerequisites
- Python 3.10 or higher
- UV package manager (recommended) or pip

### Installation

**Using UV (Recommended):**
```bash
# Install UV
curl -LsSf https://astral.sh/uv/install.sh | sh  # macOS/Linux
# Or on Windows:
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# Install FastMCP
uv pip install fastmcp
```

**Using pip:**
```bash
pip install fastmcp
```

### Verify Installation
```bash
fastmcp --version
```

## Core Concepts

FastMCP is built around three main components:

1. **Tools**: Functions that LLMs can execute (like POST endpoints)
2. **Resources**: Read-only data endpoints (like GET endpoints)  
3. **Prompts**: Reusable templates for LLM interactions

## Building Your First Server

Let's create a simple MCP server:

```python
# server.py
from fastmcp import FastMCP

# Create the server instance
mcp = FastMCP("My First Server")

@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers together"""
    return a + b

@mcp.resource("greeting://hello")
def get_greeting() -> str:
    """Return a friendly greeting"""
    return "Hello from MCP!"

if __name__ == "__main__":
    mcp.run()
```

Run the server:
```bash
fastmcp run server.py
```

## Tools - Adding Actions

Tools are functions that LLMs can execute. They should perform actions and can have side effects.

### Basic Tool
```python
@mcp.tool()
def calculate_area(length: float, width: float) -> float:
    """Calculate the area of a rectangle"""
    return length * width
```

### Tool with Complex Types
```python
from typing import List, Dict
from pydantic import BaseModel

class TodoItem(BaseModel):
    title: str
    completed: bool = False
    priority: int = 1

@mcp.tool()
def create_todo(item: TodoItem) -> Dict:
    """Create a new todo item"""
    # Your logic here
    return {
        "id": "todo-123",
        "title": item.title,
        "completed": item.completed,
        "priority": item.priority
    }
```

### Async Tools
```python
import asyncio

@mcp.tool()
async def fetch_data(url: str) -> str:
    """Fetch data from a URL asynchronously"""
    await asyncio.sleep(1)  # Simulate network delay
    return f"Data from {url}"
```

## Resources - Exposing Data

Resources provide read-only data to LLMs. They should not perform significant computation or have side effects.

### Static Resources
```python
@mcp.resource("config://app")
def get_config() -> dict:
    """Get application configuration"""
    return {
        "version": "1.0.0",
        "environment": "production"
    }
```

### Dynamic Resources with Templates
```python
@mcp.resource("users://{user_id}/profile")
def get_user_profile(user_id: str) -> dict:
    """Get a user's profile by ID"""
    # Fetch from database
    return {
        "id": user_id,
        "name": f"User {user_id}",
        "email": f"user{user_id}@example.com"
    }
```

### Resource with File Data
```python
import json

@mcp.resource("data://products")
def get_products() -> list:
    """Get list of products from file"""
    with open("products.json", "r") as f:
        return json.load(f)
```

## Prompts - Guiding Interactions

Prompts are reusable templates that help structure LLM interactions.

### Simple Prompt
```python
@mcp.prompt()
def analyze_code(language: str, code: str) -> str:
    """Generate a prompt for code analysis"""
    return f"""
    Please analyze the following {language} code:
    
    ```{language}
    {code}
    ```
    
    Provide:
    1. A brief summary of what the code does
    2. Any potential issues or improvements
    3. Suggestions for optimization
    """
```

### Multi-Message Prompt
```python
from fastmcp.prompts.base import UserMessage, AssistantMessage, Message

@mcp.prompt()
def debug_conversation(error: str) -> List[Message]:
    """Create a debugging conversation"""
    return [
        UserMessage("I encountered this error:"),
        UserMessage(error),
        AssistantMessage("I'll help you debug this. Let me analyze the error."),
        UserMessage("What could be causing this?")
    ]
```

## Context & Advanced Features

The Context object provides access to MCP session capabilities.

### Using Context for Logging
```python
from fastmcp import FastMCP, Context

@mcp.tool()
async def process_file(filename: str, ctx: Context) -> str:
    """Process a file with progress updates"""
    
    # Log information
    await ctx.info(f"Starting to process {filename}")
    
    # Simulate processing
    for i in range(5):
        await ctx.report_progress(i, 5)
        await asyncio.sleep(1)
    
    await ctx.info(f"Completed processing {filename}")
    return f"Processed {filename} successfully"
```

### Context for LLM Sampling
```python
@mcp.tool()
async def smart_summary(text: str, ctx: Context) -> str:
    """Get an AI-generated summary"""
    
    # Ask the client's LLM for a summary
    response = await ctx.sample(
        f"Please summarize the following text in 2-3 sentences:\n\n{text}"
    )
    
    return response.text
```

### Reading Resources from Tools
```python
@mcp.tool()
async def process_resource(resource_uri: str, ctx: Context) -> str:
    """Process data from a resource"""
    
    # Read another resource
    data = await ctx.read_resource(resource_uri)
    
    # Process the data
    return f"Processed {len(data.content)} bytes from {resource_uri}"
```

## Running & Deployment

### Transport Modes

FastMCP supports three transport modes:

**1. STDIO (Default) - for local tools:**
```python
mcp.run(transport="stdio")  # Default
```

**2. HTTP/SSE - for web deployments:**
```python
# HTTP (Streamable)
mcp.run(transport="http", host="127.0.0.1", port=8000, path="/mcp")

# SSE (Server-Sent Events)
mcp.run(transport="sse", host="127.0.0.1", port=8000)
```

### Integration with Claude Desktop

1. Create your server:
```python
# weather_server.py
from fastmcp import FastMCP

mcp = FastMCP("Weather Server")

@mcp.tool()
def get_weather(city: str) -> dict:
    """Get weather for a city"""
    # Mock data - replace with real API
    return {
        "city": city,
        "temperature": 72,
        "conditions": "Sunny"
    }

if __name__ == "__main__":
    mcp.run()
```

2. Install for Claude Desktop:
```bash
fastmcp install weather_server.py
```

3. Or manually edit Claude's config:
```json
// ~/Library/Application Support/Claude/claude_desktop_config.json (macOS)
{
  "mcpServers": {
    "weather": {
      "command": "uv",
      "args": ["--quiet", "run", "/path/to/weather_server.py"]
    }
  }
}
```

### Environment Variables

```python
# Using environment variables
mcp = FastMCP("My Server")

# Via .env file
fastmcp install server.py -f .env

# Or individual variables
fastmcp install server.py -e API_KEY=abc123 -e DB_URL=postgres://...
```

## Testing & Debugging

### Using MCP Inspector

The MCP Inspector is the best tool for testing:

```bash
# Run your server with inspector
fastmcp dev server.py
```

This opens a web interface where you can:
- List and test tools
- Browse resources
- Execute prompts
- View logs and debug output

### Testing with FastMCP Client

```python
# test_server.py
import asyncio
from fastmcp import FastMCP, Client

# Create server
mcp = FastMCP("Test Server")

@mcp.tool()
def multiply(a: float, b: float) -> float:
    """Multiply two numbers"""
    return a * b

async def test():
    # Connect client to server (in-memory)
    async with Client(mcp) as client:
        # List available tools
        tools = await client.list_tools()
        print(f"Tools: {tools}")
        
        # Call a tool
        result = await client.call_tool("multiply", {"a": 5, "b": 3})
        print(f"Result: {result.text}")

if __name__ == "__main__":
    asyncio.run(test())
```

## Real-World Examples

### Example 1: Database Explorer

```python
from fastmcp import FastMCP, Context
import sqlite3
from typing import List, Dict

mcp = FastMCP("Database Explorer")

@mcp.resource("schema://tables")
def get_tables() -> List[str]:
    """List all tables in the database"""
    conn = sqlite3.connect("app.db")
    cursor = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table'"
    )
    tables = [row[0] for row in cursor.fetchall()]
    conn.close()
    return tables

@mcp.tool()
def query_database(sql: str, ctx: Context) -> List[Dict]:
    """Execute a SQL query safely"""
    # Only allow SELECT statements
    if not sql.strip().upper().startswith("SELECT"):
        raise ValueError("Only SELECT queries are allowed")
    
    conn = sqlite3.connect("app.db")
    cursor = conn.execute(sql)
    
    # Get column names
    columns = [desc[0] for desc in cursor.description]
    
    # Convert rows to dictionaries
    results = []
    for row in cursor.fetchall():
        results.append(dict(zip(columns, row)))
    
    conn.close()
    return results

@mcp.prompt()
def analyze_table_prompt(table_name: str) -> str:
    """Generate analysis prompt for a table"""
    return f"""
    Please analyze the database table '{table_name}':
    1. Describe the purpose of this table
    2. Identify key columns and relationships
    3. Suggest potential queries for insights
    4. Recommend any optimizations
    """
```

### Example 2: File Processing Server

```python
from fastmcp import FastMCP, Context, Image
import os
from pathlib import Path
from PIL import Image as PILImage

mcp = FastMCP("File Processor")

@mcp.resource("files://{directory}")
def list_files(directory: str = ".") -> List[str]:
    """List files in a directory"""
    path = Path(directory)
    if not path.exists():
        return []
    
    return [str(f.name) for f in path.iterdir() if f.is_file()]

@mcp.tool()
async def process_text_file(
    filepath: str, 
    operation: str,
    ctx: Context
) -> str:
    """Process a text file with various operations"""
    
    await ctx.info(f"Processing {filepath} with operation: {operation}")
    
    with open(filepath, 'r') as f:
        content = f.read()
    
    if operation == "count_words":
        word_count = len(content.split())
        return f"Word count: {word_count}"
    
    elif operation == "count_lines":
        line_count = len(content.splitlines())
        return f"Line count: {line_count}"
    
    elif operation == "extract_urls":
        import re
        urls = re.findall(r'https?://[^\s]+', content)
        return f"Found URLs: {', '.join(urls)}"
    
    else:
        return "Unknown operation"

@mcp.tool()
def create_thumbnail(image_path: str, size: int = 100) -> Image:
    """Create a thumbnail from an image"""
    img = PILImage.open(image_path)
    img.thumbnail((size, size))
    
    # FastMCP handles the image conversion
    return Image(data=img, format="png")
```

### Example 3: API Integration Server

```python
from fastmcp import FastMCP, Context
import httpx
import asyncio
from typing import Optional

mcp = FastMCP("API Gateway", dependencies=["httpx"])

# Cache for API responses
cache = {}

@mcp.tool()
async def fetch_weather(city: str, ctx: Context) -> dict:
    """Fetch weather data for a city"""
    
    # Check cache first
    if city in cache:
        await ctx.info(f"Returning cached weather for {city}")
        return cache[city]
    
    await ctx.info(f"Fetching fresh weather data for {city}")
    
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"https://api.openweathermap.org/data/2.5/weather",
            params={"q": city, "appid": os.getenv("OPENWEATHER_API_KEY")}
        )
        
        data = response.json()
        
        # Cache the result
        cache[city] = data
        
        return {
            "city": city,
            "temperature": data["main"]["temp"],
            "description": data["weather"][0]["description"],
            "humidity": data["main"]["humidity"]
        }

@mcp.resource("weather://cached")
def get_cached_cities() -> List[str]:
    """Get list of cities with cached weather data"""
    return list(cache.keys())

@mcp.prompt()
def weather_report_prompt(cities: List[str]) -> str:
    """Generate a weather report prompt"""
    city_list = ", ".join(cities)
    return f"""
    Create a comprehensive weather report for the following cities: {city_list}
    
    For each city:
    1. Call the fetch_weather tool to get current conditions
    2. Describe the weather in natural language
    3. Provide recommendations for outdoor activities
    4. Note any weather warnings or concerns
    
    Format the report in a clear, readable manner.
    """
```

## Best Practices

### 1. Error Handling
```python
@mcp.tool()
def safe_divide(a: float, b: float) -> float:
    """Safely divide two numbers"""
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b
```

### 2. Input Validation with Pydantic
```python
from pydantic import BaseModel, Field, validator

class EmailRequest(BaseModel):
    to: str = Field(..., description="Recipient email")
    subject: str = Field(..., max_length=200)
    body: str
    
    @validator('to')
    def validate_email(cls, v):
        if '@' not in v:
            raise ValueError('Invalid email address')
        return v

@mcp.tool()
def send_email(request: EmailRequest) -> str:
    """Send an email"""
    # Implementation here
    return f"Email sent to {request.to}"
```

### 3. Performance Optimization
```python
# Use caching for expensive operations
from functools import lru_cache

@mcp.resource("data://expensive")
@lru_cache(maxsize=100)
def get_expensive_data(param: str) -> dict:
    """Cache expensive computations"""
    # Expensive operation here
    return {"result": "cached"}
```

### 4. Security Considerations
```python
@mcp.tool()
def read_file(filepath: str) -> str:
    """Safely read a file with path validation"""
    
    # Validate path to prevent directory traversal
    safe_path = Path(filepath).resolve()
    base_path = Path(".").resolve()
    
    if not str(safe_path).startswith(str(base_path)):
        raise ValueError("Access denied: Path outside allowed directory")
    
    with open(safe_path, 'r') as f:
        return f.read()
```

## Troubleshooting

### Common Issues

**1. Server not showing in Claude Desktop:**
- Check the config file location
- Verify UV is installed and in PATH
- Check server logs: `tail -n 50 ~/Library/Logs/Claude/mcp*.log`

**2. Import errors:**
- Ensure all dependencies are installed: `uv pip install -r requirements.txt`
- Check Python version: `python --version` (needs 3.10+)

**3. Tool not working:**
- Verify type hints are correct
- Check docstring format
- Test with MCP Inspector first

## Next Steps

1. **Explore Advanced Features:**
   - Authentication and security
   - Server composition and proxying
   - OpenAPI/FastAPI integration

2. **Build Complex Servers:**
   - Database integrations
   - API gateways
   - File processors
   - Multi-modal handlers (images, audio)

3. **Deploy to Production:**
   - Set up HTTP/SSE transport
   - Configure authentication
   - Add monitoring and logging
   - Scale with load balancers

## Resources

- [Official FastMCP Documentation](https://gofastmcp.com)
- [MCP Protocol Specification](https://modelcontextprotocol.io)
- [FastMCP GitHub Repository](https://github.com/jlowin/fastmcp)
- [Example Servers](https://github.com/jlowin/fastmcp/tree/main/examples)

## Summary

FastMCP makes building MCP servers incredibly simple while maintaining flexibility for complex use cases. With just a few decorators, you can expose tools, resources, and prompts that AI assistants can use to interact with your systems and data.

Key takeaways:
- Use `@mcp.tool()` for actions with side effects
- Use `@mcp.resource()` for read-only data access
- Use `@mcp.prompt()` for reusable interaction templates
- Leverage Context for advanced features
- Test with MCP Inspector before deployment
- Follow security best practices for production use
