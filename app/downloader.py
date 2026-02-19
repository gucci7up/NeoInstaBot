import os
import glob
import shutil
import logging
import instaloader
from app.config import Config
from app.utils import extract_shortcode

logger = logging.getLogger(__name__)

class InstagramDownloader:
    def __init__(self):
        self.loader = instaloader.Instaloader(
            download_pictures=True,
            download_videos=True,
            download_video_thumbnails=False,
            download_geotags=False,
            download_comments=False,
            save_metadata=False,
            compress_json=False,
            filename_pattern='{shortcode}_{date_utc}_UTC'
        )
        self.logged_in = False
        self._login()

    def _login(self):
        # Set custom user agent
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        self.loader.context.user_agent = user_agent

        session_file_path = f"/app/session/session-{Config.IG_USERNAME}"
        
        # Try to load session first
        if os.path.exists(session_file_path):
            try:
                logger.info(f"Loading session from {session_file_path}")
                self.loader.load_session_from_file(Config.IG_USERNAME, filename=session_file_path)
                self.logged_in = True
                logger.info("Session loaded successfully.")
                return
            except Exception as e:
                logger.warning(f"Failed to load session, falling back to login: {e}")

        try:
            if Config.IG_USERNAME and Config.IG_PASSWORD:
                logger.info(f"Attempting login for {Config.IG_USERNAME}...")
                self.loader.login(Config.IG_USERNAME, Config.IG_PASSWORD)
                self.logged_in = True
                logger.info("Instagram login successful.")
                
                # Save session for next time
                try:
                    self.loader.save_session_to_file(filename=session_file_path)
                    logger.info(f"Session saved to {session_file_path}")
                except Exception as e:
                    logger.warning(f"Failed to save session: {e}")
            else:
                logger.warning("Instagram credentials not provided. Public access only.")
        except Exception as e:
            logger.error(f"Instagram login failed: {e}")

    def download_post(self, url: str, target_dir: str = "downloads"):
        shortcode = extract_shortcode(url)
        if not shortcode:
            raise ValueError("Invalid Instagram URL")

        # Create unique download directory for this request
        download_path = os.path.join(target_dir, shortcode)
        if os.path.exists(download_path):
            shutil.rmtree(download_path)
        os.makedirs(download_path, exist_ok=True)

        try:
            post = instaloader.Post.from_shortcode(self.loader.context, shortcode)
            logger.info(f"Downloading post {shortcode}...")
            self.loader.download_post(post, target=shortcode)
            
            # Move downloaded files to our target dir (Instaloader downloads to current working dir by default or target param relative)
            # Instaloader 'target' parameter creates a directory with that name.
            # So if we pass 'shortcode', it creates ./shortcode/
            # We want to return the list of files.
            
            # Helper to find media files
            media_files = []
            # Since we used valid target name, let's look there
            # Instaloader downloads to the directory named by 'target'
            # Note: Instaloader behavior: target is the directory name.
            # We need to handle the files after download.
            
            # Actually, let's check where it downloaded.
            # If we run from /app, and target is shortcode, it goes to /app/{shortcode}
            
            if os.path.exists(shortcode):
                # Move to the requested download_path style or just use it
                # Let's standardize the path
                final_path = os.path.abspath(shortcode)
                
                for file in glob.glob(os.path.join(final_path, "*")):
                    if file.endswith(('.jpg', '.png', '.mp4')):
                        media_files.append(file)
                
                return media_files, final_path
            else:
                raise Exception("Download directory not found after download")

        except Exception as e:
            logger.error(f"Error downloading post {shortcode}: {e}")
            # Cleanup if failed
            if os.path.exists(shortcode):
                shutil.rmtree(shortcode)
            raise e

    def cleanup(self, path: str):
        try:
            if os.path.exists(path):
                shutil.rmtree(path)
        except Exception as e:
            logger.error(f"Error cleaning up {path}: {e}")
