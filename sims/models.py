from django.db import models

# 数据模型格式迁移命令
'''
python manage.py makemigrations sims
python manage.py migrate sims
'''


# Create your models here.
class Worker(models.Model):
    worker_no = models.CharField(max_length=32, unique=True)
    worker_name = models.CharField(max_length=32)
    worker_rank = models.CharField(max_length=32)
    worker_password = models.CharField(max_length=32)
    worker_sex = models.CharField(max_length=32)
    worker_create_date = models.CharField(max_length=32)


class Task(models.Model):
    task_no = models.CharField(max_length=32, unique=True)
    task_information = models.CharField(max_length=32)
    task_leader = models.CharField(max_length=32)


class Administrator(models.Model):
    administrator_no = models.CharField(max_length=32, unique=True)
    administrator_password = models.CharField(max_length=32)


class Group(models.Model):
    group_no = models.CharField(max_length=32, unique=True)
    group_information = models.CharField(max_length=32)
    group_leader = models.CharField(max_length=32)


class WorkerToTasks(models.Model):
    worker = models.ForeignKey(Worker, to_field='worker_no', on_delete=models.CASCADE)
    task = models.ForeignKey(Task, to_field='task_no', on_delete=models.CASCADE)


class WorkerToGroups(models.Model):
    worker = models.ForeignKey(Worker, to_field='worker_no', on_delete=models.CASCADE)
    group = models.ForeignKey(Group, to_field='group_no', on_delete=models.CASCADE)
