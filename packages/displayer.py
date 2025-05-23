import curses
from menu import Menu
from alpaca.trading.enums import OrderSide, TimeInForce, OrderType
from exceptions import InvalidOrderData


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


def draw_loading(stdscr, y, x):
    text="Press enter to continue"
    stdscr.addstr(y, x-len(text)//2, text)


def get_market_data_async(widget, widget_setup, result: list):
    while True:
        widget.add_instrument(widget_setup['uuid'])
        widget.reload_instruments()

        whole_patch = widget.get_widget_patch(1000)
        for _ in range(len(result)):
            result.pop()
        for patch in whole_patch:
            result.append(patch)


def draw_market_data(stdscr, y, x, width, result):
    whole_patch = result
    length = 0

    for patch in whole_patch:
        if length + len(patch[0]) > width-6:
            return

        stdscr.addstr(y + 1, x + 1 + length, patch[0])
        length += len(patch[0])
        
        match patch[1]:
            case 1:
                stdscr.attron(curses.color_pair(1))
                stdscr.addstr(y + 1, x + 1 + length, " /\\ ")
                length += 4
                stdscr.attroff(curses.color_pair(1))
            case -1:
                stdscr.attron(curses.color_pair(2))
                stdscr.addstr(y + 1, x + 1 + length, " \\/ ")
                length += 4
                stdscr.attroff(curses.color_pair(2))
            case _:
                stdscr.addstr(y + 1, x + 1 + length, " - ")
                length += 3

        length += 2


def draw_menu(stdscr, y, x, width, menu: Menu):
    for i, part in enumerate(menu.get_component_parts("MENU")):
        draw_block_border(stdscr, y + 1 + 3 * i, x + 1, 3, width - 2)
        if menu.menu_part_selected(part):
            stdscr.attron(curses.color_pair(3))
            stdscr.addstr(y + 2 + 3 * i, x + (width - len(part)) // 2, part)
            stdscr.attroff(curses.color_pair(3))
        else:
            stdscr.addstr(y + 2 + 3 * i, x + (width - len(part)) // 2, part)
            

def draw_action(stdscr, y, x, width, menu: Menu):
    x += 1
    width -= 2
    part_n = menu.get_component_part_buttons_number()
    part_n += part_n % 2
    part_m = part_n // 2
    for i, part_ in enumerate(menu.get_component_parts(menu.get_menu_part_selected())):
        button=part_ + "   " + menu.get_component_part_button(part_)
        

        new_y = int(x + (i // 2) * (width) / part_m + (width / part_m - len(button)) // 2)
        draw_block_border(stdscr, y + 1 + (3 * i) % 6, x + int((i // 2) * width / 3), 3, width // part_m)
        if menu.action_part_selected(part_):
            stdscr.addstr(y + 2 + (3 * i) % 6, new_y, part_)
            stdscr.attron(curses.color_pair(5))
            stdscr.addstr(y + 2 + (3 * i) % 6, new_y + len(part_) + 3, menu.get_component_part_button(part_))
            stdscr.attroff(curses.color_pair(5))
        else:
            stdscr.addstr(y + 2 + (3 * i) % 6, new_y, part_)
            stdscr.attron(curses.color_pair(4))
            stdscr.addstr(y + 2 + (3 * i) % 6, new_y + len(part_) + 3, menu.get_component_part_button(part_))
            stdscr.attroff(curses.color_pair(4))


def process_order_data(order_list: list[str]):
    try:
        order_list[1]=int(order_list[1])

        match order_list[2]:
            # case "BUY":
            #     order_list[2] = OrderSide.BUY
            case "SELL":
                order_list[2] = OrderSide.SELL
            case _:
                order_list[2] = OrderSide.BUY
        
        match order_list[3]:
            # case "MARKET":
            #     order_list[3]=OrderType.MARKET
            case "LIMIT":
                order_list[3]=OrderType.LIMIT
            case "STOP":
                order_list[3]=OrderType.STOP
            case "STOP_LIMIT":
                order_list[3]=OrderType.STOP_LIMIT
            case _:
                order_list[3]=OrderType.MARKET
        
        match order_list[4]:
            # case "DAY":
            #     order_list[4]=TimeInForce.DAY
            case "GTC":
                order_list[4]=TimeInForce.GTC
            case "OPG":
                order_list[4]=TimeInForce.OPG
            case "CLS":
                order_list[4]=TimeInForce.CLS
            case "IOC":
                order_list[4]=TimeInForce.IOC
            case "FOK":
                order_list[4]=TimeInForce.FOK
            case _:
                order_list[4]=TimeInForce.DAY
        

        order_list[5]=float(order_list[5])

    except (ValueError, IndexError):
        return -1
    return 0