from math import ceil
import os

def round1(x):
    return ceil(x * 10) / 10

def process_line(line):
    sep = line.find(b";")
    if sep == -1:
        return None, None
    city = line[:sep]
    try:
        score = float(line[sep + 1:])
        return city, score
    except ValueError:
        return None, None

def main():
    city_stats = {}
    buffer_size = 8192  # Read in chunks of 8KB

    fd_in = os.open("testcase.txt", os.O_RDONLY)
    while True:
        data = os.read(fd_in, buffer_size)
        if not data:
            break
        lines = data.splitlines()
        for line in lines:
            city, score = process_line(line)
            if city is None or score is None:
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
    for city in sorted(city_stats):
        mn, sm, mx, cnt = city_stats[city]
        mean = sm / cnt
        out += city + b"=" + \
               f"{round1(mn):.1f}/{round1(mean):.1f}/{round1(mx):.1f}\n".encode()

    fd_out = os.open("output.txt", os.O_WRONLY | os.O_CREAT | os.O_TRUNC)
    os.write(fd_out, out)
    os.close(fd_out)

if __name__ == "__main__":
    main()