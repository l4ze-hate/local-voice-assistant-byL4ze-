from openai import OpenAI
from config import OPEN_API_KEY
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

client = OpenAI(api_key=OPEN_API_KEY) if OPEN_API_KEY else None
cache = AICache(ttl_hours=24)

def ask_ai(promt):
    """Ask AI with caching and improved error handling."""
    if client is None:
        logger.warning("OPEN_API_KEY is not configured")
        return "OPEN_API_KEY is not configured. Add it to your .env file."

    # Check cache first
    cached_response = cache.get(promt)
    if cached_response:
        logger.info(f"Cache hit for prompt: {promt[:50]}...")
        return cached_response

    try:
        logger.info(f"Sending request to OpenAI: {promt[:50]}...")
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": promt}],
            timeout=15,  # 15 second timeout
            max_tokens=500
        )
        answer = response.choices[0].message.content
        
        # Cache the response
        cache.set(promt, answer)
        logger.info(f"Got response from OpenAI ({len(answer)} chars)")
        
        return answer
    except Exception as e:
        logger.error(f"OpenAI API error: {e}")
        return "Произошла ошибка при подключении к AI"