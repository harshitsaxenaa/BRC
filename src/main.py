from math import ceil

def round1(x):
    return ceil(x * 10) / 10

def main():
    import os

    city_stats = {}
    read = os.read
    write = os.write
    fd_in = os.open("testcase.txt", os.O_RDONLY)
    data = read(fd_in, os.path.getsize("testcase.txt")).splitlines()
    os.close(fd_in)

    for line in data:
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
    for city in sorted(city_stats):
        mn, sm, mx, cnt = city_stats[city]
        mean = sm / cnt
        out += city + b"=" + \
               f"{round1(mn):.1f}/{round1(mean):.1f}/{round1(mx):.1f}\n".encode()

    fd_out = os.open("output.txt", os.O_WRONLY | os.O_CREAT | os.O_TRUNC)
    write(fd_out, out)
    os.close(fd_out)

if __name__ == "__main__":
    main()
