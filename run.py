#!/usr/bin/env python
"""
Main entry point for the 2026 Music Transcriber
"""
import argparse
import logging
from src.config import settings
from src.api.routes import create_app

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(description="Music Transcriber 2026")
    parser.add_argument("--host", default="0.0.0.0", help="Host to bind")
    parser.add_argument("--port", type=int, default=5000, help="Port to bind")
    parser.add_argument("--debug", action="store_true", help="Debug mode")
    
    args = parser.parse_args()
    
    # Create Flask app
    app = create_app()
    
    logger.info(f"Starting Music Transcriber 2026 on {args.host}:{args.port}")
    app.run(host=args.host, port=args.port, debug=args.debug)

if __name__ == "__main__":
    main()