from django.shortcuts import render
from django.http import HttpResponse
from .models import Post
# Create your views here.
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic.dates import YearArchiveView

def index(request):
	return render(request, 'blog/index.html')
'''
posts=[
{
'author':'Loonycorn',
'title':'BlogPost1',
'content':'Firstpostcontent',
'date_posted':'October25，2019',
},
{
'author':'Test',
'title':'BlogPost2',
'content':'Secondpostcontent',
'date_posted':'October26，2019'
}
]
'''

def business(request):
	context={
	#'posts':posts
	'posts' : Post.objects.all()
	}
	return render(request, 'blog/business.html',context)

'''
def business(request):
	return render(request, 'blog/business.html')
'''

class PostListView(ListView):
	model=Post
	template_name='blog/business.html'
	context_object_name='posts'
	ordering=['-date_posted']

class PostDetailView(DetailView):
	model=Post


class PostCreateView(CreateView):
	model=Post
	fields=['title', 'content']

	def form_valid(self, form):
		form.instance.author=self.request.user
		return super().form_valid(form)


class PostUpdateView(UserPassesTestMixin, UpdateView):
	model=Post
	fields=['title', 'content']

	def form_valid(self, form):
		form.instance.author=self.request.user
		return super().form_valid(form)

	def test_func(self):
		post=self.get_object()
		if self.request.user==post.author:
			return True
		return False


class PostDeleteView(UserPassesTestMixin, DeleteView):
	model=Post
	success_url='/'

	def test_func(self):
		post=self.get_object()
		if self.request.user==post.author:
			return True
		return False

class PostYearArchiveView(YearArchiveView):
	queryset=Post.objects.all()
	date_field="date_posted"
	make_object_list=True
	allow_future=True

def about(request):
	return render(request, 'blog/about.html')