# 背景

今天工作时，读取了一个5万行的csv文件，该文件是由pandas读取excel文件后生成的csv数据，但是在print的时候发现数据只能显示1万行左右。

# 原因

我这里是采用的 io读取数据，这是由于pycharm的保护问题，print有行数限制，其实数据已经读到了内存里。

# csv删除多余的 \n 和 “ 符

```python
import re,os

def csvFormatting(path):
    with open(path, 'r', encoding='utf-8') as f:
        data = f.read()
    newdata = re.sub(re.compile(re.compile(r'\n+\||\|\n+ |"\n+|\n+"')), '', data.replace(' ', ''))
    os.remove(path)
    with open(path,'w', encoding='utf-8')  as f:
        f.write(newdata)


```

