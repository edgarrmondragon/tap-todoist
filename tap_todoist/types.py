import sys
from typing import Any, Callable, Mapping

import requests

if sys.version_info >= (3, 10):
    from typing import TypeAlias
else:
    from typing_extensions import TypeAlias


ConfigDict: TypeAlias = Mapping[str, Any]
StateDict: TypeAlias = Mapping[str, Any]

RequestsAuth: TypeAlias = Callable[[requests.PreparedRequest], requests.PreparedRequest]
