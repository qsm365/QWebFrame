# -*- coding:utf-8 -*-

from flask import Blueprint,render_template,jsonify,request,redirect,url_for,make_response,session
from . import app
from user_service import UserService
from role_service import RoleService
from privilege_service import PrivilegeService
from login_service import LoginService
from util import Util
from decorator.user import login_required,privilege

baseProfile = Blueprint('baseProfile', __name__)
userService = UserService()
roleService = RoleService()
privilegeService = PrivilegeService()
loginService = LoginService()
perPage = 10
util = Util()


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
    return render_template('index.html')


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
            pager = userService.get_user(query).paginate(int(page), perPage, False)
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
        ret = {}
        if userService.check_user(username, password, email):
            userService.add_user(username, password, email, role_id)
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
        if id and util.can_tune_to(id, int):
            userService.mod_user(id, password, email, role_id)
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
    return "error",400