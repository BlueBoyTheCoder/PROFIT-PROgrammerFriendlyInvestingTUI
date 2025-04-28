def draw_button(stdscr, y, x, text):
    stdscr.addstr(y, x, text)


def draw_multiple_buttons(stdscr, y, x, height, width, button_number, n, text):
    """
    multiple_button format:
    n x m >
    \/
    ┌────────────┐┌────────────┐
    │  button 1  ││  button 3  │
    └────────────┘└────────────┘
    ┌────────────┐┌────────────┐
    │  button 2  ││  button 4  │
    └────────────┘└────────────┘
    """
    m=button_number//n+1
    stdscr.addstr(y, x, text)


def draw_block_border(stdscr, y, x, height, width, name=None):
    border_up = "┌" + "─" * (width - 2) + "┐"
    border_side = "│"
    border_down = "└" + "─" * (width - 2) + "┘"

    stdscr.addstr(y, x, border_up)

    for i in range(1, height - 1):
        stdscr.addstr(y + i, x, border_side)
        stdscr.addstr(y + i, x + width - 1, border_side)

    stdscr.addstr(y + height - 1, x, border_down)

    if name:
        stdscr.addstr(y, x + (width - len(name)) // 2, name)