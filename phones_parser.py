import builtins
import logging
import os
import re
from itertools import chain

more_than_11_digits_re = re.compile(r'\d{12,}')
digits_brackets_dashes_spaces_bounded_re = re.compile(r'(?<![\.=\w])[\d()\- ]+(?![\.=\d\w])')
non_digit_re = re.compile(r'\D')

logging.basicConfig()
logger = logging.getLogger('phones_crawler.parser')


def map_for_debug(f, lst):
    result = []
    for params in lst:
        value = f(params)
        result.append(value)
    return result


def filter_for_debug(function, container):
    result = []
    function = function if function is not None else lambda *args, **kwargs: True
    for el in container:
        cond = function(el)

        if cond:
            result.append(el)

    return result


if os.getenv('DEBUG'):
    builtins.filter = filter_for_debug
    builtins.map = map_for_debug


def phones_detected(string):
    # digits, brackets, dashes, spaces that is bounded with separator
    it = map(lambda m: m.group(), digits_brackets_dashes_spaces_bounded_re.finditer(string))

    # drop tokens that has too few digits (7 digits sequence
    # considered a Moscow city phone without city phone code)
    it = filter(lambda token: len(re.sub(non_digit_re, '', token)) >= 7, it)

    # not too long sequences of digits (phones in Russia
    # always 10-digits sequences). split() used because chars
    # before and after too-long-sequence should not be merged
    it = chain.from_iterable(map(lambda token: re.split(more_than_11_digits_re, token), it))
    it = filter(None, it)

    yield from (x for x in it)


def format_phone(phone):
    phone = re.sub(non_digit_re, '', phone)

    if len(phone) == 7:
        return '8495%s' % phone

    if len(phone) not in {10, 11}:
        logger.debug('Discard too long or too short phone: %s', phone)
        return

    if len(phone) == 11:
        if phone[0] in {'7', '8'}:
            return '8%s' % phone[1:]
        else:
            logger.debug('Discard phone not started with 7 or 8: %s', phone)
            return
    if len(phone) == 10:
        if phone[0] not in {'3', '4', '8', '9'}:
            logger.debug('Discard phone not started with 3, 4, 8 or 9: %s', phone)
            return
        return '8%s' % phone

    logger.debug('Discard phone (found no reason to accept): %s', phone)


def parse(it):
    it = chain.from_iterable(map(phones_detected, it))
    it = map(format_phone, it)
    return filter(None, it)
