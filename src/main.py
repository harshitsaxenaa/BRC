import math

def round_up(value):
    
    return math.ceil(value * 10) / 10

def main():
    input_file = "testcase.txt"
    output_file = "output.txt"
    
    city_data = {}

    with open(input_file, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                city, score = line.split(";")
                score = float(score)
                if city not in city_data:
                    city_data[city] = []
                city_data[city].append(score)
            except ValueError:
                continue  

    result_lines = []
    for city in sorted(city_data.keys()):
        values = city_data[city]
        min_val = round_up(min(values))
        mean_val = round_up(sum(values) / len(values))
        max_val = round_up(max(values))
        result_lines.append(f"{city}={min_val:.1f}/{mean_val:.1f}/{max_val:.1f}")

    with open(output_file, "w") as f:
        for line in result_lines:
            f.write(line + "\n")

if __name__ == "__main__":
    main()
