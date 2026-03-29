# Open Data Mesh CLI (`odm`)

The `odm` command-line interface provides a convenient way to manage Open Data Mesh resources (Data Products and Data Contracts). It is built directly on top of the `open-data-mesh-sdk`, ensuring consistent business logic and validation across all entry points.

## Installation

```bash
pip install open-data-mesh-cli
```

## Getting Started

Initialize your local environment with SQLite:

```bash
odm init
```

By default, this will:
1.  Create a `~/.dm` directory.
2.  Initialize a local SQLite database at `~/.dm/odm.db`.
3.  Store the configuration in `~/.dm/config.yaml`.

## Usage

### Data Products

-   **Publish/Create**: `odm put dp spec.yaml`
-   **Get**: `odm get dp <id>` or `odm get dp --domain finance --name revenue`
-   **List**: `odm list dps`
-   **Delete**: `odm delete dp <id>`

### Data Contracts

-   **Create**: `odm put dc spec.yaml --dp <parent-id-or-path>` or `odm put dc spec.yaml --domain finance --dp_name revenue`
-   **Get**: `odm get dc <id>`
-   **List**: `odm list dcs`
-   **Delete**: `odm delete dc <id>`

### General Commands

-   **Reset**: `odm reset` — Wipes the local environment and reinitializes it.
-   **Deinit**: `odm deinit` — Removes all local data mesh state.
-   **Version**: `odm version`

## Configuration

The CLI configuration is stored in `~/.dm/config.yaml`. You can manually update it to point to different environments (e.g., remote REST API).

```yaml
sqlite:
  path: /absolute/path/to/your/odm.db
```

## Developer Environment

To run during local development using the SDK directly:

```bash
uv run odm --help
```
