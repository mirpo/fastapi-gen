# FastApi Gen

Create FastAPI apps with no build configuration.

FastApi Gen works on macOS and Linux.<br>
If something doesn’t work, please [file an issue](https://github.com/mirpo/fastapi-gen/issues/new).

Available templates:

1. Default - basic template with GET/POST examples.
2. Nlp - natural language processing template with examples how to use Hugginface summarization, named-entity recognition and text generation using LLM.

More to come!

## Quick Overview

```console
pip3 install fastapi-gen
fastapi-gen my_app
cd my_app
make start-dev
```

or 

```console
pipx run fastapi-gen my_app
cd my_app
make start-dev
```

If you've previously installed `fastapi-gen` globally via `pip3 install fastapi-gen`, we recommend you reinstall the package using `pip3 install --upgrade --force-reinstall fastapi-gen` or `pipx upgrade fastapi-gen` to ensure that you use the latest version.

Then open http://localhost:8000/docs to see your app OpenAPI documentation.

### Get Started Immediately

You **don’t** need to install or configure depencendeices like FastApi or Pytest.<br>
They are preconfigured and hidden so that you can focus on the code.

Create a project, and you’re good to go.

## Creating an App

**You’ll need to have Python 3.7+ or later version on your local development machine**. We recommend using the latest LTS version. You can use [pyenv](https://github.com/pyenv/pyenv) (macOS/Linux) to switch Python versions between different projects.

### basic template

```console
pip3 install fastapi-gen
fastapi-gen my_app
```

or

```console
pip3 install fastapi-gen
fastapi-gen my_app --template hello_world
```

### NLP template

```console
pip install fastapi-gen
fastapi-gen my_app --template nlp
```

Inside the newly created project, you can run some built-in commands:

### `make start`

Runs the app in development mode.<br>
Open [http://localhost:8000/docs](http://localhost:8000/docs) to view OpenAPI documentation in the browser.

The page will automatically reload if you make changes to the code.

### `make test`

Runs tests.<br>
By default, runs tests related to files changed since the last commit.

## License

`fastapi-gen` is distributed under the terms of the [MIT](https://github.com/mirpo/fastapi-gen/blob/master/LICENSE) license.
