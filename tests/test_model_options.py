import pytest

from mujocohelper.designer.model import MujocoModel


def test_set_and_get_single_option() -> None:
    model = MujocoModel()

    model.set_option("timestep", 0.001)

    assert model.get_option("timestep") == 0.001


def test_clear_option_removes_explicit_value() -> None:
    model = MujocoModel()
    model.set_option("iterations", 200)

    model.clear_option("iterations")

    assert model.get_option("iterations") is None


def test_set_options_sets_multiple_values() -> None:
    model = MujocoModel()

    model.set_options(timestep=0.005, solver="CG")

    assert model.get_option("timestep") == 0.005
    assert model.get_option("solver") == "CG"


def test_unknown_option_name_raises() -> None:
    model = MujocoModel()

    with pytest.raises(ValueError, match="Unrecognized option name"):
        model.set_option("does_not_exist", 1)


def test_invalid_option_type_raises() -> None:
    model = MujocoModel()

    with pytest.raises(TypeError, match="timestep must be a float"):
        model.set_option("timestep", "fast")
