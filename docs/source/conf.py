# -*- coding: utf-8 -*-
#
# pox documentation build configuration file, created by
# sphinx-quickstart on Tue Aug  8 06:50:58 2017.
#
# This file is execfile()d with the current directory set to its
# containing dir.
#
# Note that not all possible configuration values are present in this
# autogenerated file.
#
# All configuration values have a default; values that are commented out
# serve to show the default.

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
from datetime import datetime
import sys
scripts = os.path.abspath('../../scripts')
sys.path.insert(0, scripts)
try:
    os.symlink(scripts+os.sep+'pox', scripts+os.sep+'_pox.py')
except:
    pass

# Import the project
import pox

# -- General configuration ------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
#
# needs_sphinx = '1.0'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = ['sphinx.ext.autodoc',
    'sphinx.ext.intersphinx',
    'sphinx.ext.imgmath',
    'sphinx.ext.ifconfig',
    'sphinx.ext.napoleon']

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
#
# source_suffix = ['.rst', '.md']
source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'

# General information about the project.
project = 'pox'
year = datetime.now().year
copyright = '%d, The Uncertainty Quantification Foundation' % year
author = 'Mike McKerns'

# extension config
github_project_url = "https://github.com/uqfoundation/pox"
autoclass_content = 'both'
autodoc_default_options = {
    'members': True,
    'undoc-members': True,
    'private-members': True,
    'special-members': True,
    'show-inheritance': True,
    'imported-members': True,
    'exclude-members': (
        '__dict__,'
        '__slots__,'
        '__weakref__,'
        '__module__,'
        '_abc_impl,'
        '__init__,'
        '__annotations__,'
        '__dataclass_fields__,'
    )
}
autodoc_typehints = 'description'
autodoc_typehints_format = 'short'
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_ivar = True
napoleon_use_param = True

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# The short X.Y version.
version = pox.__version__
# The full version, including alpha/beta/rc tags.
release = version

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = 'en'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This patterns also effect to html_static_path and html_extra_path
exclude_patterns = []

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = False

# Configure how the modules, functions, etc names look
add_module_names = False
modindex_common_prefix = ['pox.']


# -- Options for HTML output ----------------------------------------------

# on_rtd is whether we are on readthedocs.io
on_rtd = os.environ.get('READTHEDOCS', None) == 'True'

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
if not on_rtd:
    html_theme = 'alabaster' #'bizstyle'
   #import sphinx_rtd_theme
   #html_theme = 'sphinx_rtd_theme'
   #html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
#
html_theme_options = {
    'github_user': 'uqfoundation',
    'github_repo': 'pox',
    'github_button': False,
    'github_banner': True,
    'travis_button': True,
    'gratipay_user': False,  # username
    'extra_nav_links': {'Module Index': 'py-modindex.html'},
#   'show_related': True,
    'show_powered_by': False
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# Custom sidebar templates, must be a dictionary that maps document names
# to template names.
#
# This is required for the alabaster theme
# refs: http://alabaster.readthedocs.io/en/latest/installation.html#sidebars
#if html_theme == 'alabaster':
html_sidebars = {
    '**': [
        'about.html',
#       'navigation.html',
        'localtoc.html', # display the toctree
        'relations.html', # needs 'show_related':True option to display
        'searchbox.html',
        'donate.html', # needs 'gratipay_user':<uname> option to display
    ]
}
#FIXME: donate / UQFoundation (home/github)


# -- Options for HTMLHelp output ------------------------------------------

# Output file base name for HTML help builder.
htmlhelp_basename = 'poxdoc'

# Logo for sidebar
html_logo = 'pathos.png'


# -- Options for LaTeX output ---------------------------------------------

latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    #
    # 'papersize': 'letterpaper',

    # The font size ('10pt', '11pt' or '12pt').
    #
    # 'pointsize': '10pt',

    # Additional stuff for the LaTeX preamble.
    #
    # 'preamble': '',

    # Latex figure (float) alignment
    #
    # 'figure_align': 'htbp',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    (master_doc, 'pox.tex', 'pox Documentation',
     'Mike McKerns', 'manual'),
]


# -- Options for manual page output ---------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    (master_doc, 'pox', 'pox Documentation',
     [author], 1)
]


# -- Options for Texinfo output -------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (master_doc, 'pox', 'pox Documentation',
     author, 'pox', 'Utilities for filesystem exploration and automated builds.',
     'Miscellaneous'),
]




# Example configuration for intersphinx: refer to the Python standard library.
intersphinx_mapping = {'https://docs.python.org/3/': None}
#    {'python': {'https://docs.python.org/': None},
#     'mystic': {'https://mystic.readthedocs.io/en/latest/', None},
#     'pathos': {'https://pathos.readthedocs.io/en/latest/', None},
#     'klepto': {'https://klepto.readthedocs.io/en/latest/', None},
#     'dill': {'https://dill.readthedocs.io/en/latest/', None},
#     'multiprocess': {'https://multiprocess.readthedocs.io/en/latest/', None},
#     'ppft': {'https://ppft.readthedocs.io/en/latest/', None},
#     'pyina': {'https://pyina.readthedocs.io/en/latest/', None},
#    }

