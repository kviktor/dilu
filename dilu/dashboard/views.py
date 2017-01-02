from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string

from dilu.models import Object, Version
from .forms import SearchForm


def search(query, version):
    version = get_object_or_404(Version, name=version)

    search_params = {'name__icontains': query, 'module__version': version}
    return Object.objects.filter(**search_params).extra(
        select={'length': 'Length(short_import) + Length(name)'}
    ).order_by("length")


def index(request):
    form = SearchForm(request.GET)
    ctx = {'form': form}
    if form.is_valid():
        ctx.update({'objects': search(**form.cleaned_data)})
    return render(request, "index.html", ctx)


def ajax_search(request):
    q = request.GET.get("q")
    version = request.GET.get("v")
    objects = search(q, version)
    return JsonResponse({
        'q': q,
        'num': objects.count(),
        'content': render_to_string("_search.html", {'objects': objects})
    })
