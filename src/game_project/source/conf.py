import os 
import sys 
sys.path.insert(0, os.path.abspath('../../'))

# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'game'
copyright = '2023, linseypy, rivenmau, falarm'
author = 'linseypy, rivenmau, falarm'
release = '1.0.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [ "sphinx.ext.autodoc", "sphinx.ext.napoleon", 'sphinx.ext.coverage',]

autodoc_default_options = {
    'undoc-members': True,
    'show-inheritance': True,
}
napoleon_google_docstring = True
napoleon_use_param = True
napoleon_use_ivar = True
napoleon_use_rtype = True


templates_path = ['_templates']
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
