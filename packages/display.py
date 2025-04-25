#import sys,os
import time
import curses
from display_texts import *
from widget import Widget
from chart import Chart
from client import Client
from menu import Menu
import json



def draw_block_border(stdscr, y, x, height, width, name=None):
    border_up = "┌"+"─"*(width-2)+"┐"
    border_side = "│"
    border_down = "└"+"─"*(width-2)+"┘"

    stdscr.addstr(y, x, border_up)

    for i in range(1,height-1):
        stdscr.addstr(y+i,x,border_side)
        stdscr.addstr(y+i,x+width-1,border_side)

    stdscr.addstr(y+height-1, x, border_down)

    if name:
        stdscr.addstr(y,x+(width-len(name))//2,name)


def draw_loading(stdscr, y, x):
    text="Loading"
    n=len(text)
    stdscr.addstr(y, x, text)
    for i in range(12):
        if i%4==0:
            stdscr.addstr(y, x+n, "   ")
        else:
            stdscr.addstr(y, x+n+i%4-1, ".")
        stdscr.refresh()
        time.sleep(0.4)


def draw_market_data(stdscr, widget, widget_setup, y, x, width):
    widget.add_instrument(widget_setup['uuid'])
    widget.reload_instruments()

    whole_patch=widget.get_widget_patch(width-2)
    length=0

    for patch in whole_patch:
        stdscr.addstr(y+1, x+1+length, patch[0])
        length+=len(patch[0])
        if patch[1]==1:
            stdscr.attron(curses.color_pair(1))
            stdscr.addstr(y+1, x+1+length, " /\\ ")
            length+=4
            stdscr.attroff(curses.color_pair(1))
        elif patch[1]==-1:
            stdscr.attron(curses.color_pair(2))
            stdscr.addstr(y+1, x+1+length, " \\/ ")
            length+=4
            stdscr.attroff(curses.color_pair(2))
        else:
            stdscr.addstr(y+1, x+1+length, " - ")
            length+=3
            
        length+=2
    
def draw_menu(stdscr, client: Client, y, x, height, width, menu: Menu):
    for i, component in enumerate(menu.get_part_components("menu")):
        draw_block_border(stdscr,y+1+3*i,x+1,3,width-2)
        if menu.get_component()==component:
            stdscr.attron(curses.color_pair(3))
            stdscr.addstr(y+2+3*i, x+(width-len(component))//2, component)
            stdscr.attroff(curses.color_pair(3))
        else:
            stdscr.addstr(y+2+3*i, x+(width-len(component))//2, component)


def draw_action_order(stdscr, client: Client, y, x, height, width, menu: Menu):
    x+=1
    width-=2
    for i, component in enumerate(menu.get_part_components("order")):
        new_y=int(x+(i//2)*(width)/3+(width/3-len(component))//2)
        draw_block_border(stdscr,y+1+(3*i)%6,x+int((i//2)*width/3),3,width//3)
        if menu.get_component()==component:
            stdscr.attron(curses.color_pair(3))
            stdscr.addstr(y+2+(3*i)%6, new_y, component)
            stdscr.attroff(curses.color_pair(3))
        else:
            stdscr.addstr(y+2+(3*i)%6, new_y, component)


def draw_action_settings(stdscr, client: Client, y, x, height, width, menu: Menu):
    x+=1
    width-=2
    for i, component in enumerate(menu.get_part_components("settings")):
        new_y=int(x+(i//2)*(width)/3+(width/3-len(component))//2)
        draw_block_border(stdscr,y+1+(3*i)%6,x+int((i//2)*width/3),3,width//3)
        if menu.get_component()==component:
            stdscr.attron(curses.color_pair(3))
            stdscr.addstr(y+2+(3*i)%6, new_y, component)
            stdscr.attroff(curses.color_pair(3))
        else:
            stdscr.addstr(y+2+(3*i)%6, new_y, component)


def draw_logging_menu(stdscr):
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)
    
    while True:
        stdscr.clear()
        height, width = stdscr.getmaxyx()

        draw_block_border(stdscr, 0, 0, height, width-1)

        x_profit,y_profit=width//2-20,height//2-4

        for i in range(len(PROFIT)):
            stdscr.addstr(y_profit+i, x_profit, PROFIT[i])

        stdscr.refresh()

        key = stdscr.getch()

        if key == ord('q'):
            return 0
        elif key in [10, 13]:
            break

    draw_working_menu(stdscr)


def draw_working_menu(stdscr):
    client=Client()
    widget=Widget()
    menu=Menu()

    action_button=-1

    with open("setup.json", "r") as json_setup:
        setup = json.load(json_setup)
    widget_setup=setup['widget']
    menu.load_menu_from_json(setup)


    while True:
        stdscr.erase()

        height, width = stdscr.getmaxyx()

        widget_height, widget_width = 3, (width-3)*2//3
        widget_y, widget_x = 1, 1

        action_height, action_width = 8, width-3
        action_y, action_x = height-1-action_height, 1

        chart_height, chart_width = height-2-widget_height-action_height, (width-3)*2//3
        chart_y, chart_x = 1+widget_height, 1

        menu_height, menu_width = height-action_height-2, width-widget_width-3
        menu_y, menu_x = 1, (width-3)*2//3+1

        draw_block_border(stdscr, 0, 0, height, width-1,"PROFIT")
        draw_block_border(stdscr,widget_y,widget_x,widget_height,widget_width,"MARKET─DATA")
        draw_block_border(stdscr,action_y,action_x,action_height,action_width,"ACTIONS")
        draw_block_border(stdscr,chart_y,chart_x,chart_height,chart_width,"CHARTS")
        draw_block_border(stdscr,menu_y,menu_x,menu_height,menu_width,"MENU")

        draw_market_data(stdscr, widget, widget_setup, widget_y, widget_x, widget_width)
        
        draw_menu(stdscr, client, menu_y, menu_x, menu_height, menu_width, menu)

        match action_button:
            case 0:
                pass
            case 1:
                draw_action_settings(stdscr, client, action_y, action_x, action_height, action_width, menu)
            case 2:
                draw_action_order(stdscr, client, action_y, action_x, action_height, action_width, menu)
            case 3:
                pass
            case _:
                pass
        

        stdscr.refresh()
        #stdscr.erase()
        stdscr.move(0,0)
        key = stdscr.getch()
        if key == ord('q'):
            break
        elif key == curses.KEY_UP:
            menu.prev_component()
        elif key == curses.KEY_DOWN:
            menu.next_component()
        elif key == curses.KEY_RIGHT:
            menu.next_part()
        elif key == curses.KEY_LEFT:
            menu.prev_part()
        elif key in [10, 13]:
            match menu.get_component():
                case "CLIENT INFO":
                    action_button=0
                case "SETTINGS":
                    action_button=1
                case "BUY/SELL":
                    action_button=2
                case "OPEN POSITIONS":
                    action_button=3
                case _:
                    action_button=-1
                



def main():
    curses.wrapper(draw_logging_menu)

if __name__ == "__main__":
    main()