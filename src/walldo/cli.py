import click
from time import sleep
from typing import Optional
from walldo import jobs
from walldo.schedule.scheduler import Scheduler
import logging
import sys
import signal


def output(txt: str, color="bright_blue"):
    click.secho(txt, fg=color)


def error(e: Exception, txt: Optional[str] = None):
    if not txt:
        txt = f"{e}"
    click.secho(txt, fg="bright_red", err=True)
    if e:
        logging.debug(txt, exc_info=e)


@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx: click.Context):
    if ctx.invoked_subcommand is None:
        ctx.invoke(cli_service)


@cli.command("quit")
def quit():
    """Quit."""
    output("Bye!", color="blue")
    sys.exit(0)

@cli.command("change", short_help="Change current wallpaper with random one")
@click.pass_context
def cli_change(ctx: click.Context):
    job_func = getattr(jobs, jobs.Job.ROTATE)
    assert job_func
    job_func()


@cli.command("service", short_help="Start api server")
@click.pass_context
def cli_service(ctx: click.Context):

    def handler_stop_signals(signum, frame):
        logging.warning("Stopping app")
        Scheduler.shutdown()
        quit()

    signal.signal(signal.SIGINT, handler_stop_signals)
    signal.signal(signal.SIGTERM, handler_stop_signals)
    try:
        logging.info(getattr(jobs, jobs.Job.ROTATE))
        Scheduler.add_job(
            func=f"walldo.jobs:{jobs.Job.ROTATE}",
            id=f"{jobs.Job.ROTATE.value}",
            trigger=jobs.JobTrigger.INTERVAL,
            minutes=30,
            misfire_grace_time=60,
            replace_existing=True,
            coalesce=True
        )
        Scheduler.start()
        while True:
            sleep(0.2)
    except KeyboardInterrupt:
        raise RuntimeError
    except AssertionError:
        output("service")
        raise RuntimeError
    except Exception as e:
        logging.error(e)
        raise RuntimeError

def run():
    try:
        cli()
    except AssertionError as e:
        raise e


if __name__ == "__main__":
    run()
