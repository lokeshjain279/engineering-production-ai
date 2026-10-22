"""Reproducible CPU-only batching policy simulation; not a GPU inference benchmark.

Usage:
  python3 examples/inference_benchmark.py --requests 2000 --rate 200 --seed 42
The model uses deterministic synthetic arrivals and a configurable service-time curve.
It does not model CUDA kernels, real GPUs, or network overhead.
"""
import argparse
import random
import statistics

def simulate(arrivals, batch_size, max_wait_ms, base_ms, per_item_ms):
    completed = []
    worker_free = 0.0
    index = 0
    n = len(arrivals)
    while index < n:
        first = arrivals[index]
        deadline = first + max_wait_ms / 1000
        batch = [first]
        index += 1
        # Batch fills at the arrival of its last item, or times out.
        while index < n and len(batch) < batch_size and arrivals[index] <= deadline:
            batch.append(arrivals[index])
            index += 1
        flush = batch[-1] if len(batch) == batch_size else deadline
        start = max(worker_free, flush)
        duration = (base_ms + per_item_ms * len(batch)) / 1000
        finish = start + duration
        completed.extend((finish - arrival) * 1000 for arrival in batch)
        worker_free = finish
    return completed, worker_free

def percentile(values, p):
    ordered = sorted(values)
    return ordered[min(len(ordered)-1, max(0, int((len(ordered)-1)*p)))]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--requests', type=int, default=2000)
    parser.add_argument('--rate', type=float, default=200.0, help='synthetic requests per second')
    parser.add_argument('--seed', type=int, default=42)
    parser.add_argument('--base-ms', type=float, default=5.0)
    parser.add_argument('--per-item-ms', type=float, default=1.0)
    args = parser.parse_args()
    if args.requests < 1 or args.rate <= 0 or args.base_ms < 0 or args.per_item_ms <= 0:
        parser.error('requests and rate must be positive; base-ms >= 0; per-item-ms > 0')
    rng = random.Random(args.seed)
    arrivals = [0.0]
    for _ in range(args.requests-1):
        arrivals.append(arrivals[-1] + rng.expovariate(args.rate))
    print('Synthetic queueing simulation (NOT GPU benchmark)')
    print('batch wait(ms) p50(ms) p95(ms) throughput(req/s)')
    for size, wait in [(1, 0), (4, 5), (8, 10), (16, 20)]:
        latency, finish = simulate(arrivals, size, wait, args.base_ms, args.per_item_ms)
        print(f'{size:>5} {wait:>8} {statistics.median(latency):>7.2f} {percentile(latency,.95):>7.2f} {args.requests / finish:>16.2f}')
if __name__ == '__main__':
    main()
