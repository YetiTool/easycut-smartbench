from kivy.uix.screenmanager import Screen
from kivy.uix.widget import Widget

INDENT = '    '

def get_python_code_from_screen(widget):
    # type: (Widget) -> str
    screen = widget.parent
    while not issubclass(type(screen), Screen):
        screen = screen.parent
    #  assuming every screen has exactly one child as the main layout!!!
    main_layout = screen.children[0]
    # now make an import string:
    s = '# IMPORTS:\n\n'
    s += 'from kivy.lang import Builder\n'
    s += 'from kivy.uix.screenmanager import Screen\n'
    d = get_import_dict_from_widget(main_layout)
    for k, v in d.items():
        imp_list = ','.join(v)
        s += 'from ' + k + ' import ' + imp_list + '\n'

    s += '\n# BUILDER_STRING:\n\n'
    s += 'Builder.load_string(\n"""'
    s += '<' + screen.name + '>\n'
    s += builder_string_from_widget(main_layout)
    s += '"""\n)'

    s += '\n# CLASS_CODE:\n\n'
    s += get_class_code(screen)

    return s



def builder_string_from_widget(widget, indent_level=1):
    # type: (Widget, int) -> str
    """
    Returns a generated builder string that represents the given widget.
    """
    base_indent = ''
    for i in range(0, indent_level * len(INDENT)):
        base_indent += ' '

    s = base_indent + type(widget).__name__ + ':\n'
    # list of attributes that need to be part of the builder string:
    attributes = {'size': '{}',
                  'size_hint': '{}',
                  'pos': '{}',
                  'source': '{}',
                  'text': '"{}"',
                  'font_size': '{}',
                  'color': '{}'}  # wrapping the actual text in ""

    for attribute in attributes.keys():
        value = getattr(widget, attribute, 'no_attr')
        if value != 'no_attr':
            s += base_indent + INDENT + attribute + ': ' + attributes[attribute].format(str(value)) + '\n'

    # now handle children
    for child in widget.children:
        s += builder_string_from_widget(child, indent_level+1)
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

    # now handle children:
    for child in widget.children:
        c = get_import_dict_from_widget(child)
        for k, v in c.items():
            if k in ret:
                ret[k].union(v)
            else:
                ret[k] = v

    return ret

def get_class_code(screen):
    # type: (Screen) -> str
    s = 'class ' + screen.name + '(Screen):\n'
    s += INDENT + 'def __init__(self, **kwargs):\n'
    s += INDENT + INDENT + 'super(' + screen.name + ', self).__init__(**kwargs)'
    return s



