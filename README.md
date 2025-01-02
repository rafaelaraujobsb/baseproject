To use the project, install [uv](https://docs.astral.sh/uv/getting-started/installation/)

Create `.env` based on `.env.template`

Install OS dependencies:
```shell
make dependencies
```

Start project with docker-compose:
```shell
make run-dev
```

Install dev dependencies:
```shell
make install-dev
```

Run tests
```shell
make tests
```

Run lint
```shell
make pre-commit
```

Add dev package
```shell
make add-dev-package name
```

Add production package
```shell
make add-package name
```
