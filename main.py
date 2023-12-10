import fastapi
from fastapi.responses import JSONResponse
from llama_cpp import Llama
from time import time
import logging


MODEL_PATH = "./stablelm-zephyr-3b.Q4_K_M.gguf"

# Logger setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Llama model
try:
    llm = Llama(
        model_path=MODEL_PATH,
        chat_format="llama-2",
        n_ctx=4096,
        n_threads=8,
        n_gpu_layers=0,
    )
except Exception as e:
    logger.error(f"Failed to load model: {e}")
    raise

app = fastapi.FastAPI()


@app.get("/")
def index():
    return fastapi.responses.RedirectResponse(url="/docs")


@app.get("/health")
def health():
    return {"status": "ok"}


# Chat Completion API
@app.get("/complete")
async def complete(
    question: str,
    system: str = "You are a story writing assistant.",
    temperature: float = 0.7,
    seed: int = 42,
) -> dict:
    try:
        st = time()
        output = llm.create_chat_completion(
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": question},
            ],
            temperature=temperature,
            seed=seed,
        )
        et = time()
        output["time"] = et - st
        return output
    except Exception as e:
        logger.error(f"Error in /complete endpoint: {e}")
        return JSONResponse(
            status_code=500, content={"message": "Internal Server Error"}
        )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
