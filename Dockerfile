FROM python:3.12-slim

# Update package list, install OpenBLAS, build tools, and other necessary tools
RUN apt-get update \
    && apt-get install -y libopenblas-dev build-essential cmake git \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy the application files
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Download the model using Hugging Face CLI
RUN huggingface-cli download TheBloke/stablelm-zephyr-3b-GGUF stablelm-zephyr-3b.Q4_K_M.gguf --local-dir . --local-dir-use-symlinks False

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
