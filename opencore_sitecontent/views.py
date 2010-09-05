from opencore.browser.base import BaseView

class SiteContentBlock(BaseView):

    def source_page(self):
        path = self.portal.getProperty(self.key)
        page = self.portal.restrictedTraverse(path)
        return page

    def set_source_page(self, path):
        if self.source_page() is None:
            self.portal.manage_addProperty(self.key, path, "string")
        else:
            self.portal.manage_changeProperties(**{self.key: path})

    def __call__(self):
        page = self.source_page()
        return page.restrictedTraverse("@@raw-view")()
            
class AboutBlock(SiteContentBlock):
    key = "sitecontent_aboutblock"

class BecomingAMemberBlock(SiteContentBlock):
    key = "sitecontent_becomingamember"

