import fastapi
from llama_cpp import Llama
from time import time


MODEL_PATH = "./stablelm-zephyr-3b.Q4_K_M.gguf"


llm = Llama(
    model_path=MODEL_PATH,
    chat_format="llama-2",
    n_ctx=4096,  # The max sequence length to use - note that longer sequence lengths require much more resources
    n_threads=8,  # The number of CPU threads to use, tailor to your system and the resulting performance
    n_gpu_layers=0,
)  # Set chat_format according to the model you are using

app = fastapi.FastAPI()


@app.get("/")
def index():
    return fastapi.responses.RedirectResponse(url="/docs")


@app.get("/health")
def health():
    return {"status": "ok"}


# Chat Completion API
@app.get("/complete")
def complete(
    user: str,
    system: str = "You are a story writing assistant.",
    temperature: float = 0.7,
) -> dict:
    st = time()
    output = llm.create_chat_completion(
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        temperature=temperature,
    )
    et = time()

    output["time"] = et - st
    return output
