from django.conf.urls.defaults import patterns, url, include
from django.core.urlresolvers import reverse
from django.shortcuts import redirect

from addons.urls import ADDON_ID
from . import views


# These will all start with /addon/<addon_id>/
addon_patterns = patterns('',
    url('^$', views.addon_detail, name='discovery.addons.detail'),
    url('^eula/(?P<file_id>\d+)?$', views.addon_eula,
        name='discovery.addons.eula'),
)

browser_re = '(?P<version>[^/]+)/(?P<platform>[^/]+)'
compat_mode_re = '(?:/(?P<compat_mode>strict|normal|ignore))?'


def pane_redirect(req, **kw):
    if not kw.get('compat_mode'):
        kw['compat_mode'] = 'strict'
    return redirect(reverse('discovery.pane', kwargs=kw), permanent=True)


urlpatterns = patterns('',
    # Force the match so this doesn't get picked up by the wide open
    # /:version/:platform regex.
    ('^addon/%s$' % ADDON_ID,
     lambda r, addon_id: redirect('discovery.addons.detail',
                                  addon_id, permanent=True)),
    url('^addon/%s/' % ADDON_ID, include(addon_patterns)),

    url('^pane/account$', views.pane_account, name='discovery.pane.account'),
    url('^pane/(?P<section>featured|up-and-coming)/%s$' % browser_re,
        views.pane_more_addons, name='discovery.pane.more_addons'),
    url('^recs/%s$' % browser_re,
        views.recommendations, name='discovery.recs'),
    url('^%s$' % (browser_re + compat_mode_re), pane_redirect),
    url('^pane/%s$' % (browser_re + compat_mode_re), views.pane,
        name='discovery.pane'),
    url('^modules$', views.module_admin, name='discovery.module_admin'),
    url('^what-the-rec$', views.recs_debug, name='discovery.recs.debug'),
)
