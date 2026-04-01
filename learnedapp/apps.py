from django.apps import AppConfig


class LearnedappConfig(AppConfig):
    name = 'learnedapp'


    def ready(self):
        import learnedapp.signals