from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Model paths
    model_cache_dir: str = "./data/models"
    
    # Audio processing
    target_sample_rate: int = 22050
    hop_length: int = 512
    max_audio_length: int = 300  # Max 5 minutes to process
    
    # Separation settings - OPTIMIZED
    demucs_model: str = "htdemucs_ft"
    use_gpu: bool = False
    demucs_enabled: bool = True  # Can disable for speed
    
    # ASR/Transcription - DISABLED BY DEFAULT (too slow)
    qwen_asr_enabled: bool = False  # Disable unless needed
    easytranscriber_enabled: bool = False
    
    # Indian music settings
    default_tonic_freq: float = 220.0
    enable_shruti_detection: bool = True
    
    # Raga/Tala detection - core features
    raga_detection_enabled: bool = True
    tala_detection_enabled: bool = True
    
    # Paths
    raga_db_path: str = "./data/raga_database.json"
    instrument_db_path: str = "./data/instrument_profiles.json"

    secret_key: Optional[str] = None
    
    class Config:
        env_file = ".env"
        extra = "ignore"

    @property
    def device(self) -> str:
        try:
            import torch
            if torch.cuda.is_available():
                return "cuda"
            try:
                import torch_directml
                if torch_directml.is_available():
                    return "dml"
            except ImportError:
                pass
        except ImportError:
            pass
        return "cpu"

settings = Settings()
