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
from rich.live import Live
import time


def make_layout() -> Layout:
    """Define the layout."""
    layout = Layout(name="root")

    layout.split(
        Layout(name="header", size=3),
        Layout(name="main", ratio=1)
    
    )
    layout["main"].split_column(
        Layout(name="side"),
        Layout(name="body"),
    )
    return layout

class Header:
    """Display header with clock."""

    def __rich__(self) -> Panel:
        grid = Table.grid(expand=True)
        grid.add_column(justify="center", ratio=1)
        grid.add_column(justify="right")
        grid.add_row(
            "[b]CPU Scheduling Simulation[/b]",
            datetime.now().ctime().replace(":", "[blink]:[/]")
        )
        return Panel(grid)

layout = make_layout()
layout["header"].update(Header())
table = Table(title="[b]COMPARISONS,1 CPU...[b]")
table.add_column("ALGORITHM", justify="center", no_wrap=True)
table.add_column("  CPU WAIT TIME  ", justify="center",  no_wrap=True)
table.add_column("  IO WAIT TIME  ", justify="center", no_wrap=True)
table.add_column("   TAT         ", justify="center",  no_wrap=True)
table.add_row("FCFS ",str(2934),str(1977),str(5041)+'\n')
table.add_row("RR ,Quantum - 3 ",str(4647),str(1178),str(5966)+'\n')
table.add_row("RR ,Quantum - 7 ",str(1960),str(3504),str(5598)+'\n')
table.add_row("SJF ",str(2499),str(269),str(2899)+'\n')
table.add_row("SRF ",str(2523),str(217),str(2862)+'\n')
table.add_row("PP ",str(2868),str(461),str(3461)+'\n')
layout["side"].update(table)


table = Table(title="[b]MULTI PROCESSING,2 CPUS...[b]")
table.add_column("ALGORITHM", justify="center", no_wrap=True)
table.add_column("  CPU WAIT TIME  ", justify="center",  no_wrap=True)
table.add_column("  IO WAIT TIME  ", justify="center", no_wrap=True)
table.add_column("   TAT         ", justify="center",  no_wrap=True)
table.add_row("FCFS ",str(428),str(4277),str(4835)+'\n')
table.add_row("RR ,Quantum : 3 ",str(864),str(3683),str(4689)+'\n')
table.add_row("RR ,Quantum : 7 ",str(628),str(4035),str(4798)+'\n')
table.add_row("SJF ",str(411),str(3719),str(4259)+'\n')
table.add_row("SRF ",str(413),str(3752),str(4295)+'\n')
table.add_row("PP ",str(472),str(3989),str(4593)+'\n')
layout["body"].update(table)

with Live(layout, refresh_per_second=10, screen=True):
    try:
        while True:
            time.sleep(0)
    except KeyboardInterrupt:
            pass
                                
