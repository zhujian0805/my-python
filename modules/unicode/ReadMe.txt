[Links]
http://www.joelonsoftware.com/articles/Unicode.html
http://www.rrn.dk/the-difference-between-utf-8-and-unicode

[Notes]
初学Python被编码格式搞的很头大，以下bug是遇到的编码问题之一：

【BUG】UnicodeEncodeError: 'ascii' codec can't encode characters in position 0-15: ordinal
not in range(128)或者UnicodeDecodeError: 'ascii' codec can't decode byte 0x?? in position
1: ordinal not in range(128)

在python在安装时，默认的编码是ascii，当程序中出现非ascii编码时，python的处理常常会报这样的错，python没办法处理非ascii编码的，此时需要自己设置将python的默认编码，一般设置为utf8的编码格式。


查询系统默认编码可以在解释器中输入以下命令：
Python代码  收藏代码
>>>sys.getdefaultencoding()  
设置默认编码时使用：
Python代码  收藏代码
>>>sys.setdefaultencoding('utf8')  
 可能会报AttributeError: 'module' object has no attribute
'setdefaultencoding'的错误，执行reload(sys)，在执行以上命令就可以顺利通过。
此时在执行sys.getdefaultencoding()就会发现编码已经被设置为utf8的了，但是在解释器里修改的编码只能保证当次有效，在重启解释器后，会发现，编码又被重置为默认的ascii了，那么有没有办法一次性修改程序或系统的默认编码呢。

# Check out this example
setdefaultencodeing-01.py
