# Copyright (C) 2022 zeebrow

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
import sys
if sys.version_info.minor == 7:
    import importlib_metadata as metadata
else:
    from importlib import metadata  # noqa: F401
import tempfile
import shutil
from pathlib import Path
from textwrap import dedent

from unittest.mock import patch
import pytest
from pytest import MonkeyPatch

from quickhost.QuickhostPlugin import (
    fetch_all_plugins,
    get_plugin,
    get_plugin_app_getter,
    get_plugin_parser_getter,
    NoPluginFoundError,
)


PLUGIN_NAME = 'fakeplugin'
PLUGIN_VERSION = 'fake.version'


@pytest.fixture
def mock_package(monkeypatch: MonkeyPatch):
    try:
        with monkeypatch.context() as m:
            temp_dir = Path(tempfile.mkdtemp())
            pkg_root = temp_dir / 'src'
            plugin_dir = pkg_root / f'quickhost_{PLUGIN_NAME}'
            plugin_dir.mkdir(parents=True)
            init_py = plugin_dir / '__init__.py'
            with init_py.open('w') as f:
                f.write(dedent(f"""\
                    def get_app(): return "{PLUGIN_NAME}_app"
                    def get_parser(): return "{PLUGIN_NAME}_parser"
                """))

            dist_info_base = temp_dir / 'test-site-pkg'
            dist_info = dist_info_base / f'quickhost_{PLUGIN_NAME}-{PLUGIN_VERSION}.dist-info'
            dist_info.mkdir(parents=True)

            METADATA_txt = dist_info / 'METADATA'
            with METADATA_txt.open('w') as f:
                f.write(dedent(f"""\
                    Metadata-Version: 2.1
                    Name: quickhost-{PLUGIN_NAME}
                    Version: {PLUGIN_VERSION}
                    Requires-Dist: quickhost
                """))

            entry_points_txt = dist_info / 'entry_points.txt'
            with entry_points_txt.open('w') as f:
                f.write(dedent(f"""\
                    [quickhost_plugin]
                    {PLUGIN_NAME}_app = quickhost_{PLUGIN_NAME}:get_app
                    {PLUGIN_NAME}_parser = quickhost_{PLUGIN_NAME}:get_parser
                """))

            m.syspath_prepend(str(pkg_root.absolute()))
            m.syspath_prepend(str(dist_info_base.absolute()))
            yield
    finally:
        shutil.rmtree(temp_dir)


@pytest.fixture
def fake_plugin_entrypoints(mock_package):
    app_getter = metadata.EntryPoint(name=f'{PLUGIN_NAME}_app', value=f'quickhost_{PLUGIN_NAME}:get_app', group='quickhost_plugin')
    parser_getter = metadata.EntryPoint(name=f'{PLUGIN_NAME}_parser', value=f'quickhost_{PLUGIN_NAME}:get_parser', group='quickhost_plugin')
    return metadata.EntryPoints({app_getter, parser_getter})


def test_plugin(fake_plugin_entrypoints):
    with patch('quickhost.QuickhostPlugin.metadata.entry_points', lambda *args, **kwargs: fake_plugin_entrypoints):
        plugin = get_plugin(PLUGIN_NAME)
        assert get_plugin_app_getter(PLUGIN_NAME)() == f"{PLUGIN_NAME}_app" == plugin.app
        assert get_plugin_parser_getter(PLUGIN_NAME)() == f"{PLUGIN_NAME}_parser" == plugin.parser
        assert plugin.name == PLUGIN_NAME
        assert plugin.version == PLUGIN_VERSION
        assert plugin.package_name == f"quickhost_{PLUGIN_NAME}"


def test_get_plugin_nonexistant_plugin_raises():
    with pytest.raises(NoPluginFoundError):
        get_plugin('nonexistant')


def test_get_plugin_app_nonexistant_plugin_raises():
    with pytest.raises(NoPluginFoundError):
        get_plugin_app_getter('nonexistant')


def test_get_plugin_parser_nonexistant_plugin_raises():
    with pytest.raises(NoPluginFoundError):
        get_plugin_parser_getter('nonexistant')


def test_fetch_all_plugins(fake_plugin_entrypoints):
    plugins = fetch_all_plugins()
    assert PLUGIN_NAME in plugins.keys()
