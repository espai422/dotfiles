# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


from libqtile.widget import base
from locale import currency
import os
import re
import socket
import subprocess
from typing import List  # noqa: F401
from libqtile import layout, bar, widget, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen, Rule
from libqtile.command import lazy
from libqtile.widget import Spacer
import netifaces
import pyperclip as clipboard
import psutil
#import arcobattery

class NetInterfaces():

    def __init__(self):
        self.refresh_interfaces()
        
        self.index = 0
        self.interfaces_len = len(self.interfaces)
        # print(self.interfaces)
        # print(self.addrs)

    def refresh_interfaces(self):
        self.addrs = [netifaces.ifaddresses(addrs)[2][0]['addr'] for addrs in netifaces.interfaces()]
        self.addrs.remove('127.0.0.1')

        self.interfaces = netifaces.interfaces()
        self.interfaces.remove('lo')

# A copy method to copy the ip addr to clipboard when widget is clicked 

    def next_interface(self):
        if self.index >= self.interfaces_len:
            self.refresh_interfaces()
            self.index = 0
        
        try:
            interface = self.interfaces[self.index][0:4]
            self.addr = self.addrs[self.index]
        except:
            return 'OFFLINE'

        self.index += 1

        return F'{interface}: {self.addr}'

    def addr_to_clipboard(self):
        clipboard.copy(str(self.addr))


class Batter_widget(base.InLoopPollText):

    def __init__(self, **config):
        self.icons = ['','','','','','']
        self.icons.reverse()
        self.charge_icon = ''
        self.battery_colors = {
            'red': ['#e06c75','#e06c75'],
            'orange': ['#d19a66','#d19a66'], 
            'green': ['#98c379','#98c379']
        }
        self.battery = psutil.sensors_battery()
        self.update_battery()

        base.InLoopPollText.__init__(self,'', **config)

    def get_battery_icon(self):
        total_icons = len(self.icons) -1
        index = (self.percent * total_icons) // 100
        return self.icons[index]

    def get_color(self):
        pass

    # def isCharging(self):
    #     pass

    def update_battery(self):
        self.plugged = self.battery.power_plugged
        self.percent = int(self.battery.percent)

    def poll(self):
        # Update Battery
        self.update_battery()
        if self.percent > 25:
            self.background = self.color1
        
        elif self.percent < 10:
            self.background = self.color3

        else:
            self.background = self.color2
        # Create formated string with battery icon and lightinig checking if is charging = True
        # Change foreground color with get color
            # self.foreground = new color
        # Change update_interval to create a kind of alarm
        icon = self.get_battery_icon()
        return icon

class colorChange(base.InLoopPollText):

    def __init__(self, **config):
        self.battery = psutil.sensors_battery()
        base.InLoopPollText.__init__(self, **config)
    
    def poll(self):
        percent = self.battery.percent
        if percent > 25:
            self.foreground = self.color1
            return self.icon
        
        elif percent < 10:
            self.foreground = self.color3
            return self.icon

        else:
            self.foreground = self.color2
            return self.icon

class BatteryPercent(base.InLoopPollText):

    def __init__(self, **config):
        self.battery = psutil.sensors_battery()
        base.InLoopPollText.__init__(self, **config)
    
    def poll(self):
        percent = self.battery.percent
        if percent > 25:
            self.background = self.color1
            return str(int(percent))
        
        elif percent < 10:
            self.background = self.color3
            return str(int(percent))

        else:
            self.background = self.color2
            return str(int(percent))

Interfaces = NetInterfaces()

#mod4 or mod = super key
mod = "mod4"
mod1 = "alt"
mod2 = "control"
home = os.path.expanduser('~')


@lazy.function
def window_to_prev_group(qtile):
    if qtile.currentWindow is not None:
        i = qtile.groups.index(qtile.currentGroup)
        qtile.currentWindow.togroup(qtile.groups[i - 1].name)

@lazy.function
def window_to_next_group(qtile):
    if qtile.currentWindow is not None:
        i = qtile.groups.index(qtile.currentGroup)
        qtile.currentWindow.togroup(qtile.groups[i + 1].name)

keys = [

# Most of our keybindings are in sxhkd file - except these

# SUPER + FUNCTION KEYS

    Key([mod], "f", lazy.window.toggle_fullscreen()),
    #Key([mod], "q", lazy.window.kill()),

    Key([mod], "w", lazy.window.kill()),
# SUPER + SHIFT KEYS

    Key([mod, "shift"], "q", lazy.window.kill()),
    Key([mod, "shift"], "r", lazy.restart()),


# QTILE LAYOUT KEYS
    Key([mod], "n", lazy.layout.normalize()),
    Key([mod], "space", lazy.next_layout()),

# CHANGE FOCUS
    Key([mod], "Up", lazy.layout.up()),
    Key([mod], "Down", lazy.layout.down()),
    Key([mod], "Left", lazy.layout.left()),
    Key([mod], "Right", lazy.layout.right()),
    Key([mod], "k", lazy.layout.up()),
    Key([mod], "j", lazy.layout.down()),
    Key([mod], "h", lazy.layout.left()),
    Key([mod], "l", lazy.layout.right()),


# RESIZE UP, DOWN, LEFT, RIGHT
    Key([mod, "control"], "l",
        lazy.layout.grow_right(),
        lazy.layout.grow(),
        lazy.layout.increase_ratio(),
        lazy.layout.delete(),
        ),
    Key([mod, "control"], "Right",
        lazy.layout.grow_right(),
        lazy.layout.grow(),
        lazy.layout.increase_ratio(),
        lazy.layout.delete(),
        ),
    Key([mod, "control"], "h",
        lazy.layout.grow_left(),
        lazy.layout.shrink(),
        lazy.layout.decrease_ratio(),
        lazy.layout.add(),
        ),
    Key([mod, "control"], "Left",
        lazy.layout.grow_left(),
        lazy.layout.shrink(),
        lazy.layout.decrease_ratio(),
        lazy.layout.add(),
        ),
    Key([mod, "control"], "k",
        lazy.layout.grow_up(),
        lazy.layout.grow(),
        lazy.layout.decrease_nmaster(),
        ),
    Key([mod, "control"], "Up",
        lazy.layout.grow_up(),
        lazy.layout.grow(),
        lazy.layout.decrease_nmaster(),
        ),
    Key([mod, "control"], "j",
        lazy.layout.grow_down(),
        lazy.layout.shrink(),
        lazy.layout.increase_nmaster(),
        ),
    Key([mod, "control"], "Down",
        lazy.layout.grow_down(),
        lazy.layout.shrink(),
        lazy.layout.increase_nmaster(),
        ),


# FLIP LAYOUT FOR MONADTALL/MONADWIDE
    Key([mod, "shift"], "f", lazy.layout.flip()),

# FLIP LAYOUT FOR BSP
    Key([mod, "mod1"], "k", lazy.layout.flip_up()),
    Key([mod, "mod1"], "j", lazy.layout.flip_down()),
    Key([mod, "mod1"], "l", lazy.layout.flip_right()),
    Key([mod, "mod1"], "h", lazy.layout.flip_left()),

# MOVE WINDOWS UP OR DOWN BSP LAYOUT
    Key([mod, "shift"], "k", lazy.layout.shuffle_up()),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down()),
    Key([mod, "shift"], "h", lazy.layout.shuffle_left()),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right()),

# MOVE WINDOWS UP OR DOWN MONADTALL/MONADWIDE LAYOUT
    Key([mod, "shift"], "Up", lazy.layout.shuffle_up()),
    Key([mod, "shift"], "Down", lazy.layout.shuffle_down()),
    Key([mod, "shift"], "Left", lazy.layout.swap_left()),
    Key([mod, "shift"], "Right", lazy.layout.swap_right()),

# TOGGLE FLOATING LAYOUT
    Key([mod, "shift"], "space", lazy.window.toggle_floating()),

    ]

def window_to_previous_screen(qtile, switch_group=False, switch_screen=False):
    i = qtile.screens.index(qtile.current_screen)
    if i != 0:
        group = qtile.screens[i - 1].group.name
        qtile.current_window.togroup(group, switch_group=switch_group)
        if switch_screen == True:
            qtile.cmd_to_screen(i - 1)

def window_to_next_screen(qtile, switch_group=False, switch_screen=False):
    i = qtile.screens.index(qtile.current_screen)
    if i + 1 != len(qtile.screens):
        group = qtile.screens[i + 1].group.name
        qtile.current_window.togroup(group, switch_group=switch_group)
        if switch_screen == True:
            qtile.cmd_to_screen(i + 1)

keys.extend([
    # MOVE WINDOW TO NEXT SCREEN
    Key([mod,"shift"], "Right", lazy.function(window_to_next_screen, switch_screen=True)),
    Key([mod,"shift"], "Left", lazy.function(window_to_previous_screen, switch_screen=True)),
])

groups = []

# FOR QWERTY KEYBOARDS
group_names = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0",]

# FOR AZERTY KEYBOARDS
#group_names = ["ampersand", "eacute", "quotedbl", "apostrophe", "parenleft", "section", "egrave", "exclam", "ccedilla", "agrave",]

#group_labels = ["1 ", "2 ", "3 ", "4 ", "5 ", "6 ", "7 ", "8 ", "9 ", "0",]
'          ךּ    ﴮ  ﰆ   '
group_labels = ["", "", "", "", "", "", "", "", "", "",]
#group_labels = ["Web", "Edit/chat", "Image", "Gimp", "Meld", "Video", "Vb", "Files", "Mail", "Music",]
group_labels = [' ',' ',' ',' ',' ',' ',' ',' ',' ','']

group_layouts = ["monadtall", "monadtall", "monadtall", "monadtall", "monadtall","monadtall", "monadtall", "monadtall", "monadtall", "monadtall",]
#group_layouts = ["monadtall", "matrix", "monadtall", "bsp", "monadtall", "matrix", "monadtall", "bsp", "monadtall", "monadtall",]

for i in range(len(group_names)):
    groups.append(
        Group(
            name=group_names[i],
            layout=group_layouts[i].lower(),
            label=group_labels[i],
        ))

for i in groups:
    keys.extend([

#CHANGE WORKSPACES
        Key([mod], i.name, lazy.group[i.name].toscreen()),
        Key([mod], "Tab", lazy.screen.next_group()),
        Key([mod, "shift" ], "Tab", lazy.screen.prev_group()),
        Key(["mod1"], "Tab", lazy.screen.next_group()),
        Key(["mod1", "shift"], "Tab", lazy.screen.prev_group()),

# MOVE WINDOW TO SELECTED WORKSPACE 1-10 AND STAY ON WORKSPACE
        #Key([mod, "shift"], i.name, lazy.window.togroup(i.name)),
# MOVE WINDOW TO SELECTED WORKSPACE 1-10 AND FOLLOW MOVED WINDOW TO WORKSPACE
        Key([mod, "shift"], i.name, lazy.window.togroup(i.name) , lazy.group[i.name].toscreen()),
    ])


def init_layout_theme():
    return {"margin":5,
            "border_width":2,
            "border_focus": "#5e81ac",
            "border_normal": "#4c566a"
            }

layout_theme = init_layout_theme()

layouts = [
    layout.MonadTall(margin=8, border_width=2, border_focus="#5e81ac", border_normal="#4c566a"),
    layout.MonadWide(margin=8, border_width=2, border_focus="#5e81ac", border_normal="#4c566a"),
    layout.Matrix(**layout_theme),
    layout.Bsp(**layout_theme),
    layout.Floating(**layout_theme),
    layout.RatioTile(**layout_theme),
    layout.Max(**layout_theme)
]

# COLORS FOR THE BAR
#Theme name : ArcoLinux Default
def init_colors():
    return [["#2F343F", "#2F343F"], # color 0
            ["#2F343F", "#2F343F"], # color 1
            ["#c0c5ce", "#c0c5ce"], # color 2
            ["#fba922", "#fba922"], # color 3
            ["#3384d0", "#3384d0"], # color 4
            ["#f3f4f5", "#f3f4f5"], # color 5
            ["#cd1f3f", "#cd1f3f"], # color 6
            ["#62FF00", "#62FF00"], # color 7
            ["#6790eb", "#6790eb"], # color 8
            ["#a9a9a9", "#a9a9a9"], # color 9
            ["#f6f7f8", "#f6f7f8"], # color 10 *
            ["#878787", "#878787"], # color 11 *
            ["#1F242F", "#1F242F"], # color 12 *
    ]
# Vscode Ondedark 
onedark = {
    'selected line': ['#2c313c','#2c313c'],
    'comment':['#767b85','#767b85'], #comment
    'inactive':  ['#6e7179','#6e7179'], #inactive
    'background':  ['#282c34','#282c34'], #background
    'dark background':  ['#21252b','#21252b'], #Dark background
    'active':  ['#d7dae0','#d7dae0'], # Selected section
    'purple':  ['#c678dd','#c678dd'], 
    'yellow':  ['#e5c07b','#e5c07b'],
    'red':  ['#e06c75','#e06c75'],
    'blue':  ['#61afef','#61afef'],
    'green':  ['#98c379','#98c379'], 
    'orange':  ['#d19a66','#d19a66'],
}
colors = init_colors()


# WIDGETS FOR THE BAR

def init_widgets_defaults():
    return dict(font="Noto Sans Bold",
                fontsize = 16,
                padding = 2,
                background=onedark['background'])

widget_defaults = init_widgets_defaults()

def init_widgets_list():
    prompt = "{0}@{1}: ".format(os.environ["USER"], socket.gethostname())
    widgets_list = [
            #    widget.Sep(
            #             linewidth = 2,
            #             padding = 10,
            #             foreground = onedark['orange'],
            #             background = onedark['background']
            #             ),
               widget.CurrentLayout(
                        font = "Noto Sans Bold",
                        background = onedark['background'],
                        foreground = onedark['active'],
                        padding = 9,
                        fontsize= 16
                        ),
                widget.TextBox(
                    text = '',
                    fontsize=40,
                    padding= -3,
                    foreground = onedark['background'],
                    background = onedark['red'],
                ),
            #    widget.Sep(
            #             linewidth = 2,
            #             padding = 10,
            #             foreground = onedark['orange'],
            #             background = onedark['background']
            #             ),
            # TODO Replace this widget for real ip widget 
               widget.GenPollText(
                        font="Noto Sans Bold",
                        func = Interfaces.next_interface,
                        background =onedark['red'],
                        foreground=onedark['background'],
                        padding = 5,
                        fontsize=16,
                        update_interval = 5,
                        mouse_callbacks = {
                            'Button1': lambda: Interfaces.addr_to_clipboard(),
                            
                        }

                        ), # 
                widget.TextBox(
                    text = '',
                    fontsize=40,
                    padding= -3,
                    foreground = onedark['red'],
                    background = onedark['background'],
                ),
                widget.TextBox(
                    text = '',
                    fontsize=35,
                    padding=4,
                    foreground = onedark['active'],
                    background = onedark['background'],
                ),
                widget.TextBox(
                    text = '',
                    fontsize=40,
                    padding= -3,
                    foreground = onedark['background'],
                    background = onedark['yellow'],
                ),
                widget.CryptoTicker( # 
                    currency = 'EUR',
                    crypto = 'BTC',
                    format = '{amount:.2f} {symbol}',
                    symbol = '€',
                    background =onedark['yellow'],
                    foreground=onedark['background'],
                ),
                widget.TextBox(
                    text = '',
                    fontsize=40,
                    padding= -3,
                    foreground = onedark['yellow'],
                    background = onedark['background'],
                ),
                widget.TextBox(
                    padding = 7,
                    text = '',
                    fontsize=40,
                    background = onedark['background'],
                    foreground = onedark['active']
                ),
                widget.TextBox(
                    text = '',
                    fontsize=40,
                    padding= -3,
                    foreground = onedark['background'],
                    background = onedark['purple'],
                ),
                widget.ThermalSensor(
                    font='Noto Sans Bold',
                    foreground=onedark['background'],
                    background=onedark['purple'],
                ),
            #    widget.Clipboard(
            #         font='Noto Sans Bold',
            #         foreground=onedark['background'],
            #         background=onedark['purple'],
            #         #fmt='CP: {}',
            #         fontsize= 16,
            #         max_chars= 45,
            #         max_width=60,
            #         timeout= 100,
            #    ),
                widget.TextBox(
                    text = '',
                    fontsize=40,
                    padding= -3,
                    foreground = onedark['purple'],
                    background = onedark['background'],
                ),
               widget.Spacer(
                        background = onedark['background']
                        ),
                widget.TextBox(
                        font="FontAwesome",
                        text="",
                        foreground=onedark['background'],
                        background=onedark['dark background'],
                        padding = 0,
                        fontsize=40 
                        ),
               widget.GroupBox(font="FontAwesome",
                        fontsize = 21, # 16
                        margin_y = 2,
                        margin_x = 0,
                        padding_y = 0,
                        padding_x = 5,
                        borderwidth = 0,
                        disable_drag = True,
                        active = onedark['active'],
                        inactive = onedark['inactive'],
                        rounded = False,
                        highlight_method = "text",
                        this_current_screen_border = onedark['purple'],
                        foreground = onedark['active'],
                        background = onedark['dark background']
                        ),
              widget.TextBox(
                        font="FontAwesome",
                        text="",
                        foreground=onedark['background'],
                        background=onedark['dark background'],
                        padding = 0,
                        fontsize=40
                        ),
                
               widget.Spacer(
                        background = onedark['background']
                        ),
            #    widget.WindowName(font="Noto Sans Bold",
            #             fontsize = 16,
            #             foreground = onedark['active'],
            #             background = onedark['background'],
            #             ),
               # battery option 2  from Qtile
                # batteryIcon
            #     colorChange(
            #         foreground= onedark["active"],
            #         icon = '',
            #         color1 = onedark['green'],
            #         color2 = onedark['yellow'],
            #         color3 = onedark['red'],
            #         background = onedark['background'],
            #         fontsize = 40,
            #         update_interval = 5
            #         #text = 'hola'
            #     ),
            #     Batter_widget(
            #         fontsize=40,
            #         update_interval = 5,
            #         padding= 5,
            #         background= onedark['green'],
            #         color1 = onedark['green'],
            #         color2 = onedark['yellow'],
            #         color3 = onedark['red'],
            #         foreground= onedark['background']
            #     ),
                
              widget.TextBox(
                        font="FontAwesome",
                        text="",
                        foreground=onedark['green'],
                        background=onedark['background'],
                        padding = 0,
                        fontsize=40
                        ),
               widget.TextBox(
                        font="FontAwesome",
                        #text="",
                        text='',
                        background=onedark['green'],
                        foreground=onedark['background'],
                        padding = 5,
                        fontsize=20
                        ), # 
            #     BatteryPercent(
            #             font="Noto Sans Bold",
            #             update_interval = 5,
            #             fontsize = 16,
            #             foreground = onedark['background'],
            #             background = onedark['green'],
            #             color1 = onedark['green'],
            #             color2 = onedark['yellow'],
            #             color3 = onedark['red'],
            #     ),
               widget.Battery(
                        font="Noto Sans Bold",
                        update_interval = 10,
                        fontsize = 16,
                        foreground = onedark['background'],
                        background = onedark['green'],
                        format='{percent:2.0%}'
	            ),
              widget.TextBox(
                        font="FontAwesome",
                        text="",
                        foreground=onedark['background'],
                        background=onedark['green'],
                        padding = 0,
                        fontsize=40
                        ),
                widget.TextBox(
                    padding =2,
                    text = '',
                    fontsize=40,
                    background = onedark['background'],
                    foreground = onedark['active']
                ),
                # colorChange(
                #     background= onedark["background"],
                #     icon = '',
                #     color1 = onedark['green'],
                #     color2 = onedark['yellow'],
                #     color3 = onedark['red'],
                #     fontsize = 40,
                #     padding= 0,
                #     update_interval = 5,
                #     #text = 'hola'
                # ),
              widget.TextBox(
                        font="FontAwesome",
                        text="",
                        foreground=onedark['blue'],
                        background=onedark['background'],
                        padding = 0,
                        fontsize=40
                        ),
               widget.TextBox(
                        font="FontAwesome",
                        text="",
                        background=onedark['blue'],
                        foreground=onedark['background'],
                        padding = 5,
                        fontsize=30
                        ), # 
               widget.Clock(
                        foreground = onedark['background'],
                        background = onedark['blue'],
                        fontsize = 16,
                        #format="%Y-%m-%d %H:%M"
                        format="%H:%M"
                        ),
              widget.TextBox(
                        font="FontAwesome",
                        text="",
                        foreground=onedark['background'],
                        background=onedark['blue'],
                        padding = 0,
                        fontsize=40
                        ),
            #    widget.Sep(
            #             linewidth = 2,
            #             padding = 10,
            #             foreground = onedark['orange'],
            #             background = onedark['background']
            #             ),
               widget.Systray(
                        background=onedark['background'],
                        icon_size=20,
                        padding = 4
                        ),
              ]
    return widgets_list

widgets_list = init_widgets_list()


def init_widgets_screen1():
    widgets_screen1 = init_widgets_list()
    return widgets_screen1

def init_widgets_screen2():
    widgets_screen2 = init_widgets_list()
    return widgets_screen2

widgets_screen1 = init_widgets_screen1()
widgets_screen2 = init_widgets_screen2()


def init_screens():
    return [Screen(top=bar.Bar(widgets=init_widgets_screen1(), size=26, opacity=1)),
            Screen(top=bar.Bar(widgets=init_widgets_screen2(), size=26, opacity=0.8))]
screens = init_screens()


# MOUSE CONFIGURATION
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size())
]

dgroups_key_binder = None
dgroups_app_rules = []

# ASSIGN APPLICATIONS TO A SPECIFIC GROUPNAME
# BEGIN

#########################################################
################ assgin apps to groups ##################
#########################################################
# @hook.subscribe.client_new
# def assign_app_group(client):
#     d = {}
#     #####################################################################################
#     ### Use xprop fo find  the value of WM_CLASS(STRING) -> First field is sufficient ###
#     #####################################################################################
#     d[group_names[0]] = ["Navigator", "Firefox", "Vivaldi-stable", "Vivaldi-snapshot", "Chromium", "Google-chrome", "Brave", "Brave-browser",
#               "navigator", "firefox", "vivaldi-stable", "vivaldi-snapshot", "chromium", "google-chrome", "brave", "brave-browser", ]
#     d[group_names[1]] = [ "Atom", "Subl", "Geany", "Brackets", "Code-oss", "Code", "TelegramDesktop", "Discord",
#                "atom", "subl", "geany", "brackets", "code-oss", "code", "telegramDesktop", "discord", ]
#     d[group_names[2]] = ["Inkscape", "Nomacs", "Ristretto", "Nitrogen", "Feh",
#               "inkscape", "nomacs", "ristretto", "nitrogen", "feh", ]
#     d[group_names[3]] = ["Gimp", "gimp" ]
#     d[group_names[4]] = ["Meld", "meld", "org.gnome.meld" "org.gnome.Meld" ]
#     d[group_names[5]] = ["Vlc","vlc", "Mpv", "mpv" ]
#     d[group_names[6]] = ["VirtualBox Manager", "VirtualBox Machine", "Vmplayer",
#               "virtualbox manager", "virtualbox machine", "vmplayer", ]
#     d[group_names[7]] = ["Thunar", "Nemo", "Caja", "Nautilus", "org.gnome.Nautilus", "Pcmanfm", "Pcmanfm-qt",
#               "thunar", "nemo", "caja", "nautilus", "org.gnome.nautilus", "pcmanfm", "pcmanfm-qt", ]
#     d[group_names[8]] = ["Evolution", "Geary", "Mail", "Thunderbird",
#               "evolution", "geary", "mail", "thunderbird" ]
#     d[group_names[9]] = ["Spotify", "Pragha", "Clementine", "Deadbeef", "Audacious",
#               "spotify", "pragha", "clementine", "deadbeef", "audacious" ]
#     ######################################################################################
#
# wm_class = client.window.get_wm_class()[0]
#
#     for i in range(len(d)):
#         if wm_class in list(d.values())[i]:
#             group = list(d.keys())[i]
#             client.togroup(group)
#             client.group.cmd_toscreen(toggle=False)

# END
# ASSIGN APPLICATIONS TO A SPECIFIC GROUPNAME



main = None

@hook.subscribe.startup_once
def start_once():
    home = os.path.expanduser('~')
    subprocess.call([home + '/.config/qtile/scripts/autostart.sh'])

@hook.subscribe.startup
def start_always():
    # Set the cursor to something sane in X
    subprocess.Popen(['xsetroot', '-cursor_name', 'left_ptr'])

@hook.subscribe.client_new
def set_floating(window):
    if (window.window.get_wm_transient_for()
            or window.window.get_wm_type() in floating_types):
        window.floating = True

floating_types = ["notification", "toolbar", "splash", "dialog"]


follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(float_rules=[
    # Run the utility of `xprop` to see the wm class and name of an X client.
    *layout.Floating.default_float_rules, 
    Match(wm_class='confirmreset'),  # gitk
    Match(wm_class='makebranch'),  # gitk
    Match(wm_class='maketag'),  # gitk
    Match(wm_class='ssh-askpass'),  # ssh-askpass
    Match(title='branchdialog'),  # gitk
    Match(title='pinentry'),  # GPG key password entry
    Match(wm_class='Arcolinux-welcome-app.py'),
    Match(wm_class='Arcolinux-tweak-tool.py'),
    Match(wm_class='Arcolinux-calamares-tool.py'),
    Match(wm_class='confirm'),
    Match(wm_class='dialog'),
    Match(wm_class='download'),
    Match(wm_class='error'),
    Match(wm_class='file_progress'),
    Match(wm_class='notification'),
    Match(wm_class='splash'),
    Match(wm_class='toolbar'),
    Match(wm_class='Arandr'),
    Match(wm_class='feh'),
    Match(wm_class='Galculator'),
    Match(wm_class='arcolinux-logout'),
    Match(wm_class='xfce4-terminal'),

],  fullscreen_border_width = 0, border_width = 0)
auto_fullscreen = True

focus_on_window_activation = "focus" # or smart

wmname = "LG3D"
