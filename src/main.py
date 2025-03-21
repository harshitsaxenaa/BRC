from math import ceil
from collections import defaultdict

def round1(x):
    return ceil(x * 10) / 10

def main():
    import os

    path_in = "testcase.txt"
    path_out = "output.txt"

    stats = defaultdict(lambda: [float('inf'), 0.0, float('-inf'), 0])

    # Read and process the file line-by-line
    with open(path_in, "rb") as fd_in:
        for line in fd_in:
            if not line:
                continue
            sep = line.find(b";")
            if sep == -1:
                continue
            city = line[:sep]
            try:
                score = float(line[sep + 1:])
            except ValueError:
                continue
            stat = stats[city]
            if score < stat[0]: stat[0] = score
            stat[1] += score
            if score > stat[2]: stat[2] = score
            stat[3] += 1

    # Prepare output efficiently
    output = []
    for city in sorted(stats.keys()):
        mn, sm, mx, cnt = stats[city]
        mean = sm / cnt
        output.append(city + b"=" + f"{round1(mn):.1f}/{round1(mean):.1f}/{round1(mx):.1f}\n".encode())

    # Write all at once to reduce I/O overhead
    with open(path_out, "wb") as fd_out:
        fd_out.writelines(output)

if __name__ == "__main__":
    main()