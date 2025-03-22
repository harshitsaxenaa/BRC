from math import ceil
from multiprocessing import Pool

def round1(x):
    return ceil(x * 10) / 10

def process_lines(lines):
    """Process a list of lines and return aggregated city statistics."""
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
            stat[0] = min(stat[0], score)  # Update min
            stat[1] += score              # Update sum
            stat[2] = max(stat[2], score) # Update max
            stat[3] += 1                  # Increment count
        else:
            city_stats[city] = [score, score, score, 1]
    return city_stats

def merge_stats(globa_stats, partial_stats):
    """Merge partial statistics into globa statistics."""
    for city, stats in partial_stats.items():
        if city in globa_stats:
            globa = globa_stats[city]
            globa[0] = min(globa[0], stats[0])  # Min
            globa[1] += stats[1]                # Sum
            globa[2] = max(globa[2], stats[2]) # Max
            globa[3] += stats[3]                # Count
        else:
            globa_stats[city] = stats

def process_file(input_file, num_processes=4, chunk_size=500_000):
    """Read and process file in parallel."""
    city_stats = {}
    with open(input_file, "r") as f:
        lines = f.readlines()
    
    chunks = [lines[i:i + chunk_size] for i in range(0, len(lines), chunk_size)]
    with Pool(num_processes) as pool:
        partial_results = pool.map(process_lines, chunks)
    
    for partial_stats in partial_results:
        merge_stats(city_stats, partial_stats)
    
    return city_stats

def write_results(city_stats, output_file):
    """Write city statistics to output file."""
    with open(output_file, "w") as f:
        for city, (mn, sm, mx, cnt) in sorted(city_stats.items()):
            mean = sm / cnt
            f.write(f"{city}={round1(mn):.1f}/{round1(mean):.1f}/{round1(mx):.1f}\n")

def main():
    input_filename = "testcase.txt"
    output_filename = "output.txt"
    num_processes = 4  # Adjust based on system capabilities
    city_stats = process_file(input_filename, num_processes=num_processes)
    write_results(city_stats, output_filename)

if __name__ == "__main__":
    main()