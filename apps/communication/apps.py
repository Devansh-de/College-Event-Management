from django.apps import AppConfig


class CommunicationConfig(AppConfig):
    name = 'apps.communication'

    def ready(self):
        import apps.communication.signals
