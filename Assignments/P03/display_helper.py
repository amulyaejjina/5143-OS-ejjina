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

prev1 = None
prev2=None
prev3=None
prev4 = None
prev5 = None
prev6 = None

def make_layout() -> Layout:
    """Define the layout."""
    layout = Layout(name="root")

    layout.split(
        Layout(name="header", size=3),
        Layout(name="main", ratio=1),
        Layout(name="footer1", size=6),
    )
    layout["main"].split_row(
        Layout(name="side"),
        Layout(name="body",ratio=2, minimum_size=60),
    )
    # layout["footer"].split_row(
        
    #     Layout(name="footer2")
    # )
    layout["side"].split(Layout(name="CPUs"), Layout(name="IOs"),Layout(name="footer2"))
    return layout


def make_sponsor_message() -> Panel:
    """Some example content."""
    sponsor_message = Table.grid(padding=0)
    sponsor_message.add_column(style="green", justify="left")
    sponsor_message.add_column(no_wrap=True)

    intro_message = Text.from_markup(
        """Process Data - """
    )

    message = Table.grid(padding=1)
    message.add_column()
    message.add_column(no_wrap=True)
    message.add_row(intro_message, sponsor_message)

    message_panel = Panel(
        Align.left(
            Group(intro_message, "\n", Align.center(sponsor_message)),
            vertical="middle",
        ),
        box=box.ROUNDED,
        padding=(1, 2),
        title="[b red]Process information as they terminate...",
        border_style="bright_blue",
    )
    return message_panel


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

def cpuFunction(no,running_process1,cpunum,state) -> Syntax:
    table = Table(title="[b]CPU DEVICES[b]")
    global prev1
    global prev2
    global prev3
    for item in range(no):
        table.add_column(f"CPU : {item+1}", justify="center", style="cyan", no_wrap=True)
    # if running_process1 is not None:
    #     table.add_row(running_process1.pid,"-2")
    if no == 1:
        if state == "enter":
            if running_process1 is not None:
                    table.add_row("Process "+running_process1.pid+ " entered")
        if state == "left":
            if running_process1 is not None:
                    table.add_row("Process "+running_process1.pid+ " left")
    elif no == 2:
        if cpunum == 1 :
            if state == "enter":
                if running_process1 is not None:
                    prev1 = running_process1.pid
                    if prev2 is None:
                        table.add_row("Process "+running_process1.pid+ " entered","None")
                    else:
                        table.add_row("Process "+running_process1.pid+ " entered","Process "+prev2+" entered")
            if state == "left":
                if running_process1 is not None:
                    prev1 = running_process1.pid
                    if prev2 is None:
                        table.add_row("Process "+running_process1.pid+ " left","None")
                    else:
                        table.add_row("Process "+running_process1.pid+ " left","Process "+prev2+" left")
        elif cpunum == 2 :
            if state == "enter":
                if running_process1 is not None:
                    prev2 = running_process1.pid
                    if prev1 is None:
                        table.add_row("None","Process "+running_process1.pid+" entered") 
                    else:
                        table.add_row("Process "+prev1+" entered","Process "+running_process1.pid+" entered") 
            if state == "left":
                if running_process1 is not None:
                    prev2 = running_process1.pid
                    if prev1 is None:
                        table.add_row("None","Process "+running_process1.pid+" left") 
                    else:
                        table.add_row("Process "+prev1+" left","Process "+running_process1.pid+" left") 
    elif no == 3:
        if cpunum == 1 :
            if state == "enter":
                if running_process1 is not None:
                    prev1 = running_process1.pid
                    if prev2 is None and prev3 is None:
                        table.add_row(running_process1.pid+ " entered","None","None")
                    elif (prev2 is not None) and (prev3 is None):
                        table.add_row(running_process1.pid+ " entered",prev2+" entered","None")
                    else:
                        table.add_row(running_process1.pid+ " entered","None",prev3+" entered")
                    # else:
                    #     table.add_row(running_process1.pid+ " entered","None",prev3+" entered")
            if state == "left":
                if running_process1 is not None:
                    prev1 = running_process1.pid
                    if prev2 is None and prev3 is None:
                        table.add_row(running_process1.pid+ " left","None","None")
                    elif (prev2 is not None) and (prev3 is None):
                        table.add_row(running_process1.pid+ " left",prev2+" left","None")
                    else:
                        table.add_row(running_process1.pid+ " left","None",prev3+" left")
        elif cpunum == 2 :
            if state == "enter":
                if running_process1 is not None:
                    prev2 = running_process1.pid
                    if prev1 is None and prev3 is None:
                        table.add_row("None",running_process1.pid+" entered","None") 
                    elif (prev1 is not None) and (prev3 is None):
                        table.add_row(prev1+" entered",running_process1.pid+" entered","None") 
                    else:
                        table.add_row("None",running_process1.pid+" entered",prev3+"entered") 
            if state == "left":
                if running_process1 is not None:
                    prev2 = running_process1.pid
                    if prev1 is None and prev3 is None:
                        table.add_row("None",running_process1.pid+" left","None") 
                    elif (prev1 is not None) and (prev3 is None):
                        table.add_row(prev1+" left",running_process1.pid+" left","None") 
                    elif (prev1 is not None) and (prev3 is not None):
                        table.add_row(prev1+"left",running_process1.pid+" left",prev3+"left") 
        elif cpunum == 3 :
            if state == "enter":
                if running_process1 is not None:
                    prev3 = running_process1.pid
                    if prev1 is None and prev2 is None:
                        table.add_row("None","None",running_process1.pid+" entered") 
                    elif (prev1 is not None) and (prev2 is None):
                        table.add_row(prev1+" entered",running_process1.pid+" entered","None") 
                    else:
                        table.add_row("None",prev2+"entered",running_process1.pid+" entered") 
            if state == "left":
                if running_process1 is not None:
                    prev3 = running_process1.pid
                    if prev1 is None and prev2 is None:
                        table.add_row("None","None",running_process1.pid+" left") 
                    elif (prev1 is not None) and (prev2 is None):
                        table.add_row(prev1+" left",running_process1.pid+" left","None") 
                    elif prev1 is not None and prev2 is not None:
                        table.add_row(prev1+"left",prev2+"left",running_process1.pid+" left") 

    return table


def ioFunction(no,running_process1,cpunum,state) -> Syntax:
    table2 = Table(title="[b]IO DEVICES[b]")
    global prev4
    global prev5
    global prev6
    for item in range(no):
        table2.add_column(f"IO : {item+1}", justify="center", style="cyan", no_wrap=True)

    if no == 1:
        if state == "enter":
            if running_process1 is not None:
                    table2.add_row("Process "+running_process1.pid+ " entered")
        if state == "left":
            if running_process1 is not None:
                    table2.add_row("Process "+running_process1.pid+ " left")
    elif no == 2:
        if cpunum == 1 :
            if state == "enter":
                if running_process1 is not None:
                    prev4 = running_process1.pid
                    if prev5 is None:
                        table2.add_row("Process "+running_process1.pid+ " entered","None")
                    else:
                        table2.add_row("Process "+running_process1.pid+ " entered","Process "+prev5+" entered")
            if state == "left":
                if running_process1 is not None:
                    prev4 = running_process1.pid
                    if prev5 is None:
                        table2.add_row("Process "+running_process1.pid+ " left","None")
                    else:
                        table2.add_row("Process "+running_process1.pid+ " left","Process "+prev5+" left")
        elif cpunum == 2 :
            if state == "enter":
                if running_process1 is not None:
                    prev5 = running_process1.pid
                    if prev4 is None:
                        table2.add_row("None","Process "+running_process1.pid+" entered") 
                    else:
                        table2.add_row("Process "+prev4+" entered","Process "+running_process1.pid+" entered") 
            if state == "left":
                if running_process1 is not None:
                    prev5 = running_process1.pid
                    if prev4 is None:
                        table2.add_row("None","Process "+running_process1.pid+" left") 
                    else:
                        table2.add_row("Process "+prev4+" left","Process "+running_process1.pid+" left") 
    elif no == 3:
        if cpunum == 1 :
            if state == "enter":
                if running_process1 is not None:
                    prev4 = running_process1.pid
                    if prev5 is None and prev6 is None:
                        table2.add_row(running_process1.pid+ " entered","None","None")
                    elif prev5 is not None and prev6 is None:
                        table2.add_row(running_process1.pid+ " entered",prev5+" entered","None")
                    else:
                        table2.add_row(running_process1.pid+ " entered","None",prev6+" entered")
                    # else:
                    #     table.add_row(running_process1.pid+ " entered","None",prev3+" entered")
            if state == "left":
                if running_process1 is not None:
                    prev4 = running_process1.pid
                    if prev5 is None and prev6 is None:
                        table2.add_row(running_process1.pid+ " left","None","None")
                    elif prev5 is not None and prev6 is None:
                        table2.add_row(running_process1.pid+ " left",prev5+" left","None")
                    else:
                        table2.add_row(running_process1.pid+ " left","None",prev6+" left")
        elif cpunum == 2 :
            if state == "enter":
                if running_process1 is not None:
                    prev5 = running_process1.pid
                    if prev4 is None and prev6 is None:
                        table2.add_row("None",running_process1.pid+" entered","None") 
                    elif prev4 is not None and prev6 is None:
                        table2.add_row(prev4+" entered",running_process1.pid+" entered","None") 
                    else:
                        table2.add_row("None",running_process1.pid+" entered",prev6+"entered") 
            if state == "left":
                if running_process1 is not None:
                    prev5 = running_process1.pid
                    if prev4 is None and prev6 is None:
                        table2.add_row("None",running_process1.pid+" left","None") 
                    elif prev4 is not None and prev6 is None:
                        table2.add_row(prev1+" left",running_process1.pid+" left","None") 
                    elif prev4 is not None and prev6 is not None:
                        table2.add_row(prev1+"left",running_process1.pid+" left",prev6+"left") 
        elif cpunum == 3 :
            if state == "enter":
                if running_process1 is not None:
                    prev6 = running_process1.pid
                    if prev4 is None and prev5 is None:
                        table2.add_row("None","None",running_process1.pid+" entered") 
                    elif prev4 is not None and prev2 is None:
                        table2.add_row(prev4+" entered",running_process1.pid+" entered","None") 
                    else:
                        table2.add_row("None",prev5+"entered",running_process1.pid+" entered") 
            if state == "left":
                if running_process1 is not None:
                    prev6 = running_process1.pid
                    if prev4 is None and prev2 is None:
                        table2.add_row("None","None",running_process1.pid+" left") 
                    elif prev4 is not None and prev5 is None:
                        table2.add_row(prev1+" left",running_process1.pid+" left","None") 
                    elif prev4 is not None and prev5 is not None:
                        table2.add_row(prev4+"left",prev5+"left",running_process1.pid+" left") 

    return table2

def proc(no,eachline) -> Syntax:
    table = Table(title="[b]Processes...[b]")
    for item in range(no):
        table.add_column(f"IO {item}", justify="center", style="cyan", no_wrap=True)
    for item in range(10):
        table.add_row("....")
    return table

class Buffer:
    def __init__(self,**kwargs):
        self.advance = kwargs.get("advance", 0)
        self.currentsize = kwargs.get("currentsize",0)
        self.name = kwargs.get("name", "")
        self.size = 6
        self.bar = ""

    def generate_buffer(self):
        self.bar =  self.name + ""
        adjust = self.advance
        for i in range(self.size+adjust):
            self.bar += ' '
        
    def __rich__(self) -> Panel:
        self.generate_buffer()
        return f'[green on #00FF00]{self.bar}'

class Buffer3:
    def __init__(self,**kwargs):
        self.min = min
        self.max = max
        self.size = 12
        self.bar2 =  ""
        self.name = kwargs.get("name", "")
        self.advance = kwargs.get("advance", 0)

    def generate_buffer(self):
        self.bar2 = self.name+""
        adjust = random.randint(-4,4)
        if self.advance == -3:
            for i in range(0):
                self.bar2 += ' '
        else:
            for i in range(self.size+adjust):
                self.bar2 += ' '    
    def __rich__(self) -> Panel:
        self.generate_buffer()
        if self.advance == -3:
            return f'[#00FF00]{self.bar2}'
        else:
            return f'[green on #00FF00]{self.bar2}'

# job_progress = Progress(
#     "{task.description}",
#     SpinnerColumn(),
#     BarColumn(),
#     TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
# )
# newtask = job_progress.add_task("[green]NEW")
# readytask = job_progress.add_task("[magenta]READY")
# runningtask = job_progress.add_task("[green]RUNNING")
# waitingtask = job_progress.add_task("[magenta]WAITING")
# iotask = job_progress.add_task("[green]IO")
# terminatetask = job_progress.add_task("[magenta]TERMINATE")




overalltask = Progress(
    "{task.description}",
    SpinnerColumn(),
    BarColumn(bar_width=110,style="black"),
    TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
)
task_id = overalltask.add_task("[#00FF00]All PROCESSES")

progress_table = Table.grid(expand=True)
progress_table.add_row(
    Panel(
        overalltask,
        title="[b]OVERALL PROGRESS[b]",
        border_style="black",
        
    )
    # Panel(
    #     job_progress,
    #     #job_progress2, 
    #     title="[b]QUEUE BUFFER[b]",
    #     border_style="green", 
    #     padding=(1, 2)),
)

def meth(adv1,adv2,adv3):
    job_progress = Buffer3(advance = adv1 ,name="NEW")
    job_progress2 = Buffer3(advance = adv2,name="READY")
    job_progress3 = Buffer3(advance = adv3,name="WAITING")
    progress_table2 = Table.grid(expand=True)
    progress_table2.add_row(Panel(job_progress,border_style="black"))
    progress_table2.add_row(Panel(job_progress2,border_style="black"))
    progress_table2.add_row(Panel(job_progress3,border_style="black"))
    return progress_table2
    # Panel(
    #     job_progress,
    #     #job_progress2, 
    #     title="[b]QUEUE BUFFER[b]",
    #     border_style="green", 
    #     padding=(1, 2)),

# def tablen(table):
#     # table = Table()
#     table.add_column("Process")
#     table.add_column("CPU WaitTime")
#     table.add_column("IO WaitTime")

# def pan(no_of_ios,no_of_cpus,table2):
#     global dummy
#     dummy = ""
#     layout = make_layout()
#     layout["header"].update(Header())
#     layout["body"].update(dummy)
#     layout["IOs"].update(Panel(io(no_of_ios), border_style="green"))
#     layout["CPUs"].update(Panel(cpu(no_of_cpus), border_style="red"))
#     layout["footer"].update(progress_table)
#     with Live(layout, refresh_per_second=10, screen=True):
#         while not overall_progress.finished:
#             sleep(0.1)
#             for job in job_progress.tasks:
#                 if not job.finished:
#                     job_progress.advance(job.id)

#             completed = sum(task.completed for task in job_progress.tasks)
#             overall_progress.update(overall_task, completed=completed)