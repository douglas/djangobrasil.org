# -*- coding: utf-8 -*-
#
#  Copyright (c) 2008 The Django Brasil Community Website Authors
#
#  This file is part of Django Brasil Project Site.
#
#  Django Brasil Project is free software; you can redistribute it
#  and/or modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 3 of
#  the License, or (at your option) any later version.
#
#  Django Brasil Project is distributed in the hope that it will be
#  useful, but WITHOUT ANY WARRANTY; without even the implied warranty
#  of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program. If not, see <http://www.gnu.org/licenses/>.
#

import twitter
import urllib, urllib2
from django.conf import settings

def post_feed_on_twitter(sender, instance, *args, **kwargs):
    """
    Post the new feed items on twitter.
    """

    # avoid to post the same item twice
    if not kwargs.get('created'):
        return False

    # there's no twitter account configured
    try:
        username = settings.TWITTER_USERNAME
        password = settings.TWITTER_PASSWORD
    except AttributeError:
        print 'Twitter account not configured.'
        return False
    
    # tinyurl'ze the feed item link
    create_api = 'http://tinyurl.com/api-create.php'
    fitem_data = urllib.urlencode(dict(url=instance.link))
    fitem_link = urllib2.urlopen(create_api, data=fitem_data).read().strip()

    # create the twitter message
    fitem_title = instance.title.decode('utf-8')
    twitter_msg = '%s - %s' % (fitem_title, fitem_link)
    if len(twitter_msg) > settings.TWITTER_MAXLENGTH:
        remove = len(twitter_msg + '...')-settings.TWITTER_MAXLENGTH
        twitter_msg = '%s... - %s' % (fitem_title[:-remove], fitem_link)

    try:
        twitter_api = twitter.Api(username, password)
        twitter_api.PostUpdate(twitter_msg)
    except urllib2.HTTPError, ex:
        print str(ex)
        return False
