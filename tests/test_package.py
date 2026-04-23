from importlib.metadata import version

import mujocohelper


def test_package_import_and_version() -> None:
    assert isinstance(mujocohelper.__version__, str)
    assert mujocohelper.__version__


def test_installed_metadata_version() -> None:
    assert version("mujocohelper") == mujocohelper.__version__


def test_renderer_export_is_available() -> None:
    assert hasattr(mujocohelper, "Renderer")
