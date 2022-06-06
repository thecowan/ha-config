import random
import re

import logging

from homeassistant.helpers import template

_LOGGER = logging.getLogger(__name__)

_TemplateEnvironment = template.TemplateEnvironment




def filterDict(dictObj, callback):
    newDict = dict()
    for (key, value) in dictObj.items():
        # Check if item satisfies the given condition then add to new dict
        if callback((key, value)):
            newDict[key] = value
    return newDict

def matches(source, target, regex):
    if regex:
        return re.match(target, source)
    else:
        return target in source

def keep_keys(input, match, regex = False):
    """Keeps all keys from the map which contain a string"""
    return filterDict(input, lambda elem: matches(elem[0], match, regex))

def keep_values(input, match, regex = False):
    """Keeps all entries in the map where the key contains a string"""
    return filterDict(input, lambda elem: matches(elem[1], match, regex))

def discard_keys(input, match, regex = False):
    """Discards all keys from the map which contain a string"""
    return filterDict(input, lambda elem: not matches(elem[0], match, regex))

def discard_values(input, match, regex = False):
    """Discards all entries in the map where the key contains a string"""
    return filterDict(input, lambda elem: not matches(elem[1], match, regex))


def random_entry(input):
    """Picks a random map entry"""
    return random.choice(list(input.items()))


#test_data = {"1 cat": "meow", "2 dogs": "woof", "3 sheep": "baa", "4 cows": "moo"}
#print("Keep key a:   " + str(keep_keys(test_data, "a")))
#print("Keep val o:   " + str(keep_values(test_data, "o")))
#print()
#print("Excl key a:   " + str(discard_keys(test_data, "a")))
#print("Excl val o:   " + str(discard_values(test_data, "o")))
#print()
#print("Keep regex:   " + str(keep_keys(test_data, r".*s$", True)))
#print("Excl regex:   " + str(discard_keys(test_data, r".*s$", True)))
#print()
#for i in range(1, 10):
#  print("Random entry: " + str(random_entry(test_data)))


def init(*args):
    """Initialize filters"""
    env = _TemplateEnvironment(*args)
    env.filters["keep_keys"] = keep_keys
    env.filters["keep_values"] = keep_values
    env.filters["discard_keys"] = discard_keys
    env.filters["discard_values"] = discard_values
    env.filters["random_entry"] = random_entry
    return env


template.TemplateEnvironment = init
template._NO_HASS_ENV.filters["keep_keys"] = keep_keys
template._NO_HASS_ENV.filters["keep_values"] = keep_values
template._NO_HASS_ENV.filters["discard_keys"] = discard_keys
template._NO_HASS_ENV.filters["discard_values"] = discard_values
template._NO_HASS_ENV.filters["random_entry"] = random_entry


async def async_setup(hass, hass_config):
    return True