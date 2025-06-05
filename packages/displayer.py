import curses
from menu import Menu
from alpaca.trading.enums import OrderSide, TimeInForce, OrderType
from time import sleep, ctime
from chartdisplay import ChartDisplay
from cursescolors import CursesColors


def draw_block_border(stdscr, y, x, height, width, name=None):
    """
    Displays frame-looking like shape
    """
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
    text = "Press enter to continue"
    stdscr.addstr(y, x - len(text) // 2, text)


def draw_order_confirmation(stdscr, window_height, window_width, order_result=True):
    """
    Displays information about result of order
    """
    if order_result:
        text = "ORDER SUBMITTED"
        width = len(text) + 4
    else:
        text = "ORDER NOT SUBMITTED"
        width = len(text) + 4
    height = 5
    x = (window_width - width) // 2
    y = (window_height - height) // 2
    draw_block_border(stdscr, y, x, height, width)
    stdscr.attron(curses.color_pair(CursesColors.MARKED))
    stdscr.addstr(y + 2, x + 2, text)
    stdscr.attroff(curses.color_pair(CursesColors.MARKED))
    stdscr.refresh()
    sleep(1.5)


def draw_positions(stdscr, window_height, window_width, positions: list[dict]):
    """
    Displays information about currently oppened positions
    """
    names = ["SYMBOL", "ENTRY PRICE", "QUANTITY", "CURRENT PRICE"]
    symbol_width = len(names[0])
    entry_price_width = len(names[1])
    qty_width = len(names[2])
    price_width = len(names[3])
    for symbol in positions:
        symbol_width = max(symbol_width, len(symbol["symbol"]))
        entry_price_width = max(entry_price_width, len(symbol["avg_entry_price"]))
        qty_width = max(qty_width, len(symbol["qty"]))
        price_width = max(price_width, len(symbol["current_price"]))

    height = len(positions) * 2 + 5
    width = symbol_width + entry_price_width + qty_width + price_width + 7

    x = (window_width - width) // 2
    y = (window_height - height) // 2

    draw_block_border(stdscr, y, x, height, width, "OPEN POSITIONS")

    stdscr.attron(curses.color_pair(CursesColors.MARKED))
    stdscr.addstr(y + 2, x + 2, names[0] + " " * (symbol_width - len(names[0]) + 1) + names[1] + " " 
                  * (entry_price_width - len(names[1]) + 1) + names[2] + " " * (qty_width - len(names[2]) + 1) 
                  + names[3] + " " * (price_width - len(names[3]) + 1))
    stdscr.attroff(curses.color_pair(CursesColors.MARKED))

    for i, symbol in enumerate(positions):
        stdscr.addstr(y + 2 * i + 4, x + 2, symbol["symbol"] + " " * (symbol_width - len(symbol["symbol"]) + 1) 
                      + symbol["avg_entry_price"] + " " * (entry_price_width - len(symbol["avg_entry_price"]) + 1) 
                      + symbol["qty"] + " " * (qty_width - len(symbol["qty"]) + 1) + symbol["current_price"] + " " 
                      * (price_width - len(symbol["current_price"]) + 1))


def get_market_data_async(widget, chartdisplay, widget_setup, result: list):
    """
    Gets market data for widget and chart
    Is used to get data in new thread asynchronously
    """
    while True:

        widget.reload_instruments()

        whole_patch = widget.get_widget_patch(1000)
        for _ in range(len(result)):
            result.pop()
        for patch in whole_patch:
            result.append(patch)

        chartdisplay.create_chart()


def draw_market_data(stdscr, y, x, width, result):
    """
    Display market data batch as one line
    """
    whole_patch = result
    length = 0

    for patch in whole_patch:
        if length + len(patch[0]) > width - 6:
            return

        stdscr.addstr(y + 1, x + 1 + length, patch[0])
        length += len(patch[0])

        match patch[1]:
            case 1:
                stdscr.attron(curses.color_pair(CursesColors.POSITIVE_TRADE))
                stdscr.addstr(y + 1, x + 1 + length, " /\\ ")
                length += 4
                stdscr.attroff(curses.color_pair(CursesColors.POSITIVE_TRADE))
            case -1:
                stdscr.attron(curses.color_pair(CursesColors.NEGATIVE_TRADE))
                stdscr.addstr(y + 1, x + 1 + length, " \\/ ")
                length += 4
                stdscr.attroff(curses.color_pair(CursesColors.NEGATIVE_TRADE))
            case _:
                stdscr.addstr(y + 1, x + 1 + length, " - ")
                length += 3

        length += 2


def draw_chart(stdscr, y, x, height, width, self: ChartDisplay):
    """
    Displays chart, based on data from self (ChartDisplay)
    """
    if self.chart == None or self.chart_available == False:
        return -1
    else:
        for i, ch in enumerate(self.chart):
            if i > width:
                stdscr.refresh()
                break
            if ch["direction"] == 1:
                color = CursesColors.POSITIVE_TRADE
            else:
                color = CursesColors.NEGATIVE_TRADE
            for j in range(ch["start"], ch["start"] + ch["length"]):
                if j >= 0 and height - j - self.place_for_data >= 0:
                    stdscr.attron(curses.color_pair(color))
                    stdscr.addstr(y + height - j - self.place_for_data, x + i, "#")
                    stdscr.attroff(curses.color_pair(color))

            if i % 20 == 10:
                stdscr.addstr(y + height - self.place_for_data + 1, x + i - 10, "|")
                stdscr.addstr(y + height - self.place_for_data + 2, x + i - 10, str(ch["date"].time()))
                stdscr.addstr(y + height - self.place_for_data + 3, x + i - 10, str(ch["date"].date()))

        for i in range(height - self.place_for_data):
            delta_price = (self.end_price - self.start_price) / (height - self.place_for_data)
            if i % 10 == 0:
                stdscr.addstr(y + height - i - self.place_for_data, x + width - self.place_for_price, "-")
                stdscr.addstr(y + height - i - self.place_for_data, x + width - self.place_for_price + 2, str(round(self.start_price + delta_price * i, 1)))

    draw_block_border(stdscr, y, x, 3, len(self.uuid) + len(str(self.price)) + 3)
    stdscr.attron(curses.color_pair(CursesColors.MARKED))
    stdscr.addstr(y + 1, x + 1, self.uuid + " " + str(self.price))
    stdscr.attroff(curses.color_pair(CursesColors.MARKED))
    stdscr.addstr(y + 1, x + 1, self.uuid + " ")
    stdscr.refresh()


def draw_menu(stdscr, y, x, width, menu: Menu):
    """
    Displays menu buttons in right colors
    """
    draw_block_border(stdscr, y + 2, x + 1, 3, width - 2, "TIME")
    current_time = ctime()
    stdscr.attron(curses.color_pair(CursesColors.MARKED))
    stdscr.addstr(y + 3, x + (width - len(current_time)) // 2, current_time)
    stdscr.attroff(curses.color_pair(CursesColors.MARKED))
    y += 2
    for i, part in enumerate(menu.get_component_parts("MENU")):
        draw_block_border(stdscr, y + 1 + 3 * (i + 1), x + 1, 3, width - 2)
        if menu.menu_part_selected(part):
            stdscr.attron(curses.color_pair(CursesColors.NORMAL_CURRENT))
            stdscr.addstr(y + 2 + 3 * (i + 1), x + (width - len(part)) // 2, part)
            stdscr.attroff(curses.color_pair(CursesColors.NORMAL_CURRENT))
        else:
            stdscr.addstr(y + 2 + 3 * (i + 1), x + (width - len(part)) // 2, part)


def draw_action(stdscr, y, x, width, menu: Menu):
    """
    Displays action menu buttons in right colors
    """
    x += 1
    width -= 2
    part_n = menu.get_component_part_buttons_number()
    part_n += part_n % 2
    part_m = part_n // 2
    for i, part_ in enumerate(menu.get_component_parts(menu.get_menu_part_selected())):
        button = part_ + "   " + menu.get_component_part_button(part_)

        new_y = int(x + (i // 2) * (width) / part_m + (width / part_m - len(button)) // 2)
        draw_block_border(stdscr, y + 1 + (3 * i) % 6, x + int((i // 2) * width / part_m), 3, width // part_m)
        if menu.action_part_selected(part_):
            stdscr.addstr(y + 2 + (3 * i) % 6, new_y, part_)
            stdscr.attron(curses.color_pair(CursesColors.MARKED_CURRENT))
            stdscr.addstr(y + 2 + (3 * i) % 6, new_y + len(part_) + 3, menu.get_component_part_button(part_))
            stdscr.attroff(curses.color_pair(CursesColors.MARKED_CURRENT))
        else:
            stdscr.addstr(y + 2 + (3 * i) % 6, new_y, part_)
            stdscr.attron(curses.color_pair(CursesColors.MARKED))
            stdscr.addstr(y + 2 + (3 * i) % 6, new_y + len(part_) + 3, menu.get_component_part_button(part_))
            stdscr.attroff(curses.color_pair(CursesColors.MARKED))

