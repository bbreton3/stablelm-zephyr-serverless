import fastapi
from llama_cpp import Llama


MODEL_PATH = "./stablelm-zephyr-3b.Q4_K_M.gguf"


# # Set gpu_layers to the number of layers to offload to GPU. Set to 0 if no GPU acceleration is available on your system.
# llm = Llama(
#     model_path=MODEL_PATH,  # Download the model file first
#     n_ctx=4096,  # The max sequence length to use - note that longer sequence lengths require much more resources
#     n_threads=8,  # The number of CPU threads to use, tailor to your system and the resulting performance
#     n_gpu_layers=0,  # The number of layers to offload to GPU, if you have GPU acceleration available
# )

# # Simple inference example
# output = llm(
#     "<|user|>\n{prompt}<|endoftext|>\n<|assistant|>",  # Prompt
#     max_tokens=512,  # Generate up to 512 tokens
#     stop=[
#         "</s>"
#     ],  # Example stop token - not necessarily correct for this specific model! Please check before using.
#     echo=False,  # Whether to echo the prompt
# )


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
def complete(user: str, system: str = "You are a story writing assistant.") -> dict:
    output = llm.create_chat_completion(
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ]
    )
    return output
