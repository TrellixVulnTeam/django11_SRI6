from urllib.parse import quote
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404
from .models import Post 
from .forms import PostForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q
# Create your views here.

def post_create(request):
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404

	# if not request.user.is_authenticated():
	# 	raise Http404


	form = PostForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		instance = form.save(commit= False)
		instance.user = request.user
		instance.save()
		messages.success(request, "Successfully created!")
		return HttpResponseRedirect(instance.get_absolute_url())
	#else:
		#messages.error(request, "Not created!")
	context = {
	  "title" : "Create new post",
	  "form"  : form,
	}
	return render(request, 'post_form.html', context)


def post_update(request, slug=None):	
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404

	instance = get_object_or_404(Post, slug=slug)

	form = PostForm(request.POST or None,request.FILES or None, instance=instance)
	if form.is_valid():
		obj = form.save(commit= False)
		obj.save()

		messages.success(request, obj.title + " has been saved successfully!")
		return HttpResponseRedirect(instance.get_absolute_url())

	context = {
		'title' :"Update " + instance.title,
		'instance'	: instance,
		'form'	: form,
	}
	return render(request, 'post_form.html', context)


def post_detail(request, slug=None):
	obj = get_object_or_404(Post, slug=slug)
	
	if obj.draft or obj.publish > timezone.now().date():
		if not request.user.is_staff or not request.user.is_superuser:
			raise Http404
	share_string = quote(obj.content)
	context = {
		'title' 		: obj.title,
		'post'			: obj,
		'share_string'	: share_string
	}
	return render(request, 'detail.html', context)


def post_list(request):
	queryset_list = Post.objects.active() #.order_by("-timestamp")
	today = timezone.now().date()

	if request.user.is_superuser or request.user.is_staff:
		queryset_list = Post.objects.all()
	query = request.GET.get("q")
	if query:
		queryset_list = queryset_list.filter(
			Q(title__icontains=query) |
			Q(content__icontains=query) |
			Q(user__first_name__icontains=query) |
			Q(user__last_name__icontains=query)

			)

	page_request_var  = "page"

	paginator = Paginator(queryset_list, 2) # Show 25 contacts per page

	page = request.GET.get(page_request_var)
	try:
		queryset = paginator.page(page)
	except PageNotAnInteger:
	# If page is not an integer, deliver first page.
		queryset = paginator.page(1)
	except EmptyPage:
	# If page is out of range (e.g. 9999), deliver last page of results.
		queryset = paginator.page(paginator.num_pages)

	context = {
	"post_list"	: queryset,
	"title"   	: 'Post list',
	"page_request_var" : page_request_var,
	"today"		: today,
	}

	return render(request, 'post_list.html', context)


def post_delete(request, slug=None):

	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404

	instance = get_object_or_404(Post, slug=id)
	instance.delete()
	messages.success(request, "Successfully deleted!")
	return redirect("posts:list")

