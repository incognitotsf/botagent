# Research Agent

The **Research Agent** application is a robust and interactive tool built with Streamlit, leveraging the Phi framework and Groq model to deliver powerful search, content generation, and news aggregation capabilities. The application is designed for researchers, content creators, and professionals looking to generate content ideas, LinkedIn posts, and retrieve relevant information quickly.

---

## Features

### 1. **Search Results**
- **Search Engine**: Uses DuckDuckGo for retrieving relevant search results.
- **Output**: Results are structured with titles, links, and snippets.

### 2. **Content Ideas**
- **Purpose**: Generates creative and engaging content ideas based on user-provided keywords.
- **Output**: Provides actionable suggestions in clear markdown format.

### 3. **LinkedIn Post Generator**
- **Purpose**: Converts content ideas into professional LinkedIn posts.
- **Output**:
  - Follows best practices for LinkedIn posts.
  - Includes hooks, storytelling, value delivery, and call-to-action.
  - Allows character count validation for LinkedIn's post limits.

### 4. **News Articles**
- **Purpose**: Fetches trending news articles related to the keywords.
- **Output**: Displays titles and snippets of relevant news articles.

---

## Prerequisites

### Environment Setup
- Python 3.8+
- Required dependencies listed in `requirements.txt`

### API Keys
1. **Groq API Key**: Obtainable from the Groq platform.
2. **News API Key**: Obtainable from a news aggregation service (e.g., News API).

Add these keys to a `.env` file in the following format:
```
GROQ_API_KEY=<your_groq_api_key>
NEWS_API_KEY=<your_news_api_key>
```

---

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd research_agent
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file and add your API keys (see above).

4. Run the application:
   ```bash
   streamlit run bot.py
   ```

---

## File Structure

```
.
|-- bot.py                # Main application script
|-- news.py               # Helper script for fetching trending news articles
|-- requirements.txt      # Required Python dependencies
|-- .env                  # Environment variables (not included in the repo)
```

---

## Usage

1. Launch the application by running the `bot.py` file.
2. Enter keywords (one per line) in the input field.
3. Select the number of results to display.
4. Click **Start Research**.
5. Explore the results in four tabs:
   - **Search Results**: Displays DuckDuckGo search results.
   - **Content Ideas**: Shows generated content ideas.
   - **LinkedIn Posts**: Provides editable LinkedIn posts.
   - **News Articles**: Lists relevant news articles.

---

## Key Technologies

- **Streamlit**: Provides an interactive UI for user input and display.
- **Phi Framework**: Powers the agent-based interaction model.
- **Groq**: LLM used for advanced content generation and search.
- **DuckDuckGo**: Utilized for search functionality.
- **Requests**: Fetches news articles via the News API.

---

## Development Notes

### Error Handling
- Validates API keys and displays errors if keys are missing.
- Provides user-friendly messages in case of failed searches or content generation.

### Extensibility
- Modular design allows easy addition of new agents or tools.
- Example: Add more search engines or customize the LinkedIn post template.

---

## Future Enhancements

1. Add support for multiple search engines.
2. Integrate sentiment analysis for trending news articles.
3. Provide export options for generated content.
4. Include a scheduler for automated reports.

---

## Contact
For issues or feature requests, feel free to open an issue in the repository or contact the author.

---

### License
This project is licensed under the MIT License. See the `LICENSE` file for details.

