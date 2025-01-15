# research_agent/bot.py
import os
from dotenv import load_dotenv
import streamlit as st
from phi.agent import Agent, RunResponse
from phi.tools.duckduckgo import DuckDuckGo
from phi.model.groq import Groq
import requests  # Import requests for fetching news articles
# Import the fetch_trending_articles function
from news import fetch_trending_articles

# Load environment variables from .env file
load_dotenv()
# Set up API keys
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")  # Add your News API key

# Validate API keys
if not GROQ_API_KEY:
    raise ValueError("Missing required GROQ API key. Please check your .env file.")
if not NEWS_API_KEY:
    raise ValueError("Missing required News API key. Please check your .env file.")

# Initialize Groq model
groq_model = Groq(
    id="llama-3.3-70b-versatile",
    api_key=GROQ_API_KEY
)

def create_search_agent():
    # DuckDuckGo Agent with news functionality
    ddg_agent = Agent(
        tools=[DuckDuckGo()],
        model=groq_model,
        markdown=True,
        description="You are a search agent that helps users find information and news using DuckDuckGo.",
        instructions=[
            "When searching, return results in a structured format.",
            "Each result should include a title, link, and snippet.",
            "Focus on providing accurate and relevant information.",
            "If possible, return results as a list of dictionaries."
        ],
        show_tool_calls=True
    )
    
    return ddg_agent

def search_with_agent(agent, keyword) -> list:
    try:
        run: RunResponse = agent.run(f"Find detailed information and news about: {keyword}")
        
        # Check if run.content is a string (direct response)
        if isinstance(run.content, str):
            return [{
                'title': 'Search Result',
                'link': '',
                'snippet': run.content
            }]
        
        # If it's a dictionary with results
        elif isinstance(run.content, dict) and 'results' in run.content:
            return [{
                'title': item.get('title', 'No title'),
                'link': item.get('link', ''),
                'snippet': item.get('snippet', '')
            } for item in run.content['results']]
        
        # If it's a list of results
        elif isinstance(run.content, list):
            return [{
                'title': item.get('title', 'No title'),
                'link': item.get('link', ''),
                'snippet': item.get('snippet', '')
            } for item in run.content]
        
        else:
            return [{
                'title': 'Search Result',
                'link': '',
                'snippet': str(run.content)
            }]
            
    except Exception as e:
        st.error(f"Search failed: {str(e)}")
        return []

def generate_content_ideas(keywords):
    try:
        content_agent = Agent(
            model=groq_model,
            markdown=True,
            description="You are a creative content idea generator.",
            instructions=[
                "Generate engaging content ideas based on keywords.",
                "Format the output in clear markdown.",
                "Be specific and actionable in your suggestions."
            ]
        )
        
        prompt = f"""Given these keywords: {', '.join(keywords)}
        Generate 5 content ideas that would be interesting and engaging.
        For each idea, provide:
        1. A catchy title
        2. A brief description
        3. Key points to cover
        
        Format each idea clearly with ### separators."""
        
        run: RunResponse = content_agent.run(prompt)
        return run.content
    except Exception as e:
        st.error(f"Content generation failed: {str(e)}")
        return "Failed to generate content ideas."

def generate_linkedin_posts(keywords, content_ideas):
    try:
        linkedin_agent = Agent(
            model=groq_model,
            markdown=True,
            description="You are an expert LinkedIn copywriter who transforms content ideas into engaging posts.",
            instructions=[
                "Convert content ideas into compelling LinkedIn posts",
                "Create text-only posts that drive engagement",
                "Use professional copywriting techniques",
                "Focus on value delivery and storytelling",
                "Maintain LinkedIn's best practices"
            ]
        )
        
        prompt = f"""Based on these content ideas:

        {content_ideas}

        Transform them into 5 engaging LinkedIn posts. For each post:

        1. HOOK: Start with a powerful hook (question/statistic/statement)
        2. STORY/VALUE: Share insights or key points from the content
        3. CREDIBILITY: Include relevant data or experience
        4. VALUE DELIVERY: Explain the main benefit for readers
        5. CTA: End with a clear call-to-action
        6. HASHTAGS: Add 3-5 relevant hashtags

        Make posts:
        - Conversational yet professional
        - Easy to read (use line breaks)
        - Around 1000-1300 characters
        - Ready to copy and share
        - No images or emojis

        Format each post with ### separators."""
        
        run: RunResponse = linkedin_agent.run(prompt)
        return run.content
    except Exception as e:
        st.error(f"LinkedIn post generation failed: {str(e)}")
        return "Failed to generate LinkedIn posts."

def fetch_news_articles(keywords):
    articles = []
    for keyword in keywords:
        articles.extend(fetch_trending_articles(NEWS_API_KEY, [keyword.strip()]))
    return articles

# Set up Streamlit page config
st.set_page_config(
    page_title="Research Agent",
    page_icon="🔍",
    layout="wide"
)

# Initialize agent
ddg_agent = create_search_agent()

# Add title and description to the Streamlit app
st.title("Research Agent")
st.write("Enter keywords to search for information and news, and generate content ideas.")

# Create input field for keywords
keywords_input = st.text_area("Enter keywords (one per line)", height=100)
max_results = st.slider("Maximum results", min_value=1, max_value=10, value=5)

if st.button("Start Research"):
    if keywords_input:
        keywords = [k.strip() for k in keywords_input.split('\n') if k.strip()]
        
        with st.spinner('Searching and generating content ideas...'):
            # Create tabs for different results
            search_tab, ideas_tab, linkedin_tab, news_tab = st.tabs([
                "Search Results", 
                "Content Ideas", 
                "LinkedIn Posts", 
                "News Articles"
            ])
            
            # Perform searches
            search_results = []
            for keyword in keywords:
                with st.status(f"Searching for: {keyword}") as status:
                    st.write("Searching DuckDuckGo for information and news...")
                    ddg_results = search_with_agent(ddg_agent, keyword)
                    search_results.extend(ddg_results[:max_results])
                    
                    status.update(label="Search completed!", state="complete")

            # Display search results in the first tab
            with search_tab:
                if not search_results:
                    st.warning("No results found.")
                else:
                    for idx, result in enumerate(search_results, 1):
                        with st.container():
                            st.markdown(f"### Result {idx}")
                            title = result.get('title', 'No title')
                            link = result.get('link', '')
                            snippet = result.get('snippet', '')
                            
                            if title and title != 'No title':
                                st.markdown(f"{title}")
                            if link:
                                st.markdown(f"🔗 [{link}]({link})")
                            if snippet:
                                st.markdown(f"{snippet}")
                            st.divider()

            # Generate and display content ideas in the second tab
            with ideas_tab:
                content_ideas = generate_content_ideas(keywords)
                st.markdown("### Content Ideas")
                st.markdown(content_ideas)

            # Display LinkedIn posts in the third tab
            with linkedin_tab:
                st.markdown("### LinkedIn Posts")
                # Generate posts based on content ideas
                linkedin_posts = generate_linkedin_posts(keywords, content_ideas)
                posts = linkedin_posts.split("###")[1:]  # Skip first empty section
                
                for i, post in enumerate(posts, 1):
                    try:
                        with st.container():
                            st.markdown(f"**Post {i}**")
                            
                            with st.expander("View/Edit Post", expanded=True):
                                # Display the complete post in a text area
                                edited_post = st.text_area(
                                    "Edit your post",
                                    value=post.strip(),
                                    height=400,
                                    key=f"linkedin_post_{i}"
                                )
                                
                                col1, col2, col3 = st.columns([1, 1, 1])
                                with col1:
                                    if st.button(f"Copy Post", key=f"copy_btn_{i}"):
                                        st.write("Post copied to clipboard! 📋")
                                with col2:
                                    char_count = len(edited_post)
                                    st.write(f"Character count: {char_count}/3000")
                                with col3:
                                    if char_count > 3000:
                                        st.error("Post exceeds LinkedIn's limit!")
                                    elif char_count < 200:
                                        st.warning("Post might be too short")
                                    else:
                                        st.success("Post length is good!")
                                
                                st.markdown("#### Writing Tips:")
                                st.markdown("""
                                - Open with an attention-grabbing hook
                                - Share valuable insights from your content
                                - Use data to build credibility
                                - Add clear value for your audience
                                - End with an engaging call-to-action
                                - Use relevant hashtags for visibility
                                """)
                            
                            st.markdown("---")
                    except Exception as e:
                        st.error(f"Error displaying post {i}: {str(e)}")

            # Fetch and display news articles in the fourth tab
            with news_tab:
                news_articles = fetch_news_articles(keywords)
                if not news_articles:
                    st.warning("No news articles found.")
                else:
                    for idx, article in enumerate(news_articles, 1):
                        with st.container():
                            st.markdown(f"### Article {idx}")
                            
                            # Display only title and content
                            st.markdown(f"**{article['title']}**")
                            st.markdown("---")
                            st.text(article['content'])  # Using st.text to display plain text
                            st.divider()
    else:
        st.error("Please enter at least one keyword")

# Add footer with information
st.markdown("---")
st.markdown("Built with Streamlit, Phi Framework, and Groq")