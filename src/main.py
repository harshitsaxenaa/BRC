import os
import mmap
import multiprocessing
from math import ceil
from collections import defaultdict

def round1(x):
    return ceil(x * 10) / 10

def process_chunk(args):
    data, start, end = args
    local_stats = {}

    # Ensure we start and end on line boundaries
    while start > 0 and data[start-1] != ord('\n'):
        start -= 1
    while end < len(data) and data[end-1] != ord('\n'):
        end += 1

    i = start
    while i < end:
        j = data.find(b'\n', i)
        if j == -1:
            break
        line = data[i:j]
        i = j + 1

        sep = line.find(b";")
        if sep == -1:
            continue

        city = line[:sep]
        try:
            score = float(line[sep + 1:])
        except:
            continue

        stat = local_stats.get(city)
        if stat:
            if score < stat[0]: stat[0] = score
            stat[1] += score
            if score > stat[2]: stat[2] = score
            stat[3] += 1
        else:
            local_stats[city] = [score, score, score, 1]

    return local_stats

def merge_stats(stats_list):
    final_stats = {}

    for stats in stats_list:
        for city, values in stats.items():
            if city in final_stats:
                fs = final_stats[city]
                fs[0] = min(fs[0], values[0])
                fs[1] += values[1]
                fs[2] = max(fs[2], values[2])
                fs[3] += values[3]
            else:
                final_stats[city] = values

    return final_stats

def main():
    with open("testcase.txt", "rb") as f:
        mm = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
        data = mm[:]
        mm.close()

    n = multiprocessing.cpu_count()
    chunk_size = len(data) // n

    chunks = [(data, i * chunk_size, (i + 1) * chunk_size if i < n - 1 else len(data)) for i in range(n)]

    with multiprocessing.Pool(processes=n) as pool:
        results = pool.map(process_chunk, chunks)

    final_stats = merge_stats(results)

    output = bytearray()
    for city in sorted(final_stats):
        mn, sm, mx, cnt = final_stats[city]
        mean = sm / cnt
        output.extend(city)
        output.extend(b"=%.1f/%.1f/%.1f\n" % (
            round1(mn),
            round1(mean),
            round1(mx)
        ))

    with open("output.txt", "wb") as f:
        f.write(output)

if __name__ == "__main__":
    main()
