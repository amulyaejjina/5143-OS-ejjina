import locale
import sys
import curses
'''
--------------------------------------------------------------
LESS : Used to display page wise content of a file
Usage: less filename
       Up arrow/Down arrow to navigate
--------------------------------------------------------------
'''
def load():
    filename = "history.txt"
    with open(filename) as f:
        return f.readlines(), filename
    return [], ""

def main():
    locale.setlocale(locale.LC_ALL, "")
    lines, filename = load()
    try:
        screen = curses.initscr()
        curses.noecho() # no echo key input
        curses.cbreak() # input with no-enter keyed
        curses.curs_set(0) # hide cursor
        page = Page(screen, lines)
        page.show()
        while page.do_command():
            pass
        pass
    finally:
        curses.curs_set(1)
        curses.nocbreak()
        curses.echo()
        curses.endwin()
        pass
    pass

class Page:
    def __init__(self, screen, lines):
        self.screen = screen
        self.lines = lines
        self.rows = len(lines)
        self.cols = max(len(l) for l in lines)
        self.top = 0
        self.left = 0
        
        # logcal window for line texts
        self.pad = curses.newpad(self.rows + 1, self.cols)
        self.pad.keypad(1) # accept arrow keys
        for i in range(len(lines)):
            self.pad.addstr(i, 0, lines[i])
            pass
        pass
    
    def show(self):
        size = self.screen.getmaxyx() # current screen size
        self.pad.refresh(self.top, self.left, 0, 0, size[0] - 1, size[1] - 2)
        pass
    
    def do_command(self):
        ch = self.pad.getch()
        if ch == ord("q"): return False
        if ch == curses.KEY_UP:
            self.top = max(self.top - 1, 0)
            self.show()
            pass
        if ch == curses.KEY_DOWN:
            size = self.screen.getmaxyx()
            self.top = min(self.top + 1, self.rows - size[0])
            self.show()
            pass
        if ch == curses.KEY_LEFT:
            self.left = max(self.left - 1, 0)
            self.show()
            pass
        if ch == curses.KEY_RIGHT:
            size = self.screen.getmaxyx()
            self.left = min(self.left + 1, self.cols - size[1] + 1)
            self.show()
            pass
        return True
    pass

main()