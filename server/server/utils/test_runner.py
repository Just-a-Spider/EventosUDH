from django.test.runner import DiscoverRunner

class CustomTestRunner(DiscoverRunner):
    def build_suite(self, *args, **kwargs):
        suite = super().build_suite(*args, **kwargs)
        # Add custom test discovery logic here if needed
        return suite