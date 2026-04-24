from dataclasses import asdict, dataclass
from typing import Literal, TypedDict

try:
    from typing import Unpack
except ImportError:  # pragma: no cover - only used on Python < 3.11
    from typing_extensions import Unpack


IntegratorType = Literal["Euler", "RK4", "implicit", "implicitfast"]
ConeType = Literal["pyramidal", "elliptic"]
JacobianType = Literal["dense", "sparse", "auto"]
SolverType = Literal["PGS", "CG", "Newton"]


class MujocoOptions(TypedDict, total=False):
    timestep: float
    impratio: float
    gravity: tuple[float, float, float]
    wind: tuple[float, float, float]
    magnetic: tuple[float, float, float]
    density: float
    viscosity: float
    o_margin: float
    integrator: IntegratorType
    cone: ConeType
    jacobian: JacobianType
    solver: SolverType
    iterations: int
    tolerance: float
    ls_iterations: int
    ls_tolerance: float
    noslip_iterations: int
    noslip_tolerance: float
    ccd_iterations: int
    ccd_tolerance: float
    sdf_iterations: int
    sdf_initpoints: int


ALLOWED_FLAG_NAMES: frozenset[str] = frozenset({
    "constraint",
    "equality",
    "frictionloss",
    "limit",
    "contact",
    "spring",
    "damper",
    "gravity",
    "clampctrl",
    "warmstart",
    "filterparent",
    "actuation",
    "refsafe",
    "sensor",
    "midphase",
    "nativeccd",
    "island",
    "eulerdamp",
    "autoreset",
    "override",
    "energy",
    "fwdinv",
    "invdiscrete",
    "multiccd",
    "sleep",
})

ALLOWED_OPTIONS: frozenset[str] = frozenset(MujocoOptions.__annotations__.keys())

OPTION_LITERAL_VALUES: dict[str, frozenset[str]] = {
    "integrator": frozenset({"Euler", "RK4", "implicit", "implicitfast"}),
    "cone": frozenset({"pyramidal", "elliptic"}),
    "jacobian": frozenset({"dense", "sparse", "auto"}),
    "solver": frozenset({"PGS", "CG", "Newton"}),
}

VECTOR_OPTION_NAMES: frozenset[str] = frozenset({"gravity", "wind", "magnetic"})
FLOAT_OPTION_NAMES: frozenset[str] = frozenset(
    {
        "timestep",
        "impratio",
        "density",
        "viscosity",
        "o_margin",
        "tolerance",
        "ls_tolerance",
        "noslip_tolerance",
        "ccd_tolerance",
    }
)
INT_OPTION_NAMES: frozenset[str] = frozenset(
    {
        "iterations",
        "ls_iterations",
        "noslip_iterations",
        "ccd_iterations",
        "sdf_iterations",
        "sdf_initpoints",
    }
)

class MujocoModel:
    def __init__(self, name: str = "MuJoCo Model"):
        self._name = name

        self._options: dict[str, object] = {}
        self._flags: dict[str, bool] = {}


    def _validate_option_name(self, option_name: str) -> str:
        name = option_name.strip().lower()
        if name not in ALLOWED_OPTIONS:
            valid = ", ".join(sorted(ALLOWED_OPTIONS))
            raise ValueError(f"Unrecognized option name: {option_name!r}. Valid options: {valid}")
        return name


    def _validate_option_value(self, option_name: str, value: object) -> object:
        if option_name in FLOAT_OPTION_NAMES:
            if not isinstance(value, (int, float)):
                raise TypeError(f"{option_name} must be a float")
            return float(value)

        if option_name in INT_OPTION_NAMES:
            if not isinstance(value, int):
                raise TypeError(f"{option_name} must be an int")
            return value

        if option_name in VECTOR_OPTION_NAMES:
            if not isinstance(value, tuple) or len(value) != 3:
                raise TypeError(f"{option_name} must be a tuple[float, float, float]")
            if not all(isinstance(x, (int, float)) for x in value):
                raise TypeError(f"{option_name} must contain only numeric values")
            return (float(value[0]), float(value[1]), float(value[2]))

        if option_name in OPTION_LITERAL_VALUES:
            if not isinstance(value, str):
                raise TypeError(f"{option_name} must be a string")
            allowed = OPTION_LITERAL_VALUES[option_name]
            if value not in allowed:
                valid = ", ".join(sorted(allowed))
                raise ValueError(f"Invalid value for {option_name!r}: {value!r}. Valid values: {valid}")
            return value

        return value


    def set_option(self, option_name: str, value: object | None) -> None:
        """Set a single simulation option.

        Args:
            option_name: Name of the option (case-sensitive).
            value: Option value to set explicitly, None to unset (use default).

        Raises:
            ValueError: If the option name is not recognized.
        """
        name = self._validate_option_name(option_name)

        if value is None:
            self._options.pop(name, None)
            return

        self._options[name] = self._validate_option_value(name, value)


    def set_options(self, **options: Unpack[MujocoOptions]) -> None:
        """Set multiple simulation options at once.

        Args:
            **options: Keyword arguments where keys are option names and values
                are option values or None.

        Raises:
            ValueError: If any option name is not recognized.
        """
        for name, value in options.items():
            self.set_option(name, value)


    def get_option(self, option_name: str) -> object | None:
        """Get the current explicit value of a simulation option.

        Args:
            option_name: Name of the option (case-sensitive).

        Returns:
            The current explicit value of the option, or None if not explicitly set.

        Raises:
            ValueError: If the option name is not recognized.
        """
        name = self._validate_option_name(option_name)
        return self._options.get(name)


    def clear_option(self, option_name: str) -> None:
        """Clear explicit value so default behavior is used.

        Args:
            option_name: Name of the option (case-sensitive).

        Raises:
            ValueError: If the option name is not recognized.
        """
        self.set_option(option_name, None)


    def set_flag(self, flag_name: str, value: bool | None) -> None:
        """Set a single simulation flag.

        Args:
            flag_name: Name of the flag (case-insensitive).
            value: True/False to set explicitly, None to unset (use default).
        
        Raises:
            ValueError: If the flag name is not recognized.
        """
        name = flag_name.strip().lower()

        # Validate flag name
        if name not in ALLOWED_FLAG_NAMES:
            valid = ", ".join(sorted(ALLOWED_FLAG_NAMES))
            raise ValueError(f"Unrecognized flag name: {flag_name!r}. Valid flags: {valid}")

        # Set or clear the flag
        if value is None:
            self._flags.pop(name, None)
            return

        self._flags[name] = bool(value)


    def set_flags(self, **flags: bool | None) -> None:
        """Set multiple simulation flags at once.
        
        Args:
            **flags: Keyword arguments where keys are flag names (case-insensitive) and 
                values are True/False or None.
        
        Raises:
            ValueError: If any flag name is not recognized.
        """
        for name, value in flags.items():
            self.set_flag(name, value)


    def get_flag(self, flag_name: str) -> bool | None:
        """Get the current value of a simulation flag.
        
        Args:
            flag_name (str): Name of the flag (case-insensitive).

        Returns:
            The current value of the flag, or None if not explicitly set.
        
        Raises:
            ValueError: If the flag name is not recognized.
        """
        name = flag_name.strip().lower()
        if name not in ALLOWED_FLAG_NAMES:
            valid = ", ".join(sorted(ALLOWED_FLAG_NAMES))
            raise ValueError(f"Unrecognized flag name: {flag_name!r}. Valid flags: {valid}")
        return self._flags.get(name)


    def clear_flag(self, flag_name: str) -> None:
        """Clear explicit value so default behavior is used.
        
        Args:
            flag_name (str): Name of the flag (case-insensitive).
            
        Raises:
            ValueError: If the flag name is not recognized.
        """
        self.set_flag(flag_name, None)

# TODO: Meta Elements
# TODO: Compiler Options
# TODO: Size Parameters
# TODO: Statistics Parameters