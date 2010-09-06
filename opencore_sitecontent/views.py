from opencore.browser.base import BaseView
from opencore.interfaces import IOpenPage
from opencore.browser.formhandler import post_only

class ManageSiteContentBlocks(BaseView):
    def handle_request(self):
        if self.request.environ['REQUEST_METHOD'] != "POST":
            return

        project = self.request.form['project']
        project = 'projects/%s' % project
        
        for key in self.keys():
            value = self.request.form[key]
            if not value: 
                continue
            value = '%s/%s' % (project, value)
            self.set_source_page(key, value)

    def set_source_page(self, key, path):
        source_page = self.portal.getProperty(key)
        if source_page is None:
            self.portal.manage_addProperty(key, path, "string")
        else:
            self.portal.manage_changeProperties(**{key: path})
    
    def keys(self):
        return [
            "sitecontent_aboutblock",
            "sitecontent_becomingamember",
            "sitecontent_homepageaboutblock",
            ]

class SiteContentBlock(BaseView):

    def source_page(self):
        path = self.portal.getProperty(self.key)
        if not path:
            raise KeyError("Property %s has not been set on the OpenCore site root" % self.key)
        page = self.portal.restrictedTraverse(path)
        return IOpenPage(page)

    def __call__(self):
        is_admin = self.admin_loggedin()
        try:
            try:
                page = self.source_page()
            except KeyError, e:
                if not is_admin:
                    raise
                return str(e)
            except AttributeError, e:
                if not is_admin:
                    raise
                return "No wiki page exists at %s" % self.portal.getProperty(self.key)
            except TypeError, e:
                if not is_admin:
                    raise
                return "The page at %s is not a wiki page, but we need a wiki page" % (
                    self.portal.getProperty(self.key))
        except:
            return ''
        if is_admin:
            title = page.Title()
            url = page.absolute_url()
            manage_url = '%s/%s' % (self.portal.absolute_url(),
                                    'manage-site-content-blocks')
            flash = """
The content of this page block is being pulled in from <a href="%s">the wiki page &quot;%s&quot;</a>. 
As a site administrator, you can set a different wiki page to pull content 
from using <a href="%s">this form</a>.""" % (
                url, title, manage_url)
            self.addPortalStatusMessage(flash)
        return page.restrictedTraverse("@@raw-view")()
            
class AboutBlock(SiteContentBlock):
    key = "sitecontent_aboutblock"

class BecomingAMemberBlock(SiteContentBlock):
    key = "sitecontent_becomingamember"

class HomeAboutBlock(SiteContentBlock):
    key = "sitecontent_homepageaboutblock"
