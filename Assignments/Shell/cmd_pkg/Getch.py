'''
--------------------------------------------------------------
GETCH : This is used to fetch charachters from terminal 
        as they are being entered
--------------------------------------------------------------
'''
class Getch:                             # Getch class to fetch input (char wise) from user as they are bring entered
    def __init__(self):
        try:
            self.impl = _GetchUnix()
        except ImportError:
            print("Error...")

    def __call__(self):
        return self.impl()


class _GetchUnix:
    def __init__(self):
        import tty
        import sys

    def __call__(self):
        import sys
        import tty
        import termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch