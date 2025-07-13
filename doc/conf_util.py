import sys
import inspect
from typing import Any
from typing import List
from typing import Set
from typing import Dict
from typing import Deque

# docutils
import docutils.nodes
from docutils.nodes import Node as DocUtilsNode
from docutils.nodes import Text as DocUtilsText
from docutils.nodes import NodeVisitor
from docutils.nodes import TreePruningException

# sphinx
from sphinx.util.logging import SphinxLoggerAdapter
from sphinx.application import Sphinx
from sphinx.util.logging import getLogger as sphinx_get_logger

# mlx.traceability
from mlx.traceability import TraceableCollection as MlxTraceableCollection
from mlx.traceable_item import TraceableItem as MlxTraceableItem
from mlx.traceability_exception import TraceabilityException as MlxTraceabilityException

# docxbuilder
from docxbuilder import DocxBuilder

class ConfUtil:
    """
    ConfUtil class.
    """
    logger: SphinxLoggerAdapter = sphinx_get_logger(".".join([__name__, __qualname__]))

    docutils_text_visited_nodes: None | Deque[DocUtilsNode] = None
    docutils_old_dispatch_visit = None
    docutils_new_dispatch_visit = None
    docutils_old_dispatch_departure = None
    docutils_new_dispatch_departure = None

    docxbuilder_assemble_doctree_log: bool = False
    docxbuilder_assemble_doctree_log_before: bool = False
    docxbuilder_assemble_doctree_log_after: bool = False
    docxbuilder_old_assemble_doctree = None
    docxbuilder_new_assemble_doctree = None

    @classmethod
    def sphinx_setup(
        cls,

        sphinx_application: None | Sphinx | Any,

        docutils_text_visited_nodes_size: int = 10,
        docutils_dispatch_visit_override: bool = True,
        docutils_dispatch_departure_override: bool = True,

        docxbuilder_assemble_doctree_log: bool = False,
        docxbuilder_assemble_doctree_log_before: bool = False,
        docxbuilder_assemble_doctree_log_after: bool = False,
        docxbuilder_assemble_doctree_override: bool = True
    ) -> None:
        if sphinx_application is None:
            raise Exception("'sphinx_application' is none!")
        elif not isinstance(sphinx_application, Sphinx):
            raise Exception(f"'sphinx_application' is not an instance of 'Sphinx' it is instance of '{type(sphinx_application)}'")

        if docutils_dispatch_visit_override or docutils_dispatch_departure_override:
            cls.docutils_text_visited_nodes = Deque([], docutils_text_visited_nodes_size)
        if docutils_dispatch_visit_override:
            cls.docutils_old_dispatch_visit = getattr(NodeVisitor, 'dispatch_visit')
            cls.docutils_new_dispatch_visit = lambda docutils_self, node: cls.docutils_dispatch_visit(docutils_self, node)
            setattr(NodeVisitor, 'dispatch_visit', cls.docutils_new_dispatch_visit)
        if docutils_dispatch_departure_override:
            cls.docutils_old_dispatch_departure = getattr(NodeVisitor, 'dispatch_departure')
            cls.docutils_new_dispatch_departure = lambda docutils_self, node: cls.docutils_dispatch_departure(docutils_self, node)
            setattr(NodeVisitor, 'dispatch_departure', cls.docutils_new_dispatch_departure)

        cls.docxbuilder_assemble_doctree_log = docxbuilder_assemble_doctree_log
        cls.docxbuilder_assemble_doctree_log_before = docxbuilder_assemble_doctree_log_before
        cls.docxbuilder_assemble_doctree_log_after = docxbuilder_assemble_doctree_log_after

        if docxbuilder_assemble_doctree_override:
            cls.docxbuilder_old_assemble_doctree = getattr(DocxBuilder, 'assemble_doctree')
            cls.docxbuilder_new_assemble_doctree = lambda docxbuilder_self, master, toctree_only: cls.docxbuilder_assemble_doctree(docxbuilder_self, master, toctree_only)
            setattr(DocxBuilder, 'assemble_doctree', cls.docxbuilder_new_assemble_doctree)

    @classmethod
    def log_message_as_warning_or_error(
        cls,
        message: None | str | Any,
        as_error: bool = True,
        exit_code: int = 1
    ) -> None:
        if as_error:
            cls.logger.error(message)
            sys.exit(exit_code)
        else:
            cls.logger.warning(message)

    @classmethod
    def docutils_to_string(cls, node: None | DocUtilsNode, include_path: bool = True) -> str:
        if node is None:
            raise Exception("'node' is None")
        if include_path:
            path = []
            n = node
            while n is not None:
                path.append(n)
                n = n.parent
            path.reverse()
            path.pop(len(path) - 1)
            strings = [i.astext() if isinstance(i, DocUtilsText) else i.__class__.__name__ for i in path]
            node_string = "['" + "', '".join(strings) + "']: '" + (node.astext() if isinstance(node, DocUtilsText) else node.__class__.__name__)
        else:
            node_string = node.astext() if isinstance(node, DocUtilsText) else node.__class__.__name__
        return node_string

    @classmethod
    def docutils_log_node(cls, node: DocUtilsNode) -> None:
        cls.logger.info(f"-- {inspect.currentframe().f_code.co_name} start")
        nodes = node.traverse()
        entries = []
        for node in nodes:
            if isinstance(node, DocUtilsText) or len(node) == 0:
                entry = []
                n = node
                while n is not None:
                    entry.append(n)
                    n = n.parent
                entry.reverse()
                strings = [i.astext() if isinstance(i, DocUtilsText) else i.__class__.__name__ for i in entry]
                entries.append(strings)
        for entry in entries:
            cls.logger.info(f"-- {entry}")
        cls.logger.info(f"-- {inspect.currentframe().f_code.co_name} end")

    @classmethod
    def docutils_find_nodes(cls, node: DocUtilsNode, class_names: None | List[str] = None, index_key: None | str = None, include_self: bool = False) -> List[DocUtilsNode]:
        if class_names is None:
            raise Exception("Unspecified 'class_names'")

        if index_key is None:
            raise Exception("Unspecified 'index_key'")

        result: List[DocUtilsNode] = []

        for n in node.traverse(include_self=include_self):
            if n.__class__.__name__ in class_names:
                n[index_key] = len(result)
                result.append(n)

        return result

    @classmethod
    def docutils_dispatch_visit(cls, docutils_self, node: DocUtilsNode):
        try:
            if node is not None and node.__class__.__name__ == 'Text':
                cls.docutils_text_visited_nodes.append(node)
            return cls.docutils_old_dispatch_visit(docutils_self, node)
        except TreePruningException as e:
            raise e
        except Exception as e:
            for n in cls.docutils_text_visited_nodes:
                cls.logger.error(f"-- {inspect.currentframe().f_code.co_name} (previous): {cls.docutils_to_string(n)}")
            cls.logger.error(f"-- {inspect.currentframe().f_code.co_name} (current): {cls.docutils_to_string(node)}")
            cls.logger.error(e, exc_info = True)
            raise e

    @classmethod
    def docutils_dispatch_departure(cls, docutils_self, node: DocUtilsNode):
        try:
            return cls.docutils_old_dispatch_departure(docutils_self, node)
        except TreePruningException as e:
            raise e
        except Exception as e:
            for n in cls.docutils_text_visited_nodes:
                cls.logger.error(f"-- {inspect.currentframe().f_code.co_name} (previous): '{cls.docutils_to_string(n)}'")
            cls.logger.error(f"-- {inspect.currentframe().f_code.co_name} (current): {cls.docutils_to_string(node)}")
            cls.logger.error(e, exc_info = True)
            raise e

    @classmethod
    def docxbuilder_unwrap(cls, value: DocUtilsNode, class_names: None | List[str] = None) -> DocUtilsNode:
        if class_names is None:
            raise Exception("Unspecified 'class_names'")

        value_nodes = []

        for node in value:
            value_nodes.append(node)

        result: DocUtilsNode = value
        result.clear()

        for node in value_nodes:
            if node.__class__.__name__ == 'paragraph':
                paragraph = docutils.nodes.paragraph()
                for n in node:
                    if n.__class__.__name__ in class_names:
                        if len(paragraph) > 0:
                            result.append(paragraph)
                            paragraph = docutils.nodes.paragraph()
                        result.append(n)
                    else:
                        paragraph.append(n)
                if len(paragraph) > 0:
                    result.append(paragraph)
            else:
                result.append(node)

        return result

    @classmethod
    def docxbuilder_fix_node(cls, value: DocUtilsNode) -> DocUtilsNode:
        if value.__class__.__name__ == 'table':
            for table_node in value:
                if table_node.__class__.__name__ == 'tgroup':
                    for tgroup_node in table_node:
                        if tgroup_node.__class__.__name__ == 'colspec' and tgroup_node.get('colwidth') == 'auto':
                            tgroup_node['colwidth'] = 10000
            return value
        else:
            extract_from_paragraph = [
                'paragraph',
                'bullet_list',
                'enumerated_list',
                'definition_list',
                'table',
                'seealso',
                'desc',
                'math_block',
                'literal_block',
                'image'
            ]
            wrap_with_paragraph = [
                'emphasis'
            ]
            result = cls.docxbuilder_unwrap(value, class_names=extract_from_paragraph)

            target_class_names = ['list_item', 'definition', 'note']
            for target_class_name in target_class_names:
                target_index_key = 'docxbuilder_fix_desc_content_' + target_class_name + '_index'
                target_nodes = cls.docutils_find_nodes(result, class_names=[target_class_name], index_key=target_index_key)
                target_nodes.reverse()
                for node in target_nodes:
                    node_parent = node.parent
                    if node_parent is None:
                        raise Exception("'node_parent' is 'None'")
                    target_index = node[target_index_key]
                    for child_index, child in enumerate(node_parent):
                        if child.__class__.__name__ == target_class_name and child[target_index_key] == target_index:
                            old_node = node_parent[child_index]
                            new_node = cls.docxbuilder_unwrap(old_node, class_names=extract_from_paragraph)
                            node_parent[child_index] = new_node

            target_class_name = 'enumerated_list'
            target_index_key = 'docxbuilder_fix_desc_content_' + target_class_name + '_index'
            target_nodes = cls.docutils_find_nodes(result, class_names=[target_class_name], index_key=target_index_key)
            target_nodes.reverse()
            for node in target_nodes:
                node['enumtype'] = 'arabic'
                node['prefix'] = ''
                node['suffix'] = '.'
                node['start'] = 1

            target_class_name = 'container'
            target_index_key = 'docxbuilder_fix_desc_content_' + target_class_name + '_index'
            target_nodes = cls.docutils_find_nodes(result, class_names=[target_class_name], index_key=target_index_key)
            target_nodes.reverse()
            for node in target_nodes:
                for child_index, child in enumerate(node):
                    if child.__class__.__name__ in wrap_with_paragraph:
                        paragraph = docutils.nodes.paragraph()
                        paragraph.append(child)
                        node[child_index] = paragraph

            return result

    @classmethod
    def docxbuilder_assemble_doctree(cls, docxbuilder_self, master, toctree_only):
        if cls.docxbuilder_assemble_doctree_log:
            cls.logger.info(f"-- {inspect.currentframe().f_code.co_name}")

        tree = cls.docxbuilder_old_assemble_doctree(docxbuilder_self, master, toctree_only)

        if cls.docxbuilder_assemble_doctree_log and cls.docxbuilder_assemble_doctree_log_before:
            cls.logger.info(f"-- {inspect.currentframe().f_code.co_name} log node before")
            cls.docutils_log_node(tree)

        if cls.docxbuilder_assemble_doctree_log:
            cls.logger.info(f"-- {inspect.currentframe().f_code.co_name} find 'desc_content' nodes")

        class_names = ['section', 'desc_content', 'table']
        index_key = 'docxbuilder_new_assemble_doctree_index'
        nodes = cls.docutils_find_nodes(tree, class_names=class_names, index_key=index_key)
        nodes.reverse()

        if cls.docxbuilder_assemble_doctree_log:
            cls.logger.info(f"-- {inspect.currentframe().f_code.co_name} found nodes len: '{len(nodes)}'")

        if cls.docxbuilder_assemble_doctree_log:
            cls.logger.info(f"-- {inspect.currentframe().f_code.co_name} process")

        for node_index, node in enumerate(nodes):
            if cls.docxbuilder_assemble_doctree_log:
                cls.logger.info(f"-- {inspect.currentframe().f_code.co_name} process node {node_index + 1} of {len(nodes)}")

            node_parent = node.parent

            if node_parent is None:
                raise Exception(f"node_parent is None")

            index_value = node[index_key]

            for child_index, child in enumerate(node_parent):
                if (
                        child.__class__.__name__ in class_names
                        and child[index_key] == index_value
                ):
                    old_node = node_parent[child_index]
                    new_node = cls.docxbuilder_fix_node(old_node)
                    node_parent[child_index] = new_node

        if cls.docxbuilder_assemble_doctree_log and cls.docxbuilder_assemble_doctree_log_after:
            cls.logger.info(f"-- {inspect.currentframe().f_code.co_name} log node after")
            cls.docutils_log_node(tree)

        return tree

    @classmethod
    def mlx_traceability_inspect_item(
        cls,
        name: None | str | Any,
        collection: None | MlxTraceableCollection | Any,
        config: None | Dict[str, List[str]] | Any = None,
        warning_to_error: bool = True,
        log: bool = False
    ) -> None:
        if config is None:
            return

        if log:
            cls.logger.info(f"-- {inspect.currentframe().f_code.co_name} name: '{name}'")

        # check-input
        if name is None:
            cls.log_message_as_warning_or_error(f"'name' is none.", warning_to_error)
        elif not isinstance(name, str):
            cls.log_message_as_warning_or_error(f"'name' is not an instance of 'str'.", warning_to_error)

        if collection is None:
            cls.log_message_as_warning_or_error(f"'collection' is none.", warning_to_error)
        elif not isinstance(collection, MlxTraceableCollection):
            cls.log_message_as_warning_or_error(f"'collection' is not an instance of 'MlxTraceableCollection'.", warning_to_error)

        if config is None:
            cls.log_message_as_warning_or_error(f"'config' is none.", warning_to_error)
        elif not isinstance(config, Dict):
            cls.log_message_as_warning_or_error(f"'config' is not an instance of 'Dict'.", warning_to_error)

        # process
        item: None | MlxTraceableItem | Any = collection.get_item(name)

        if item is None:
            cls.log_message_as_warning_or_error(f"'item' is none.", warning_to_error)

        try:
            item.self_test()
        except MlxTraceabilityException as e:
            cls.log_message_as_warning_or_error(f"{e}", warning_to_error)
            if warning_to_error:
                raise e

        item_dict: Dict[str, Any] = item.to_dict()
        item_id: str = item_dict['id']
        item_targets: Dict[str, Any] = item_dict.get('targets', dict())
        config_keys: Set[str] = set(config.keys())

        if log:
            cls.logger.info(f"-- {inspect.currentframe().f_code.co_name} config keys: {config_keys}")

        while config_keys:
            prefix: str = config_keys.pop()
            if not item_id.startswith(prefix):
                continue
            if log:
                cls.logger.info(f"-- {inspect.currentframe().f_code.co_name} validate id: '{item_id}' targets: {item_targets}")
            types: List[str] = config[prefix]
            item_links: List[str] = []
            for k, v in item_targets.items():
                if k in types:
                    item_links.extend(v)
            if len(item_links) < 1:
                cls.log_message_as_warning_or_error(f"'{item_id}' has no links with types: {types}", warning_to_error)
