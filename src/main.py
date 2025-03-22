import os
import mmap
from math import ceil

def round1(x):
    return ceil(x * 10) / 10

def main():
    city_stats = {}
    stat_get = city_stats.get

    with open("testcase.txt", "rb") as f:
        mmapped = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
        lines = bytes(mmapped).split(b"\n")  

    for line in lines:
        sep = line.find(b";")
        if sep == -1:
            continue
        city = line[:sep]
        try:
            score = float(line[sep + 1:])
        except:
            continue

        stat = stat_get(city)
        if stat:
            if score < stat[0]: stat[0] = score
            stat[1] += score
            if score > stat[2]: stat[2] = score
            stat[3] += 1
        else:
            city_stats[city] = [score, score, score, 1]

    result = []
    for city in sorted(city_stats):
        mn, sm, mx, cnt = city_stats[city]
        mean = sm / cnt
        result.append(
            b"%s=%.1f/%.1f/%.1f\n" % (
                city,
                round1(mn),
                round1(mean),
                round1(mx)
            )
        )

    with open("output.txt", "wb") as f:
        f.write(b"".join(result))

if __name__ == "__main__":
    main()
