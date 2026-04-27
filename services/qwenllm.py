import logging
from pathlib import Path
from llama_cpp import Llama
# this service is responsible for loading the qwen llm model. The model is loaded using the llama_cpp library, which provides a simple interface for loading and interacting with the model, and allows for it to run locally
# eliminates typical cost concerns associated with using a hosted llm and token limits

MODEL_PATH = Path(__file__).resolve().parents[1] / "model" / "qwen2.5-1.5b-instruct-q4_k_m.gguf"

logging.getLogger("llama_cpp").setLevel(logging.ERROR) # suppress llama_cpp logging, which can be very verbose and not useful for our purposes

llm = None # global variable to hold the llm instance, we will lazy load it on first use to avoid long startup times when not needed

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
        