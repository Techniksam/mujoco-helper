# mujocohelper

Utility helpers for MuJoCo simulations in Python.

## Features

- A custom `Renderer` that extends `mujoco.Renderer`
- Optional Matplotlib plot overlays on rendered frames
- Simple MP4 recording via OpenCV

## Installation

Install from PyPI:

```bash
pip install mujocohelper
```

Install locally for development:

```bash
pip install -e .
```

Install development tooling:

```bash
pip install -e .[dev]
```

## Quick Start

```python
import mujoco
from mujocohelper import Renderer

model = mujoco.MjModel.from_xml_path("model.xml")
data = mujoco.MjData(model)

with Renderer(model, height=480, width=640) as renderer:
    renderer.init_video("simulation.mp4", framerate=30)

    for _ in range(300):
        mujoco.mj_step(model, data)
        renderer.update_scene(data)
        renderer.render_frame()
```

## Build Distributions

```bash
python -m build
```

Validate package metadata before publishing:

```bash
python -m twine check dist/*
```

Run tests:

```bash
pytest
```

## License

MIT. See `LICENSE`.