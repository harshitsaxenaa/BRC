from math import ceil
import os, mmap

def round1(x):
    return ceil(x * 10) / 10

def main():
    input_path = "testcase.txt"
    output_path = "output.txt"

    with open(input_path, "rb") as f:
        mm = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
        lines = mm.read().split(b"\n")

    city_stats = {}

    for line in lines:
        sep = line.find(b";")
        if sep == -1:
            continue
        city = line[:sep]
        try:
            score = float(line[sep+1:])
        except:
            continue

        if city in city_stats:
            stat = city_stats[city]
            if score < stat[0]: stat[0] = score
            stat[1] += score
            if score > stat[2]: stat[2] = score
            stat[3] += 1
        else:
            city_stats[city] = [score, score, score, 1]

    out = bytearray()
    join = b"=".join
    for city in sorted(city_stats):
        mn, sm, mx, cnt = city_stats[city]
        mean = sm / cnt
        out += city + b"=" + \
               f"{round1(mn):.1f}/{round1(mean):.1f}/{round1(mx):.1f}\n".encode()

    with open(output_path, "wb") as f:
        f.write(out)

if __name__ == "__main__":
    main()
