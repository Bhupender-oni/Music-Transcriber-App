#!/usr/bin/env python
"""
Music Transcriber Application Entry Point
Run this from project root: python run.py
"""
import argparse
import logging
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).resolve().parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.config import settings
from src.api.routes import create_app

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(
        description="Music Transcriber 2026 - Indian Classical Music Analysis",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run.py                    # Start on localhost:5000
  python run.py --port 8000        # Custom port
  python run.py --debug            # Debug mode (auto-reload)
  python run.py --host 0.0.0.0     # Listen on all interfaces
        """
    )
    parser.add_argument("--host", default="127.0.0.1", help="Host to bind (default: 127.0.0.1)")
    parser.add_argument("--port", type=int, default=5000, help="Port to bind (default: 5000)")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    
    args = parser.parse_args()
    
    logger.info("=" * 60)
    logger.info("Music Transcriber 2026 - Indian Classical Music Analysis")
    logger.info("=" * 60)
    logger.info(f"Starting on {args.host}:{args.port}")
    logger.info(f"Configuration: {settings.device.upper()} mode")
    logger.info(f"Demucs enabled: {settings.demucs_enabled}")
    logger.info(f"Raga detection: {settings.raga_detection_enabled}")
    logger.info(f"Tala detection: {settings.tala_detection_enabled}")
    logger.info("=" * 60)
    
    try:
        app = create_app()
        app.run(host=args.host, port=args.port, debug=args.debug, use_reloader=args.debug)
    except Exception as e:
        logger.error(f"Failed to start server: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()
