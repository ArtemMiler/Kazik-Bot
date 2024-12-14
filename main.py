from Logic import SlotCheck, SlotSpin

my_spin = SlotSpin()
print(my_spin)

check = SlotCheck()
check.check_win(my_spin.get_slot)
print(f"\n{check}")
print(f"\nWays: {check.ways}")
print(f"\n{check.dict_for_rows}")

my_spin = SlotSpin()
print(my_spin)
check.check_win(my_spin.get_slot)
print(f"\n{check}")
print(f"\nWays: {check.ways}")
print(f"\n{check.dict_for_rows}")
