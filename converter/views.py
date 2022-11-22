from django.views.generic import FormView
from django.shortcuts import render
from .forms import ConverterForm
from . import romanizer


def converter(request):
    if request.method == 'POST':
        form = ConverterForm(request.POST)
        if form.is_valid():
            to_conv = form.cleaned_data['to_convert']
            form = ConverterForm({'to_convert': romanizer.Romanizer(to_conv).romanize()})

    else:
        form = ConverterForm()
    return render(request, 'converter.html', {'form': form})
