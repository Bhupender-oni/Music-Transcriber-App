from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Model paths
    model_cache_dir: str = "./data/models"
    
    # Audio processing
    target_sample_rate: int = 22050
    hop_length: int = 512
    
    # Separation settings
    demucs_model: str = "htdemucs_ft"   # Best quality
    use_gpu: bool = False                # Force CPU (Intel Iris)
    
    # Indian music settings
    default_tonic_freq: float = 220.0   # A3
    enable_shruti_detection: bool = True
    
    # Paths
    raga_db_path: str = "./data/raga_database.json"
    instrument_db_path: str = "./data/instrument_profiles.json"

    secret_key: Optional[str] = None
    
    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()