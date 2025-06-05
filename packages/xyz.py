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
from yfinance.shared import *
from displayer import *

HEIGHT_MIN = 40
WIDTH_MIN = 140
WRONG_SIZE_MESSAGE = "Your window is to small.\nTry to increase window size."


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

        # if height<HEIGHT_MIN or width<WIDTH_MIN:
        #     stdscr.addstr(0, 0, WRONG_SIZE_MESSAGE)
        #     stdscr.refresh()

        #     key = stdscr.getch()

        #     if key == ord('q'):
        #         return 0
        #     else:
        #         continue

        draw_block_border(stdscr, 1, 1, 17, 52)

        x_profit, y_profit = width // 2 - 20, height // 2 - 4

        for i in range(len(PROFIT)):
            stdscr.addstr(i+3, 7, PROFIT[i])

        stdscr.addstr(10, 15, "-PROgrammer Friendly")
        stdscr.addstr(12, 15, "-Investing")
        stdscr.addstr(14, 15, "-Text user interface")

        #draw_loading(stdscr,20, 20)


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
    draw_positions_ = 0   


    x, y = 0, 0
    typed=""


    with open("setup.json", "r") as json_setup:
        setup = json.load(json_setup)

    widget_setup = setup['widget']
    chart_setup = setup['chart']
    menu.load_menu_from_json(setup)
    widget.add_instrument(widget_setup['uuid'])

    height, width = stdscr.getmaxyx() #60, 190#63, 237#stdscr.getmaxyx()

    widget_height, widget_width = 3, (width - 3) * 2 // 3
    widget_y, widget_x = 1, 1

    action_height, action_width = 8, width - 3
    action_y, action_x = height - 1 - action_height, 1

    chart_height, chart_width = height - 2 - widget_height - action_height, (width - 3) * 2 // 3
    chart_y, chart_x = 1 + widget_height, 1

    utc_m4 = timezone(timedelta(hours=-4))
    chartdisplay.update(uuid=chart_setup["uuid"][0],time_frame=120,start_date=datetime.now(utc_m4 )-timedelta(hours=0+(chart_width-2)*2), end_date=datetime.now(utc_m4)+timedelta(hours=1),height=chart_height, width=chart_width)  


    result=[]

    thread = threading.Thread(target=get_market_data_async, args=(widget, chartdisplay, widget_setup, result), daemon=True)
    thread.start()

    menu_height, menu_width = height - action_height - 2, width - widget_width - 3
    menu_y, menu_x = 1, (width - 3) * 2 // 3 + 1

    draw_block_border(stdscr, 0, 0, height, width - 1, "PROFIT")
    draw_block_border(stdscr, widget_y, widget_x, widget_height, widget_width, "MARKET─DATA")
    draw_block_border(stdscr, action_y, action_x, action_height, action_width, "ACTIONS")
    draw_block_border(stdscr, chart_y, chart_x, chart_height, chart_width, "CHARTS")
    draw_block_border(stdscr, menu_y, menu_x, menu_height, menu_width, "MENU")

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

        chartdisplay.update(height=chart_height, width=chart_width)
        stdscr.erase()


        
        

        draw_block_border(stdscr, 0, 0, height, width - 1, "PROFIT")
        draw_block_border(stdscr, widget_y, widget_x, widget_height, widget_width, "MARKET─DATA")
        draw_block_border(stdscr, action_y, action_x, action_height, action_width, "ACTIONS")
        draw_block_border(stdscr, chart_y, chart_x, chart_height, chart_width, "CHARTS")
        draw_block_border(stdscr, menu_y, menu_x, menu_height, menu_width, "MENU")

        draw_market_data(stdscr, widget_y, widget_x, widget_width, result)
        draw_menu(stdscr, menu_y, menu_x, menu_width, menu)
        draw_action(stdscr, action_y, action_x, action_width, menu)

        if draw_positions_:
            draw_positions(stdscr, height, width,client.get_client_positions())

        draw_chart(stdscr, chart_y+1, chart_x+1, chart_height-2, chart_width-2, chartdisplay)

        if draw_positions_:
            draw_positions(stdscr, height, width,client.get_client_positions())


        def set_button():
            nonlocal typed
            if typed!="":
                menu.set_button_text(typed)
            typed=""
        

        #stdscr.refresh()
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

                    if process_order_data(data) != 1:
                        orders.update_order(*data)
                        if orders.submit_order()==0:
                            draw_order_confirmation(stdscr, height, width, True)
                        else:
                            draw_order_confirmation(stdscr, height, width, False)
                    else:
                        draw_order_confirmation(stdscr, height, width, False)
                elif menu.menu_part_selected("WIDGET SETTINGS"):
                    widget.set_pending_instruments(widget_setup['uuid'])
                    # widget.pop_all_instruments()
                    # widget.add_instrument(widget_setup['uuid'])
                elif menu.menu_part_selected("CHART SETTINGS"):
                    chartdisplay.set_pending_uuid(chart_setup["uuid"][0])
                elif menu.menu_part_selected("OPEN POSITIONS"):
                    draw_positions_ = (draw_positions_ + 1) % 2
                else:
                    parts=menu.get_component_parts("CHART MANIPULATION")

                    part_selected=menu.action_current_part_selected()
                    if part_selected==parts[0]: 
                        chartdisplay.date_down(factor=0.1)
                    elif part_selected==parts[1]: 
                        chartdisplay.date_up(factor=0.1)
                    elif part_selected==parts[2]: 
                        chartdisplay.date_span_down()
                    elif part_selected==parts[3]: 
                        chartdisplay.date_span_up()
                    elif part_selected==parts[4]: 
                        chartdisplay.price_down(factor=0.1)
                    elif part_selected==parts[5]: 
                        chartdisplay.price_up(factor=0.1)
                    elif part_selected==parts[6]: 
                        chartdisplay.price_span(factor=1.2)
                    elif part_selected==parts[7]: 
                        chartdisplay.price_span(factor=0.8)
                    chartdisplay.current_data=False

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
                        button_n=menu.get_button_number()
                        widget_setup['uuid'][button_n]=typed
                        chart_setup["uuid"][0]=typed
                else:
                    typed += chr(key)
                    stdscr.addch(y, x, key)
                    x += 1
                    menu.set_button_text(typed)
                    button_n=menu.get_button_number()
                    widget_setup['uuid'][button_n]=typed
                    chart_setup["uuid"][0]=typed
        
        stdscr.refresh()



def main():
    curses.wrapper(draw_logging_menu)


if __name__ == "__main__":
    main()
