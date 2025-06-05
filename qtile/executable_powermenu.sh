options=" 󰒲  Suspend\n 󰜉  Restart\n 󰐥  Shutdown"
selected=$(echo -e "$options" | rofi -dmenu -p "" -l 3 -theme "$HOME"/.config/rofi/configpowermenu.rasi)

case "$selected" in
    " 󰐥  Shutdown")
        shutdown now
        ;;
    " 󰜉  Restart")
        reboot
        ;;
    " 󰒲  Suspend")
        systemctl suspend
        ;;
    *)
        echo "Invalid option!"
        ;;
esac
