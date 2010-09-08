Motivation
==========

The base package ``opencore`` provides "site-level content" directly
in templates. This is simple -- the built-in i18n mechanisms can be
used to provide translated content, and you don't have to worry about
filling in any text when you're installing a new site.

However, a site will often want to replace these blocks of content
with their own custom text.

Also, a site will often want to let those blocks of content be created
or edited by certain non-technical users.  In these cases, the text
should be treated as managed content within the site's database,
instead of static text in a template on the filesystem.

The plugin ``opencore_sitecontent`` addresses these needs, providing a
mechanism for overriding any view (or registering a new view) to pull
its content from a designated wiki page within the site.

Overview
========

This plugin implicitly makes distinctions between four types of
people, based on their responsibilities and levels of trust:

 * System admin: a person with server access who is installing the
   site and knows how to install plugins, register overrides, etc, to
   customize the behavior of the OpenCore installation.

 * Site admin: a person who has full admin/manager privileges on the
   site,  but does not have direct filesystem access to the server.

 * Site content manager: a person who the site admin trusts to write
   and maintain the content that will appear in sitewide blurbs such
   as the "About" page or the "Becoming a member" widget -- but does
   not have full manager privileges on the site.

 * Regular user: any other user of the site.

These roles are not formally defined by this plugin -- they are the
roles that are assumed to exist between the humans running the site.

This plugin provides a ZCML directive <opencore:contentView> which
will register a new "ContentView", a view that pulls in its content
from a wiki page on the site.

Responsibilities
================

The system admin will register the set of ContentViews, and assign a
key to each ContentView.

The site admin will associate each key with a wiki page on the site.

The site content manager will edit the wiki pages associated with the
ContentViews.

For simplicity, there is a (light) assumption that all the wiki pages
associated with ContentViews are within the same project.  This lets
the site administrators create a single "Site Content Development"
project whose team members are all site content managers.

If this assumption is incorrect, it is possible to overrule it by
using the ZMI instead of the management view provided by this plugin.
This would be used if, for instance, you want one set of users able to
edit the About page text, but another set of users able to edit the
"Becoming a Member" text.
