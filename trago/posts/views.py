from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Post 
from .forms import PostForm
# Create your views here.

def post_create(request):
	form = PostForm(request.POST or None)
	# if request.method == 'POST':
	# 	print( request.POST.get("content") )
	# 	print( request.POST.get("title") )
	if form.is_valid():
		obj = form.save(commit= False)
		print( form.cleaned_data.get("title") )
		obj.save()

	context = {
	  "form" : form,
	}
	return render(request, 'post_form.html', context)


def post_detail(request, id):

	post = get_object_or_404(Post, id=id)
	context = {
		'title' : post.title,
		'post': post,
	}
	return render(request, 'detail.html', context)
def post_list(request):
	# if request.user.is_authenticated():
	# 	context = {
	# 		"title" : "My User"
	# 	}
	# else:
	# 	context = {
	# 		"title" : "List"
	# 	}

	post_list = Post.objects.all()
	context = {
		"post_list": post_list,
		"title"   : 'Post list'
	}

	return render(request, 'index.html', context)


def post_update(request):
	return HttpResponse("<h1>update</h1>")



def post_delete(request):
	return HttpResponse("<h1>delete</h1>")

