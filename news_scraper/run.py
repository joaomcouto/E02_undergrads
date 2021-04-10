import sys


def run(argv):
    interface = False

    if argv[0] == '-i':
        interface = True
        url = argv[1]
    else:
        url = argv[0]


if __name__ == "__main__":
    run(sys.argv[1:])
