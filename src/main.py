import mmap
from collections import defaultdict
from math import ceil

def round1(x):
    return ceil(x * 10) / 10

def parse_score(score_bytes):
    val = 0
    i = 0
    while i < len(score_bytes) and score_bytes[i] != 46:  # ord('.') == 46
        val = val * 10 + (score_bytes[i] - 48)
        i += 1
    i += 1  # skip '.'
    if i < len(score_bytes):
        val = val * 10 + (score_bytes[i] - 48)
    else:
        val *= 10
    return val

def main():
    stats = defaultdict(lambda: [1000000, 0, -1, 0])  # min, sum, max, count

    with open("testcase.txt", "rb") as f:
        mm = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
        readline = mm.readline

        while True:
            line = readline()
            if not line:
                break
            sep = line.find(b";")
            if sep == -1:
                continue
            city = line[:sep]
            score_bytes = line[sep+1:].strip()
            try:
                score = parse_score(score_bytes)
            except:
                continue
            s = stats[city]
            if score < s[0]: s[0] = score
            s[1] += score
            if score > s[2]: s[2] = score
            s[3] += 1

    output = bytearray()
    for city in sorted(stats):
        mn, sm, mx, cnt = stats[city]
        mean = (sm + cnt // 2) // cnt  # rounded
        output.extend(city)
        output.extend(b"=%.1f/%.1f/%.1f\n" % (
            round1(mn / 10),
            round1(mean / 10),
            round1(mx / 10)
        ))

    with open("output.txt", "wb") as f:
        f.write(output)

if __name__ == "__main__":
    main()
