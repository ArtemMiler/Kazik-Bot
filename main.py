from Logic import Bonus, SlotCheck, SlotSpin, WinCount

for _ in range(5):

    my_spin = SlotSpin()
    print(my_spin)
    check = SlotCheck()
    check.check_win(my_spin.slot)
    print(f"\n{check}")
    print(f"\nWays: {check.ways}")
    print(f"\n{check.dict_for_rows}")
    my_win = WinCount(10)
    my_win.count_win(check)
    my_bonus = Bonus(my_spin.slot, my_win.bet)
    my_bonus.play_bonus(my_win.bet)

