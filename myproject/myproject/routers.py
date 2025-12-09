# routers.py

class MainRouter:
    """
    Диспетчер данных, перенаправляющий запросы к записям моделей
    из приложений 'admin', 'auth', 'contenttypes' и 'sessions'
    в базу данных utility, а все остальные запросы - в базу default.
    """
    
    route_app_labels = {'admin', 'auth', 'contenttypes', 'sessions'}

    def db_for_read(self, model, **hints):
        """
        Выбор базы данных для чтения записей.
        """
        if model._meta.app_label in self.route_app_labels:
            return 'utility'
        return 'default'

    def db_for_write(self, model, **hints):
        """
        Выбор базы данных для записи записей.
        """
        if model._meta.app_label in self.route_app_labels:
            return 'utility'
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        """
        Разрешить установку связи.
        """
        # Если обе записи принадлежат моделям из приложений, входящих
        # в перечень route_app_label, или, наоборот, обе записи принадлежат
        # моделям из приложений, не входящих в перечень route_app_label,
        # разрешаем установление связи, в противном случае — запрещаем 
        if ((obj1._meta.app_label in self.route_app_labels and obj2._meta.app_label in self.route_app_labels) or (obj1._meta.app_label not in self.route_app_labels and obj2._meta.app_label not in self.route_app_labels)):
            return True
        else:
            return False
    
    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Разрешить миграцию.
        """
        if app_label in self.route_app_labels:
            # Если приложение в списке, разрешить миграцию только в 'utility'
            return db == 'utility'
        # В противном случае, разрешить миграцию только в 'default'
        return db == 'default'