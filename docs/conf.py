# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys

sys.path.insert(0, os.path.abspath(".."))

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "Meltano EDK"
copyright = "2022, Meltano Core Team and Contributors"
author = "Meltano Core Team and Contributors"
release = "0.0.1"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.autosummary",
    "sphinx_rtd_theme",
    "sphinx_copybutton",
    "myst_parser",
]

# Auto-parse markdown (using myst_parser) as well as RST
source_suffix = [".rst", ".md"]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# Show typehints in the description, along with parameter descriptions
autodoc_typehints = "signature"
autodoc_class_signature = "separated"

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_logo = "_static/img/logo.svg"
html_theme = "furo"
html_theme_options = {
    # general
    "source_repository": "https://github.com/meltano/sdk/",
    "source_branch": "main",
    "source_directory": "docs/",
    "sidebar_hide_name": True,
    # branding
    "light_css_variables": {
        "font-stack": "Hanken Grotesk,-apple-system,Helvetica,sans-serif",
        "color-foreground-primary": "#080216",
        "color-background-primary": "#E9E5FB",
        "color-link": "#3A64FA",
        "color-link-underline": "transparent",
        "color-link--hover": "#3A64FA",
        "color-link-underline--hover": "#3A64FA",
        # brand
        "color-brand-primary": "#311772",
        "color-brand-content": "#311772",
        # sidebar
        "color-sidebar-background": "#311772",
        "color-sidebar-search-background": "#E9E5FB",
        "color-sidebar-item-background--hover": "#18c3fa",
        "color-sidebar-item-expander-background--hover": "#311772",
        "color-sidebar-brand-text": "white",
        "color-sidebar-caption-text": "rgba(255, 255, 255, 0.7)",
        "color-sidebar-link-text": "white",
        "color-sidebar-link-text--top-level": "white",
    },
    "dark_css_variables": {
        "color-background-primary": "#080216",
        "color-link": "#18c3fa",
        "color-link--hover": "#18c3fa",
        "color-link-underline--hover": "#18c3fa",
        # brand
        "color-brand-content": "rgba(255, 255, 255, 0.7)",
        # sidebar
        "color-sidebar-search-background": "#080216",
    },
}


# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

html_css_files = [
    "css/custom.css",
]

# TODO: set this back to 3 after MyST-Parser 0.18.0 is released
myst_heading_anchors = 4
