from datetime import datetime

from ivy.ivy import IvyServer


class VisionIvy(IvyServer):
    def __init__(self, where):
        self.savewhere = where
        IvyServer.__init__(self, "VisionIvy")
        self.start(where)
        self.bind_msg(self.cb, '(.*)')

    def cb(self, *args):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print('\033[94m'+"["+current_time +
              "]("+str(args[0])+"): "+'\033[96m', args[1])


if __name__ == "__main__":
    print("Where do you want to connect (default: 127.255.255.255:2010): ")
    where = input()
    if where == "":
        where = '127.255.255.255:2010'
    vi = VisionIvy(where)
    print("Now connected to : ", vi.savewhere)
    print("All messages will be displayed here. You can also send messages.")
    print()
    while(True):
        message = input()
        vi.send_msg(message)
