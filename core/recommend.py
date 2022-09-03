#  Copyright 2021 Coding for Kidz Project
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
# documentation files (the "Software"), to deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of
# the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
# THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
"""Finds what to recommend
Definition: Listener: Person who needs recommendations
Definition: Suggester: Person who suggests stuff
"""
import math
from math import sqrt


def prepare_lists(suggester: list, listener: list, items: list) -> list:
    """Prepares new comparison suggester being the suggester and listener being the listener"""
    new_suggester = []
    new_listener = []
    new_items = []
    for i in range(len(suggester)):
        item = suggester[i]
        if item != -1:
            new_suggester.append(item)
            new_listener.append(listener[i])
            new_items.append(items[i])
    return [new_listener, new_suggester, new_items]


def similarity(l1: list, l2: list) -> float:
    """Checks how close two lists are to each other"""
    sum_to_sqrt = 0
    for i in range(0, len(l1)):
        if (l1[i] != -1) and (l2[i] != -1):
            if l1[i] - l2[i] >= 0:
                temp = l1[i] - l2[i]
            else:
                temp = l2[i] - l1[i]
            sum_to_sqrt += temp**2
    return sqrt(sum_to_sqrt)


def weight(time: float) -> float:
    """Function"""
    r = (2**time) / (100 - time)  # nice curve
    if r <= 0:  # no negatives
        return 0
    return (2**time) / (100 - time)


def recommend(l1: list, l2: list, items: list) -> list:
    """Recommends things that l2 liked to l1 from order of most liked to least liked."""
    recommendations = {}
    for i in range(0, len(l1)):
        j = len(l1) - 1 - i  # does them backwards
        if l1[j] == -1:  # -1 means they have not read it
            recommendations[l2[j]] = items[j]
    # Sort them by the other persons ratings
    new_recommendations = []
    recommendations_keys = list(recommendations.keys())
    recommendations_keys.sort()
    recommendations_keys.reverse()
    for item in recommendations_keys:
        new_recommendations.append(recommendations[item])
    return new_recommendations


def is_eligible(l1, l2):
    """Checks if l1 is eligible to recommend stuff to l2"""
    not_viewed = []
    for item in l1:
        if item == -1:
            not_viewed.append(item)

    ticks = 0
    for item in l2:
        if (item == -1) and (item in not_viewed):
            ticks += 1

    if (ticks / len(not_viewed)) >= 0.5:
        return False

    ticks = 0
    for item in l2:
        if (item == -1) and (item not in not_viewed):
            ticks += 1

    if (ticks / len(not_viewed)) >= 0.5:
        return False
    return True


def find_recommendations(
    listener: list, peoples_preferences: list, items: list
) -> list:
    """Finds recommendations for listener when peoples_preferences is everyone else's preferences."""
    closeness = []
    for preference_list in peoples_preferences:
        if is_eligible(listener, preference_list):
            closeness.append(similarity(preference_list, listener))
        else:
            closeness.append(math.inf)  # Very large number
    lowest = 0  # lowest closeness index
    lowest_value = closeness[0]  # lowest value (lowest_value = closeness[lowest])
    for i in range(1, len(closeness)):  # Search for the closest lists
        if closeness[i] < lowest_value:
            lowest = i
            lowest_value = closeness[i]
    prepare = prepare_lists(peoples_preferences[lowest], listener, items)
    return recommend(prepare[0], prepare[1], prepare[2])
