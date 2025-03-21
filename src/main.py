import math

def round_up(value):
    return math.ceil(value * 10) / 10

def main():
    input_file = "testcase.txt"
    output_file = "output.txt"

    city_data = {}

    with open(input_file, "r") as f:
        for line in f:
            if ";" not in line:
                continue
            parts = line.rstrip().split(";")
            if len(parts) != 2:
                continue
            city, score_str = parts
            try:
                score = float(score_str)
            except ValueError:
                continue
            city_data.setdefault(city, []).append(score)

    result = [
        f"{city}="
        f"{round_up(min(scores)):.1f}/"
        f"{round_up(sum(scores)/len(scores)):.1f}/"
        f"{round_up(max(scores)):.1f}"
        for city, scores in sorted(city_data.items())
    ]

    with open(output_file, "w") as f:
        f.write("\n".join(result) + "\n")

if __name__ == "__main__":
    main()
