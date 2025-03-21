from collections import defaultdict
from math import ceil

def round_up(val):
    return ceil(val * 10) / 10

def main():
    city_scores = defaultdict(list)

    with open("testcase.txt", "r") as infile:
        for line in infile:
            if ";" not in line:
                continue
            parts = line.split(";")
            if len(parts) != 2:
                continue
            city, score = parts
            try:
                city_scores[city].append(float(score))
            except ValueError:
                continue  # Skip lines with invalid scores

    result = [
        f"{city}={round_up(min(scores)):.1f}/{round_up(sum(scores)/len(scores)):.1f}/{round_up(max(scores)):.1f}"
        for city, scores in sorted(city_scores.items())
    ]

    with open("output.txt", "w") as outfile:
        outfile.write("\n".join(result) + "\n")

if __name__ == "__main__":
    main()
