from opencore.browser.base import BaseView
from opencore.interfaces import IOpenPage

class SiteContentBlock(BaseView):

    def source_page(self):
        path = self.portal.getProperty(self.key)
        if not path:
            raise KeyError("Property %s has not been set on the OpenCore site root" % self.key)
        page = self.portal.restrictedTraverse(path)
        return IOpenPage(page)
        
    def set_source_page(self, path):
        if self.source_page() is None:
            self.portal.manage_addProperty(self.key, path, "string")
        else:
            self.portal.manage_changeProperties(**{self.key: path})

    def __call__(self):
        try:
            try:
                page = self.source_page()
            except KeyError, e:
                if not self.admin_loggedin():
                    raise
                return str(e)
            except AttributeError, e:
                if not self.admin_loggedin():
                    raise
                return "No wiki page exists at %s" % self.portal.getProperty(self.key)
            except TypeError, e:
                if not self.admin_loggedin():
                    raise
                return "The page at %s is not a wiki page, but we need a wiki page" % (
                    self.portal.getProperty(self.key))
        except:
            return ''
        return page.restrictedTraverse("@@raw-view")()
            
class AboutBlock(SiteContentBlock):
    key = "sitecontent_aboutblock"

class BecomingAMemberBlock(SiteContentBlock):
    key = "sitecontent_becomingamember"

