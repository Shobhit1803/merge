from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Post, User, Comment
from .forms import PostForm
from django.shortcuts import redirect
from django.contrib.auth import login, authenticate, logout
from .forms import SignupForm
from django.contrib.auth.decorators import login_required
from .forms import LoginForm
from django.contrib.auth.hashers import make_password
from .forms import ProfileEditForm
from .forms import CommentForm
from .models import Category, Tag
from .forms import FileUploadForm
from .models import Student



# Create your views here.



def post_list(request):
	posts = Post.objects.all()
	print(Post,"22222222222222222222222")
	return render(request, 'post_list.html', {'posts': posts})

def signup_view(request):
	if request.method == 'POST':
		form = SignupForm(request.POST,request.FILES)
		if form.is_valid():
			if form.cleaned_data.get('password') == form.cleaned_data.get('re_password'):
				user = form.save(commit=False)
				user.password = make_password(form.cleaned_data.get('password'))
				form.save()
				return redirect('login')
	else:
		form = SignupForm()
	return render(request, 'blog/signup.html', {'form': form})

def login_view(request):
	if request.method == 'POST':
		form = LoginForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user:
				login(request, user)
				return redirect('post_list')
			else:
				return redirect('login')
	else:
		form = LoginForm()

	return render(request, 'blog/login.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    return redirect('post_list')


@login_required
def profile_view(request):
    user_profile = User.objects.all().last()
    return render(request, 'blog/profile.html', {'user_profile': user_profile})


@login_required
def profile_edit_view(request):
    profile = User.objects.all().last()

    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileEditForm(instance=profile)

    return render(request, 'blog/profile_edit.html', {'form': form})

def post_detail(request, slug):
	post = get_object_or_404(Post, slug=slug)
	comments = Comment.objects.filter(post=post, parent__isnull=True)
	form = CommentForm
	new_comment = None 
	parent = None

	if request.method == 'POST':
		comment_form = CommentForm(request.POST)
		if comment_form.is_valid():
			
			try:
				parent = request.POST.get('comment_id')
				parent = Comment.objects.filter(id=parent).last()
			except:
				parent=None
			
			new_comment = comment_form.save(commit=False)
			new_comment.post = post
			new_comment.parent = parent
			new_comment.save()
			return redirect('post_detail', slug=post.slug)

		else:
			form = CommentForm()
			
	return render(request, 'blog/post_detail.html', {'post': post, 'comments': comments, 'form': CommentForm, 'new_comment': new_comment, 'parent':parent})

def post_new(request):
	if request.method == "POST":
		form = PostForm(request.POST,request.FILES)
		if form.is_valid():
			post = form.save(commit=False)
			post.author = request.user
			post.published_date = timezone.now()
			post.save()
			form.save_m2m()
			return redirect('post_detail', slug=post.slug)
	else:
		form = PostForm()
	return render(request, 'blog/post_edit.html', {'form': form})

def post_edit(request, slug):
	post = get_object_or_404(Post, slug=slug)
	if request.method == "POST":
		form = PostForm(request.POST, request.FILES,instance=post)
		if form.is_valid():
			post = form.save(commit=False)
			post.author = request.user
			post.published_date = timezone.now()
			post.save()
			form.save_m2m()
			return redirect('post_detail', slug=post.slug)
	else:
		form = PostForm(instance=post)
	return render(request, 'blog/post_edit.html', {'form': form})


def post_category(request, id):
    posts = Post.objects.filter(category__id=id)
    return render(request, 'blog/post_list.html', {'posts': posts})


# def post_category(request, slug):
#     category = Category.objects.filter(slug=slug).last()
#     print(category, "sssssssssssssssssssssss")
#     posts = Post.objects.filter(category=category).all()
#     print(posts,"uuuuuuuuuuuuuuuuuuuuuuuuuuuuuuu")
#     return render(request, 'blog/category.html', {'posts': posts})



def post_Tag(request, id):
    posts = Post.objects.filter(tag__id=id)
    return render(request, 'blog/post_list.html', {'posts': posts})


def post_author(request, id):
    posts = Post.objects.filter(author__id=id)
    return render(request, 'blog/post_list.html', {'posts': posts})


def file_handling(request):
    files = Post.objects.all()

    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user  # Assign the logged-in user as the author
            post.save()
    else:
        form = FileUploadForm()

    return render(request, 'blog/file_handling.html', {'form': form, 'files': files})

def edit_file(request, file_id):
    file = get_object_or_404(Post, pk=file_id)
    
    if request.method == 'POST':
        new_content = request.POST.get('new_content')
        if new_content is not None:
            with open(file.file.path, 'w', encoding='iso-8859-1') as f:
                f.write(new_content)
            return redirect('file_handling')

    with open(file.file.path, 'r', encoding='iso-8859-1') as f:
        current_content = f.read()

    return render(request, 'blog/edit_file.html', {'current_content': current_content, 'file': file})


student_data = [
	{"code":111, "name":"A", "age":25, "city":"jaipur"},
	{"code":112, "name":"AB", "age":26, "city":"jaipur"},
	{"code":113, "name":"AC", "age":27, "city":"jaipur"},
	{"code":114, "name":"AD", "age":28, "city":"jaipur"},
	{"code":115, "name":"AE", "age":29, "city":"jaipur"},
	{"code":111, "name":"AF", "age":24, "city":"jaipur"},
	{"code":112, "name":"AG", "age":23, "city":"jaipur"}
]

def insert_in_db(student_data):
	for student in student_data:
		if_exist = Student.objects.filter(code=student['code'])
		if not if_exist.exists():

			student_obj = Student(
				code = student['code'],
				name = student['name'],
				age  = student['age'],
				city = student['city']
			)
			student_obj.save()
		else:
			student_obj = if_exist.first()
			student_obj.code = student['code']
			student_obj.name = student['name']
			student_obj.age = student['age']
			student_obj.city = student['city']
			student_obj.save()
	# print(student, "xxxxxxxxxxxxxxxxxxxx")



insert_in_db(student_data)