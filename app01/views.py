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
    #查询所有的出版社
    all_publishers = models.Publisher.objects.all()

    #get 返回一个form表单
    return render(request,'book_add.html',{'all_publishers':all_publishers})