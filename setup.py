import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.md')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

requires = [
    'django',
    'pgintranet'
    ]

setup(name='pu_in_favorites',
      version="1.0.0a",
      description='PythonUnited Intranet Favorites',
      long_description=README + '\n\n' +  CHANGES,
      classifiers=[
        "Development Status :: 3 - Alpha",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: Freely Distributable",
        "Programming Language :: Python",
        "Topic :: Internet :: WWW/HTTP :: Site Management",
        "Topic :: Software Development :: Libraries :: Application Frameworks"
        ],
      author='PythonUnited',
      author_email='info@pythonunited.com',
      license='beer-ware',
      url='https://github.com/PythonUnited/pu.intranet.favorites',
      keywords='Django Intranet Favorites',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires = requires,
      tests_require= requires,
      test_suite="pu-in-favorites",
      entry_points = """\
      [pu.in.app]
      urls=pu_in_favorites:get_urls
      """
      )
