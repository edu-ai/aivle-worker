# aiVLE Worker

There are two parts in `aivle-worker` module:

- Sandbox: `sandbox.py` and everything under `profiles`, `requirements`, `scripts`
- (Celery) worker: everything else

If you want to test whether your aiVLE task bundle works, you may focus on *sandbox* part only.

## Requirement

This project is tested on the following environment. Similar environment may work but there is no guarantee.

* Ubuntu 20.04
* Firejail 0.9.62
* Python 3.8 (with `python3.8-venv`)

## Installation

From Test PyPI: `pip install -i https://test.pypi.org/simple/ aivle-worker`

From PyPI: `pip install aivle-worker`

## Getting Started

We assume you already installed `aivle-worker` by `pip install aivle-worker`.
(If `pip install` doesn't work, try `pip install -i https://test.pypi.org/simple/ aivle-worker` to fetch from Test PyPI)

1. Create `.env` (if you only intend to test sandbox, put dummy values on the RHS is enough):

Required fields:
```dotenv
API_BASE_URL=...
BROKER_URI=amqp://...# use sqs:// for AWS SQS, and remember to pip install celery[sqs] for dependencies
ACCESS_TOKEN=...

```
Optional fields (shown here are the default values):
```dotenv
TASK_QUEUE=gpu/private/default
CELERY_CONCURRENCY=1
WORKER_NAME=celery
ZMQ_PORT=15921
```

2. `python -m aivle-worker` **in the same directory** as your `.env` file (reason: `load_dotenv` will look for `.env`
in the current working directory).

## Test Sandbox

To test the standalone sandbox, you need to clone this repository and modify the source code under `src`.

### tl;dr

Under `src/aivle-worker/entry_point.py`, rewrite paths in `start_sandbox()` function, run that function.

**NOTE**:

1. There are three `/` in the URL (i.e. `file:///home/...`)
2. You need to use absolute path

### Details on how to run `start_sandbox()`

1. Rewrite paths in `start_sandbox()` function defined in `entry_point.py`
2. In the `if __name__ == "__main__":` block of `__main.py`, include `start_sandbox()` only
3. Make sure your current directoy is `src`, and `.env` is in `src` (i.e., `.env` is at the same level as 
`/aivle-worker`)
4. Run `python -m aivle-worker`

### How It Works

Referring to `settings.py`, by default the sandbox will load security profile from `profiles/aivle-base.profile`
and the shell script to create new virtual environment will be `scripts/create-venv.sh`, and the temporary folder will
be `/tmp/aivle-worker`. You don't need to change the settings if you're happy with the defaults.

The basic steps aivle Worker takes to evaluate an agent in your task bundle are:

1. Download and unzip task and agent archives
2. Create a new virtual environment (and activate it)
3. `pip install -r requirements.txt` (therefore in the root of your task bundle there must be a `requirements.txt`)
4. Inside the sandbox, run `bash bootstrap.sh` (similarly, `bootstrap.sh` comes from your task bundle)

## Test Sandbox + Worker (for devs only)

// TODO
