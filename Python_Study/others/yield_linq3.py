

def make_numbers(num):
    n = 1
    while True:
        if n > num:
            break
        yield n
        n += 1


def add_one(stream):
    while True:
        num = next(stream)
        yield num + 1


def add_two(stream):
    while True:
        num = next(stream)
        if num > 8:     # 终止这个链
            break
        yield num + 2.5


def run():
    stream = make_numbers(10)
    stream = add_one(stream)
    stream = add_two(stream)
    for i in stream:
        print(i)


if __name__ == '__main__':
    run()
