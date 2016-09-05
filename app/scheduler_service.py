# -*- coding:utf-8 -*-

import time
from sqlalchemy import or_,and_

from model import db
from model.Scheduler import DatabaseSchedulerEntry,CrontabSchedule,IntervalSchedule,SchedulerHistory,Task

from decorator.task import celery

class SchedulerService:

    def __init__(self):
        pass

    @staticmethod
    def add_schedule(name, task, args, kwargs, enabled, every=None, period=None, minute=None, hour=None, day_of_week=None,
               day_of_month=None, month_of_year=None):
        dse = DatabaseSchedulerEntry()
        dse.name = name
        dse.task = task
        if not args:
            args='[]'
        if not kwargs:
            kwargs='{}'
        dse.arguments = args
        dse.keyword_arguments = kwargs
        dse.enabled=enabled
        if every and period:
            dse.interval = IntervalSchedule(every=every, period=period)
        elif minute or hour or day_of_week or day_of_month or month_of_year:
            dse.crontab = CrontabSchedule(minute=minute, hour=hour, day_of_week=day_of_week, day_of_month=day_of_month, month_of_year=month_of_year)
        db.session.add(dse)
        db.session.commit()

    @staticmethod
    def del_schedule(sid):
        dse = DatabaseSchedulerEntry.query.get(sid)
        db.session.delete(dse)
        db.session.commit()

    @staticmethod
    def get_schedule_list():
        ss = DatabaseSchedulerEntry.query.all()
        return ss

    @staticmethod
    def get_schedule_detail(sid):
        dse = DatabaseSchedulerEntry.query.get(sid)
        return dse.detail()

    @staticmethod
    def get_task_list():
        ret = list()
        for t in celery.tasks:
            n = str(t)
            if n[0:6]!='celery':
                ret.insert(0, str(t))
        return ret

    @staticmethod
    def get_task_history(query, start_at):
        ss = db.session.query(DatabaseSchedulerEntry.id).filter(or_(DatabaseSchedulerEntry.name.like("%" + query + "%") if query is not None else "",
                                                     DatabaseSchedulerEntry.task.like("%" + query + "%") if query is not None else ""))
        sh = SchedulerHistory.query.filter(SchedulerHistory.schedule_id.in_(ss),
                                           and_(SchedulerHistory.date_start >= start_at + ' 00:00:00',
                                                SchedulerHistory.date_start <= start_at + ' 23:59:59') if start_at is not None else "")
        return sh

    @staticmethod
    def get_task_history_detail(sh_id):
        ret = dict()
        sh = SchedulerHistory.query.get(sh_id)
        if sh:
            ret['id'] = sh.id
            ret['args'] = sh.schedule.arguments
            ret['kwargs'] = sh.schedule.keyword_arguments
            task_id = sh.task_id
            task = Task.query.filter(Task.task_id==task_id).first()
            if task:
                ret['result'] = task.result
                ret['traceback'] = task.traceback
            else:
                ret['result'] = None
                ret['traceback'] = None
            return ret
