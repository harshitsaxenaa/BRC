from math import ceil
from multiprocessing import Pool, Manager
import os

def round1(x):
    return ceil(x * 10) / 10

def process_chunk(lines):
    """Process a chunk of lines and return city statistics."""
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
            stat[0] = min(stat[0], score)  # Min
            stat[1] += score              # Sum
            stat[2] = max(stat[2], score) # Max
            stat[3] += 1                  # Count
        else:
            city_stats[city] = [score, score, score, 1]
    return city_stats

def merge_results(partials):
    """Merge results from all processes."""
    final_stats = {}
    for partial_stats in partials:
        for city, stats in partial_stats.items():
            if city in final_stats:
                final = final_stats[city]
                final[0] = min(final[0], stats[0])  # Min
                final[1] += stats[1]                # Sum
                final[2] = max(final[2], stats[2])  # Max
                final[3] += stats[3]                # Count
            else:
                final_stats[city] = stats
    return final_stats

def process_file_in_parallel(input_file, num_processes=4, chunk_size=100_000):
    """Split the file into chunks and process in parallel."""
    with open(input_file, "r") as f:
        lines = f.readlines()

    chunks = [lines[i:i + chunk_size] for i in range(0, len(lines), chunk_size)]
    with Pool(num_processes) as pool:
        partial_results = pool.map(process_chunk, chunks)

    return merge_results(partial_results)

def write_results(city_stats, output_file):
    """Write final city statistics to the output file."""
    with open(output_file, "w") as f:
        for city, (mn, sm, mx, cnt) in sorted(city_stats.items()):
            mean = sm / cnt
            f.write(f"{city}={round1(mn):.1f}/{round1(mean):.1f}/{round1(mx):.1f}\n")

def main():
    input_filename = "testcase.txt"
    output_filename = "output.txt"
    num_processes = 4  # Adjust based on available cores

    city_stats = process_file_in_parallel(input_filename, num_processes=num_processes)
    write_results(city_stats, output_filename)

if __name__ == "__main__":
    main()