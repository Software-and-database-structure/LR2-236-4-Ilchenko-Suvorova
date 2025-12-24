
class MainRouter:
    route_app_labels = {'admin', 'auth', 'contenttypes', 'sessions'}

    def db_for_read(self, model, **hints):
        if model._meta.app_label in self.route_app_labels:
            return 'utility'
        return 'default'

    def db_for_write(self, model, **hints):
        if model._meta.app_label in self.route_app_labels:
            return 'utility'
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        if ((obj1._meta.app_label in self.route_app_labels and obj2._meta.app_label in self.route_app_labels) or (obj1._meta.app_label not in self.route_app_labels and obj2._meta.app_label not in self.route_app_labels)):
            return True
        else:
            return False
    
    def allow_migrate(self, db, app_label, model_name=None, **hints):

        if app_label in self.route_app_labels:
            # Если приложение в списке, разрешить миграцию только в 'utility'
            return db == 'utility'
        # В противном случае, разрешить миграцию только в 'default'
        return db == 'default'