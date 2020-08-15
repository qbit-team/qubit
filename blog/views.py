from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.views import auth_login
from django.contrib.auth.decorators import login_required
from django.http import *
import html
from .models import Blog

#@login_required(redirect_field_name='my_redirect_field')

def make_comments_tree_template (request,blog):
    if len(blog.blog_set.all()) == 0:
        if blog.is_visible:
            """
            <button type="button" class="btn btn-primary" data-toggle="modal" data-target="#ReplyModal">Reply</button>
            <button type="button" class="btn btn-primary" data-toggle="modal" data-target="#ReplyModal">Edit</button>
            """
            return """

            <div class="text-right card my-4 border-dark">
                <section id="{2}">
                <h5 class="text-right border-dark card-header">
                    {0}
                </h5>
                </section>
                <div class="card-body">
                    <iframe id="comment-{2}" class="text-right" style="width:100%;display:block;" srcdoc="&lt;div dir=&quot;rtl&quot;&gt;{1}&lt;/div&gt;" frameborder="0" sandbox></iframe>
                    <!--<script>document.getElementById("comment-{2}").style.height = document.getElementById("comment-{2}").contentWindow.document.body.offsetHeight + 'px';</script>-->
                </div>
            </div>

            """.format(blog.author.first_name,html.escape(blog.text,quote=True),blog.id)
        else:
            return """

            <div class="text-right card my-4 border-dark">
                <section id="{1}">
                <h5 class="text-right border-dark card-header">
                    {0}
                </h5>
                </section>
                <div class="card-body">
                    This comment could not be shown.
                </div>
            </div>

            """.format(blog.author.first_name,blog.id)
    else:
        if blog.is_visible :
            if blog.parent != None:
                result = """

                <div class="text-right card my-4 border-dark">
                    <section id="{2}"
                    <h5 class="text-right border-dark card-header">
                        {0}
                    </h5>
                    </section>
                    <div class="card-body">
                        <iframe class="text-right" style="width:100%;display:block;" srcdoc="&lt;div dir=&quot;rtl&quot;&gt;{1}&lt;/div&gt;" frameborder="0" sandbox></iframe>
                """.format(blog.author.first_name,html.escape(blog.text,quote=True),blog.id)
            else:
                result = ""
            for child in blog.blog_set.all():
                result = result+ make_comments_tree_template (request, child)
            if blog.parent != None:
                result = result + """</div></div>"""
            else:
                pass
            return result
        else:
            if blog.parent != None:
                result = """

                <div class="text-right card my-4 border-dark">
                    <section id="{1}">
                    <h5 class="text-right border-dark card-header">
                        {0}
                    </h5>
                    </section>
                    <div class="card-body">
                       This comment could not be shown.
                """.format(blog.author.first_name,blog.id)
            else:
                result = ""
            for child in blog.blog_set.all():
                result = result+ make_comments_tree_template (request, child)
            if blog.parent != None:
                result = result + """</div></div>"""
            else:
                pass
            return result

def redirect_to_page (request):
    return HttpResponseRedirect("/blog/page/1/")

def index(request, post_id):
    blog = get_object_or_404(Blog, id=int(post_id))
    #return HttpResponse(len(blog.blog_set.all()))
    if not blog.is_comment :
        if blog.is_visible:
            if len(blog.blog_set.all()) != 0:
                return render(request, 'blog/post.html',
                {'blog':blog,
                'pinned_blogs':Blog.objects.filter(is_visible=True, is_comment=False, pin__gt=0).order_by('-pin'),
                'comments':make_comments_tree_template(request, blog),
                })
            else:
                return render(request, 'blog/post.html',
                {'blog':blog,
                'pinned_blogs':Blog.objects.filter(is_visible=True, is_comment=False, pin__gt=0).order_by('-pin'),
                'comments':"NONE",
                })
        else:
            return HttpResponse("This blog is not visible.")
    else:
        return HttpResponse("You can not see comments.")

def page(request, page_number):
    found_blogs = Blog.objects.filter(is_visible=True, is_comment=False).order_by('-id')[5*(int(page_number)-1):5*int(page_number)]
    return render(request, 'blog/index.html',
    {'blogs':found_blogs,
    'previous_page':str(int(page_number)+1),
    'next_page':str(int(page_number)-1),
    'current_page':str(int(page_number)),
    'last_page':str(int(len(Blog.objects.filter(is_visible=True, is_comment=False))/5)+1),
    'pinned_blogs':Blog.objects.filter(is_visible=True, is_comment=False, pin__gt=0).order_by('-pin'),
    })

@login_required
def add_comment (request, post_id, comment_id):
    if request.method == "POST":
        if comment_id == post_id:
            new_comment_text = request.POST.get("new_comment_text")
            if new_comment_text == "":
                blog = Blog.objects.get(id=int(post_id))
                return render(request, 'blog/post.html',
                {'blog':blog,
                'pinned_blogs':Blog.objects.filter(is_visible=True, is_comment=False, pin__gt=0).order_by('-pin'),
                'comments':make_comments_tree_template(request, blog),
                'errors':"FILL",
                })
            new_blog = Blog(author = User.objects.get(username = request.user.username),
            parent = Blog.objects.get(id=post_id),
            text = new_comment_text,
            is_comment = True,
            is_visible = True,
            pin = 0
            )
            new_blog.save()
            return HttpResponseRedirect("/blog/"+str(post_id))
        else:
            raise Http404()
    else:
        raise Http404()
