import torch
import torchaudio
from pathlib import Path
from typing import Dict
import logging
from demucs import pretrained
from demucs.apply import apply_model
from demucs.audio import AudioFile

logger = logging.getLogger(__name__)

class DemucsSeparator:
    def __init__(self, model_name: str = "htdemucs_ft", device: str = "cpu"):
        self.model_name = model_name
        self.device = device
        logger.info(f"Loading Demucs {model_name} on {self.device}...")
        self.model = pretrained.get_model(model_name)
        self.model.to(self.device)
        self.model.eval()
        self.sources = self.model.sources

    def separate_file(self, audio_path: str, output_dir: str = "separated") -> Dict[str, str]:
        out_path = Path(output_dir) / self.model_name / Path(audio_path).stem
        out_path.mkdir(parents=True, exist_ok=True)

    # Read audio using Demucs' AudioFile (may return numpy array or torch tensor)
        wav = AudioFile(audio_path).read(
            streams=0,
            samplerate=self.model.samplerate,
            channels=self.model.audio_channels
        )

        # Ensure shape is (channels, samples)
        if wav.shape[1] != self.model.audio_channels:
            wav = wav.T

        # Convert to torch tensor if it's not already one
        if not isinstance(wav, torch.Tensor):
            wav = torch.from_numpy(wav).float()
        else:
            wav = wav.float()

        # Add batch dimension and move to device
        wav = wav.to(self.device).unsqueeze(0)

        with torch.no_grad():
            sources = apply_model(self.model, wav, device=self.device)[0]

        stem_paths = {}
        for idx, name in enumerate(self.sources):
            stem_path = out_path / f"{name}.wav"
            torchaudio.save(str(stem_path), sources[idx].cpu(), self.model.samplerate)
            stem_paths[name] = str(stem_path)
            logger.info(f"Saved {name} to {stem_path}")

        return stem_paths