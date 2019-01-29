from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'apps.users'
    verbose_name = "用户管理信息"

    def ready(self):
        import users.signals
