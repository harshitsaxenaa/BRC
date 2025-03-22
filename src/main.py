import os
import mmap
import math
import multiprocessing


def compute_line_block(chunk):
    city_map = {}

    for line in chunk.split(b'\n'):
        if not line:
            continue
        split_at = line.find(b';')
        if split_at == -1:
            continue

        city = line[:split_at]
        try:
            value = float(line[split_at + 1:])
        except:
            continue

        if city not in city_map:
            city_map[city] = [value, value, value, 1]
        else:
            cur = city_map[city]
            cur[0] = min(cur[0], value)  # min
            cur[1] = max(cur[1], value)  # max
            cur[2] += value              # sum
            cur[3] += 1                  # count

    return city_map


def process_chunk(file_path, begin, end):
    with open(file_path, 'rb') as f:
        mm = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
        size = len(mm)

        if begin != 0:
            while begin < size and mm[begin] != ord('\n'):
                begin += 1
            begin += 1

        if end < size:
            while end < size and mm[end] != ord('\n'):
                end += 1
            end += 1

        chunk = mm[begin:end]
        mm.close()

    return compute_line_block(chunk)


def combine_maps(maps):
    final_map = {}
    for part in maps:
        for city, stat in part.items():
            if city not in final_map:
                final_map[city] = stat[:]
            else:
                existing = final_map[city]
                existing[0] = min(existing[0], stat[0])
                existing[1] = max(existing[1], stat[1])
                existing[2] += stat[2]
                existing[3] += stat[3]
    return final_map


def round1(x):
    return math.ceil(x * 10) / 10


def process_file(input_file="testcase.txt", output_file="output.txt"):
    with open(input_file, "rb") as f:
        mm = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
        size = len(mm)
        mm.close()

    num_chunks = multiprocessing.cpu_count() * 2
    step = size // num_chunks
    segments = []

    for i in range(num_chunks):
        start = i * step
        end = (i + 1) * step if i != num_chunks - 1 else size
        segments.append((input_file, start, end))

    with multiprocessing.Pool(num_chunks) as pool:
        maps = pool.starmap(process_chunk, segments)

    final_result = combine_maps(maps)

    with open(output_file, "wb") as f:
        for city in sorted(final_result.keys(), key=lambda x: x.decode()):
            mn, mx, sm, ct = final_result[city]
            mean = sm / ct
            f.write(f"{city.decode()}={round1(mn):.1f}/{round1(mean):.1f}/{round1(mx):.1f}\n".encode())


if __name__ == "__main__":
    process_file()
