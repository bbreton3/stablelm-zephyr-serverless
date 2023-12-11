import httpx
import time
import random
import argparse
import json

# Define a set of questions
QUESTIONS = [
    "What is the meaning of life?",
    "What is the best movie of all time?",
    "What is the answer to the ultimate question?",
    "Is the following statement positive or negative: 'I hated the movie, it sucked'",
    "How many fingers can you find on a human hand?",
]

# Number of requests to send
NUM_REQUESTS = 100

parser = argparse.ArgumentParser()
parser.add_argument("--url", type=str)
parser.add_argument("--num_requests", type=int, default=NUM_REQUESTS)

args = parser.parse_args()


def send_request(client, question):
    response = client.get(f"{args.url}/complete?question={question}", timeout=120.0)
    return response


def benchmark_requests(client):
    response_times = []
    tokens_per_second = []

    for _ in range(min(args.num_requests, 3)):  # Limit concurrency to 3
        question = random.choice(QUESTIONS)
        start_time = time.time()
        response = send_request(client, question)
        end_time = time.time()

        response_time = end_time - start_time
        response_times.append(response_time)

        if response.status_code == 200:
            try:
                data = response.json()
                completed_tokens = data["usage"]["completion_tokens"]
                tokens_sec = (
                    completed_tokens / response_time if response_time > 0 else 0
                )
                tokens_per_second.append(tokens_sec)
            except (KeyError, json.JSONDecodeError):
                print(
                    "Error processing response data for tokens per second calculation."
                )

    return response_times, tokens_per_second


def main():
    with httpx.Client() as client:
        # Warm-up request to trigger cold start
        warmup_start_time = time.time()
        send_request(
            client, random.choice(QUESTIONS)
        )  # Sending a random question for warm-up
        warmup_end_time = time.time()
        warmup_time = warmup_end_time - warmup_start_time

        # Benchmark subsequent requests
        response_times, tokens_per_second = benchmark_requests(client)

    total_time = sum(response_times)
    print(f"Warm-up (cold start) time: {warmup_time:.2f} seconds")
    print(f"Total time for subsequent requests: {total_time:.2f} seconds")
    print(
        f"Average request time: {total_time / len(response_times):.2f} seconds per request"
    )
    print(
        f"Average tokens per second: {sum(tokens_per_second) / len(tokens_per_second):.2f} tokens/sec"
        if tokens_per_second
        else "No valid responses for token/sec calculation"
    )


if __name__ == "__main__":
    main()
