from math import ceil

def round_up(x):
    return ceil(x * 10) / 10

def main():
    input_file = "testcase.txt"
    output_file = "output.txt"

    city_stats = {}

    with open(input_file, "r") as f:
        for line in f:
            sep = line.find(";")
            if sep == -1:
                continue
            city = line[:sep]
            try:
                score = float(line[sep + 1:])
            except ValueError:
                continue

            if city in city_stats:
                stats = city_stats[city]
                if score < stats[0]: stats[0] = score     
                stats[1] += score                          
                if score > stats[2]: stats[2] = score     
                stats[3] += 1
            else:
                city_stats[city] = [score, score, score, 1]

    with open(output_file, "w") as f:
        for city in sorted(city_stats):
            mn, sm, mx, cnt = city_stats[city]
            mean = sm / cnt
            f.write(f"{city}={round_up(mn):.1f}/{round_up(mean):.1f}/{round_up(mx):.1f}\n")

if __name__ == "__main__":
    main()
