from inspect import signature
from openhands.sel.selenium_tester import driver, create_driver
from IPython.display import Image
from openhands.runtime.plugins.agent_skills import file_ops, file_reader
from openhands.runtime.plugins.agent_skills.utils.dependency import import_functions

import_functions(
    module=file_ops, function_names=file_ops.__all__, target_globals=globals()
)
import_functions(
    module=file_reader, function_names=file_reader.__all__, target_globals=globals()
)
# __all__ = file_ops.__all__ + file_reader.__all__
__all__ = file_ops.__all__

DOCUMENTATION = ''
for func_name in __all__:
    if func_name in ['clean_workspace', 'custom_import']:
        continue
    func = globals()[func_name]

    cur_doc = func.__doc__
    # remove indentation from docstring and extra empty lines
    cur_doc = '\n'.join(filter(None, map(lambda x: x.strip(), cur_doc.split('\n'))))
    # now add a consistent 4 indentation
    cur_doc = '\n'.join(map(lambda x: ' ' * 4 + x, cur_doc.split('\n')))

    fn_signature = f'{func.__name__}' + str(signature(func))
    DOCUMENTATION += f'{fn_signature}:\n{cur_doc}\n\n'


# Add file_editor (a function)
from openhands.runtime.plugins.agent_skills.file_editor import file_editor  # noqa: E402

__all__ += ['file_editor']

def dss():
    '''
    Alias to driver.get_screenshot_as_png()
    '''
    return driver.get_screenshot_as_png()

__all__ += ['driver', 'dss', 'create_driver']
