
from zope.interface import Interface
from zope.schema import TextLine
from zope.configuration.exceptions import ConfigurationError
from zope.configuration.fields import Path, GlobalInterface, GlobalObject
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from zope.security.zcml import Permission
from zope.app.component.back35 import LayerField

class IContentView(Interface):
    """
    Register an OpenCore SiteContent browser view for contexts of the given interface.

    A SiteContent view is not associated with a template.  Instead, it is associated
    with an IOpenPage on the site.  When the view is rendered, it dynamically pulls
    in the content of the IOpenPage it is associated with, and renders that content.

    This allows site users to manage blocks of content that are rendered as static
    blocks in the site.

    Each SiteContent view is associated with a string key. When the
    SiteContent view is called, it looks up its key as a property on
    the portal object.  The value of that key on the portal object is
    a traversal path, relative to the site root, to the IOpenPage that
    will be used to render the view.  For most uses this key should be
    unique, so that each SiteContent view can be independently associated
    with a wiki page, even if two SiteContent views happen to share a
    wiki page. However no uniqueness constraints are enforced, so if you
    want to force two SiteContent views to always share a wiki page, you
    can assign them the same key.

    This layer of separation allows (only) site administrators to assign content blocks
    to wiki pages, while allowing content development by any site user with permission
    to edit the given wiki page.

    When a SiteContent view is registered with the opencore:contentView directive,
    it is also added to the @@manage-site-content-blocks form.
    """

    for_ = GlobalInterface(
        title=u"The interface this view is for.",
        required=False
        )

    layer = LayerField(
        title=u"The layer the default view is declared for",
        description=u"The default layer for which the default view is "
                    u"applicable. By default it is applied to all layers.",
        required=False
        )

    permission = Permission(
        title=u"Permission",
        description=u"The permission needed to use the view.",
        required=True
        )

    name = TextLine(
        title=u"The name of the page (view)",
        description=u"""
        The name shows up in URLs/paths. For example 'foo' or
        'foo.html'. This attribute is required.""",
        required=True
        )

    key = TextLine(
        title=u"The unique key for this SiteContent view",
        description=u"""
        The key is used to identify a (SiteContent, IOpenPage)
        association. This key is stored as a property on the
        site root.""",
        required=True
        )

from Products.Five.browser.metaconfigure import page
from opencore_contentviews.views import SiteContentBlock
from opencore_contentviews import _registry

def factory(_context, name, permission, for_,
            layer=IDefaultBrowserLayer,
            allowed_interface=None, allowed_attributes=None,
            key=None,
            ):

    class_ = SiteContentBlock

    if key not in _registry:
        _registry.append(key)

    setattr(class_, 'key', key)

    page(_context, name, permission, for_,
         layer=layer, class_=class_,
         allowed_interface=allowed_interface,
         allowed_attributes=allowed_attributes)         
    
