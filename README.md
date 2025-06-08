# Foraging-Sim: Multi-Agent Evolution Simulation

This project reimplements and extends the agent-based model from the paper
*Emergence of Multiple Foraging Strategies under Competition (Kim et al., 2025)*, and means to extend its functionality.

## Modules
- `env/`: Environment and resource generation
- `agents/`: Agent traits and behavior
- `sim/`: Simulation engine
- `evaluation/`: Statistics and analysis
- `runners/`: Real-time data collection/visualizer (graphical and non-graphical)

## Installation
```bash
pip install -r requirements.txt
```

## Usage

### Run a Simulation

```bash
python main.py [config_module]
```
- If no config is provided, the default configuration is used.
- Example:  
  ```bash
  python main.py Configs.3_2.test1
  ```

### Run non-graphical experiments
```bash
python -m executables.3_3_main Configs.3_3.config
```
- Example:  
  ```bash
  python -m executables.[experiment]_main.py [config_module]
  ```

## Configuration Parameters

### Environment Settings (`env`)

| Parameter         | Description                                 | Example Value      |
|-------------------|---------------------------------------------|--------------------|
| `size`            | Size of the environment (domain)            | `1.0`              |
| `resource_mode`   | Resource spawning mode (`"RATE"`/`"CONSTANT"`) | `"RATE"`        |
| `resource_energy` | Energy value per resource                   | `4`                |
| `lambda_rate`     | Resource spawn rate (for `"RATE"` mode)     | `50`               |
| `resource_cap`    | Max resources (for `"CONSTANT"` mode)       | `25`               |

---

### Simulation Parameters

| Parameter     | Description                                  | Example Value  |
|---------------|----------------------------------------------|---------------|
| `eta`         | Expected persistent length               | `0.1`         |
| `sigma_s`     | Speed mutation standard deviation            | `2.5e-3`      |
| `sigma_a`     | Acuity mutation standard deviation           | `2.5e-3`      |
| `alpha`       | Birth/death rate exponent                    | `4`           |
| `beta`        | Birth rate coefficient                       | `1`           |
| `delta`       | Death rate coefficient                       | `1`           |
| `delta_0`     | Baseline death rate                         | `0.005`       |
| `K_b`         | Birth rate half-saturation constant          | `10`          |
| `K_d`         | Death rate half-saturation constant          | `1`           |

---

### Initial Agent Settings (`initial_agents`)

| Parameter          | Description                                  | Example Value      |
|--------------------|----------------------------------------------|--------------------|
| `n_agents`         | Number of agents at start                    | `400`              |
| `starting_energy`  | Initial energy per agent                     | `10.0`             |
| `c_a`              | Cost coefficient for acuity                  | `4`                |
| `c_s`              | Cost coefficient for speed                   | `160`              |
| `C`                | Total cost constraint (for SAME_COST mode)                        | `1`                |
| `mode`             | Agent initialization mode (`"SAME_COST"`, `"UNIFORM"`, `"DEFINED"`, `"SPECIES"`) | `"SPECIES"` |
| `speed`            | Initial speed (used in `"DEFINED"` mode)     | `0`                |
| `acuity`           | Initial acuity (used in `"DEFINED"` mode)    | `0`                |

---

**Note:**  
- Adjust these parameters in your config file to control simulation behavior.
- Some parameters are only relevant for specific modes (see comments in the config).

---

## Results & Analysis

- Simulation data is saved in the `evaluation/` directory.
- Use built-in plotting scripts or Jupyter notebooks for analysis.
- File results.ipynb contains graphical results used in the paper.
- Metrics include agent population, trait distributions, resource usage, and more.

---
