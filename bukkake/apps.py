from django.apps import AppConfig


class BukkakeConfig(AppConfig):
    name = 'bukkake'
    verbose_name = 'Images bookmarks'

    def ready(self):
        # import signals handlers
        from bukkake.signals import users_like_changed
