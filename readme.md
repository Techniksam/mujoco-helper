# mujocohelper

Utility helpers for MuJoCo simulations in Python.

## Features

- A custom `Renderer` that extends `mujoco.Renderer`
- Optional Matplotlib plot overlays on rendered frames
- Simple MP4 recording via OpenCV

## Installation

Install directly from the repository via pip + git:

```bash
pip install "git+https://github.com/Techniksam/mujocohelper.git"
```

Install a specific tag or branch:

```bash
pip install "git+https://github.com/Techniksam/mujocohelper.git@v0.1.0"
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

## CI Workflows

- `package-check.yml` runs tests and verifies installation through a git URL.
- `git-install-release-check.yml` validates that the release tag is installable via pip from GitHub.

Run tests:

```bash
pytest
```

## License

MIT. See `LICENSE`.