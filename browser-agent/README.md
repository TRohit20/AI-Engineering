# Intelligent Browser Automation using GPT 4o

Browser Agent built by leveraging the GPT-4o, computer vision, and sophisticated DOM understanding to create a intelligent browser automation tool that makes it easy for the browser to understand your intentions and executes complex online operations on the web.

## Key Features

### Natural Language Control
Control any website with plain English. No complex syntax or programming languages.
```
> go to apple.com/in and search for Airpods Max
> Add the product to cart with basic configuration available.
> extract data
```

### Vision-Powered Analysis
Browser Agent leverages GPT-4o Vision to analyze screenshots, understand page layouts, and identify interactive elements even when the DOM is complex or dynamic.

### Autonomous Task Planning
Describe complex, multi-step tasks in natural language and let Browser Agent break them down into smaller sub-tasks and execute them:
```
> plan find information about system design programming courses, compare prices, and save screenshots
```

### Advanced DOM Understanding
Unlike other browser automation tools, Browser Agent understands webpage structure extensively, extracting interactive elements, form fields, and content areas for more precise interactions.

### Async Architecture
Built on Playwright's async API for fast, non-blocking operations and better performance.

## Getting Started

### Installation

```bash
# Clone the repository
git clone https://github.com/TRohit20/AI-Engineering.git
cd browser-agent

# Install dependencies 
pip install -r requirements.txt

# Install and start chromium
playwright install chromium
playwright run chromium

# Set your OpenAI API key
echo "OPENAI_API_KEY=your_api_key_here" > .env
```

### Usage

Start the interactive CLI:
```bash
python cli.py
```

Run with a starting URL:
```bash
python cli.py https://www.your-wish.com
```

Execute an autonomous task:
```bash
python cli.py --task "research about calvin klein wacthes for women under 20,000 INR and create a comparison"
```

## 💻 Command Reference

### Navigation
- `go to apple.com` - Navigate to a website
- `back` / `forward` / `refresh` - Basic navigation
- `search for Airpods Max` - Search on the current site

### Interaction
- `click "Sign In"` - Click elements by text
- `click selector "#submit-button"` - Click by CSS selector
- `type "john@example.com" in "email"` - Fill form fields
- `submit` - Submit forms
- `scroll down 500` - Scroll the page

### Analysis
- `analyze` - Perform AI analysis of the current page
- `extract data` - Extract structured data
- `screenshot` - Capture screenshot

### Autonomous Features
- `plan find the best, yet affordable macbook pro for a university student pursuing biotechnology` - Plan a complex task
- `execute plan` - Execute the last created plan

## How It Works

1. **Command Interpretation**: Natural language commands are interpreted using sophisticated pattern matching and context awareness.

2. **DOM Extraction**: Advanced JavaScript injection extracts interactive elements, content structure, and page metadata.

3. **Vision Analysis**: GPT-4o Vision analyzes screenshots to understand content even when the DOM doesn't tell the whole story.

4. **Autonomous Planning**: Complex tasks are broken down into actionable steps using AI planning techniques.

5. **Context-Aware Execution**: Each step is refined based on the current page state before execution.

## Limitations

Browser Agent is a tool under active development:

- **Accuracy**: The agent may occasionally misinterpret complex page structures or dynamic elements
- **Website Compatibility**: Some websites with unusual structures or heavy JavaScript might present challenges
- **Task Complexity**: While capable of handling complex tasks, extremely multi-faceted operations may require breaking down into smaller tasks
- **Rate Limitations**: Heavy usage may be subject to OpenAI API rate limits

please be aware that some operations may require retries or human assistance. The autonomous planning feature works best with clear, specific task descriptions.

## Some Use Cases

- **Market Research**: Automate the collection of pricing and product information across multiple sites
- **Content Monitoring**: Regular checks on websites for changes or updates
- **Form Automation**: Streamline complex form filling processes
- **Data Extraction**: Collect information from structured or semi-structured websites
- **UX Testing**: Simulate user journeys through applications

## Advanced Configuration

Browser Agent can be customized through the `config.py` file, which allows you to:
- Configure site-specific selectors
- Adjust timing and wait behaviors
- Customize prompt templates
- Set up headless operation

## Contributing
Contributions are welcome! If you have suggestions for improvements or new features, please fork the repository and submit a pull request.
