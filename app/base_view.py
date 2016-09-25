# -*- coding:utf-8 -*-

from flask import Blueprint,render_template,jsonify,request,redirect,url_for,make_response,session
from . import app
from user_service import UserService
from role_service import RoleService
from privilege_service import PrivilegeService
from login_service import LoginService
from task_pool import TaskPool
from scheduler_service import SchedulerService
from util import Util
from decorator.user import login_required,privilege
from decorator.task import celery

baseProfile = Blueprint('baseProfile', __name__)
userService = UserService()
roleService = RoleService()
privilegeService = PrivilegeService()
loginService = LoginService()
taskPool = TaskPool()
schedulerService = SchedulerService()
perPage = 10
util = Util()



@app.route('/test', methods=['GET','POST'])
def test():
    result = taskPool.test2.delay(1, 2)
    print result.id
    #result.wait()
    return 'ok', 200


@app.route('/test2', methods=['GET','POST'])
def test2():
    res_id = request.values.get('res_id')
    print res_id
    result = celery.AsyncResult(res_id)
    print result.state
    print result.get(timeout=10)
    #result.wait()
    return 'ok', 200


@app.route('/test3', methods=['GET','POST'])
def test3():
    return jsonify(schedulerService.get_schedule_detail(2))


@app.route('/login', methods=['GET'])
def login():
    if session.get('token') is not None:
        return redirect(url_for('home'))
    else:
        return render_template('login.html',title=u'登录')


@app.route('/logout', methods=['GET'])
def logout():
    session.pop('token')
    resp = make_response(redirect(url_for('login')))
    resp.set_cookie('token', '', expires=0)
    return resp


@app.route('/authenticate', methods=['POST'])
def authenticate():
    username = request.values.get('username')
    password = request.values.get('password')
    ret = {}
    user_id = loginService.authenticate(username, password)
    if user_id:
        login_ip=util.get_ip_addr()
        loginService.add_login_history(username,login_ip)
        loginService.add_user_login_count(username)
        token = loginService.give_token(username)
        session['token'] = token
        session['userId'] = user_id
        ret['result'] = 1
        resp = make_response(jsonify(ret))
        resp.set_cookie('token',token)
    else:
        ret['result'] = 0
        resp = make_response(jsonify(ret))
    return resp


@app.route('/register', methods=['GET'])
def register():
    #show register
    return render_template('register.html',title=u'注册')


@app.route('/create-user', methods=['POST'])
def create_user():
    username = request.values.get('username')
    password = request.values.get('password')
    email = request.values.get('email')
    ret = {}
    if userService.check_user(username,password,email):
        userService.add_user(username,password,email)
        ret['result'] = 1
    else:
        ret['result'] = 2
    return jsonify(ret), 200;


@app.route('/',methods=['GET'])
@login_required()
@privilege('home')
def home():
    #show index
    return render_template('index.html', title=u'首页')


@app.route('/admin-user', methods=['GET'])
@login_required()
@privilege('admin_user')
def admin_user():
    #show admin-user
    return render_template('admin-user.html',title=u'用户管理')


@app.route('/admin-user/user', methods=['PUT','DELETE','POST','GET'])
@login_required()
@privilege('admin_user__user')
def admin_user__user():
    if request.method == 'GET':
        query = request.values.get('query')
        page = request.values.get('p',1)
        if util.can_tune_to(page, int):
            ret = dict()
            ret['result'] = 1
            pager = userService.get_users(query).paginate(int(page), perPage, False)
            #'has_next', 'has_prev', 'items', 'iter_pages', 'next', 'next_num', 'page', 'pages', 'per_page', 'prev', 'prev_num', 'query', 'total'
            user_list = pager.items
            data=dict()
            data['userList'] = [e.serialize() for e in user_list]
            data['prevNum'] = pager.prev_num
            data['nextNum'] = pager.next_num
            data['total'] = pager.total
            data['perPage'] = perPage
            ret['data'] = data
            return jsonify(ret)
    elif request.method == 'PUT':
        username = request.values.get('username')
        password = request.values.get('password')
        email = request.values.get('email')
        role_id = request.values.get('roleId')
        active = request.values.get('active')
        ret = dict()
        if userService.check_user(username, password, email) and util.can_tune_to(active, int):
            userService.add_user(username, password, email, role_id, active)
            ret['result'] = 1
        else:
            ret['result'] = 2
        return jsonify(ret), 200;
    elif request.method == 'DELETE':
        id = request.values.get('id')
        if id and util.can_tune_to(id, int):
            userService.del_user(int(id))
            ret = {}
            ret['result'] = 1
            return jsonify(ret)
    elif request.method == 'POST':
        id = request.values.get('id')
        password = request.values.get('password')
        email = request.values.get('email')
        role_id = request.values.get('roleId')
        active = request.values.get('active')
        if id and util.can_tune_to(id, int) and util.can_tune_to(active, int):
            userService.mod_user(id, password, email, role_id, active)
            ret = {}
            ret['result'] = 1
            return jsonify(ret)
    return "error", 400


@app.route('/admin-role', methods=['GET'])
@login_required()
@privilege('admin_role')
def admin_role():
    return render_template('admin-role.html',title=u'权限管理')


@app.route('/admin-role/role', methods=['PUT', 'DELETE', 'POST', 'GET', 'LINK'])
@login_required()
@privilege('admin_role__role')
def admin_role__role():
    if request.method == 'GET':
        ret = dict()
        ret['result'] = 1
        role_list = roleService.get_role()
        ret['data'] = [e.serialize() for e in role_list]
        return jsonify(ret)
    elif request.method == 'PUT':
        name = request.values.get('name')
        alias = request.values.get('alias')
        if name and alias:
            ret = dict()
            if not roleService.is_exist(name):
                roleService.add_role(name,alias)
                ret['result'] = 1
            else:
                ret['result'] = 2
            return jsonify(ret)
    elif request.method == 'DELETE':
        id = request.values.get('id')
        if id and util.can_tune_to(id, int):
            roleService.del_role(int(id))
            ret = {}
            ret['result'] = 1
            return jsonify(ret)
    elif request.method == 'POST':
        id = request.values.get('id')
        alias = request.values.get('alias')
        if id and util.can_tune_to(id, int) and alias:
            roleService.mod_role(int(id), alias)
            ret = dict()
            ret['result'] = 1
            return jsonify(ret)
    elif request.method == 'LINK':
        user_id = request.values.get('userId')
        role_id = request.values.get('roleId')
        if user_id and util.can_tune_to(user_id, int) and role_id and util.can_tune_to(role_id, int):
            roleService.link_user_role(user_id, role_id)
            ret = dict()
            ret['result'] = 1
            return jsonify(ret)
    return "error", 400


@app.route('/admin-role/privilege', methods=['PUT','DELETE','POST','GET','LINK'])
@login_required()
@privilege('admin_role__privilege')
def admin_role__privilege():
    if request.method == 'GET':
        role_id = request.values.get('roleId')
        if role_id:
            if util.can_tune_to(role_id, int):
                ret = dict()
                ret['result'] = 1
                privilege_list = privilegeService.get_role_privileges(role_id)
                ret['data'] = [e.serialize() for e in privilege_list]
                return jsonify(ret)
        else:
            ret = dict()
            ret['result'] = 1
            privilege_list = privilegeService.get_privileges()
            ret['data'] = [e.serialize() for e in privilege_list]
            return jsonify(ret)
    elif request.method == 'PUT':
        name = unicode(request.values.get('name'))
        alias = unicode(request.values.get('alias'))
        if name and alias:
            ret = dict()
            if not privilegeService.is_exist(name):
                privilegeService.add_privilege(name, alias)
                ret['result'] = 1
            else:
                ret['result'] = 2
            return jsonify(ret)
    elif request.method == 'DELETE':
        id = request.values.get('id')
        if id and util.can_tune_to(id, int):
            privilegeService.del_privilege(int(id))
            ret = dict()
            ret['result'] = 1
            return jsonify(ret)
    elif request.method == 'POST':
        id = request.values.get('id')
        alias = request.values.get('alias')
        if id and alias and util.can_tune_to(int(id), int):
            privilegeService.mod_privilege(id, alias)
            ret = dict()
            ret['result'] = 1
            return jsonify(ret)
    elif request.method == 'LINK':
        role_id = request.values.get('roleId')
        privilege_id = request.values.get('privilegeId')
        read = unicode(request.values.get('read'))
        write = unicode(request.values.get('write'))
        if role_id and privilege_id and read and write and util.can_tune_to(role_id, int) \
                and util.can_tune_to(privilege_id, int):
            privilegeService.link_role_privilege(int(role_id), int(privilege_id), read == '1', write == '1')
            ret = dict()
            ret['result'] = 1
            return jsonify(ret)
    return "error", 400


@app.route('/login-his', methods=['GET'])
@login_required()
@privilege('login_his')
def login_his():
    return render_template('login-his.html',title=u'登录记录')


@app.route('/login-his/his', methods=['GET'])
@login_required()
@privilege('login_his__his')
def login_his__his():
    query = request.values.get('query','')
    login_at = util.check_date_str(request.values.get('loginAt'))
    page = request.values.get('p', 1)
    if util.can_tune_to(page, int):
        pager = loginService.get_login_history(query, login_at).paginate(int(page), perPage, False)
        ret = dict()
        ret['result'] = 1
        his_list = pager.items
        data = dict()
        data['hisList'] = [e.serialize() for e in his_list]
        data['prevNum'] = pager.prev_num
        data['nextNum'] = pager.next_num
        data['total'] = pager.total
        data['perPage'] = perPage
        ret['data'] = data
        return jsonify(ret)
    return "error", 400


@app.route('/task-config', methods=['GET'])
@login_required()
@privilege('task_config')
def task_config():
    return render_template('task-config.html', title=u'任务配置')


@app.route('/task-config/schedule', methods=['GET', 'PUT', 'DELETE', 'POST'])
@login_required()
@privilege('task_config__schedule')
def task_config__schedule():
    if request.method == 'GET':
        sid = request.values.get('id')
        if sid and Util.can_tune_to(sid, int):
            ret = dict()
            ret['result'] = 1
            ret['data'] = schedulerService.get_schedule_detail(int(sid))
            return jsonify(ret)
        else:
            ret = dict()
            ret['result'] = 1
            ss = schedulerService.get_schedule_list()
            ret['data'] = [e.serialize() for e in ss]
            return jsonify(ret)
    elif request.method == 'DELETE':
        sid = request.values.get('id')
        if sid and Util.can_tune_to(sid, int):
            ret = dict()
            ret['result'] = 1
            schedulerService.del_schedule(int(sid))
            return jsonify(ret)
    elif request.method == 'PUT':
        name = request.values.get('name')
        task = request.values.get('task')
        args = request.values.get('args')
        kwargs = request.values.get('kwargs')
        enabled = request.values.get('enabled')
        every = request.values.get('every')
        period = request.values.get('period')
        minute = request.values.get('minute')
        hour = request.values.get('hour')
        day_of_week = request.values.get('day_of_week')
        day_of_month = request.values.get('day_of_month')
        month_of_year = request.values.get('month_of_year')
        if every and Util.can_tune_to(every, int):
            ret = dict()
            ret['result'] = 1
            schedulerService.add_schedule(name, task, args, kwargs, enabled, every=every, period=period)
            return jsonify(ret)
        elif minute or hour or day_of_week or day_of_month or month_of_year:
            ret = dict()
            ret['result'] = 1
            schedulerService.add_schedule(name, task, args, kwargs, enabled, minute=minute, hour=hour,
                                    day_of_week=day_of_week, day_of_month=day_of_month, month_of_year=month_of_year)
            return jsonify(ret)
    elif request.method == 'POST':
        sid = request.values.get('id')
        if sid and Util.can_tune_to(sid, int):
            name = request.values.get('name')
            task = request.values.get('task')
            args = request.values.get('args')
            kwargs = request.values.get('kwargs')
            enabled = request.values.get('enabled')
            every = request.values.get('every')
            period = request.values.get('period')
            minute = request.values.get('minute')
            hour = request.values.get('hour')
            day_of_week = request.values.get('day_of_week')
            day_of_month = request.values.get('day_of_month')
            month_of_year = request.values.get('month_of_year')
            if every and Util.can_tune_to(every, int):
                ret = dict()
                ret['result'] = 1
                schedulerService.mod_schedule(sid, name, task, args, kwargs, enabled, every=every, period=period)
                return jsonify(ret)
            elif minute or hour or day_of_week or day_of_month or month_of_year:
                ret = dict()
                ret['result'] = 1
                schedulerService.mod_schedule(sid, name, task, args, kwargs, enabled, minute=minute, hour=hour,
                                              day_of_week=day_of_week, day_of_month=day_of_month,
                                              month_of_year=month_of_year)
                return jsonify(ret)
    return "error", 400


@app.route('/task-config/task', methods=['GET'])
@login_required()
@privilege('task_config__task')
def task_config__task():
    if request.method=='GET':
        ret = dict()
        ret['result'] = 1
        ts = schedulerService.get_task_list()
        ret['data'] = ts
        return jsonify(ret)
    return "error", 400


@app.route('/task-his', methods=['GET'])
@login_required()
@privilege('task_his')
def task_his():
    return render_template('task-his.html', title=u'执行记录')


@app.route('/task-his/his', methods=['GET'])
@login_required()
@privilege('task_his__his')
def task_his__his():
    sh_id = request.values.get('id')
    if sh_id:
        if util.can_tune_to(sh_id, int):
            td = schedulerService.get_task_history_detail(int(sh_id))
            ret = dict()
            if td:
                ret['result'] = 1
                ret['data'] = td
            else:
                ret['result'] = 2
            print ret
            return jsonify(ret)
    else:
        query = request.values.get('query', '')
        start_at = util.check_date_str(request.values.get('startAt'))
        page = request.values.get('p', 1)
        if util.can_tune_to(page, int):
            pager = schedulerService.get_task_history(query, start_at).paginate(int(page), perPage, False)
            ret = dict()
            ret['result'] = 1
            his_list = pager.items
            data = dict()
            data['hisList'] = [e.serialize() for e in his_list]
            data['prevNum'] = pager.prev_num
            data['nextNum'] = pager.next_num
            data['total'] = pager.total
            data['perPage'] = perPage
            ret['data'] = data
            return jsonify(ret)
    return "error", 400


@app.route('/user-center', methods=['GET', 'POST'])
@login_required()
def user_center():
    if request.method == 'GET':
        u = userService.get_user(session['userId'])
        return render_template('user-center.html', title=u'用户中心', user=u)
    elif request.method == 'POST':
        user_id = session['userId']
        password = request.values.get('password')
        email = request.values.get('email')
        userService.mod_user(user_id, password, email, None, None)
        ret = dict()
        ret['result'] = 1
        return jsonify(ret), 200;
    return "error", 400