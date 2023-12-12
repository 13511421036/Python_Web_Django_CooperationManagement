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
# （增加特权管理员，可以删除普通管理员，修改普通管理员密码）
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
                if administrator_no == 'root':
                    cursor.execute(
                        "SELECT administrator_no, administrator_password FROM sims_administrator")
                    administrator = cursor.fetchall()
                    return render(request, 'main/vip_administrator.html', {'administrators': administrator})

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
# （未实现判断管理员id重复，普通管理员不能创建新管理员）
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
                "SELECT administrator_no, administrator_password FROM sims_administrator")
            administrator = cursor.fetchall()
            return render(request, 'main/vip_administrator.html', {'administrators': administrator})


# 修改管理员密码
def edit_administrator(request):
    if request.method == 'GET':
        administrator_no = request.GET.get("administrator_no")
        conn = MySQLdb.connect(host="localhost", user="root", passwd="123456", db="cooperation", charset='utf8')
        with conn.cursor(cursorclass=MySQLdb.cursors.DictCursor) as cursor:
            cursor.execute("SELECT * FROM sims_administrator where administrator_no=%s", [administrator_no])
            account = cursor.fetchone()
            administrator = account
            return render(request, 'main/edit_administrator.html', {'administrator': administrator})
    else:
        administrator_no = request.POST.get('administrator_no', '')
        administrator_password = request.POST.get('administrator_password', '')
        conn = MySQLdb.connect(host="localhost", user="root", passwd="123456", db="cooperation", charset='utf8')
        with conn.cursor(cursorclass=MySQLdb.cursors.DictCursor) as cursor:
            cursor.execute(
                "UPDATE sims_administrator set administrator_password=%s where administrator_no =%s",
                [administrator_password, administrator_no])
            conn.commit()
            cursor.execute(
                "SELECT administrator_no, administrator_password FROM sims_administrator")
            administrator = cursor.fetchall()
            return render(request, 'main/vip_administrator.html', {'administrators': administrator})


# 删除管理员
def delete_administrator(request):
    administrator_no = request.GET.get("administrator_no")
    conn = MySQLdb.connect(host="localhost", user="root", passwd="123456", db="cooperation", charset='utf8')
    with conn.cursor(cursorclass=MySQLdb.cursors.DictCursor) as cursor:
        cursor.execute("DELETE FROM sims_administrator WHERE administrator_no =%s", [administrator_no])
        conn.commit()
        cursor.execute(
            "SELECT administrator_no, administrator_password FROM sims_administrator")
        administrator = cursor.fetchall()
        return render(request, 'main/vip_administrator.html', {'administrators': administrator})


#########################################################################################################################
# 员工相关
# 员工登录
# （增加员工是否为任务负责人，组负责人判断，若是则可以提交任务或新增组员）
# （增加个人信息界面按钮）
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
                    "SELECT group_no, group_information, group_leader FROM sims_group "
                    "JOIN sims_workertogroups ON sims_group.group_no = sims_workertogroups.group_id "
                    "WHERE sims_workertogroups.worker_id = %s ",
                    [worker_no])
                groups = cursor.fetchall()

                cursor.execute(
                    "SELECT task_no, task_information, task_leader FROM sims_task "
                    "JOIN sims_workertotasks ON sims_task.task_no = sims_workertotasks.task_id "
                    "WHERE sims_workertotasks.worker_id = %s ",
                    [worker_no])
                tasks = cursor.fetchall()
                return render(request, 'main/worker_main.html', {'groups': groups, 'tasks': tasks})


# 新增员工
# （未实现重复工号返回）
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


# 员工信息修改（管理员视角）
# （工号不允许修改）
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


# 员工信息删除
def delete_worker(request):
    worker_no = request.GET.get("worker_no")
    conn = MySQLdb.connect(host="localhost", user="root", passwd="123456", db="cooperation", charset='utf8')
    with conn.cursor(cursorclass=MySQLdb.cursors.DictCursor) as cursor:
        # 检查该员工是否为某任务负责人
        cursor.execute(
            "SELECT task_no,task_leader FROM sims_task WHERE task_leader = %s ",
            [worker_no])
        account = cursor.fetchone()
        if account:
            cursor.execute("SELECT * FROM sims_task where task_leader =%s", [account['task_leader']])
            task = cursor.fetchone()
            return render(request, 'task/edit_task.html',
                          {'task': task, 'show_popup': True,
                           'popup_message': '该员工为某任务负责人，请先修改任务负责人'})

        # 检查该员工是否为某组负责人
        cursor.execute(
            "SELECT group_no,group_leader FROM sims_group WHERE group_leader = %s ",
            [worker_no])
        account = cursor.fetchone()
        if account:
            cursor.execute("SELECT * FROM sims_group where group_leader =%s", [account['group_leader']])
            group = cursor.fetchone()
            return render(request, 'group/edit_group.html',
                          {'group': group, 'show_popup': True, 'popup_message': '该员工为某组负责人，请先修改组负责人'})

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


# 员工个人信息查看(员工视角)
# （空）
def view_worker_self(request):
    return None


#########################################################################################################################
# 任务相关


# 新增任务
# （未实现任务号判重，或者任务号自添加？）
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
        return render(request, 'task/edit_task.html', {'task': task}, 'show_popup', False)
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


# 查看任务
def view_task(request):
    task_no = request.GET.get("task_no")

    # 连接数据库
    conn = MySQLdb.connect(host="localhost", user="root", passwd="123456", db="cooperation", charset='utf8')

    with conn.cursor(cursorclass=MySQLdb.cursors.DictCursor) as cursor:
        # 查询任务信息和任务领导者编号

        # 查询组信息和组领导者编号

        cursor.execute(
            "SELECT task_no, task_information, task_leader FROM sims_task WHERE task_no = %s", [task_no])
        task = cursor.fetchone()

        # 查询领导者姓名
        cursor.execute(
            "SELECT worker_name FROM sims_worker WHERE worker_no = %s", [task['task_leader']])
        leader = cursor.fetchone()
        leader_name = leader['worker_name'] if leader else None

        # 查询任务成员的详细信息
        cursor.execute(
            "SELECT worker_no, worker_name, worker_sex, worker_rank FROM sims_worker "
            "JOIN sims_workertotasks ON sims_worker.worker_no = sims_workertotasks.worker_id ")

        # 查询小组成员的详细信息
        cursor.execute(
            "SELECT worker_no, worker_name, worker_sex, worker_rank FROM sims_worker "
            "JOIN sims_workertotasks ON sims_worker.worker_no = sims_workertotasks.worker_id "

            "WHERE sims_workertotasks.task_id = %s AND sims_worker.worker_no != %s",
            [task_no, task['task_leader']])
        workers = cursor.fetchall()

    #
    return render(request, 'task/view_task.html', {
        'task': task,
        'leader_name': leader_name,
        'workers': workers
    })


# 新增任务成员(管理员)
def add_worker_task(request):
    if request.method == 'GET':
        worker_no = request.GET.get("worker_no")
        return render(request, 'task/add_worker_task.html', {'worker_no': worker_no})
    else:
        task_id = request.POST.get('task_id', '')
        worker_id = request.POST.get('worker_id', '')
        conn = MySQLdb.connect(host="localhost", user="root", passwd="123456", db="cooperation", charset='utf8')
        with conn.cursor(cursorclass=MySQLdb.cursors.DictCursor) as cursor:
            cursor.execute("INSERT INTO sims_workertotasks (task_id, worker_id) values (%s,%s)", [task_id, worker_id])
            conn.commit()
        with conn.cursor(cursorclass=MySQLdb.cursors.DictCursor) as cursor:
            # 查询任务信息和任务领导者编号
            cursor.execute(
                "SELECT task_no, task_information, task_leader FROM sims_task WHERE task_no = %s", [task_id])
            task = cursor.fetchone()

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
# 新增分组
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
        return render(request, 'group/edit_group.html', {'group': group}, 'show_popup', False)
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


def view_group(request):
    group_no = request.GET.get("group_no")

    # 连接数据库
    conn = MySQLdb.connect(host="localhost", user="root", passwd="123456", db="cooperation", charset='utf8')

    with conn.cursor(cursorclass=MySQLdb.cursors.DictCursor) as cursor:
        # 查询组信息和组领导者编号
        cursor.execute(
            "SELECT group_no, group_information, group_leader FROM sims_group WHERE group_no = %s", [group_no])
        group = cursor.fetchone()

        # 查询领导者姓名
        cursor.execute(
            "SELECT worker_name FROM sims_worker WHERE worker_no = %s", [group['group_leader']])
        leader = cursor.fetchone()
        leader_name = leader['worker_name'] if leader else None

        # 查询小组成员的详细信息
        cursor.execute(
            "SELECT worker_no, worker_name, worker_sex, worker_rank FROM sims_worker "
            "JOIN sims_workertogroups ON sims_worker.worker_no = sims_workertogroups.worker_id "
            "WHERE sims_workertogroups.group_id = %s AND sims_worker.worker_no != %s",
            [group_no, group['group_leader']])
        workers = cursor.fetchall()

    #
    return render(request, 'group/view_group.html', {
        'group': group,
        'leader_name': leader_name,
        'workers': workers
    })


# 给小组新增组员(管理员指派)
def add_worker_group(request):
    if request.method == 'GET':
        group_no = request.GET.get("group_no")
        return render(request, 'group/add_worker_group.html', {'group_no': group_no})
    else:
        group_id = request.POST.get('group_id', '')
        worker_id = request.POST.get('worker_id', '')
        conn = MySQLdb.connect(host="localhost", user="root", passwd="123456", db="cooperation", charset='utf8')
        with conn.cursor(cursorclass=MySQLdb.cursors.DictCursor) as cursor:
            cursor.execute("INSERT INTO sims_workertogroups (group_id, worker_id) "
                           "values (%s,%s)", [group_id, worker_id])
            conn.commit()
            # 查询组信息和组领导者编号
            cursor.execute(
                "SELECT group_no, group_information, group_leader FROM sims_group WHERE group_no = %s", [group_id])
            group = cursor.fetchone()

            # 查询领导者姓名
            cursor.execute(
                "SELECT worker_name FROM sims_worker WHERE worker_no = %s", [group['group_leader']])
            leader = cursor.fetchone()
            leader_name = leader['worker_name'] if leader else None

            # 查询小组成员的详细信息
            cursor.execute(
                "SELECT worker_no, worker_name, worker_sex, worker_rank FROM sims_worker "
                "JOIN sims_workertogroups ON sims_worker.worker_no = sims_workertogroups.worker_id "
                "WHERE sims_workertogroups.group_id = %s AND sims_worker.worker_no != %s",
                [group_id, group['group_leader']])
            workers = cursor.fetchall()

            #
        return render(request, 'group/view_group.html', {
            'group': group,
            'leader_name': leader_name,
            'workers': workers
        })
#########################################################################################################################
