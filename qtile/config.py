# ~/.config/qtile/config.py

# Import modules
from typing import List
from libqtile import bar, layout, widget, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
import os
import subprocess
from qtile_extras.widget import PulseVolume

# Define keys
mod = "mod4"  # Windows key
terminal = "alacritty"
browser = "microsoft-edge-stable"

# Keys
keys = [
    # Window navigation
    Key([mod], "Left", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "Right", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "Down", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "Up", lazy.layout.up(), desc="Move focus up"),

    # Shuffle window
    Key([mod, "shift"], "Left", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "Right", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "Down", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "Up", lazy.layout.shuffle_up(), desc="Move window up"),

    # Resize window
    Key([mod, "control"], "Left", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "Right", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "Down", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "Up", lazy.layout.grow_up(), desc="Grow window up"),

    # To confuse to categorize it
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    Key([mod], "f", lazy.window.toggle_fullscreen()),
    Key([mod, "shift"], "Return", lazy.layout.toggle_split(), desc="Toggle between split and unsplit sides of stack",),
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "q", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),

    # Launch apps
    Key([mod], "d", lazy.spawn("rofi -show drun")),
    Key([mod], "b", lazy.spawn(browser)),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    Key([mod],"e", lazy.spawn("thunar"), desc='file manager'),
    Key([mod], "h", lazy.spawn("roficlip"), desc='clipboard'),
    Key([mod], "s", lazy.spawn("flameshot gui"), desc='Screenshot'),
    
    # Volume up
    Key([], "XF86AudioRaiseVolume", lazy.spawn(
       'bash -c "wpctl set-volume @DEFAULT_AUDIO_SINK@ 5%+ && '
       'vol=$(wpctl get-volume @DEFAULT_AUDIO_SINK@ | awk \'{print int($2 * 100)}\') && '
       'dunstify -h int:value:$vol -i audio-volume-high -t 2000 \'Volume Up\'"'
    )),

    # Volume down
    Key([], "XF86AudioLowerVolume", lazy.spawn(
       'bash -c "wpctl set-volume @DEFAULT_AUDIO_SINK@ 5%- && '
       'vol=$(wpctl get-volume @DEFAULT_AUDIO_SINK@ | awk \'{print int($2 * 100)}\') && '
       'dunstify -h int:value:$vol -i audio-volume-low -t 2000 \'Volume Down\'"'
    )),

    # Mute toggle
    Key([], "XF86AudioMute", lazy.spawn(
       'bash -c "wpctl set-mute @DEFAULT_AUDIO_SINK@ toggle && '
       'mute_state=$(wpctl get-mute @DEFAULT_AUDIO_SINK@ | awk \'{print $2}\') && '
       'if [ $mute_state = true ]; then '
       'dunstify -i audio-volume-muted -t 2000 \'Muted\'; '
       'else '
       'dunstify -i audio-volume-high -t 2000 \'Unmuted\'; '
       'fi"'
    )),

    # Media controls with playerctl
    Key([], "XF86AudioPlay", lazy.spawn("playerctl play-pause"), desc='playerctl play-pause'),
    Key([], "XF86AudioPrev", lazy.spawn("playerctl previous"), desc='playerctl previous'),
    Key([], "XF86AudioNext", lazy.spawn("playerctl next"), desc='playerctl next'),

    # Brightness controls with brightnessctl and notifications
    Key([], "XF86MonBrightnessUp", lazy.spawn(
       "bash -c 'brightnessctl set 5%+ && "
       "current=$(brightnessctl get) && max=$(brightnessctl max) && "
       "percent=$(( current * 100 / max )) && "
       "dunstify -h int:value:$percent -i display-brightness-high -t 2000 \"Brightness Up\"'"
   )),
   Key([], "XF86MonBrightnessDown", lazy.spawn(
       "bash -c 'brightnessctl set 5%- && "
       "current=$(brightnessctl get) && max=$(brightnessctl max) && "
       "percent=$(( current * 100 / max )) && "
       "dunstify -h int:value:$percent -i display-brightness-low -t 2000 \"Brightness Down\"'"
   )),
]

# Groups
groups = [Group(i) for i in "123456789"]
for i in groups:
    keys.extend(
        [
            # mod + group number = switch to group
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc=f"Switch to group {i.name}",
            ),
            # mod + shift + group number = switch to & move focused window to group
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=True),
                desc=f"Switch to & move focused window to group {i.name}",
            ),
            # Or, use below if you prefer not to switch to that group.
            # # mod + shift + group number = move focused window to group
            # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
            #     desc="move focused window to group {}".format(i.name)),
        ]
    )

# Layouts
lay_config = {
    "border_width": 4,
    "margin": 10,
    "border_focus": "#88c0d0",
    "border_normal": "#4c566a",
    "font": "FiraCode Nerd Font",
    "grow_amount": 1,
}

layouts = [
    layout.Bsp(**lay_config, fair=False, border_on_single=True),
    layout.Columns(
        **lay_config,
        border_on_single=True,
        num_columns=2,
        split=False,
    ),
    layout.Floating(**lay_config),
    layout.Max(**lay_config),
]

widget_defaults = {
    "font": "CaskaydiaCove NF Bold",
    "fontsize": 12,
    "padding": 10,
}

extension_defaults = widget_defaults.copy()

# Bar
screens = [
    Screen(
        top=bar.Bar(
            [
                widget.Spacer(length=15, background='#2E3440'),

                widget.Image(
                    filename='~/.config/qtile/Assets/launch_Icon.png',
                    margin=2,
                    background='#2E3440',
                    mouse_callbacks={'Button1': lazy.spawn("sh -c ~/.config/qtile/powermenu.sh")},
                ),

                widget.Image(filename='~/.config/qtile/Assets/6.png'),

                widget.GroupBox(
                    font="JetBrainsMono Nerd Font",
                    fontsize=16,
                    borderwidth=3,
                    highlight_method='block',
                    active='#8FBCBB',
                    block_highlight_text_color="#81A1C1",
                    highlight_color='#3B4252',
                    inactive='#2E3440',
                    foreground='#4C566A',
                    background='#3B4252',
                    this_current_screen_border='#3B4252',
                    this_screen_border='#3B4252',
                    other_current_screen_border='#3B4252',
                    other_screen_border='#3B4252',
                    urgent_border='#3B4252',
                    rounded=True,
                    disable_drag=True,
                ),

                widget.Spacer(length=8, background='#3B4252'),

                widget.Image(filename='~/.config/qtile/Assets/1.png'),

                widget.CurrentLayoutIcon(
                    custom_icon_paths=["~/.config/qtile/Assets/layout"],
                    background='#3B4252',
                    scale=0.50,
                ),

                widget.Image(filename='~/.config/qtile/Assets/5.png'),

                widget.TextBox(
                    text=" ",
                    font="Font Awesome 6 Free Solid",
                    fontsize=13,
                    background='#2E3440',
                    foreground='#8FBCBB',
                    mouse_callbacks={'Button1': lazy.spawn("rofi -show drun")},
                ),
                widget.TextBox(
                    fmt='Search',
                    background='#2E3440',
                    font="JetBrainsMono Nerd Font Bold",
                    fontsize=13,
                    foreground='#8FBCBB',
                    mouse_callbacks={'Button1': lazy.spawn("rofi -show drun")},
                ),

                widget.Image(filename='~/.config/qtile/Assets/4.png'),

                widget.WindowName(
                    background='#3B4252',
                    font="JetBrainsMono Nerd Font Bold",
                    fontsize=13,
                    empty_group_string="Desktop",
                    max_chars=130,
                    foreground='#8FBCBB',
                ),

                widget.Image(filename='~/.config/qtile/Assets/3.png'),

                widget.Systray(background='#2E3440', fontsize=2),
                widget.TextBox(text=' ', background='#2E3440'),

                widget.Image(filename='~/.config/qtile/Assets/6.png', background='#3B4252'),

                widget.TextBox(
                    text="",
                    font="Font Awesome 6 Free Solid",
                    fontsize=13,
                    background='#3B4252',
                    foreground='#8FBCBB',
                ),
                widget.Memory(
                    background='#3B4252',
                    format='{MemUsed: .0f}{mm}',
                    foreground='#8FBCBB',
                    font="JetBrainsMono Nerd Font Bold",
                    fontsize=13,
                    update_interval=5,
                ),

                widget.Image(filename='~/.config/qtile/Assets/2.png'),
                widget.Spacer(length=8, background='#3B4252'),

                widget.TextBox(
                    text=" ",
                    font="Font Awesome 6 Free Solid",
                    fontsize=13,
                    background='#3B4252',
                    foreground='#8FBCBB',
                ),

                widget.Battery(
                    font="JetBrainsMono Nerd Font Bold",
                    fontsize=13,
                    background='#3B4252',
                    foreground='#8FBCBB',
                    format='{percent:2.0%}',
                ),

                widget.Image(filename='~/.config/qtile/Assets/2.png'),
                widget.Spacer(length=8, background='#3B4252'),

		widget.TextBox(
		    text=" ",
		    font="Font Awesome 6 Free Solid",
		    fontsize=13,
		    background='#3B4252',
		    foreground='#8FBCBB',
		    mouse_callbacks={
		        'Button1': lazy.spawn(
		            "bash -c 'brightnessctl set 5%+ && "
			    "current=$(brightnessctl get) && max=$(brightnessctl max) && "
   		            "percent=$(( current * 100 / max )) && "
		            "dunstify -h int:value:$percent -i display-brightness-high -t 2000 \"Brightness Up\"'"
	                ),
		        'Button3': lazy.spawn(
		            "bash -c 'brightnessctl set 10%- && "
			    "current=$(brightnessctl get) && max=$(brightnessctl max) && "
  		            "percent=$(( current * 100 / max )) && "
  		            "dunstify -h int:value:$percent -i display-brightness-low -t 2000 \"Brightness Down\"'"
        		),
		    },
		),

                widget.Backlight(
                    backlight_name='intel_backlight',
                    font="JetBrainsMono Nerd Font Bold",
                    fontsize=13,
                    background='#3B4252',
                    foreground='#8FBCBB',
                    format='{percent:2.0%}',
                ),

		widget.TextBox(
		    text="",  # Font Awesome volume icon
		    font="Font Awesome 6 Free Solid",
		    fontsize=13,
		    background="#3B4252",
		    foreground="#8FBCBB",
		    mouse_callbacks={
                    	'Button1': lazy.spawn(
			    'bash -c "wpctl set-volume @DEFAULT_AUDIO_SINK@ 5%+ && '
		            'vol=$(wpctl get-volume @DEFAULT_AUDIO_SINK@ | awk \'{print int($2 * 100)}\') && '
		            'dunstify -h int:value:$vol -i audio-volume-high -t 2000 \'Volume Up\'"'
                        ),
                        'Button3': lazy.spawn(
			    'bash -c "wpctl set-volume @DEFAULT_AUDIO_SINK@ 5%- && '
       		       	    'vol=$(wpctl get-volume @DEFAULT_AUDIO_SINK@ | awk \'{print int($2 * 100)}\') && '
 		            'dunstify -h int:value:$vol -i audio-volume-low -t 2000 \'Volume Down\'"'
                        ),
                    },
                ),

		widget.GenPollText(
		    update_interval=1,
		    background="#3B4252",
		    foreground="#8FBCBB",
		    fontsize=13,
		    font="JetBrainsMono Nerd Font Bold",
		    func=lambda: subprocess.getoutput("pamixer --get-volume-human"),
		),

                widget.Image(filename='~/.config/qtile/Assets/5.png', background='#3B4252'),

                widget.TextBox(
                    text=" ",
                    font="Font Awesome 6 Free Solid",
                    fontsize=13,
                    background='#2E3440',
                    foreground='#8FBCBB',
                ),

                widget.Clock(
                    format='%I:%M %p',
                    background='#2E3440',
                    foreground='#8FBCBB',
                    font="JetBrainsMono Nerd Font Bold",
                    fontsize=13,
                ),

                widget.Spacer(length=15, background='#2E3440'),
            ],
            30,
            border_color='#2E3440',
            border_width=[0, 0, 0, 0],
            margin=[10, 10, 5, 10],
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
floats_kept_above = True
cursor_warp = False
floating_layout = layout.Floating(
    border_focus="#88c0d0",   # nord8
    border_normal="#4c566a",  # nord3
    border_width=4,
    float_rules=[
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),    # gitk
        Match(wm_class="maketag"),       # gitk
        Match(wm_class="ssh-askpass"),   # ssh-askpass
        Match(title="branchdialog"),     # gitk
        Match(title="pinentry"),         # GPG key password entry
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

@hook.subscribe.startup
def autostart():
      home = os.path.expanduser('~/.config/qtile/autostart.sh')
      subprocess.call([home])

wmname = "Qtile"
