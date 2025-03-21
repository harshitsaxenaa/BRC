from math import ceil
import os

def round1(x):
    return ceil(x * 10) / 10

def main():
    city_stats = {}
    read = os.read
    write = os.write

    fd_in = os.open("testcase.txt", os.O_RDONLY)
    data = read(fd_in, os.path.getsize("testcase.txt")).splitlines()
    os.close(fd_in)

    get = city_stats.get
    for line in data:
        sep = line.find(b";")
        if sep == -1:
            continue
        city = line[:sep]
        try:
            score = float(line[sep+1:])
        except:
            continue

        stat = get(city)
        if stat:
            if score < stat[0]: stat[0] = score
            stat[1] += score
            if score > stat[2]: stat[2] = score
            stat[3] += 1
        else:
            city_stats[city] = [score, score, score, 1]

    out = bytearray()
    append = out.extend  # faster access

    for city in sorted(city_stats):
        mn, sm, mx, cnt = city_stats[city]
        mean = sm / cnt
        append(city)
        append(b"=")
        append(f"{round1(mn):.1f}".encode())
        append(b"/")
        append(f"{round1(mean):.1f}".encode())
        append(b"/")
        append(f"{round1(mx):.1f}".encode())
        append(b"\n")

    fd_out = os.open("output.txt", os.O_WRONLY | os.O_CREAT | os.O_TRUNC)
    write(fd_out, out)
    os.close(fd_out)

if __name__ == "__main__":
    main()
