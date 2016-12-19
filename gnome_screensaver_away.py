# -*- coding: utf-8 -*-
#
# Copyright 2016 Gerard Ryan <gerard@ryan.lt>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Changelog:
#
# 2016-11-05: Gerard Ryan <gerard@ryan.lt>
#     0.1.0 : Initial version
#
# 2016-12-17: Gerard Ryan <gerard@ryan.lt>
#     0.2.0 : Prevent changing manually-set away status
#
# Contributions welcome at:
# https://github.com/grdryn/weechat-gnome-screensaver-away

from __future__ import print_function

try:
    import dbus
    import weechat
except ImportError:
    print('This program is intended to be run by weechat, and expects the')
    print('dbus-python library to be installed.')

SCRIPT_NAME    = 'gnome-screensaver-away'
SCRIPT_AUTHOR  = 'Gerard Ryan <gerard@ryan.lt>'
SCRIPT_VERSION = '0.1.0'
SCRIPT_LICENSE = 'GPLv3+'
SCRIPT_DESC    = 'Set away status based on GNOME ScreenSaver status'

SCREENSAVER = dbus.SessionBus().get_object('org.gnome.ScreenSaver',
                                           '/org/gnome/ScreenSaver')

AWAY_MSG = 'I am away'

# TODO: track the away status of each IRC server independently
def check_away_status():
    away = (False, False)
    irc_servers = weechat.infolist_get("irc_server", "", "")

    while weechat.infolist_next(irc_servers):
        is_away = bool(weechat.infolist_integer(irc_servers, "is_away"))
        is_away_by_me = weechat.infolist_string(irc_servers, "away_message") == AWAY_MSG
        away = (is_away, is_away_by_me)

    return away

def check_screensaver_status(data, remaining_calls):
    away, auto_away = check_away_status()

    screensaver_on = SCREENSAVER.GetActive(
        dbus_interface='org.gnome.ScreenSaver')

    if screensaver_on and not away:
        weechat.command('', '/away -all {0}'.format(AWAY_MSG))
    elif away and auto_away and not screensaver_on:
        weechat.command('', '/away -all')

    return weechat.WEECHAT_RC_OK

if __name__ == '__main__':
    weechat.register(SCRIPT_NAME, SCRIPT_AUTHOR, SCRIPT_VERSION, SCRIPT_LICENSE,
                 SCRIPT_DESC, '', '')

    weechat.hook_timer(5000, 0, 0, 'check_screensaver_status', '')
