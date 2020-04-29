from threading import Thread
from xici_spider import XiciProxyQueue


def main():
    p = XiciProxyQueue()
    Thread(target=p.loop_set_list).start()


if __name__ == '__main__':
    main()
