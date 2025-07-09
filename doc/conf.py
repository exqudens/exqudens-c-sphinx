# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html
import sys
import json
from pathlib import Path
from datetime import datetime

# sphinx
import sphinx.util
from sphinx.application import Sphinx

# mlx.traceability
import mlx.traceability

# local
sys.path.append(Path(__file__).parent.as_posix())
from conf_util import ConfUtilDocUtils
from conf_util import ConfUtilDocxBuilder

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

logger = sphinx.util.logging.getLogger(__name__)
confJson = json.loads(Path(__file__).parent.joinpath('conf.json').read_text())
projectDir = confJson['PROJECT_DIR']
logger.info(f"-- projectDir: '{projectDir}'")
project = Path(projectDir).joinpath('name-version.txt').read_text().split(':')[0].strip()
logger.info(f"-- project: '{project}'")
copyright = '2023, exqudens'
author = 'exqudens'
release = Path(projectDir).joinpath('name-version.txt').read_text().split(':')[1].strip()
logger.info(f"-- release: '{release}'")
rst_prolog = '.. |project| replace:: ' + project + '\n\n'
rst_prolog += '.. |release| replace:: ' + release + '\n\n'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autosectionlabel',
    'linuxdoc.rstFlatTable',
    'breathe',
    'mlx.traceability',
    'docxbuilder',
    'rst2pdf.pdfbuilder'
]

templates_path = []
exclude_patterns = []

# -- Options for AUTO_SECTION_LABEL output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/extensions/autosectionlabel.html#configuration

autosectionlabel_prefix_document = True

# -- Options for docutils -------------------------------------------------
docutils_text_visited_nodes_size = 10

# -- Options for TRACEABILITY output -------------------------------------------------
# https://melexis.github.io/sphinx-traceability-extension/configuration.html#configuration

traceability_render_relationship_per_item = True
traceability_notifications = {
    'undefined-reference': 'UNDEFINED_REFERENCE'
}

# -- Options for BREATHE -------------------------------------------------
# https://breathe.readthedocs.io/en/latest/quickstart.html

breathe_projects = {
    'main': str(Path(projectDir).joinpath('build', 'doxygen', 'main', 'xml')),
    'test': str(Path(projectDir).joinpath('build', 'doxygen', 'test', 'xml'))
}
breathe_domain_by_extension = {
    'h': 'c',
    'c': 'c',
    'hpp': 'cpp',
    'cpp': 'cpp'
}
breathe_default_project = confJson['PROJECT_BREATHE_DEFAULT']

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = [str(Path(mlx.traceability.__file__).parent.joinpath('assets'))]

# -- Options for DOCX output -------------------------------------------------
# https://docxbuilder.readthedocs.io/en/latest/docxbuilder.html#usage

docx_documents = [
    (
        'index',
        confJson['PROJECT_TITLE'].replace(' ', '_') + '.docx',
        {
            'title': project + ' documentation',
            'created': datetime.now().strftime('%Y-%m-%dT%H:%M:%S'),
            'subject': project + '-' + release,
            'keywords': ['sphinx']
        },
        False
    )
]
docx_coverpage = False
docx_style = '' if confJson.get('PROJECT_DOCX_STYLE') is None else confJson['PROJECT_DOCX_STYLE']
docx_pagebreak_before_section = int('0' if confJson.get('PROJECT_DOCX_PAGEBREAK_BEFORE_SECTION') is None else confJson['PROJECT_DOCX_PAGEBREAK_BEFORE_SECTION'])

# -- Options for PDF output -------------------------------------------------
# https://rst2pdf.org/static/manual.html#sphinx

pdf_documents = [
    ('index', confJson['PROJECT_TITLE'].replace(' ', '_'), release, author)
]
pdf_use_toc = True
pdf_use_coverpage = False
#pdf_break_level = 2
#pdf_breakside = 'any'

# -- Project setup -----------------------------------------------------
def setup(app: Sphinx):

    ConfUtilDocUtils.initialize(logger)
    ConfUtilDocxBuilder.initialize(logger)
