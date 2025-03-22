from math import ceil
from multiprocessing import Pool, Manager

def round1(x):
    return ceil(x * 10) / 10

def process_chunk(lines):
    city_stats = {}
    for line in lines:
        sep = line.find(";")
        if sep == -1:
            continue
        city = line[:sep]
        try:
            score = float(line[sep + 1:])
        except ValueError:
            continue

        if city in city_stats:
            stat = city_stats[city]
            stat[0] = min(stat[0], score)
            stat[1] += score
            stat[2] = max(stat[2], score)
            stat[3] += 1
        else:
            city_stats[city] = [score, score, score, 1]
    return city_stats

def merge_stats(aggregated_stats, partial_stats):
    for city, stats in partial_stats.items():
        if city in aggregated_stats:
            agg = aggregated_stats[city]
            agg[0] = min(agg[0], stats[0])  # Min
            agg[1] += stats[1]             # Sum
            agg[2] = max(agg[2], stats[2]) # Max
            agg[3] += stats[3]             # Count
        else:
            aggregated_stats[city] = stats

def main():
    # Step 1: Read the file and split into chunks
    with open("testcase.txt", "r", buffering=64 * 1024) as f:
        lines = f.readlines()
    num_processes = 4  # Adjust based on the number of CPU cores
    chunk_size = len(lines) // num_processes
    chunks = [lines[i:i + chunk_size] for i in range(0, len(lines), chunk_size)]

    # Step 2: Use multiprocessing to process chunks
    with Pool(num_processes) as pool:
        partial_results = pool.map(process_chunk, chunks)

    # Step 3: Merge partial results
    aggregated_stats = {}
    for partial_stats in partial_results:
        merge_stats(aggregated_stats, partial_stats)

    # Step 4: Write results to the output file
    with open("output.txt", "w", buffering=64 * 1024) as f:
        for city, (mn, sm, mx, cnt) in sorted(aggregated_stats.items()):
            mean = sm / cnt
            f.write(f"{city}={round1(mn):.1f}/{round1(mean):.1f}/{round1(mx):.1f}\n")

if __name__ == "__main__":
    main()