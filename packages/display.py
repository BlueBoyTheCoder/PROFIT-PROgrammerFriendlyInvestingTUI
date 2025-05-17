import curses
from display_texts import *
from widget import Widget
from client import Client
from menu import Menu
from orders import Orders
from chartdisplay import ChartDisplay
import json
import threading
from datetime import datetime, timedelta, timezone
from displayer import *


def draw_logging_menu(stdscr):
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(4, 220, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_BLACK, 220)


    while True:
        stdscr.clear()
        height, width = stdscr.getmaxyx()

        draw_block_border(stdscr, 0, 0, height, width - 1)

        x_profit, y_profit = width // 2 - 20, height // 2 - 4

        for i in range(len(PROFIT)):
            stdscr.addstr(y_profit + i, x_profit, PROFIT[i])

        draw_loading(stdscr,y_profit+len(PROFIT)+2, width//2)


        stdscr.refresh()

        key = stdscr.getch()

        if key == ord('q'):
            return 0
        elif key in [10, 13]:
            break

    draw_working_menu(stdscr)


def draw_working_menu(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.timeout(1000)

    client = Client()
    widget = Widget()
    menu = Menu()
    orders = Orders(client.get_trading_client())
    chartdisplay=ChartDisplay( start_price=180, end_price=230)        


    x, y = 0, 0
    typed=""


    with open("setup.json", "r") as json_setup:
        setup = json.load(json_setup)

    widget_setup = setup['widget']
    chart_setup = setup['chart']
    menu.load_menu_from_json(setup)

    height, width = 60, 250#63, 237#stdscr.getmaxyx()

    utc_m4 = timezone(timedelta(hours=-4))
    #chartdisplay.update(uuid=chart_setup['uuid'][0], time_frame=120, width=chart_width-2, height=chart_height-2, start_date=datetime.now(tz=utc_m4)-timedelta(hours=2*(chart_width-2)),end_date=datetime.now(tz=utc_m4)+timedelta(days=1))
    chartdisplay.update(uuid="AAPL",time_frame=120,start_date=datetime.now(utc_m4 )-timedelta(hours=0+(width-2)*2), end_date=datetime.now(utc_m4)+timedelta(days=1),height=height, width=width)  
    # chartdisplay.update(width=chart_width-2, height=chart_height-2)


    result=[]

    thread = threading.Thread(target=get_market_data_async, args=(widget, chartdisplay, widget_setup, result), daemon=True)
    thread.start()

    # thread_chart = threading.Thread(target=chartdisplay.create_chart(), args=(), daemon=True)
    # thread_chart.start()

    stdscr.clear()
    

    while True:
        height, width = stdscr.getmaxyx()

        widget_height, widget_width = 3, (width - 3) * 2 // 3
        widget_y, widget_x = 1, 1

        action_height, action_width = 8, width - 3
        action_y, action_x = height - 1 - action_height, 1

        chart_height, chart_width = height - 2 - widget_height - action_height, (width - 3) * 2 // 3
        chart_y, chart_x = 1 + widget_height, 1

        menu_height, menu_width = height - action_height - 2, width - widget_width - 3
        menu_y, menu_x = 1, (width - 3) * 2 // 3 + 1


        

        #chartdisplay.update(width=chart_width-2, height=chart_height-2)
        #chartdisplay.create_chart()
        #chartdisplay.display_chart(stdscr, chart_y+1, chart_x+1)
        #chartdisplay.create_chart()

        draw_market_data(stdscr, widget_y, widget_x, widget_width, result)
        draw_chart(stdscr, chart_y+1, chart_x+1, chart_height-2, chart_width-2, chartdisplay)
        draw_menu(stdscr, menu_y, menu_x, menu_width, menu)
        draw_action(stdscr, action_y, action_x, action_width, menu)

        draw_block_border(stdscr, 0, 0, height, width - 1, "PROFIT")
        draw_block_border(stdscr, widget_y, widget_x, widget_height, widget_width, "MARKET─DATA")
        draw_block_border(stdscr, action_y, action_x, action_height, action_width, "ACTIONS")
        draw_block_border(stdscr, chart_y, chart_x, chart_height, chart_width, "CHARTS")
        draw_block_border(stdscr, menu_y, menu_x, menu_height, menu_width, "MENU")


        def set_button():
            nonlocal typed
            if typed!="":
                menu.set_button_text(typed)
            typed=""
        

        stdscr.refresh()
        stdscr.move(0, 0)

        key = stdscr.getch()
        match key:
            case -1:
                pass
            case char if char == ord('q'):
                break
            case 10:
                if menu.menu_part_selected("BUY/SELL"):
                    data = menu.get_current_component_parts_values()
                    if process_order_data(data) != -1:
                        orders.update_order(*data)
                        orders.submit_order()

            case char if char == ord('\t'):
                menu.next_button()
            case curses.KEY_UP:
                set_button()
                menu.prev_part()
            case curses.KEY_DOWN:
                set_button()
                menu.next_part()
            case curses.KEY_RIGHT:
                set_button()
                menu.next_component()
            case curses.KEY_LEFT:
                set_button()
                menu.next_component()
            case _:
                if key in [curses.KEY_BACKSPACE, 127]:
                    if x > 0:
                        x -= 1
                        typed = typed[:-1]
                        menu.set_button_text(typed)
                else:
                    typed += chr(key)
                    stdscr.addch(y, x, key)
                    x += 1
                    menu.set_button_text(typed)

    
        stdscr.erase()



def main():
    curses.wrapper(draw_logging_menu)


if __name__ == "__main__":
    main()
