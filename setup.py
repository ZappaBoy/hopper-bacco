# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
    ['hopper-bacco',
     'hopper-bacco.routes',
     'hopper-bacco.routes.hopper',
     'hopper-bacco.routes.hopper.dto',
     'hopper-bacco.shared',
     'hopper-bacco.shared.decorators',
     'hopper-bacco.shared.deps',
     'hopper-bacco.shared.middlewares',
     'hopper-bacco.shared.models',
     'hopper-bacco.shared.models.settings',
     'hopper-bacco.shared.utilities']

package_data = \
    {'': ['*']}

install_requires = \
    ['fastapi-utils>=0.2.1,<0.3.0',
     'fastapi>=0.95.1,<0.96.0',
     'loguru>=0.7.0,<0.8.0',
     'pydantic>=1.10.7,<2.0.0',
     'starlette>=0.26.1,<0.27.0',
     'uvicorn>=0.21.1,<0.22.0']

entry_points = \
    {'console_scripts': ['hopper-bacco = hopper-bacco:main', 'test = pytest:main']}

setup_kwargs = {
    'name': 'hopper-bacco',
    'version': '0.1.0',
    'description': 'Hopper-Bacco (Oh perbacco) is a simple utility that forward requests changing IP and User Agent to avoid bans.',
    'long_description': '# hopper-bacco\nHopper-Bacco (Oh perbacco) is a simple utility that forward requests changing IP and User Agent to avoid bans.\n',
    'author': 'ZappaBoy',
    'author_email': 'federico.zappone@justanother.cloud',
    'maintainer': 'ZappaBoy',
    'maintainer_email': 'federico.zappone@justanother.cloud',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}

setup(**setup_kwargs)
