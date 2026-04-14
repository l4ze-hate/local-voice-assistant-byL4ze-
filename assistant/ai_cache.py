"""AI response caching module."""
import json
import os
import hashlib
from datetime import datetime, timedelta


class AICache:
    """Cache for AI responses to avoid repeated API calls."""
    
    def __init__(self, cache_file="ai_cache.json", ttl_hours=24):
        """
        Initialize cache.
        
        Args:
            cache_file: Path to cache file
            ttl_hours: Time to live for cache entries (hours)
        """
        self.cache_file = cache_file
        self.ttl = timedelta(hours=ttl_hours)
        self.cache = {}
        self._load_cache()
    
    def _load_cache(self):
        """Load cache from file."""
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    self.cache = json.load(f)
            except Exception:
                self.cache = {}
    
    def _save_cache(self):
        """Save cache to file."""
        try:
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump(self.cache, f, ensure_ascii=False, indent=2)
        except Exception:
            pass
    
    def _get_key(self, prompt):
        """Generate cache key from prompt."""
        return hashlib.md5(prompt.lower().strip().encode('utf-8')).hexdigest()
    
    def get(self, prompt):
        """Get cached response if exists and not expired."""
        key = self._get_key(prompt)
        if key in self.cache:
            entry = self.cache[key]
            cached_time = datetime.fromisoformat(entry['timestamp'])
            if datetime.now() - cached_time < self.ttl:
                return entry['response']
            else:
                # Expired, remove
                del self.cache[key]
        return None
    
    def set(self, prompt, response):
        """Cache a response."""
        key = self._get_key(prompt)
        self.cache[key] = {
            'prompt': prompt,
            'response': response,
            'timestamp': datetime.now().isoformat()
        }
        self._save_cache()
    
    def clear(self):
        """Clear all cache."""
        self.cache = {}
        if os.path.exists(self.cache_file):
            os.remove(self.cache_file)
    
    def get_stats(self):
        """Get cache statistics."""
        now = datetime.now()
        total = len(self.cache)
        valid = 0
        expired = 0
        
        for entry in self.cache.values():
            cached_time = datetime.fromisoformat(entry['timestamp'])
            if now - cached_time < self.ttl:
                valid += 1
            else:
                expired += 1
        
        return {
            'total': total,
            'valid': valid,
            'expired': expired
        }
