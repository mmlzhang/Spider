
import random


def make_random_ticket():
    s = 'sadfwiueyiadhfkajrqijfalkjvoiroei12343238'
    ticket = ''
    for i in range(28):
        ticket += random.choice(s)
    return ticket


def random_num():
    pass