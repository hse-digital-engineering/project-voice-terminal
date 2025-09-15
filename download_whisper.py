import os
from huggingface_hub import snapshot_download

# Which model should be loaded?
# tiny/base/small/medium/large-v3 -> "Systran/faster-whisper-<size>"

model_size = os.environ.get("WHISPER_MODEL", "medium")
repo = f"Systran/faster-whisper-{model_size}"

print(f"Downloading Whisper model: {repo}")

snapshot_download(
    repo_id=repo,
    local_dir=f"/models/faster-whisper-{model_size}",
    local_dir_use_symlinks=False,
    resume_download=True,
    max_workers=4,
)

print(f"Model {repo} downloaded to /models/faster-whisper-{model_size}")
