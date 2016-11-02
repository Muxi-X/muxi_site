# coding:utf-8
# !/usr/bin/python

"""
    manage.py
    ~~~~~~~~

            1>服务器启动运行
            2>python shell(Ipython) 配置
                自动加载环境
                数据库迁移
                数据库更新

            定义的命令：
                python manage.py --help             显示帮助
                python manage.py runserver          启动服务器
                python manage.py db init            创建迁移文件夹
                python manage.py db migrate -m ""   执行数据库迁移
                python manage.py db upgrade         执行数据库更新
                python manage.py insert_roles       创建用户角色
                python manage.py adduser            创建用户
"""

import sys
from muxiwebsite import app, db
from muxiwebsite.models import Book, User, Share, Role, Comment, Blog, Type, Permission
from flask.ext.script import Manager, Shell
from flask.ext.migrate import Migrate, MigrateCommand

"""编码设置"""
reload(sys)
sys.setdefaultencoding('utf-8')

manager = Manager(app)
migrate = Migrate(app, db)

def make_shell_context():
    """自动加载环境"""
    return dict(
        app=app,
        db=db,
        Book=Book,
        User=User,
        Share=Share,
        Role=Role,
        Comment=Comment,
		Blog=Blog,
        Type=Type
    )

"""add manager command"""
manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


@manager.command
def adduser():
    """
    add users
    -------------------------------
    User: write & comment
    Moderator: write & comment & moderate_comments
    Administrator: full permissions
    """
    from getpass import getpass

    email = raw_input('email: ')
    username = raw_input('username: ')
    role_id = input('user:3, admin:2, moderator:1: ')
    password = getpass('password: ')
    confirm = getpass('confirm: ')
    if password == confirm:
        user = User(
            email=email,
            username=username,
            password=password,
            role_id=role_id
        )
        db.session.add(user)
        db.session.commit()
        return "user %s add in database !" % username
    else:
        return "password not confirmed !"
        sys.exit(0)


@manager.command
def insert_roles():
    """
    insert all Roles in command line
    -------------------------------
    User: write & comment
    Moderator: write & comment & moderate_comments
    Administrator: full permissions
    """
    roles = {
        'User': (Permission.COMMENT | Permission.WRITE_ARTICLES, True),
        'Moderator': (Permission.COMMENT |
                      Permission.WRITE_ARTICLES |
                      Permission.MODERATE_COMMENTS, False),
        'Administrator': (0xff, False)
    }
    for r in roles:
        role = Role.query.filter_by(name=r).first()
        if role is None:
            role = Role(name=r)
        role.permissions = roles[r][0]
        role.default = roles[r][1]
        db.session.add(role)
    db.session.commit()


if __name__ == '__main__':
    app.debug = True
    manager.run()
