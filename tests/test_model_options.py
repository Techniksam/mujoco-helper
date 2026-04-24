import pytest

from mujocohelper.designer.model import MujocoModel, MujocoOption


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


def test_get_options_returns_effective_options() -> None:
    model = MujocoModel()
    model.set_options(timestep=0.01, wind=(1.0, 0.0, 0.0))

    options = model.get_options()

    assert isinstance(options, MujocoOption)
    assert options.timestep == 0.01
    assert options.wind == (1.0, 0.0, 0.0)
    assert options.solver == "Newton"


def test_unknown_option_name_raises() -> None:
    model = MujocoModel()

    with pytest.raises(ValueError, match="Unrecognized option name"):
        model.set_option("does_not_exist", 1)


def test_invalid_option_type_raises() -> None:
    model = MujocoModel()

    with pytest.raises(TypeError, match="timestep must be a float"):
        model.set_option("timestep", "fast")
