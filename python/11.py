#!/usr/bin/python3


def calculate_power_level(x, y, serial_number):
    rack_id = x + 10
    power_level = rack_id * y
    power_level += serial_number
    power_level *= rack_id
    s = str(power_level)
    power_level = 0 if len(s) < 3 else int(s[-3])
    power_level -= 5
    return power_level


def range_sum(row_or_col, start, length):
    return sum(row_or_col[start:start+length])


def square_sum(rows, x, y, size):
    ssum = 0
    for i in range(y, y+size):
        ssum += range_sum(rows[i], x, size)
    return ssum


def best_area(grid_serial_number, square_sizes):
    rows = []
    for y in range(300):
        rows.append([calculate_power_level(x+1, y+1, grid_serial_number) for x in range(300)])
    cols = []
    for x in range(300):
        cols.append([row[x] for row in rows])

    best_x, best_y, best_size, best_power = 0, 0, 0, None

    for size in square_sizes:
        x = 0
        max_coord = 300 - size
        power = square_sum(rows, 0, 0, size)
        if best_power is None:
            best_power = power
        for y in range(max_coord+1):
            if y != 0:
                power -= range_sum(rows[y-1], x, size)
                power += range_sum(rows[y-1+size], x, size)
            if x == 0:
                while True:
                    if x != 0:
                        power -= range_sum(cols[x-1], y, size)
                        power += range_sum(cols[x-1+size], y, size)
                    if power > best_power:
                        best_power, best_x, best_y, best_size = power, x, y, size
                    if x == max_coord:
                        break
                    x += 1
            else:
                while True:
                    if x != max_coord:
                        power -= range_sum(cols[x+size], y, size)
                        power += range_sum(cols[x], y, size)
                    if power > best_power:
                        best_power, best_x, best_y, best_size = power, x, y, size
                    if x == 0:
                        break
                    x -= 1

    return (best_x+1, best_y+1, best_power, best_size)


def main():
    x = best_area(1723, [3])
    print(x[0], x[1], sep=',')

    x = best_area(1723, range(1, 301))
    print(x[0], x[1], x[3], sep=',')


if __name__ == "__main__":
    main()
