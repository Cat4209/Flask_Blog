from flask import Flask, redirect, url_for, request
from config import Configuration
from flask_sqlalchemy import SQLAlchemy

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from flask_admin import Admin
from flask_admin import AdminIndexView
from flask_admin.contrib.sqla import ModelView

from flask_security import SQLAlchemyUserDatastore, Security, current_user

app = Flask(__name__)
app.config.from_object(Configuration)


db = SQLAlchemy(app)

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


##ADMIN
from models import * 
class MixinAdmin:
    def is_accessible(self):
        return current_user.has_role('admin')
    
    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('security.login', next=request.url ))
    
class BaseModelView(ModelView):
    def on_model_change(self, form, model, is_created):
        model.generate_slug()
        return super(BaseModelView, self).on_model_change(form, model, is_created)

class PostAdminView(MixinAdmin, BaseModelView):
    form_columns = ['title', 'body', 'tags']

class TagAdminView(MixinAdmin, BaseModelView):
    form_columns = ['name', 'posts']

class AdminView(MixinAdmin, ModelView):
    pass

class HomeAdminView(MixinAdmin, AdminIndexView):
    pass

    
admin = Admin(app, 'FlaskApp', url='/', index_view=HomeAdminView(name='Home'))
admin.add_view(PostAdminView(Post, db.session))
admin.add_view(TagAdminView(Tag, db.session))
admin.add_view(AdminView(User, db.session))
admin.add_view(AdminView(Role, db.session))

##FLASK SECURITY 
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)