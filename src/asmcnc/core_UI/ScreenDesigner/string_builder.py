import re

from kivy.uix.screenmanager import Screen
from kivy.uix.widget import Widget

from asmcnc.comms.logging_system.logging_system import Logger
from asmcnc.core_UI import path_utils as pu

GENERATED_SCREENS_FOLDER = pu.get_path('generated_code/screens')
GENERATED_WIDGETS_FOLDER = pu.get_path('generated_code/widgets')

INDENT = '    '

# Classes that are used in BuilderString but their children will not be processed (like inner BoxLayouts and alike)
DONT_DO_CHILDREN = ['ProbeButton', 'SpindleButton', 'VacuumButton', 'XYMove']

# Classes that can only be used in code due to their init parameters:
CODE_ONLY_ITEMS = {'ProbeButton': ['{} = ProbeButton(MagicMock(), App.get_running_app().sm, Localization())  # TODO: fill args!',
                                   '{}.size = [70, 70]'],
                   'SpindleButton': ['{} = SpindleButton(MagicMock(), MagicMock(), App.get_running_app().sm)  # TODO: fill args!',
                                     '{}.size = [71, 72]'],
                   'VacuumButton': ['{} = VacuumButton(MagicMock(), MagicMock())  # TODO: fill args!',
                                    '{}.size = [71, 72]'],
                   'XYMove': ['{} = XYMove(machine=MagicMock(), screen_manager=App.get_running_app().sm, localization=Localization())   # TODO: fill args!',
                              '{}.size = [270.5, 391.6]']}

# Comment tokens used for search and replace when updating files:
IMPORTS_START = '# GENERATED_IMPORTS_START'
IMPORTS_END = '# GENERATED_IMPORTS_END'
BUILDER_STRING_START = '# BUILDER_STRING_START'
BUILDER_STRING_END = '# BUILDER_STRING_END'
CODE_START = '# GENERATED_CODE_START'  # two lines before class code
CODE_END = '# GENERATED_CODE_END'  # final new line


def get_code_from_file(modifying_screen, class_name, filename, base_class):
    s = ''
    if modifying_screen:
        if 'Screen' in base_class:
            path = pu.join(GENERATED_SCREENS_FOLDER, filename + '.py')
        elif 'Widget' in base_class:
            path = pu.join(GENERATED_WIDGETS_FOLDER, filename + '.py')
        with open(path, 'r') as f:
            s = f.read()
    else:
        s += IMPORTS_START + '\n'
        s += IMPORTS_END + '\n'
        s += BUILDER_STRING_START + '\n'
        s += BUILDER_STRING_END + '\n'
        s += CODE_START + '\n'
        s += CODE_END + '\n'
    return s


def get_python_code_from_screen(widget, modifying_screen, class_name, filename, base_class):
    # type: (Widget, bool, str, str) -> str
    """
    widget = entrypoint into the screen's widget tree.
    modifying_screen => True: load code from file. False: create dummy code with comment markers
    class_name => Name of the screen and class
    filename => corresponding filename
    base_class => either 'Screen' or 'Widget'

    Walks through the whole widget tree of the screen and generates either kivy builder string or python code
    for each widget.
    Imports are gathered and generated.
    Basic class code is generated.
    """
    code_from_file = get_code_from_file(modifying_screen, class_name, filename, base_class)
    #  assuming given class is the main layout!!!
    main_layout = widget
    imports_py, code_py, imports_kivy, code_kivy = gather_data_from_widget_tree(main_layout)
    # now make an import string:
    s = IMPORTS_START
    s += '\n\n'
    s += 'from kivy.lang import Builder\n'
    if base_class == 'Screen':
        s += 'from kivy.uix.screenmanager import Screen\n'
    elif base_class == 'Widget':
        s += 'from kivy.uix.widget import Widget\n'
    if 'MagicMock()' in code_py:
        s += 'from mock.mock import MagicMock\n'
    if 'App.' in code_py:
        s += 'from kivy.app import App\n\n'
    if 'Localization()' in code_py:
        s += 'from asmcnc.comms.localization import Localization\n'
    for import_path, import_list in imports_py.items():
        imp_list = ','.join(import_list)
        s += 'from ' + import_path + ' import ' + imp_list + '\n'
    s += IMPORTS_END
    pattern_imports_py = r'{}.*{}'.format(IMPORTS_START, IMPORTS_END)
    code_from_file = re.sub(pattern_imports_py, s, code_from_file, flags=re.M|re.S)

    # builder string:
    s = BUILDER_STRING_START
    s += '\n\n'
    s += 'Builder.load_string("""\n\n'
    #:import hex kivy.utils.get_color_from_hex
    for import_path, import_list in imports_kivy.items():
        for imp in import_list:
            s += '#:import ' + imp + ' ' + import_path + '\n'
    s += '\n<' + class_name + '>\n'
    s += code_kivy
    s += '""")\n'
    s += BUILDER_STRING_END
    pattern_builder_string = r'{}.*{}'.format(BUILDER_STRING_START, BUILDER_STRING_END)
    code_from_file = re.sub(pattern_builder_string, s, code_from_file, flags=re.M|re.S)

    # python code:
    s = CODE_START
    s += '\n\n\n'  # two new lines before class
    s += get_class_code(class_name, base_class)
    s += code_py
    s += CODE_END
    pattern_class_code = r'{}.*{}'.format(CODE_START, CODE_END)
    code_from_file = re.sub(pattern_class_code, s, code_from_file, flags=re.M|re.S)

    return code_from_file


def gather_data_from_widget_tree(widget, indent_level=1):
    # type: (Widget, int) -> (dict, str, dict, str)
    """
    Collects all data for the give widget (imports, builder string, python code).
    Calls itself to get the data from the children if needed.

    Returns a tuple with: (imports_py, code_py, imports_kivy, code_kivy)
    """
    imports_py = {}
    code_py = ''
    imports_kivy = {}
    code_kivy = ''

    if type(widget).__name__ in CODE_ONLY_ITEMS:
        code_py += get_code_for_widget(widget)
        imps_widget = get_import_dict_from_widget(widget)
        for import_path, import_list in imps_widget.items():
            # check if the same module is needed -> update set:
            if import_path in imports_py:
                imports_py[import_path].union(import_list)
            else:
                imports_py[import_path] = import_list
    else:
        code_kivy += get_builder_string_from_widget(widget, indent_level)
        imps_widget = get_import_dict_from_widget(widget)
        try:
            for import_path, import_list in imps_widget.items():
                # check if the same module is needed -> update set:
                if import_path in imports_kivy:
                    imports_kivy[import_path].union(import_list)
                else:
                    imports_kivy[import_path] = import_list
        except Exception as ex:
            Logger.exception(ex)
            Logger.error('BOOM!!!')
            pass
        # now handle children if needed:
        if type(widget).__name__ not in DONT_DO_CHILDREN:
            for child in widget.children:
                c_imp_py, c_code_py, c_imp_kivy, c_code_kivy = gather_data_from_widget_tree(child, indent_level+1)
                # update python imports:
                for import_path, import_list in c_imp_py.items():
                    # check if the same module is needed -> update set:
                    if import_path in imports_py:
                        imports_py[import_path].union(import_list)
                    else:
                        imports_py[import_path] = import_list
                # update python code:
                code_py += c_code_py
                # update kivy imports:
                for import_path, import_list in c_imp_kivy.items():
                    # check if the same module is needed -> update set:
                    if import_path in imports_kivy:
                        imports_kivy[import_path].union(import_list)
                    else:
                        imports_kivy[import_path] = import_list
                # update kivy code:
                code_kivy += c_code_kivy

    return (imports_py, code_py, imports_kivy, code_kivy)


def get_code_for_widget(widget):
    # type: (Widget) -> str
    """
    Returns python code for the given widget.
    """
    s= ''
    s += INDENT + INDENT + '# Code for {}:\n'.format(str(widget.id))
    # add specific code block:
    for line in CODE_ONLY_ITEMS[type(widget).__name__]:
        s += INDENT + INDENT + line.format(widget.id) + '\n'
    s += INDENT + INDENT + str(widget.id) + '.pos = ' + str(widget.pos) + '\n'
    s += INDENT + INDENT + str(widget.id) + '.id = "' + str(widget.id) + '"\n'
    s += INDENT + INDENT + str(widget.id) + '.size_hint = [None, None]\n'
    s += INDENT + INDENT + 'self.children[0].add_widget(' + str(widget.id) + ')\n'
    return s


def get_builder_string_from_widget(widget, indent_level):
    # type: (Widget, int) -> str
    """
    Returns a generated builder string that represents the given widget.
    """
    # list of attributes with specific formatting options. E.g.: wrapping the actual text in ""
    # attributes = {'allow_stretch': '{}',
    #               'always_release': '{}',
    #               'center_x': '{}',
    #               'center_y': '{}',
    #               'cols': '{}',
    #               'background_color': '{}',
    #               'background_normal': '"{}"',
    #               'background_down': '"{}"',
    #               'border': '{}',
    #               'color': '{}',
    #               'font_size': 'dp({})',
    #               'halign': '"{}"',
    #               'height': '{}',
    #               'id': '{}',
    #               'markup': '{}',
    #               'orientation': '"{}"',
    #               'padding': 'dp({})',
    #               'padding_x': 'dp({})',
    #               'padding_y': 'dp({})',
    #               'pos': '{}',
    #               'rows': '{}',
    #               'size': '{}',
    #               # 'size_hint': '{}',
    #               'size_hint_x': '{}',
    #               'size_hint_y': '{}',
    #               'source': '"{}"',
    #               'spacing': 'dp({})',
    #               'text': '"{}"',
    #               'text_size': '{}',
    #               'width': '{}',
    #               'valign':  '"{}"'
    #               }
    attributes = {'allow_stretch': '{}',
                  'cols': '{}',
                  'background_color': '{}',
                  'background_normal': '"{}"',
                  'background_down': '"{}"',
                  'border': '{}',
                  'color': '{}',
                  'font_size': 'dp({})',
                  'halign': '"{}"',
                  # 'height': '{}',
                  'id': '{}',
                  'pos': '{}',
                  'size': '{}',
                  'size_hint': '{}',
                  'size_hint_x': '{}',
                  'size_hint_y': '{}',
                  'source': '"{}"',
                  'text': '"{}"',
                  'text_size': '{}',
                  # 'width': '{}',
                  'valign':  '"{}"'
                  }
    # setup indentation level:
    base_indent = ''
    for i in range(0, indent_level * len(INDENT)):
        base_indent += ' '

    s = base_indent + type(widget).__name__ + ':\n'

    # list of attributes that need to be part of the builder string:
    for attribute in attributes.keys():
        value = getattr(widget, attribute, 'no_attr')
        if value and value != 'no_attr':
            s += base_indent + INDENT + attribute + ': ' + attributes[attribute].format(str(value)) + '\n'
    s += '\n'
    return s


def get_import_dict_from_widget(widget):
    # type: (Widget) -> dict
    """
    Returns a dictionary with the widgets module name as the key and the class names as the value.
    """
    ret = {}
    klass = widget.__class__
    module = klass.__module__
    if module != 'builtins':
        ret = {module: {klass.__name__}}
    return ret


def get_class_code(class_name, base_class):
    # type: (str, str) -> str
    """
    Returns basic class code (ctor and super call) as string.
    sets the name attribute of the screen!
    """
    s = 'class ' + class_name + '(' + base_class + '):\n'
    s += INDENT + 'def __init__(self, **kwargs):\n'
    s += INDENT + INDENT + 'super(' + class_name + ', self).__init__(name="' + class_name + '", **kwargs)\n'
    return s



