from contextlib import contextmanager
import logging
import os
from pathlib import Path
from llama_cpp import Llama
# this service is responsible for loading the qwen llm model. The model is loaded using the llama_cpp library, which provides a simple interface for loading and interacting with the model, and allows for it to run locally
# eliminates typical cost concerns associated with using a hosted llm and token limits

MODEL_PATH = Path(__file__).resolve().parents[1] / "model" / "qwen2.5-1.5b-instruct-q4_k_m.gguf"

llm = None # global variable to hold the llm instance, we will lazy load it on first use to avoid long startup times when not needed

@contextmanager
def suppress_stderr():
    devnull = os.open(os.devnull, os.O_WRONLY)
    saved_stderr = os.dup(2)
    try:
        os.dup2(devnull, 2)
        yield
    finally:
        os.dup2(saved_stderr, 2)
        os.close(devnull)
        os.close(saved_stderr)

def get_llm():
    global llm
    try:
        if llm is None:
            if not MODEL_PATH.exists():
                raise FileNotFoundError(f"Model file not found at {MODEL_PATH}.")
            with suppress_stderr():
                llm = Llama(
                    model_path=str(MODEL_PATH),
                    n_ctx=2048,
                    n_threads=4,
                    verbose=False,
                )
    except Exception as e:
        logging.error(f"Error loading LLM model: {e}")
        raise e
    return llm
        