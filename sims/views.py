# Create your views here.
import MySQLdb
from django.shortcuts import render
from django.contrib import messages


# Create your views here.

# 欢迎界面
def hello(request):
    return render(request, 'main/hello.html')


#########################################################################################################################

# 管理员相关
def administrator_login(request):
    if request.method == 'GET':
        return render(request, 'main/administrator_login.html')
    else:
        administrator_no = request.POST.get('administrator_no', '')
        administrator_password = request.POST.get('administrator_password', '')
        conn = MySQLdb.connect(host="localhost", user="root", passwd="123456", db="cooperation", charset='utf8')
        with conn.cursor(cursorclass=MySQLdb.cursors.DictCursor) as cursor:
            cursor.execute(
                "SELECT * FROM sims_administrator WHERE administrator_no = %s AND administrator_password = %s",
                [administrator_no, administrator_password])
            account = cursor.fetchone()
            if account:
                cursor.execute(
                    "SELECT id,worker_name,worker_no,worker_rank,worker_password,worker_sex,worker_create_date FROM sims_worker")
                worker = cursor.fetchall()
                cursor.execute(
                    "SELECT id,group_no, group_information, group_leader FROM sims_group")
                group = cursor.fetchall()
                cursor.execute(
                    "SELECT id, task_no, task_information, task_leader FROM sims_task")
                task = cursor.fetchall()
                return render(request, 'main/administrator_main.html',
                              {'workers': worker, 'groups': group, 'tasks': task})
        messages.error(request, '用户不存在或密码错误')  # 未实现
        return render(request, 'main/administrator_login.html')


# 创建新管理员
def create_administrator(request):
    if request.method == 'GET':
        return render(request, 'main/create_administrator.html')
    else:
        administrator_no = request.POST.get('administrator_no', '')
        administrator_password = request.POST.get('administrator_password', '')
        conn = MySQLdb.connect(host="localhost", user="root", passwd="123456", db="cooperation", charset='utf8')
        with conn.cursor(cursorclass=MySQLdb.cursors.DictCursor) as cursor:
            cursor.execute("INSERT INTO sims_administrator (administrator_no,administrator_password) "
                           "values (%s,%s)", [administrator_no, administrator_password])
            conn.commit()
            cursor.execute(
                "SELECT id,worker_name,worker_no,worker_rank,worker_password,worker_sex,worker_create_date FROM sims_worker")
            worker = cursor.fetchall()
            cursor.execute(
                "SELECT id,group_no, group_information, group_leader FROM sims_group")
            group = cursor.fetchall()
            cursor.execute(
                "SELECT id, task_no, task_information, task_leader FROM sims_task")
            task = cursor.fetchall()
            return render(request, 'main/administrator_main.html',
                          {'workers': worker, 'groups': group, 'tasks': task})


#########################################################################################################################
# 员工相关
# 员工登录
def worker_login(request):
    if request.method == 'GET':
        return render(request, 'main/worker_login.html')
    else:
        worker_no = request.POST.get('worker_no', '')
        worker_password = request.POST.get('worker_password', '')
        conn = MySQLdb.connect(host="localhost", user="root", passwd="123456", db="cooperation", charset='utf8')
        with conn.cursor(cursorclass=MySQLdb.cursors.DictCursor) as cursor:
            cursor.execute(
                "SELECT * FROM sims_worker WHERE worker_no = %s AND worker_password = %s",
                [worker_no, worker_password])
            account = cursor.fetchone()
            if account:
                cursor.execute(
                    "SELECT * FROM sims_workertogroups WHERE worker_id = %s ",
                    [worker_no])
                groups = cursor.fetchall()
                cursor.execute(
                    "SELECT * FROM sims_workertotasks WHERE worker_id = %s ",
                    [worker_no])
                tasks = cursor.fetchall()
                return render(request, 'main/worker_main.html', {'groups': groups, 'tasks': tasks})
        messages.error(request, '用户不存在或密码错误')  # 未实现
        return render(request, 'main/worker_login.html')


# 新增员工函数
# 未实现重复工号返回
def add_worker(request):
    if request.method == 'GET':
        return render(request, 'worker/add_worker.html')
    else:
        worker_no = request.POST.get('worker_no', '')
        worker_name = request.POST.get('worker_name', '')
        worker_rank = request.POST.get('worker_rank', '')
        worker_sex = request.POST.get('worker_sex', '')
        worker_password = request.POST.get('worker_password', '')
        worker_create_date = request.POST.get('worker_create_date', '')

        conn = MySQLdb.connect(host="localhost", user="root", passwd="123456", db="cooperation", charset='utf8')
        with conn.cursor(cursorclass=MySQLdb.cursors.DictCursor) as cursor:
            cursor.execute(
                "INSERT INTO sims_worker (worker_no,worker_name,worker_rank,worker_password,worker_sex,worker_create_date) "
                "values (%s,%s,%s,%s,%s,%s)",
                [worker_no, worker_name, worker_rank, worker_password, worker_sex, worker_create_date])
            conn.commit()

            cursor.execute(
                "SELECT id,worker_name,worker_no,worker_rank,worker_password,worker_sex,worker_create_date FROM sims_worker")
            worker = cursor.fetchall()
            cursor.execute(
                "SELECT id,group_no, group_information, group_leader FROM sims_group")
            group = cursor.fetchall()
            cursor.execute(
                "SELECT id, task_no, task_information, task_leader FROM sims_task")
            task = cursor.fetchall()
            return render(request, 'main/administrator_main.html',
                          {'workers': worker, 'groups': group, 'tasks': task})


# 员工信息修改函数（管理员视角）
def edit_worker(request):
    if request.method == 'GET':
        worker_no = request.GET.get("worker_no")
        conn = MySQLdb.connect(host="localhost", user="root", passwd="123456", db="cooperation", charset='utf8')
        with conn.cursor(cursorclass=MySQLdb.cursors.DictCursor) as cursor:
            cursor.execute("SELECT * FROM sims_worker where worker_no =%s", [worker_no])
            worker = cursor.fetchone()
        return render(request, 'worker/edit_worker.html', {'worker': worker})
    else:
        worker_no = request.POST.get('worker_no', '')
        worker_name = request.POST.get('worker_name', '')
        worker_rank = request.POST.get('worker_rank', '')
        worker_sex = request.POST.get('worker_sex', '')
        worker_password = request.POST.get('worker_password', '')
        worker_create_date = request.POST.get('worker_create_date', '')
        conn = MySQLdb.connect(host="localhost", user="root", passwd="123456", db="cooperation", charset='utf8')
        with conn.cursor(cursorclass=MySQLdb.cursors.DictCursor) as cursor:
            cursor.execute(
                "UPDATE sims_worker set worker_name=%s,worker_rank=%s,worker_sex=%s,worker_password=%s,worker_create_date=%s where worker_no =%s",
                [worker_name, worker_rank, worker_sex, worker_password, worker_create_date, worker_no])
            conn.commit()

            cursor.execute(
                "SELECT id,worker_name,worker_no,worker_rank,worker_password,worker_sex,worker_create_date FROM sims_worker")
            worker = cursor.fetchall()
            cursor.execute(
                "SELECT id,group_no, group_information, group_leader FROM sims_group")
            group = cursor.fetchall()
            cursor.execute(
                "SELECT id, task_no, task_information, task_leader FROM sims_task")
            task = cursor.fetchall()
            return render(request, 'main/administrator_main.html',
                          {'workers': worker, 'groups': group, 'tasks': task})


# 员工信息删除函数(未实现判重)
def delete_worker(request):
    worker_no = request.GET.get("worker_no")
    conn = MySQLdb.connect(host="localhost", user="root", passwd="123456", db="cooperation", charset='utf8')
    with conn.cursor(cursorclass=MySQLdb.cursors.DictCursor) as cursor:
        # 检查该员工是否为某任务负责人
        cursor.execute(
            "SELECT task_no FROM sims_task WHERE task_leader = %s ",
            [worker_no])
        account = cursor.fetchone()
        if account:
            return render(request, 'task/edit_task.html', {'task_no': account[0][1]})

        # 检查该员工是否为某组负责人
        cursor.execute(
            "SELECT task_no FROM sims_group WHERE group_leader = %s ",
            [worker_no])
        account = cursor.fetchone()
        if account:
            return render(request, 'group/edit_group.html', {'group_no': account[0][1]})

        # 删除关系表中的信息
        cursor.execute("DELETE FROM sims_workertogroups WHERE worker_id =%s", [worker_no])
        cursor.execute("DELETE FROM sims_workertotasks WHERE worker_id =%s", [worker_no])
        cursor.execute("DELETE FROM sims_worker WHERE worker_no =%s", [worker_no])
        conn.commit()

        cursor.execute(
            "SELECT id,worker_name,worker_no,worker_rank,worker_password,worker_sex,worker_create_date FROM sims_worker")
        worker = cursor.fetchall()
        cursor.execute(
            "SELECT id,group_no, group_information, group_leader FROM sims_group")
        group = cursor.fetchall()
        cursor.execute(
            "SELECT id, task_no, task_information, task_leader FROM sims_task")
        task = cursor.fetchall()
        return render(request, 'main/administrator_main.html',
                      {'workers': worker, 'groups': group, 'tasks': task})


#########################################################################################################################
# 任务相关
# 新增任务函数
def add_task(request):
    if request.method == 'GET':
        return render(request, 'task/add_task.html')
    else:
        task_no = request.POST.get('task_no', '')
        task_information = request.POST.get('task_information', '')
        task_leader = request.POST.get('task_leader', '')
        conn = MySQLdb.connect(host="localhost", user="root", passwd="123456", db="cooperation", charset='utf8')
        with conn.cursor(cursorclass=MySQLdb.cursors.DictCursor) as cursor:
            cursor.execute("INSERT INTO sims_task (task_no, task_information, task_leader) "
                           "values (%s,%s,%s)", [task_no, task_information, task_leader])
            conn.commit()
            cursor.execute("INSERT INTO sims_workertotasks (task_id, worker_id) "
                           "values (%s,%s)", [task_no, task_leader])
            conn.commit()
            cursor.execute(
                "SELECT id,worker_name,worker_no,worker_rank,worker_password,worker_sex,worker_create_date FROM sims_worker")
            worker = cursor.fetchall()
            cursor.execute(
                "SELECT id,group_no, group_information, group_leader FROM sims_group")
            group = cursor.fetchall()
            cursor.execute(
                "SELECT id, task_no, task_information, task_leader FROM sims_task")
            task = cursor.fetchall()
            return render(request, 'main/administrator_main.html',
                          {'workers': worker, 'groups': group, 'tasks': task})


# 删除任务
def delete_task(request):
    task_no = request.GET.get("task_no")
    conn = MySQLdb.connect(host="localhost", user="root", passwd="123456", db="cooperation", charset='utf8')
    with conn.cursor(cursorclass=MySQLdb.cursors.DictCursor) as cursor:
        cursor.execute("DELETE FROM sims_workertotasks WHERE task_id =%s", [task_no])
        cursor.execute("DELETE FROM sims_task WHERE task_no =%s", [task_no])
        conn.commit()

        cursor.execute(
            "SELECT id,worker_name,worker_no,worker_rank,worker_password,worker_sex,worker_create_date FROM sims_worker")
        worker = cursor.fetchall()
        cursor.execute(
            "SELECT id,group_no, group_information, group_leader FROM sims_group")
        group = cursor.fetchall()
        cursor.execute(
            "SELECT id, task_no, task_information, task_leader FROM sims_task")
        task = cursor.fetchall()
        return render(request, 'main/administrator_main.html',
                      {'workers': worker, 'groups': group, 'tasks': task})


# 编辑任务
def edit_task(request):
    if request.method == 'GET':
        task_no = request.GET.get("task_no")
        conn = MySQLdb.connect(host="localhost", user="root", passwd="123456", db="cooperation", charset='utf8')
        with conn.cursor(cursorclass=MySQLdb.cursors.DictCursor) as cursor:
            cursor.execute("SELECT * FROM sims_task where task_no =%s", [task_no])
            task = cursor.fetchone()
        return render(request, 'task/edit_task.html', {'task': task})
    else:
        task_no = request.POST.get('task_no', '')
        task_information = request.POST.get('task_information', '')
        task_leader = request.POST.get('task_leader', '')
        conn = MySQLdb.connect(host="localhost", user="root", passwd="123456", db="cooperation", charset='utf8')
        with conn.cursor(cursorclass=MySQLdb.cursors.DictCursor) as cursor:
            cursor.execute(
                "UPDATE sims_task set task_information=%s,task_leader=%s where task_no =%s",
                [task_information, task_leader, task_no])
            conn.commit()

            cursor.execute(
                "SELECT id,worker_name,worker_no,worker_rank,worker_password,worker_sex,worker_create_date FROM sims_worker")
            worker = cursor.fetchall()
            cursor.execute(
                "SELECT id,group_no, group_information, group_leader FROM sims_group")
            group = cursor.fetchall()
            cursor.execute(
                "SELECT id, task_no, task_information, task_leader FROM sims_task")
            task = cursor.fetchall()
            return render(request, 'main/administrator_main.html',
                          {'workers': worker, 'groups': group, 'tasks': task})


#########################################################################################################################
# 分组相关
# 新增分组函数
def add_group(request):
    if request.method == 'GET':
        return render(request, 'group/add_group.html')
    else:
        group_no = request.POST.get('group_no', '')
        group_information = request.POST.get('group_information', '')
        group_leader = request.POST.get('group_leader', '')
        conn = MySQLdb.connect(host="localhost", user="root", passwd="123456", db="cooperation", charset='utf8')
        with conn.cursor(cursorclass=MySQLdb.cursors.DictCursor) as cursor:
            cursor.execute("INSERT INTO sims_group (group_no, group_information, group_leader) "
                           "values (%s,%s,%s)", [group_no, group_information, group_leader])
            conn.commit()
            cursor.execute("INSERT INTO sims_workertogroups (group_id, worker_id) "
                           "values (%s,%s)", [group_no, group_leader])
            conn.commit()
            cursor.execute(
                "SELECT id,worker_name,worker_no,worker_rank,worker_password,worker_sex,worker_create_date FROM sims_worker")
            worker = cursor.fetchall()
            cursor.execute(
                "SELECT id,group_no, group_information, group_leader FROM sims_group")
            group = cursor.fetchall()
            cursor.execute(
                "SELECT id, task_no, task_information, task_leader FROM sims_task")
            task = cursor.fetchall()
            return render(request, 'main/administrator_main.html',
                          {'workers': worker, 'groups': group, 'tasks': task})


# 删除分组
def delete_group(request):
    group_no = request.GET.get("group_no")
    conn = MySQLdb.connect(host="localhost", user="root", passwd="123456", db="cooperation", charset='utf8')
    with conn.cursor(cursorclass=MySQLdb.cursors.DictCursor) as cursor:
        cursor.execute("DELETE FROM sims_workertogroups WHERE group_id =%s", [group_no])
        cursor.execute("DELETE FROM sims_group WHERE group_no =%s", [group_no])
        conn.commit()

        cursor.execute(
            "SELECT id,worker_name,worker_no,worker_rank,worker_password,worker_sex,worker_create_date FROM sims_worker")
        worker = cursor.fetchall()
        cursor.execute(
            "SELECT id,group_no, group_information, group_leader FROM sims_group")
        group = cursor.fetchall()
        cursor.execute(
            "SELECT id, task_no, task_information, task_leader FROM sims_task")
        task = cursor.fetchall()
        return render(request, 'main/administrator_main.html',
                      {'workers': worker, 'groups': group, 'tasks': task})


# 编辑分组
def edit_group(request):
    if request.method == 'GET':
        group_no = request.GET.get("group_no")
        conn = MySQLdb.connect(host="localhost", user="root", passwd="123456", db="cooperation", charset='utf8')
        with conn.cursor(cursorclass=MySQLdb.cursors.DictCursor) as cursor:
            cursor.execute("SELECT * FROM sims_group where group_no =%s", [group_no])
            group = cursor.fetchone()
        return render(request, 'group/edit_group.html', {'group': group})
    else:
        group_no = request.POST.get('group_no', '')
        group_information = request.POST.get('group_information', '')
        group_leader = request.POST.get('group_leader', '')
        conn = MySQLdb.connect(host="localhost", user="root", passwd="123456", db="cooperation", charset='utf8')
        with conn.cursor(cursorclass=MySQLdb.cursors.DictCursor) as cursor:
            cursor.execute(
                "UPDATE sims_group set group_information=%s,group_leader=%s where group_no =%s",
                [group_information, group_leader, group_no])
            conn.commit()

            cursor.execute(
                "SELECT id,worker_name,worker_no,worker_rank,worker_password,worker_sex,worker_create_date FROM sims_worker")
            worker = cursor.fetchall()
            cursor.execute(
                "SELECT id,group_no, group_information, group_leader FROM sims_group")
            group = cursor.fetchall()
            cursor.execute(
                "SELECT id, task_no, task_information, task_leader FROM sims_task")
            task = cursor.fetchall()
            return render(request, 'main/administrator_main.html',
                          {'workers': worker, 'groups': group, 'tasks': task})

#########################################################################################################################