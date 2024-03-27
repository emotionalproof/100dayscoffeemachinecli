from data import MENU
import math

profit = 0
resources = {
    "water": 300,
    "milk": 200,
    "coffee": 100,
}


def coffee_selection():
    """Receive order input from user, validate for correct options, and return the order string"""
    options = ["e", "c", "l"]
    order = input("  What would you like? Espresso, Cappuccino, or Latte?  ").lower()
    if order[0] not in options:
        coffee_selection()
    else:
        return order


def check_resources(needed):
    """Iterate over order resources and compare with supply"""
    for resource in needed:
        if needed[resource] > resources[resource]:
            return resource
        else:
            return True


def adjust_resources(needed, reverse):
    """Reduce the supplies needed for order from total supplies"""
    reducer = 1
    if reverse:
        reducer = -1
    for resource in needed:
        resources[resource] -= needed[resource] * reducer


def get_coins():
    """Get input from user for each coin type."""
    coins = {
        "25": int(input("How many quarters?  ")),
        "10": int(input("How many dimes?  ")),
        "5": int(input("How many nickels?  ")),
        "1": int(input("How many pennies?  "))
    }
    return coins


def check_total(coins, order):

    cost = MENU[order]['cost']
    cents = cost * 100
    total = 0
    for coin in coins:
        change_amount = int(coin) * coins[coin]
        total += change_amount
    if total < cents:
        return False
    else:
        return cents


def check_coin(coin, change):
    coin_type = int(coin)
    coin_count = change["coins"][coin]
    divisible = math.floor(change["remaining"] / coin_type)
    if divisible > coin_count:
        divisible = coin_count
    change["remaining"] -= (divisible * coin_type)
    change["refund"] += coin_type * (coin_count - divisible)
    return change


def calculate(coins, cents):
    """Calculates the amount of change from each coin that will be returned to customer."""
    change = {
        "coins": coins,
        "remaining": cents,
        "refund": 0
    }
    for coin in change['coins']:
        change = check_coin(coin, change)
    if change["refund"] > 0:
        refund = float(change["refund"]/100)
        formatted_refund = format(refund, '.2f')
        print(f"Here is ${formatted_refund} in change.")

def get_change(coins, order):
    cents = check_total(coins, order)
    if not cents:
        print("Sorry, that's not enough money. Money refunded.")
        adjust_resources(MENU[order]["ingredients"], True)
        init()
        return
    else:
        calculate(coins, cents)


def init():
    order = coffee_selection()
    needed_resources = MENU[order]['ingredients']
    supply = check_resources(needed_resources)
    if supply != True:
        print(f"Sorry, there is not enough {supply}.")
        init()
        return
    adjust_resources(needed_resources, False)
    coins = get_coins()
    get_change(coins, order)
    print(f"Here is your {order} ☕️ .  Enjoy!")
    init()


init()
