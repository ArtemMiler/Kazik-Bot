from Logic import SlotSpin, WinCount

for _ in range(5):
    my_spin = SlotSpin()
    print(my_spin)

    my_win = WinCount(10)
    my_win.count_win(my_spin.slot)
