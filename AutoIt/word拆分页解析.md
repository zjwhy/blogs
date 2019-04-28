# Autoit 实现word拆分页解析 （python同理）

## 背景

之前一直在做相关工作，由于没有找到解决最佳解决方案，老办法思路是 python先将word 转成pdf，按照页码 提取文字，从而实现word的页索引工作。

最近研究了一下vba，终于找到了最佳解决方案！！！

## AutoIt

我用AutoIt测试的，AutoIt调用vba

```
#include <MsgBoxConstants.au3>
#include <Word.au3>

; 创建应用对象
Local $oWord = _Word_Create()
If @error Then Exit MsgBox($MB_SYSTEMMODAL, "Word UDF: _Word_DocOpen 示例", _
        "创建新 Word 应用对象时发生错误." & @CRLF & "@error = " & @error & ", @extended = " & @extended)

; *****************************************************************************
; 只读打开文档
; *****************************************************************************
Local $sDocument = 'D:\Desktop\tzcpa\BJ自动打印\新建文件夹\AutoPrinter\log\backupFile\2019-04-03 08h39m03s140\天职业字[2019]11884号\2.单体审计报告2018-标准无保留意见.docx'
Local $doc = _Word_DocOpen($oWord, $sDocument, Default, Default, True)
If @error Then Exit MsgBox($MB_SYSTEMMODAL, "Word UDF: _Word_DocOpen 示例 1", "打开文档 '.\Extras\Test.doc' 发生错误." & _
        @CRLF & "@error = " & @error & ", @extended = " & @extended)

;关键部分!!!! 
; $doc 是当前活动文档，Pages是页码索引,Item是矩形框索引 改成请自行更改测试，因为一页可能有多个矩形框 
;返回值时 活动文档某一页的 矩形框中的文本

Local $objPage = $doc.ActiveWindow _
 .Panes(1).Pages(2).Rectangles.Item(2).Range.Text
MsgBox(1,1,$objPage)


MsgBox($MB_SYSTEMMODAL, "Word UDF: _Word_DocOpen 示例 1", "文档 '" & $sDocument & "' 已成功打开.")

```



## 思路

整体思路是调用vba，由于目前python没有发现 有库可以对 **页对象**进行操作，所以采用了调用底层vba来操作

在vba中 页对象有一个是 **Rectangles**属性,解释如下

下面的示例返回活动文档中第一页的**矩形**集合。

```vb
Dim objRectangles As Rectangles 
 
Set objRectangles = ActiveDocument.ActiveWindow _ 
 .Panes(1).Pages(1).Rectangles
```

然后顺藤摸瓜找到了Rectangles对象可以操作Range ,这样就可以获得某一页的某一矩形 内的 text，之后对于大多数页对象的操作也就解决了。

python同理，使win32库调用 vba就好了



[附vba官方中文文档]: https://docs.microsoft.com/zh-cn/office/vba/api/
[之前的思路]: https://mp.csdn.net/mdeditor/87099782#	"之前的思路"

