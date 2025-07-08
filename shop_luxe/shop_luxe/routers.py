# shop_luxe/routers.py (فایل جدید)

class MongoRouter:
    """
    A router to control all database operations on models in the
    'products' application.
    """
    route_app_labels = {'products'} # نام اپلیکیشنی که مدل‌های مونگو در آن است

    def db_for_read(self, model, **hints):
        if model._meta.app_label in self.route_app_labels:
            return 'mongo'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label in self.route_app_labels:
            return 'mongo'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        if (
            obj1._meta.app_label in self.route_app_labels or
            obj2._meta.app_label in self.route_app_labels
        ):
           return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label in self.route_app_labels:
            return db == 'mongo'
        return db == 'default'