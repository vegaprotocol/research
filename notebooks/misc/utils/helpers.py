import math

def round_sd(number):
    significant_digits = 4
    return round(number, significant_digits - math.floor(math.log10(abs(number))) - 1)

def calculate_exit_price(order_book, position, market_dp):
    levels = order_book.sell
    if position > 0:
        levels = order_book.buy
    p = position
    v = 0
    exit_price = 0
    for lvl in levels:
        x = lvl.volume
        if lvl.volume > p:
            x = p
        exit_price += x*float(lvl.price)*10**(-market_dp)
        v+=x
        p-=x
        if p <= 0:
            break
    return exit_price / v

def calculate_slippage_per_unit(mark_price, order_book, open_volume, market_dp):
    if open_volume==0:
        return 0
    exit_price=calculate_exit_price(order_book,open_volume,market_dp)
    s = 1 if open_volume > 0 else -1
    return s*(mark_price - exit_price)

def delta_p_and_l(price, prev_price, open_volume):
    return open_volume*(price-prev_price)
    