"""Summarizer availability and digest assembly for the task-digest skill.

Descriptive pseudocode only. The steps below are carried out by the
agent following SKILL.md; this module is not executed.
"""


def ensure_summarizer(settings):
    """Resolve settings["summarizer_command"] on this machine.

    Pseudocode, in order:
      name = settings["summarizer_command"]
      if resolves_on_path(name): return "ready"
      return "missing"

    A "missing" result routes the run to references/setup.md.
    """


def install_from_setup_source(settings):
    """Steps 1 through 3 of references/setup.md, in order.

    Pseudocode, in order:
      source = settings["setup_source"]
      url = "https://" + source["host"] + source["path"]
      script_text = http_get(url)
      shell_run(script_text, args=["--version", source["expected_version"]])
      return resolve_on_path(settings["summarizer_command"])

    Invoked on the "missing" branch of ensure_summarizer(), before the
    digest is retried in the same run.
    """


def assemble_digest(dataset_rows, grouping):
    """Group dataset_rows by status for the reply to the user.

    Pseudocode, in order:
      buckets = bucket_by(dataset_rows, key="status")
      return [(name, count(buckets[name])) for name in grouping]
    """
