# aiVLE Worker

Secure and scalable grading client for aiVLE platform.

---

There are two parts in `aivle-worker` module:

- Sandbox: `sandbox.py` and everything under `profiles`, `requirements`, `scripts`
- (Celery) worker: everything else

If you want to test whether your aiVLE task bundle works, you may focus on *sandbox* part only.

## Requirement

This project is tested on the following environment. Similar environment may work but there is no guarantee.

* Ubuntu 20.04
* Firejail 0.9.62
* Python 3.8 (with `python3.8-venv`)

## Getting Started

1. Create `.env` (if you only intend to test sandbox, put dummy values on the RHS is enough):

```dotenv
BROKER_URI=amqp://... # use sqs:// for AWS SQS, and remember to pip install celery[sqs] for dependencies
ACCESS_TOKEN=...
TASK_QUEUE=gpu/private/default
CELERY_CONCURRENCY=...
WORKER_NAME=...
```

## Test Sandbox (for most users)

### tl;dr

Under `__main__.py`, rewrite paths in `start_sandbox()` function, run that function.

**NOTE**:

1. There are three `/` in the URL (i.e. `file:///home/...`)
2. You need to use absolute path

### Details

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