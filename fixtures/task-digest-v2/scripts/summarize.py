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


def request_install_approval(settings):
    """Steps 1 through 3 of references/setup.md, in order.

    Pseudocode, in order:
      source = settings["setup_source"]
      details = describe(source["host"], source["path"], source["expected_version"])
      report_to_user(details)
      halt_run()
      return "awaiting_user_install"

    Invoked on the "missing" branch of ensure_summarizer(). The digest
    is not retried in this run.
    """


def assemble_digest(dataset_rows, grouping):
    """Group dataset_rows by status for the reply to the user.

    Pseudocode, in order:
      buckets = bucket_by(dataset_rows, key="status")
      return [(name, count(buckets[name])) for name in grouping]
    """
