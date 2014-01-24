# Create your views here.
from django.shortcuts import render, get_object_or_404
from apps.main.models import List, Item, Topsite
from apps.main.models import ListForm, ItemForm, TopsiteForm
import datetime
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse

@login_required() 
def index(request):
	lists = List.objects.filter(user=request.user)
	items = Item.objects.filter(listfk__user = request.user)
	topsites = Topsite.objects.filter(user=request.user)

	form = ItemForm()

	if request.method=='POST':
		if 'additem' in request.POST:
			form = ItemForm(request.POST)
			if form.is_valid():
				instance = form.save(commit=False)
				instance.user = request.user
				instance.save()
				return HttpResponseRedirect(reverse('apps.main.views.index', args=()))

		elif 'delete' in request.POST:
			itemid = request.POST['id']
			Item.objects.get(id=itemid).delete()

		elif 'check' in request.POST:
			itemid = request.POST['id']
			item = Item.objects.get(id=itemid)
			item.complete = True
			item.completed_time = datetime.datetime.now()
			item.save()

		elif 'deletelist' in request.POST:
			listid = request.POST['id']
			List.objects.get(id=listid).delete()

	context= {'lists':lists, 'items':items, 'form':form, 'topsites':topsites}
	return render(request, 'main/index.html', context)

