from pathlib import Path
from typing import Any, Optional
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from pytz import utc
from appdirs import user_data_dir
from walldo import __name__

SQLITE_DB = Path(user_data_dir(__name__)) / "scheduler.sqlite"
if not SQLITE_DB.parent.exists():
    SQLITE_DB.parent.mkdir(parents=True)

class scheduler_meta(type):

    __instance: Optional['scheduler_creator'] = None
    __jobstore: Optional[SQLAlchemyJobStore] = None

    def __call__(cls, *args: Any, **kwds: Any) -> Any:
        if not cls.__instance:
            cls.__instance = type.__call__(cls, *args, **kwds)
        return cls.__instance

    @ property
    def jobstore(cls) -> SQLAlchemyJobStore:
        if not cls.__jobstore:
            cls.__jobstore = SQLAlchemyJobStore(
                url=f'sqlite:///{SQLITE_DB.as_posix()}'
            )

        return cls.__jobstore


class scheduler_creator(object, metaclass=scheduler_meta):
    def __init__(self) -> None:
        self.__scheduler = BackgroundScheduler(
            jobstores={
                **dict(default=scheduler_creator.jobstore)
            },
            executors={
                **dict(
                    default=ThreadPoolExecutor(20),
                    processpool=ProcessPoolExecutor(5)
                )
            },
            job_defaults={
                **dict(
                    coalesce=False,
                    max_instances=1
                )
            },
            timezone=utc
        )

    @property
    def scheduler(self) -> BackgroundScheduler:
        return self.__scheduler


Scheduler: BackgroundScheduler = scheduler_creator().scheduler
