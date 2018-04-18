# coding=utf-8

from datetime import datetime

from django.utils.translation import pgettext, ugettext as _

__all__ = ("date",)


def get_now(time):
    return datetime.now(time.tzinfo)


def date(time):
    now = get_now(time)

    if time > now:
        past = False
        diff = time - now
    else:
        past = True
        diff = now - time

    days = abs(time.date() - now.date()).days

    if days is 0 or diff.total_seconds() < 60 * 60 * 24:
        return get_small_increments(diff.seconds, past)
    else:
        return get_large_increments(days, past)


def get_small_increments(seconds, past):
    if seconds < 10:
        result = _(u'刚刚')
    elif seconds < 60:
        result = _pretty_format(seconds, 1, _(u'秒'), past)
    elif seconds < 120:
        result = past and _(u'1分钟前') or _('in a minute')
    elif seconds < 3600:
        result = _pretty_format(seconds, 60, _(u'分钟'), past)
    elif seconds < 7200:
        result = past and _(u'1小时前') or _('一小时后')
    else:
        result = _pretty_format(seconds, 3600, _(u'小时'), past)
    return result


def get_large_increments(days, past):
    if days == 1:
        result = past and _(u'昨天') or _(u'明天')
    elif days < 7:
        result = _pretty_format(days, 1, _(u'天'), past)
    elif days < 14:
        result = past and _(u'上周') or _(u'下周')
    elif days < 31:
        result = _pretty_format(days, 7, _(u'周'), past)
    elif days < 61:
        result = past and _(u'上个月') or _(u'下个月')
    elif days < 365:
        result = _pretty_format(days, 30, _(u'月'), past)
    elif days < 730:
        result = past and _(u'一年前') or _(u'next year')
    else:
        result = _pretty_format(days, 365, _(u'年'), past)
    return result


def _pretty_format(diff_amount, units, text, past):
    pretty_time = (diff_amount + units / 2) / units
    if past:
        base = pgettext(
            'Moment in the past',
            u"%(amount)d%(quantity)s前"
        )
    else:
        base = pgettext(
            'Moment in the future',
            u"%(amount)d %(quantity)s后"
        )
    return base % dict(amount=pretty_time, quantity=text)
