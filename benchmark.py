import httpx
import time

import argparse

# Number of requests to send
NUM_REQUESTS = 100

QUESTIONS = [
    "What is the meaning of life?",
    "What is the best movie of all time?",
    "What is the answer to the ultimate question?",
    """Is the following statement positive or negative: 
    "I hated the movie, it sucked""",
    "How many fingers can uou find on a human hand?",
]

parser = argparse.ArgumentParser()
parser.add_argument("--url", type=str)
parser.add_argument("--num_requests", type=int, default=NUM_REQUESTS)

args = parser.parse_args()


def send_request(client):
    response = client.get(args.url)
    return response


def benchmark_requests(client):
    response_times = []
    for _ in range(NUM_REQUESTS):
        start_time = time.time()
        response = send_request(client)
        end_time = time.time()
        response_times.append((end_time - start_time, response))
    return response_times


def main():
    with httpx.Client() as client:
        # Warm-up request to trigger cold start
        warmup_start_time = time.time()
        send_request(client)
        warmup_end_time = time.time()
        warmup_time = warmup_end_time - warmup_start_time

        # Benchmark subsequent requests
        response_times = benchmark_requests(client)

    total_time = sum(t for t, _ in response_times)
    successful_responses = len([r for _, r in response_times if r.status_code == 200])

    print(f"Warm-up (cold start) time: {warmup_time:.2f} seconds")
    print(
        f"Total time for {args.num_requests} requests after warm-up: {total_time:.2f} seconds"
    )
    print(
        f"Average request time (after warm-up): {total_time / args.num_requests:.2f} seconds per request"
    )
    print(f"Number of successful responses: {successful_responses}")


if __name__ == "__main__":
    main()
