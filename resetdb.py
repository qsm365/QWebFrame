# -*- coding:utf-8 -*-

from app.model import db
from app.role_service import RoleService
from app.privilege_service import PrivilegeService
from app.user_service import UserService
from app.vsphere_sync import VsphereSync

db.drop_all()
db.create_all()

roleService = RoleService()
privilegeService = PrivilegeService()
userService = UserService()

roleService.add_role('admin',u'管理员')
roleService.add_role('user',u'默认用户')

userService.add_user('admin', '3d4f2bf07dc1be38b20cd6e46949a1071f9d0e3d', 'admin@localhost', 1)
userService.add_user('user', '3d4f2bf07dc1be38b20cd6e46949a1071f9d0e3d', 'user@localhost')

roleService.link_user_role(1, 1)
roleService.link_user_role(2, 2)

privilegeService.add_privilege('home', u'首页')
privilegeService.add_privilege('admin_user', u'用户管理')
privilegeService.add_privilege('admin_user__user', u'用户管理用户接口')
privilegeService.add_privilege('admin_role', u'角色管理')
privilegeService.add_privilege('admin_role__role', u'角色管理角色接口')
privilegeService.add_privilege('admin_role__privilege', u'角色管理权限接口')
privilegeService.add_privilege('login_his', u'用户登录记录管理')
privilegeService.add_privilege('login_his__his', u'用户登录记录管理记录接口')
privilegeService.add_privilege('task_config', u'任务配置')
privilegeService.add_privilege('task_config__schedule',u'任务配置计划接口')
privilegeService.add_privilege('task_config__task',u'任务配置任务接口')
privilegeService.add_privilege('task_his', u'执行记录')
privilegeService.add_privilege('task_his__his', u'执行记录记录接口')

privilegeService.link_role_privilege(1, 1, True, True)
privilegeService.link_role_privilege(1, 2, True, True)
privilegeService.link_role_privilege(1, 3, True, True)
privilegeService.link_role_privilege(1, 4, True, True)
privilegeService.link_role_privilege(1, 5, True, True)
privilegeService.link_role_privilege(1, 6, True, True)
privilegeService.link_role_privilege(1, 7, True, True)
privilegeService.link_role_privilege(1, 8, True, True)
privilegeService.link_role_privilege(1, 9, True, True)
privilegeService.link_role_privilege(1, 10, True, True)
privilegeService.link_role_privilege(1, 11, True, True)
privilegeService.link_role_privilege(1, 12, True, True)
privilegeService.link_role_privilege(1, 13, True, True)

privilegeService.link_role_privilege(2, 1, True, False)

vsphereSync = VsphereSync()
vsphereSync.sync()