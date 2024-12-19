# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Expreseau for QGIS 3'
copyright = '2024, Lucas FAGES'
author = 'Lucas FAGES'
release = '0.1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration
def setup(app):
    app.setup_extension('myst_parser')

extensions = [      # Pour générer la documentation à partir des docstrings
    'sphinx.ext.napoleon',       # Pour le support des formats Google et NumPy docstrings
    'sphinx.ext.viewcode',       # Pour générer des liens vers le code source dans la doc
    'sphinx.ext.intersphinx',
"myst_parser"    # Pour lier à la documentation d'autres projets
        # Thème Read the Docs
]


templates_path = ['_templates']

exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

language = 'fr'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
