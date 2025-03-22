import os
from math import ceil
import heapq

def round1(x):
    return ceil(x * 10) / 10

def process_file_and_write(input_file, output_file):
    city_stats = {}

    with open(input_file, "rb", buffering=64 * 1024) as f:
        for line in f:
            sep = line.find(b";")
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

    with open(output_file, "wb", buffering=64 * 1024) as f:
        for city in sorted(city_stats):
            mn, sm, mx, cnt = city_stats[city]
            mean = sm / cnt
            f.write(
                b"%s=%.1f/%.1f/%.1f\n" % (
                    city,
                    round1(mn),
                    round1(mean),
                    round1(mx)
                )
            )

def main():
    input_filename = "testcase.txt"
    output_filename = "output.txt"
    process_file_and_write(input_filename, output_filename)

if __name__ == "__main__":
    main()