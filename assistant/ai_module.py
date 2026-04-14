from openai import OpenAI
from config import AI_PROVIDER, OPEN_API_KEY, OPENAI_MODEL, LOCAL_AI_URL, LOCAL_AI_MODEL, GROQ_API_KEY, GROQ_MODEL
from assistant.ai_cache import AICache
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('assistant.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('AI')

cache = AICache(ttl_hours=24)

# Initialize client based on provider
def _init_client():
    """Initialize AI client with appropriate configuration."""
    if AI_PROVIDER == "groq":
        if not GROQ_API_KEY:
            logger.error("GROQ_API_KEY is not set")
            return None
        logger.info(f"Using Groq API with model {GROQ_MODEL}")
        return OpenAI(
            api_key=GROQ_API_KEY,
            base_url="https://api.groq.com/openai/v1"
        )
    elif AI_PROVIDER == "local":
        logger.info(f"Using local AI provider at {LOCAL_AI_URL} with model {LOCAL_AI_MODEL}")
        return OpenAI(
            api_key="not-needed",  # Local servers don't require API key
            base_url=LOCAL_AI_URL + "/v1"
        )
    elif AI_PROVIDER == "openai" and OPEN_API_KEY:
        logger.info(f"Using OpenAI with model {OPENAI_MODEL}")
        return OpenAI(api_key=OPEN_API_KEY)
    else:
        logger.warning(f"Invalid AI_PROVIDER '{AI_PROVIDER}' or missing configuration")
        return None

client = _init_client()

def ask_ai(promt):
    """Ask AI with caching and improved error handling."""
    if client is None:
        if AI_PROVIDER == "groq":
            msg = "Groq API key is not configured. Add GROQ_API_KEY to key.env"
        elif AI_PROVIDER == "local":
            msg = f"Cannot connect to local AI server at {LOCAL_AI_URL}. Make sure it's running."
        else:
            msg = "AI is not configured. Check AI_PROVIDER and API key settings."
        logger.warning(msg)
        return msg

    # Check cache first
    cached_response = cache.get(promt)
    if cached_response:
        logger.info(f"Cache hit for prompt: {promt[:50]}...")
        return cached_response

    try:
        if AI_PROVIDER == "groq":
            model = GROQ_MODEL
        elif AI_PROVIDER == "local":
            model = LOCAL_AI_MODEL
        else:
            model = OPENAI_MODEL
            
        logger.info(f"Sending request (provider={AI_PROVIDER}, model={model}): {promt[:50]}...")
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": promt}],
            timeout=30,  # Increased timeout for local servers
            max_tokens=500
        )
        answer = response.choices[0].message.content
        
        # Cache the response
        cache.set(promt, answer)
        logger.info(f"Got response ({len(answer)} chars)")
        
        return answer
    except Exception as e:
        logger.error(f"AI request error: {e}")
        return "Произошла ошибка при подключении к AI"