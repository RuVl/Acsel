import json
import sys
from datetime import datetime
from importlib import util
from typing import Any

from core import bot


class TGDecoder(json.JSONDecoder):
    """ Write decoder for all you need in state.get_data """

    def __init__(self, *args, **kwargs):
        super(TGDecoder, self).__init__(object_hook=self.object_hook, *args, **kwargs)

    @staticmethod
    def import_type(module_name: str, type_name: str) -> Any:
        """ Import type from module """

        module = sys.modules.get(module_name)  # Use last imported module

        # Import module if is not imported
        if module is None:
            spec = util.find_spec(module_name)
            if spec is None:
                raise ValueError(f'Spec of {module_name} is not found!')

            spec.loader = util.LazyLoader(spec.loader)

            try:
                module = util.module_from_spec(spec)
                sys.modules[module_name] = module
                spec.loader.exec_module(module)
            except ImportError:
                raise ImportError(f'Cannot load module {module_name}!')

        # Get a type from module
        type_ = getattr(module, type_name, None)
        if type_ is None:
            raise ValueError(f'Cannot find type {type_name} in module {module_name}!')

        return type_

    def object_hook(self, o: dict[str, Any]) -> Any:
        _type, _value = o.get('_type'), o.get('_value')
        if _type is None or _value is None:
            return o

        _module = '.'.join(_type.split('.')[:-1])
        _type = _type.removeprefix(_module + '.')

        if not _module or not _type:
            return o

        # Check for special types
        if _module == _type == 'datetime':
            return datetime.fromisoformat(_value)

        # Try to import other modules
        class_ = self.import_type(_module, _type)
        if class_ is None:
            return o

        o = class_(**_value)

        # Additional attributes for instance
        if _module.startswith('aiogram.types'):
            o._bot = bot

        return o
