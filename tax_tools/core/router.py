class Core_Router:
    """
    A router to control all database operations on models in the
    core application.
    """
    def db_for_read(self, model, **hints):
        """
        Attempts to read core models go to core_db.
        """
        if 'Return' in model.__name__ or 'Filing' in model.__name__:
            return '990s'
        else:
            return 'default'

    def db_for_write(self, model, **hints):
        """
        Attempts to write core models go to core_db.
        """
        if 'Metadata' in model.__name__:
            return 'default'
        else:
            return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the core app is involved.
        """
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the core app only appears in the 'auth_db'
        database.
        """
        if 'Return' in model_name:
            return False
        elif 'Metadata' in model_name:
            return True
