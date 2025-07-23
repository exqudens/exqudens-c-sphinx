# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html
import sys
import inspect
from pathlib import Path
from datetime import datetime

# sphinx
import sphinx.util
from sphinx.application import Sphinx
from sphinx.config import Config

# mlx.traceability
import mlx.traceability

# local
sys.path.append(Path(__file__).parent.as_posix())
from conf_util import ConfUtil

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

logger = sphinx.util.logging.getLogger(__name__)
logger.info('-- bgn')
# conf_json = json.loads(Path(__file__).parent.joinpath('conf.json').read_text())
project_dir: str = Path(__file__).parent.parent.as_posix()
logger.info(f"-- projectDir: '{project_dir}'")
project: str = Path(project_dir).joinpath('name-version.txt').read_text().split(':')[0].strip()
logger.info(f"-- project: '{project}'")
copyright: str = '2023, exqudens'
author: str = 'exqudens'
release: str = Path(project_dir).joinpath('name-version.txt').read_text().split(':')[1].strip()
logger.info(f"-- release: '{release}'")
rst_prolog = '.. |project| replace:: ' + project + '\n\n'
rst_prolog += '.. |release| replace:: ' + release + '\n\n'
project_types_config: dict[str, object] = {
    'docx': {
        'index': (
            'index',
            'Documentation.docx',
            {
                'title': 'Documentation',
                'created': datetime.now().strftime('%Y-%m-%dT%H:%M:%S'),
                'subject': project + '-' + release,
                'keywords': ['sphinx']
            },
            False
        ),
        'modules': (
            'modules/modules-toctree',
            'Modules_Documentation.docx',
            {
                'title': 'Modules Documentation',
                'created': datetime.now().strftime('%Y-%m-%dT%H:%M:%S'),
                'subject': project + '-' + release,
                'keywords': ['sphinx']
            },
            False
        ),
        'files': (
            'files/files-toctree',
            'Files_Documentation.docx',
            {
                'title': 'Files Documentation',
                'created': datetime.now().strftime('%Y-%m-%dT%H:%M:%S'),
                'subject': project + '-' + release,
                'keywords': ['sphinx']
            },
            False
        ),
        'modules2files': (
            'modules2files/modules2files',
            'Modules_To_Files_Documentation.docx',
            {
                'title': 'Modules To Files Documentation',
                'created': datetime.now().strftime('%Y-%m-%dT%H:%M:%S'),
                'subject': project + '-' + release,
                'keywords': ['sphinx']
            },
            False
        )
    },
    'pdf': {
        'index': (
            'index',
            'Documentation',
            release,
            author
        ),
        'modules': (
            'modules/modules-toctree',
            'Modules_Documentation',
            release,
            author
        ),
        'files': (
            'files/files-toctree',
            'Files_Documentation',
            release,
            author
        ),
        'modules2files': (
            'modules2files/modules2files',
            'Modules_To_Files_Documentation',
            release,
            author
        )
    }
}

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

# -- Options for TRACEABILITY output -------------------------------------------------
# https://melexis.github.io/sphinx-traceability-extension/configuration.html#configuration

traceability_render_relationship_per_item = False
traceability_notifications = {
    'undefined-reference': 'UNDEFINED_REFERENCE'
}

def traceability_inspect_item(name, collection):
    ConfUtil.mlx_traceability_inspect_item(
        name=name,
        collection=collection,
        config={
            'module_': ['implemented_by']
        }
    )

# -- Options for BREATHE -------------------------------------------------
# https://breathe.readthedocs.io/en/latest/quickstart.html

breathe_projects = {
    'main': str(Path(project_dir).joinpath('build', 'doxygen', 'main', 'xml')),
    'main-no-group': str(Path(project_dir).joinpath('build', 'doxygen', 'main-no-group', 'xml'))
}
breathe_domain_by_extension = {
    'h': 'c',
    'c': 'c',
    'hpp': 'cpp',
    'cpp': 'cpp'
}
breathe_default_project = 'main' # conf_json.get('PROJECT_BREATHE_DEFAULT', 'main')

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = [str(Path(mlx.traceability.__file__).parent.joinpath('assets'))]

# -- Options for DOCX output -------------------------------------------------
# https://docxbuilder.readthedocs.io/en/latest/docxbuilder.html#usage

docx_documents = []
docx_coverpage = False
docx_style = Path(__file__).parent.joinpath('style.docx').as_posix() # '' if conf_json.get('PROJECT_DOCX_STYLE') is None else conf_json['PROJECT_DOCX_STYLE']
docx_pagebreak_before_section = 1 # int(conf_json.get('PROJECT_DOCX_PAGEBREAK_BEFORE_SECTION', '1'))

# -- Options for PDF output -------------------------------------------------
# https://rst2pdf.org/static/manual.html#sphinx

pdf_documents = []
pdf_use_toc = True
pdf_use_coverpage = False
#pdf_break_level = 2
#pdf_breakside = 'any'

# -- Project setup -----------------------------------------------------
def config_inited(app: Sphinx, config: Config) -> None:
    logger.info(f"-- [{inspect.currentframe().f_code.co_name}] bgn")

    logger.info(f"-- [{inspect.currentframe().f_code.co_name}] config.project_builder: '{config.project_builder}'")
    logger.info(f"-- [{inspect.currentframe().f_code.co_name}] config.project_types: {config.project_types}")

    builder_name: str = str(config.project_builder) if config.project_builder else ''

    if builder_name not in project_types_config:
        raise Exception(f"unsupported builder name: '{builder_name}' supported: {set(project_types_config.keys())}")

    project_types: list[str] = list(config.project_types) if config.project_types else ['']

    for index, value in enumerate(project_types):
        if not value:
            raise Exception(f"'project_types[{index}]' value is none or empty.")
        project_type: str = str(value)
        if project_type not in project_types_config[builder_name]:
            raise Exception(f"unsupported project type: '{project_type}' supported: {set(project_types_config[builder_name].keys())}")

        if builder_name == 'docx':
            config.docx_documents.append(project_types_config[builder_name][project_type])
        elif builder_name == 'pdf':
            config.pdf_documents.append(project_types_config[builder_name][project_type])

    logger.info(f"-- [{inspect.currentframe().f_code.co_name}] end")

def setup(app: Sphinx):
    app.add_config_value('project_builder', None, True)
    app.add_config_value('project_types', ['index'], True)

    ConfUtil.sphinx_setup(sphinx_application=app)

    app.connect('config-inited', config_inited)

logger.info('-- end')
