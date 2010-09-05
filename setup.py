from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(name='opencore_sitecontent',
      version=version,
      description="build site-level pages from site content configured by site admins",
      long_description="""\
""",
      classifiers=[],
      keywords='',
      author='Ethan Jucovy',
      author_email='opencore-dev@lists.coactivate.org',
      url='',
      license='',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[

      ],
      entry_points="""
      [opencore.versions]
      opencore_sitecontent = opencore_sitecontent
      [topp.zcmlloader]
      opencore = opencore_sitecontent
      """,
      )