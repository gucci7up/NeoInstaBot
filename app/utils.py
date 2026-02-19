import logging
import re
from app.config import Config

# Setup logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=getattr(logging, Config.LOG_LEVEL.upper(), logging.INFO)
)
logger = logging.getLogger(__name__)

INSTAGRAM_URL_REGEX = re.compile(
    r'(https?://(?:www\.)?instagram\.com/(?:p|reels?|tv)/([^/?#&]+)).*'
)

def extract_shortcode(url: str) -> str | None:
    match = INSTAGRAM_URL_REGEX.search(url)
    if match:
        return match.group(2)
    return None

def is_instagram_url(url: str) -> bool:
    return bool(INSTAGRAM_URL_REGEX.search(url))
