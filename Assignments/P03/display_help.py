from rich.console import Console
from rich.table import Table
import json
from rich.layout import Layout
from rich import box
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
from rich.syntax import Syntax
from rich.table import Table
from rich.table import Table
from rich.text import Text
from rich.align import Align
from rich.console import Console, Group
from datetime import datetime
import random
from time import sleep
from rich.live import Live
from rmain import *
from termcolor import colored
from rich import *

class Header:
    """Display header with clock."""

    def __rich__(self) -> Panel:
        grid = Table.grid(expand=True)
        grid.add_column(justify="center", ratio=1)
        grid.add_column(justify="right")
        grid.add_row(
            "[b]READER WRITER PART 1[/b]",
            datetime.now().ctime().replace(":", "[blink]:[/]")
        )
        return Panel(grid)
def make_layout() -> Layout:
    """Define the layout."""
    layout = Layout(name="root")

    layout.split(
        Layout(name="header", ratio=1),
        Layout(name="main",ratio=8),
    )
    layout["main"].split_row(
        Layout(name="side"),
        Layout(name="body"),
    )
    return layout



# with open("memory.json") as f:
#     data = json.load(f)

# layout = make_layout()
# layout["header"].update(Header())
# layout["side"].update(Panel(loaddata_to_table(data," BEFORE"), border_style="#00FF00"))
# layout["body"].update(Panel(loaddata_to_table(data," AFTER"), border_style="#00FF00"))

# with Live(layout, screen=True, redirect_stderr=False) as live:
#     try:
#         while True:
#             sleep(0)
#     except KeyboardInterrupt:
#         pass
