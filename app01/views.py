from django.shortcuts import render,HttpResponse,redirect
from app01 import models
# Create your views here.
def publisher_list(request):
    #逻辑
    #获取所有的出版社的信息
    #返回一个页面，页面呈现所有出版社的信息
    all_publishers = models.Publisher.objects.all().order_by('id')#对象列表  #按照id进行排序
    # for i in all_publishers:
    #     print(i)
    #     print(i.id)
    #     print(i.name)
    return render(request,'publisher_list.html',{'all_publishers':all_publishers})


#新增出版
def publisher_add(request):
    #get请求返回一个form表单，
    #获取用户提交的数据


    if request.method == 'POST':
        pub_name = request.POST.get('pub_name')
        # print(pub_name)
        if not pub_name:
            return render(request,'publisher_add.html',{'error':'出版社名称不能为空'})

        if models.Publisher.objects.filter(name=pub_name):
            #数据库中有重复的名字
            return render(request,'publisher_add.html',{'error':'出版社名称已存在'})
        # 将数据新增到数据库中
        models.Publisher.objects.create(name=pub_name)
    #返回一个重定向到展示出版社的页面

        return redirect('/publisher_list/')
    return render(request,'publisher_add.html')
def publisher_del(request):

    #获取删除的id
    pk = request.GET.get('pk')
    # print(pk)
    #根据pk到数据库进行删除
    # models.Publisher.objects.get(pk=pk).delete()#查询到一个对象 删除
    models.Publisher.objects.filter(pk=pk).delete()#查询到一个对象列表 删除

    return redirect('/publisher_list/')
def publisher_edit(request):

    pk = request.GET.get('pk')
    pub_obj = models.Publisher.objects.get(pk=pk)
    if request.method=='GET':
        #get 返回一个页面 包含input 输入的数据
        return render(request,'publisher_edit.html',{'pub_obj':pub_obj})
    else:
        #post
        #获取用户提交的出版社的名称
        pub_name = request.POST.get('pub_name')
        #修改数据库中对应的数据
        pub_obj.name = pub_name#只是在内存中修改了
        pub_obj.save()#将修改操作提交到数据库
        #返回重定向到展示的出版社页面
        return redirect('/publisher_list/')


def book_list(request):
    all_books = models.Book.objects.all()
    return render(request,'book_list.html',{'all_books':all_books})
def book_add(request):
    error = ''

    if request.method == 'POST':#POST请求
        #获取用户提交的数据
        book_name = request.POST.get('book_name')
        pub_id = request.POST.get('pub')
        if not book_name:
            #用户输入名称为空
            error = '书名不能为空'
        elif models.Book.objects.filter(name = book_name):
            #名字重复
            error = '书名重复'
        else:
            #将数据插入到数据库
            models.Book.objects.create(name=book_name,publisher_id=pub_id)
            return redirect('/book_list/')

    #查询所有的出版社
    all_publishers = models.Publisher.objects.all()

    #get 返回一个form表单
    return render(request,'book_add.html',{'all_publishers':all_publishers,'error':error})
def book_del(request):
    pk = request.GET.get('pk')
    models.Book.objects.filter(pk=pk).delete()
    return redirect('/book_list/')
def book_edit(request):
    #查找id
    pk = request.GET.get('pk')
    #根据id查找要编辑的对象
    book_obj = models.Book.objects.get(pk=pk)
    if request.method == 'POST':
        #post
    #获取用户新提交的数据

        book_name = request.POST.get('book_name')
        pub = request.POST.get('pub')
        #方法一
        # #编辑对应的对象做出修改
        # book_obj.name = book_name
        # book_obj.publisher_id = pub
        # book_obj.save()
        #方法二
        models.Book.objects.filter(pk=pk).update(name=book_name,publisher_id = pub)
        return redirect('/book_list/')





    #get与post都要用
    allpublishers = models.Publisher.objects.all()
    return render(request,'book_edit.html',{'allpublishers':allpublishers,'book_obj':book_obj})

def author_list(request):
    all_authors = models.Author.objects.all()
    # for author in all_authors:
    #     print(author.books.all())#关系管理对象
    return render(request,'author_list.html',{'all_authors':all_authors})
def author_add(request):

    #post
    if request.method == 'POST':
        #获取用户提交的数据
        author_name = request.POST.get('author_name')
        book_ids = request.POST.getlist('book_ids')#获取多个数据
        #向数据库中插入数据
        #向作者报表中插入数据
        author_obj = models.Author.objects.create(name=author_name)
        #该作者和提交的数据绑定多对多的关系
        author_obj.books.set(book_ids) #设置多对多的关系
        #返回重定向到展示作者页面
        return redirect('/author_list/')
    #GEt
    #查询所有书籍
    all_books = models.Book.objects.all()
    #返回一个页面，包含所有信息，让用户输入作者， 选择作品
    return render(request,'author_add.html',{'all_books':all_books})

def author_del(request):
    #获取目标id
    pk = request.GET.get('id')
    #根据id进行删除
    models.Author.objects.filter(pk=pk).delete()
    #返回重定向到展示页面
    return redirect('/author_list/')
def author_edit(request):
    pk = request.GET.get('id')
    #获取作者的对象
    author_obj = models.Author.objects.get(pk=pk)
    #获取选中的书籍
    all_books = models.Book.objects.all()
    if request.method=='POST':
        # post
        # 获取用户提交的数据
        author_name = request.POST.get('author_name')
        book_ids = request.POST.getlist('book_ids')

    #给该对象修改数据
    #修改作者的姓名
        author_obj.name = author_name
        author_obj.save()
        #修改作者和书的多对多关系
        author_obj.books.set(book_ids)
        #返回重定向到展示页面
        return redirect('/author_list/')



    #get
    return render(request,'author_edit.html',{'author_obj':author_obj,'all_books':all_books})