from pathlib import Path
from llama_cpp import Llama

MODEL_PATH = Path(__file__).resolve().parents[1] / "model" / "qwen2.5-1.5b-instruct-q4_k_m.gguf"

llm = None

def get_llm():
    global llm
    if llm is None:
        if not MODEL_PATH.exists():
            raise FileNotFoundError(f"Model file not found at {MODEL_PATH}.")
        llm = Llama(
            model_path=str(MODEL_PATH),
            n_ctx=2048,
            n_threads=4,
            verbose=False,
        )
    return llm
        