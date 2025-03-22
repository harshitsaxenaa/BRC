def main():
    import sys

    stats = {}

    with open("input.txt", "rb", buffering=2**20) as f:
        for line in f:
            try:
                sep = line.index(b";")
                city = line[:sep]
                temp = float(line[sep+1:].strip())

                if city in stats:
                    mn, mx, s, c = stats[city]
                    if temp < mn:
                        mn = temp
                    if temp > mx:
                        mx = temp
                    stats[city] = (mn, mx, s + temp, c + 1)
                else:
                    stats[city] = (temp, temp, temp, 1)

            except Exception:
                continue  # skip malformed lines

    with open("output.txt", "w", buffering=2**20) as out:
        for city in sorted(stats):
            mn, mx, s, c = stats[city]
            mean = s / c
            out.write(f"{city.decode()}={mn:.1f}/{mean:.1f}/{mx:.1f}\n")

if __name__ == "__main__":
    main()
