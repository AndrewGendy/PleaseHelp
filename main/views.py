from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = "index.html"


class ErrorView(TemplateView):
    template_name = "error_page.html"
