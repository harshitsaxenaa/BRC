from math import ceil
import mmap
import multiprocessing
from collections import defaultdict

def round1(x):
    return ceil(x * 10) / 10

def initialize_stats():
    return [float("inf"), 0.0, float("-inf"), 0]

def split_file(filename, num_chunks):
    with open(filename, "rb") as f:
        mmapped = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
        file_size = mmapped.size()
        chunk_size = file_size // num_chunks
        offsets = [0]
        for i in range(1, num_chunks):
            mmapped.seek(i * chunk_size)
            mmapped.readline() 
            offsets.append(mmapped.tell())
        offsets.append(file_size)
    return offsets

def process_chunking(start, end, filename):
    city_stats = defaultdict(initialize_stats)
    with open(filename, "rb") as f:
        mmapped = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
        mmapped.seek(start)

        while mmapped.tell() < end:
            line = mmapped.readline()
            if not line:
                break
            sep = line.find(b";")
            if sep == -1:
                continue
            city = line[:sep]
            try:
                score = float(line[sep + 1:])
            except ValueError:
                continue
            stats = city_stats[city]
            stats[0] = min(stats[0], score)  
            stats[1] += score               
            stats[2] = max(stats[2], score) 
            stats[3] += 1                   
    return city_stats

def merging_of_stats(global_stats, partial_stats):
    for city, stats in partial_stats.items():
        if city in global_stats:
            agg = global_stats[city]
            agg[0] = min(agg[0], stats[0])  
            agg[1] += stats[1]              
            agg[2] = max(agg[2], stats[2])  
            agg[3] += stats[3]              
        else:
            global_stats[city] = stats



def write_results_to_file(global_stats, output_file):
    with open(output_file, "w") as f:
        for city, (mn, sm, mx, cnt) in sorted(global_stats.items()):
            mean = sm / cnt
            f.write(f"{city.decode('ascii')}={round1(mn):.1f}/{round1(mean):.1f}/{round1(mx):.1f}\n")

def main():
    input_filename = "testcase.txt"
    output_filename = "output.txt"
    num_processes = multiprocessing.cpu_count()
    offsets = split_file(input_filename, num_processes)

    with multiprocessing.Pool(num_processes) as pool:
        chunk_results = pool.starmap(
            process_chunking,
            [(offsets[i], offsets[i + 1], input_filename) for i in range(len(offsets) - 1)]
        )

    global_stats = defaultdict(initialize_stats)
    for partial_stats in chunk_results:
        merging_of_stats(global_stats, partial_stats)

    write_results_to_file(global_stats, output_filename)

if __name__ == "__main__":
    main()