from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import ConnectionRequest, STATUS_CHOICES
from .forms import ConnectionRequestForm
from developers.models import Developer


def connection_create(request):
    initial = {}
    developer_id = request.GET.get('developer')
    if developer_id:
        try:
            developer = Developer.objects.get(pk=developer_id)
            initial['receiver'] = developer
        except Developer.DoesNotExist:
            pass

    if request.method == 'POST':
        form = ConnectionRequestForm(request.POST)
        if form.is_valid():
            connection = form.save()
            messages.success(request, f'Solicitação enviada para {connection.receiver.name} com sucesso!')
            return redirect('connection_list')
    else:
        form = ConnectionRequestForm(initial=initial)

    return render(request, 'connections/create.html', {'form': form})


def connection_list(request):
    connections = ConnectionRequest.objects.select_related('receiver', 'skill').all()
    status_filter = request.GET.get('status', '')
    if status_filter:
        connections = connections.filter(status=status_filter)

    context = {
        'connections': connections,
        'status_choices': STATUS_CHOICES,
        'current_status': status_filter,
    }
    return render(request, 'connections/list.html', context)


def connection_status_update(request, pk):
    connection = get_object_or_404(ConnectionRequest, pk=pk)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        valid_statuses = [s[0] for s in STATUS_CHOICES]
        if new_status in valid_statuses:
            old_status = connection.get_status_display()
            connection.status = new_status
            connection.save()
            messages.success(request, f'Status atualizado para "{connection.get_status_display()}".')
        else:
            messages.error(request, 'Status inválido.')
    return redirect('connection_list')
