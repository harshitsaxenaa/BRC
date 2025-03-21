from math import ceil
from collections import defaultdict

def round1(x):
    return ceil(x * 10) / 10

def main():
    import os

    read = os.read
    write = os.write
    path_in = "testcase.txt"
    path_out = "output.txt"
    size = os.path.getsize(path_in)

    
    stats = defaultdict(lambda: [float('inf'), 0.0, float('-inf'), 0])

    fd_in = os.open(path_in, os.O_RDONLY)
    raw = read(fd_in, size)
    os.close(fd_in)

    lines = raw.split(b"\n")

    for line in lines:
        if not line:
            continue
        sep = line.find(b";")
        if sep == -1:
            continue
        city = line[:sep]
        try:
            score = float(line[sep + 1:])
        except:
            continue
        stat = stats[city]
        if score < stat[0]: stat[0] = score
        stat[1] += score
        if score > stat[2]: stat[2] = score
        stat[3] += 1

  
    output = bytearray()
    for city in sorted(stats):
        mn, sm, mx, cnt = stats[city]
        mean = sm / cnt
        output += city + b"=" + \
            f"{round1(mn):.1f}/{round1(mean):.1f}/{round1(mx):.1f}\n".encode()

    fd_out = os.open(path_out, os.O_WRONLY | os.O_CREAT | os.O_TRUNC)
    write(fd_out, output)
    os.close(fd_out)

if __name__ == "__main__":
    main()
