from math import ceil
from collections import defaultdict

def round1(x):
    return ceil(x * 10) / 10

def main():
    import os

    path_in = "testcase.txt"
    path_out = "output.txt"

    
    stats = defaultdict(lambda: [float('inf'), 0.0, float('-inf'), 0])

    
    with open(path_in, "rb") as fd_in:
        append_to_stats = stats.__getitem__
        for line in fd_in:
            sep = line.find(b";")
            if sep == -1:
                continue
            city = line[:sep]
            try:
                score = float(line[sep + 1:])
            except ValueError:
                continue
            stat = append_to_stats(city)
            stat[0] = min(stat[0], score)
            stat[1] += score
            stat[2] = max(stat[2], score)
            stat[3] += 1

    
    output = bytearray()
    stats_sorted = sorted(stats.items())
    for city, (mn, sm, mx, cnt) in stats_sorted:
        mean = sm / cnt
        output.extend(city + b"=" + f"{round1(mn):.1f}/{round1(mean):.1f}/{round1(mx):.1f}\n".encode())

    
    with open(path_out, "wb") as fd_out:
        fd_out.write(output)

if __name__ == "__main__":
    main()