from django.shortcuts import render
from .models import Post, Tag
from .forms import TagForm, PostForm
from django.shortcuts import redirect
from django.views import View
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
# Create your views here.

def allblog(request, slug=None):
	seach_query =  request.GET.get('search', '')

	if seach_query:
		posts = Post.objects.filter(Q(title__icontains=seach_query) | Q(body__icontains=seach_query))

	else:
		posts = Post.objects.all()

	if slug:
		post = Post.objects.get(slug=slug)
		return render(request, 'blog/detail.html', {'post':post})
	

	paginator = Paginator(posts, 6)
	page_number = request.GET.get('page', 1)
	page = paginator.get_page(page_number)

	is_paginated = page.has_other_pages()

	if page.has_previous():
		prev_url = f'?page={page.previous_page_number()}'
	else:
		prev_url = ''
	if page.has_next():
		next_url = f'?page={page.next_page_number()}'
	else:
		next_url = ''
	tags = Tag.objects.all()

	context = {
		'page_object': page,
		'is_paginated': is_paginated,
		'next_url': next_url,
		'prev_url': prev_url,
		'tags': tags
	}

	return render(request, 'base_all.html', context=context)


def tags(request, slug=None):
	#tags = Tag.objects.all()
	if slug:
		tag = Tag.objects.get(slug=slug)
		print('here')
		return render(request, 'blog/tag_detail.html', {'tag': tag})
	tags = Tag.objects.all()
	return render(request, 'blog/tags.html', {'tags': tags})

@login_required
def create_tag(request):
	if request.method == 'POST':
		form = TagForm(request.POST)
		if form.is_valid():
			new_form = form.save()
			return redirect(tags)
	form = TagForm()
	return render(request, 'blog/create_tag.html', {'form': form})

@login_required
def create_post(request):
	if request.method == 'POST':
		form = PostForm(request.POST)
		if form.is_valid():
			new_form = form.save()
			return redirect(new_form)
	form = PostForm()
	return render(request, 'blog/create_post.html', {'form': form})

@login_required
def tag_update(request, slug):
	if request.method == 'POST':
		obj = Tag.objects.get(slug=slug)
		bound_form = TagForm(request.POST, instance=obj)

		if bound_form.is_valid():
			new_form = bound_form.save()
			return redirect(tags)

	obj = Tag.objects.get(slug=slug)
	bound_form = TagForm(instance=obj)
	return render(request, 'blog/tag_update.html', 
			{'bound_form': bound_form, 'obj': obj})

@login_required
def blog_update(request, slug):
	if request.method == 'POST':
		obj = Post.objects.get(slug=slug)
		bound_form = PostForm(request.POST, instance=obj)

		if bound_form.is_valid():
			new_form = bound_form.save()
			return redirect(new_form)

	obj = Post.objects.get(slug=slug)
	bound_form = PostForm(instance=obj)
	return render(request, 'blog/post_update.html', 
			{'bound_form': bound_form, 'obj': obj})

@login_required
def tag_delete(request, slug):
	if request.method == 'POST':
		obj = Tag.objects.get(slug=slug)
		obj.delete()
		return redirect(tags)
	obj = Tag.objects.get(slug=slug)
	return render(request, 'blog/tag_delete.html', {'obj': obj})
	
@login_required
def blog_delete(request, slug):
	if request.method == 'POST':
		obj = Post.objects.get(slug=slug)
		obj.delete()
		return redirect(reverse('blogs'))
	obj = Post.objects.get(slug=slug)
	return render(request, 'blog/post_delete.html', {'obj': obj})


class SignUpView(generic.CreateView):
	form_class = UserCreationForm
	success_url = reverse_lazy('login')
	template_name = 'registration/signup.html'