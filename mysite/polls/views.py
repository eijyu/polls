from django.template import Context, loader, RequestContext
from polls.models import Poll
from django.shortcuts import render, render_to_response, get_object_or_404
from django.http import HttpResponse, Http404
from django.core.urlresolvers import reverse
from polls.models import Choice, Poll

# Create your views here.

def index(request):
    latest_poll_list = Poll.objects.all().order_by('-pub_date')[:5]
    return render_to_response('polls/index.html',
            {'latest_poll_list': latest_poll_list})

def detail(request, poll_id):
    p = get_object_or_404(Poll, pk=poll_id)
    return render_to_response('polls/detail.html', {'poll': p},
            context_instance=RequestContext(request))

def results(request, poll_id):
    p = get_object_or_404(Poll, pk=poll_id)
    return render_to_response('polls/result.html', {'poll': p})

def vote(request, poll_id):
    p = get_object_or_404(Poll, pk=poll_id)
    try:
        selected_choice = p.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render_do_response('polls/detail.html', {
            'poll': p,
            'error_message': "選択肢を選んでいません。",
            }, context_instance=RequestContext(request))
    else:
        selected_choice.votes += 1
        selected_choice.save()
        
        return HttpResponseRedirect(reverse('polls.views.results', args=(p.id)))
