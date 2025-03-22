import os
from math import ceil

def round1(x):
    return ceil(x * 10) / 10

def process_file(filename):
    city_stats = {}

    # Use buffered file reading for improved I/O performance
    with open(filename, "rb", buffering=64 * 1024) as f:
        for line in f:
            sep = line.find(b";")
            if sep == -1:
                continue
            city = line[:sep]
            try:
                score = float(line[sep + 1:])
            except ValueError:
                continue

            stat = city_stats.setdefault(city, [float("inf"), 0.0, float("-inf"), 0])
            stat[0] = min(stat[0], score)  # Minimum
            stat[1] += score              # Sum
            stat[2] = max(stat[2], score) # Maximum
            stat[3] += 1                  # Count

    return city_stats

def generate_results(city_stats):
    result = []
    for city, (mn, sm, mx, cnt) in sorted(city_stats.items()):
        mean = sm / cnt
        result.append(
            b"%s=%.1f/%.1f/%.1f\n" % (
                city,
                round1(mn),
                round1(mean),
                round1(mx)
            )
        )
    return result

def write_results(results, output_filename):
    # Use a buffered write for improved output performance
    with open(output_filename, "wb", buffering=64 * 1024) as f:
        f.write(b"".join(results))

def main():
    input_filename = "testcase.txt"
    output_filename = "output.txt"

    city_stats = process_file(input_filename)
    results = generate_results(city_stats)
    write_results(results, output_filename)

if __name__ == "__main__":
    main()