# debug 原理详解

[TOC]

# 概述

debug是排除计算机故障的意思，在开发程序的过程中，可以帮助开发者进行程序调试，同时，debug也是优秀开发者必备的技能。在实际的程序开发过程中，debug在解决程序故障（bug）方面有着重大的帮助作用。

常用的debug插件有，pycharm集成的pydev，vscode中python debugger插件，python解释器标准库中的pdb，两个插件都支持本地调试与远程调试。实现的功能基本都一样，包括:步进、步入、步出、步进一行，运行至鼠标焦点等功能，大同小异。

# debug插件原理

python实现debug的核心方法依赖于 `sys.settrace（tracefunc ）`

> [说明文档]: https://docs.python.org/3/library/sys.html#sys.settrace	"sys.settrace"
> [说明文档]: https://docs.python.org/3/library/sys.html#sys.gettrace	"sys.gettrace（）"

## sys.settrace(tracefunc )

### 英文说明

> 

### 中文说明

> 设置系统的跟踪功能，该功能允许您在Python中实现Python源代码调试器。该函数是特定于线程的；为了使调试器支持多个线程，它必须[`settrace()`](https://docs.python.org/3/library/sys.html#sys.settrace)为正在调试的每个线程或使用注册一个跟踪功能 [`threading.settrace()`](https://docs.python.org/3/library/threading.html#threading.settrace)。
>
> 跟踪函数应具有三个参数：*frame*，*event*和 *arg*。*frame*是当前的堆栈帧。 *事件*是一个字符串：`'call'`， `'line'`，`'return'`，`'exception'`或`'opcode'`。 *arg*取决于事件类型。
>
> 每当输入新的本地范围时，都会调用trace函数（*事件*设置为`'call'`）。它应返回对要用于新范围的本地跟踪函数的引用，或者`None`如果不应该跟踪该范围，则应返回该引用。
>
> 本地跟踪函数应返回对自身的引用（或对另一个函数的引用，以在该范围内进行进一步的跟踪），或`None`关闭该范围内的跟踪。
>
> 如果跟踪函数中发生任何错误，则将其取消设置，就像`settrace(None)`被调用一样。
>
> 这些事件具有以下含义：
>
> - `'call'`
>
>     调用一个函数（或输入其他代码块）。全局跟踪函数被称为；*arg*是`None`; 返回值指定本地跟踪函数。
>
> - `'line'`
>
>     解释器将要执行新的代码行或重新执行循环条件。局部跟踪函数被调用；*arg*是 `None`; 返回值指定新的本地跟踪函数。有关`Objects/lnotab_notes.txt`的详细说明，请参见 。每行的事件可以用于一帧通过设置被禁用 `f_trace_lines`到[`False`](https://docs.python.org/3/library/constants.html#False)该帧上。
>
> - `'return'`
>
>     一个函数（或其他代码块）即将返回。局部跟踪函数被调用；*arg*是将返回的值，或者`None` 事件是由引发异常引起的。跟踪函数的返回值将被忽略。
>
> - `'exception'`
>
>     发生异常。局部跟踪函数被调用；*arg*是一个元组; 返回值指定新的本地跟踪函数。`(exception, value, traceback)`
>
> - `'opcode'`
>
>     解释程序将要执行新的操作码（请参阅[`dis`](https://docs.python.org/3/library/dis.html#module-dis)参考资料以获取操作码详细信息）。局部跟踪函数被调用；*arg*是 `None`; 返回值指定新的本地跟踪函数。每个操作码事件默认情况下都不发出：必须通过在框架上设置`f_trace_opcodes`为显式请求它们[`True`](https://docs.python.org/3/library/constants.html#True)。
>
> 请注意，由于异常是在调用者链中传播的，因此`'exception'`在每个级别都会生成一个 事件。
>
> 对于更细粒度的用法，可以通过显式分配来设置跟踪函数，而不是依赖于通过已安装的跟踪函数的返回值间接设置跟踪函数。这对于激活当前帧上的跟踪功能也是必需的，但不这样做。请注意，为了使此功能正常运行，必须安装了全局跟踪功能才能启用运行时跟踪机制，但是它不必是相同的跟踪功能（例如，它可以是与只需返回以立即在每个帧上禁用自己）。`frame.f_trace = tracefunc`[`settrace()`](https://docs.python.org/3/library/sys.html#sys.settrace)[`settrace()`](https://docs.python.org/3/library/sys.html#sys.settrace)`None`
>
> 有关代码和框架对象的更多信息，请参阅[标准类型层次结构](https://docs.python.org/3/reference/datamodel.html#types)。
>
> 引发不带参数的[审核事件](https://docs.python.org/3/library/sys.html#auditing) `sys.settrace`。

### 解释

sys.settrace是开启系统跟踪功能，可在自己的代码中加入该方法开启跟踪功能，也就说所说的调试，该方法的入参为一个函数，可以理解为一个函数指针，如果参数为None会关闭调试功能，传入的这个函数有三个实参，分别为frame,event,arg。

在传入的该函数中我们可以拿到这三个实参进行处理。

frame为当前的堆栈帧信息，可以根据frame对象获取当前堆栈帧出的代码行，变量，文件名等等信息，该处可以使用inspace标准库操作起来比较方便。

event的值为当前堆栈帧处的时间，是一个字符串，可以理解为'call'`， `'line'`，`'return'`，`'exception'`或`'opcode'其中之一。

"call" ：调用一个函数（或输入其他代码块）。全局跟踪函数被称为；*arg*是`None`; 返回值指定本地跟踪函数。

"line"：解释器将要执行新的代码行或重新执行循环条件。局部跟踪函数被调用；*arg*是 `None`; 返回值指定新的本地跟踪函数。有关`Objects/lnotab_notes.txt`的详细说明，请参见 。每行的事件可以用于一帧通过设置被禁用 `f_trace_lines`到[`False`](https://docs.python.org/3/library/constants.html#False)该帧上。

"return":一个函数（或其他代码块）即将返回。局部跟踪函数被调用；*arg*是将返回的值，或者`None` 事件是由引发异常引起的。跟踪函数的返回值将被忽略。

"exception":发生异常。局部跟踪函数被调用；*arg*是一个元组; 返回值指定新的本地跟踪函数。`(exception, value, traceback)`

"opcode":解释程序将要执行新的操作码（请参阅[`dis`](https://docs.python.org/3/library/dis.html#module-dis)参考资料以获取操作码详细信息）。局部跟踪函数被调用；*arg*是 `None`; 返回值指定新的本地跟踪函数。每个操作码事件默认情况下都不发出：必须通过在框架上设置`f_trace_opcodes`为显式请求它们[`True`](https://docs.python.org/3/library/constants.html#True)。

## bdb源码解读

大多数插件都是在Bdb标准库的基础上进行开发的，该库实现了断点管理与堆栈帧信息处理功能。

https://www.osgeo.cn/cpython/library/bdb.html#bdb.Bdb.stop_here

> # [`bdb`](https://www.osgeo.cn/cpython/library/bdb.html#module-bdb) ---调试器框架
>
> **源代码：** [Lib/bdb.py](https://github.com/python/cpython/tree/master/Lib/bdb.py)
>
> ------
>
> 这个 [`bdb`](https://www.osgeo.cn/cpython/library/bdb.html#module-bdb) 模块处理基本的调试器功能，如设置断点或通过调试器管理执行。
>
> 定义了以下异常：
>
> - *exception* `bdb.``BdbQuit`
>
>     由引发的异常 [`Bdb`](https://www.osgeo.cn/cpython/library/bdb.html#bdb.Bdb) 用于退出调试器的类。
>
> 这个 [`bdb`](https://www.osgeo.cn/cpython/library/bdb.html#module-bdb) 模块还定义了两个类：
>
> - *class* `bdb.``Breakpoint`(*self*, *file*, *line*, *temporary=0*, *cond=None*, *funcname=None*)
>
>     此类实现临时断点、忽略计数、禁用和（重新）启用以及条件。断点通过一个名为 `bpbynumber` 并且通过 `(file, line)` 成对通过 `bplist` . 前者指向类的单个实例 [`Breakpoint`](https://www.osgeo.cn/cpython/library/bdb.html#bdb.Breakpoint) . 后者指向此类实例的列表，因为每行可能有多个断点。创建断点时，其关联的文件名应为规范格式。如果A *函数名* 如果定义了，则在执行该函数的第一行时将计算断点命中。条件断点总是计算命中次数。[`Breakpoint`](https://www.osgeo.cn/cpython/library/bdb.html#bdb.Breakpoint) 实例具有以下方法：`deleteMe`()从与文件/行关联的列表中删除断点。如果它是该位置上的最后一个断点，它还将删除文件/行的条目。`enable`()将断点标记为已启用。`disable`()将断点标记为禁用。`bpformat`()返回一个字符串，其中包含有关断点的所有信息，格式良好：断点编号。是否是临时的。它的文件，行位置。导致中断的情况。如果必须在接下来的n次中忽略它。断点命中计数。*3.2 新版功能.*`bpprint`(*out=None*)打印的输出 [`bpformat()`](https://www.osgeo.cn/cpython/library/bdb.html#bdb.Breakpoint.bpformat) 文件 *out* ，或者如果是 `None` ，到标准输出。
>
> - *class* `bdb.``Bdb`(*skip=None*)
>
>     这个 [`Bdb`](https://www.osgeo.cn/cpython/library/bdb.html#bdb.Bdb) 类充当通用的Python调试器基类。这个类负责跟踪工具的细节；派生类应该实现用户交互。标准调试器类 ([`pdb.Pdb`](https://www.osgeo.cn/cpython/library/pdb.html#pdb.Pdb) ）就是一个例子。这个 *skip* 参数（如果给定）必须是全局样式模块名称模式的iterable。调试器不会单步进入源自与这些模式之一匹配的模块的帧中。帧是否被视为源自某个模块，由 `__name__` 在帧全局中。*3.1 新版功能:* 这个 *skip* 参数。以下方法 [`Bdb`](https://www.osgeo.cn/cpython/library/bdb.html#bdb.Bdb) 通常不需要重写。`canonic`(*filename*)以规范形式获取文件名的辅助方法，即，作为大小写规范化（在不区分大小写的文件系统上）的绝对路径，去掉周围的尖括号。`reset`()设置 `botframe` ， `stopframe` ， `returnframe` 和 `quitting` 具有值的属性已准备好开始调试。`trace_dispatch`(*frame*, *event*, *arg*)此函数作为调试帧的跟踪函数安装。它的返回值是新的跟踪函数（在大多数情况下，就是它本身）。默认实现根据即将执行的事件类型（作为字符串传递）决定如何分派帧。 *事件* 可以是以下之一：`"line"` ：将执行新的代码行。`"call"` ：一个函数即将被调用，或输入另一个代码块。`"return"` ：函数或其他代码块即将返回。`"exception"` ：发生异常。`"c_call"` ：即将调用C函数。`"c_return"` ：C函数已返回。`"c_exception"` ：C函数引发了异常。对于python事件，调用专门的函数（见下文）。对于C事件，不采取任何措施。这个 *arg* 参数取决于上一个事件。参见文档 [`sys.settrace()`](https://www.osgeo.cn/cpython/library/sys.html#sys.settrace) 有关跟踪函数的详细信息。有关代码和框架对象的详细信息，请参阅 [标准类型层次结构](https://www.osgeo.cn/cpython/reference/datamodel.html#types) .`dispatch_line`(*frame*)如果调试器应在当前行上停止，则调用 [`user_line()`](https://www.osgeo.cn/cpython/library/bdb.html#bdb.Bdb.user_line) 方法（应在子类中重写）。举起一个 [`BdbQuit`](https://www.osgeo.cn/cpython/library/bdb.html#bdb.BdbQuit) 例外情况，如果 `Bdb.quitting` 设置标志（可从 [`user_line()`](https://www.osgeo.cn/cpython/library/bdb.html#bdb.Bdb.user_line) ）返回对 [`trace_dispatch()`](https://www.osgeo.cn/cpython/library/bdb.html#bdb.Bdb.trace_dispatch) 在该范围内进一步跟踪的方法。`dispatch_call`(*frame*, *arg*)如果调试器应在此函数调用上停止，请调用 [`user_call()`](https://www.osgeo.cn/cpython/library/bdb.html#bdb.Bdb.user_call) 方法（应在子类中重写）。举起一个 [`BdbQuit`](https://www.osgeo.cn/cpython/library/bdb.html#bdb.BdbQuit) 例外情况，如果 `Bdb.quitting` 设置标志（可从 [`user_call()`](https://www.osgeo.cn/cpython/library/bdb.html#bdb.Bdb.user_call) ）返回对 [`trace_dispatch()`](https://www.osgeo.cn/cpython/library/bdb.html#bdb.Bdb.trace_dispatch) 在该范围内进一步跟踪的方法。`dispatch_return`(*frame*, *arg*)如果调试器应在此函数返回时停止，则调用 [`user_return()`](https://www.osgeo.cn/cpython/library/bdb.html#bdb.Bdb.user_return) 方法（应在子类中重写）。举起一个 [`BdbQuit`](https://www.osgeo.cn/cpython/library/bdb.html#bdb.BdbQuit) 例外情况，如果 `Bdb.quitting` 设置标志（可从 [`user_return()`](https://www.osgeo.cn/cpython/library/bdb.html#bdb.Bdb.user_return) ）返回对 [`trace_dispatch()`](https://www.osgeo.cn/cpython/library/bdb.html#bdb.Bdb.trace_dispatch) 在该范围内进一步跟踪的方法。`dispatch_exception`(*frame*, *arg*)如果调试器应在此异常处停止，则调用 [`user_exception()`](https://www.osgeo.cn/cpython/library/bdb.html#bdb.Bdb.user_exception) 方法（应在子类中重写）。举起一个 [`BdbQuit`](https://www.osgeo.cn/cpython/library/bdb.html#bdb.BdbQuit) 例外情况，如果 `Bdb.quitting` 设置标志（可从 [`user_exception()`](https://www.osgeo.cn/cpython/library/bdb.html#bdb.Bdb.user_exception) ）返回对 [`trace_dispatch()`](https://www.osgeo.cn/cpython/library/bdb.html#bdb.Bdb.trace_dispatch) 在该范围内进一步跟踪的方法。通常，派生类不会重写以下方法，但如果它们想要重新定义停止和断点的定义，则可能会重写这些方法。`stop_here`(*frame*)此方法检查 *框架* 在下面的某个地方 `botframe` 在调用堆栈中。 `botframe` 是调试开始的帧。`break_here`(*frame*)此方法检查文件名和属于的行中是否存在断点 *框架* 或者，至少在当前函数中。如果断点是临时断点，则此方法将删除它。`break_anywhere`(*frame*)此方法检查当前帧的文件名中是否存在断点。派生类应该重写这些方法以获得对调试器操作的控制。`user_call`(*frame*, *argument_list*)此方法是从 [`dispatch_call()`](https://www.osgeo.cn/cpython/library/bdb.html#bdb.Bdb.dispatch_call) 当被调用函数内的任何地方可能需要中断时。`user_line`(*frame*)此方法是从 [`dispatch_line()`](https://www.osgeo.cn/cpython/library/bdb.html#bdb.Bdb.dispatch_line) 当任一 [`stop_here()`](https://www.osgeo.cn/cpython/library/bdb.html#bdb.Bdb.stop_here) 或 [`break_here()`](https://www.osgeo.cn/cpython/library/bdb.html#bdb.Bdb.break_here) 产量 `True` .`user_return`(*frame*, *return_value*)此方法是从 [`dispatch_return()`](https://www.osgeo.cn/cpython/library/bdb.html#bdb.Bdb.dispatch_return) 什么时候？ [`stop_here()`](https://www.osgeo.cn/cpython/library/bdb.html#bdb.Bdb.stop_here) 产量 `True` .`user_exception`(*frame*, *exc_info*)此方法是从 [`dispatch_exception()`](https://www.osgeo.cn/cpython/library/bdb.html#bdb.Bdb.dispatch_exception) 什么时候？ [`stop_here()`](https://www.osgeo.cn/cpython/library/bdb.html#bdb.Bdb.stop_here) 产量 `True` .`do_clear`(*arg*)处理当断点是临时断点时必须如何删除它。此方法必须由派生类实现。派生类和客户端可以调用以下方法来影响单步执行状态。`set_step`()在一行代码后停止。`set_next`(*frame*)停在给定帧内或其下方的下一行。`set_return`(*frame*)从给定帧返回时停止。`set_until`(*frame*)当到达不大于当前行的行或从当前帧返回时停止。`set_trace`([*frame*])从开始调试 *框架* . 如果 *框架* 未指定，调试从调用方的帧开始。`set_continue`()仅在断点处或完成时停止。如果没有断点，请将系统跟踪函数设置为 `None` .`set_quit`()设置 `quitting` 属性到 `True` . 这提出 [`BdbQuit`](https://www.osgeo.cn/cpython/library/bdb.html#bdb.BdbQuit) 在下一个调用中 `dispatch_*()` 方法。派生类和客户端可以调用以下方法来操作断点。如果发生错误，这些方法返回包含错误消息的字符串，或者 `None` 如果一切都好的话。`set_break`(*filename*, *lineno*, *temporary=0*, *cond*, *funcname*)设置新断点。如果 *林诺* 行不存在 *filename* 作为参数传递，返回错误消息。这个 *filename* 应采用规范形式，如 [`canonic()`](https://www.osgeo.cn/cpython/library/bdb.html#bdb.Bdb.canonic) 方法。`clear_break`(*filename*, *lineno*)删除中的断点 *filename* 和 *林诺* . 如果未设置，则返回错误消息。`clear_bpbynumber`(*arg*)删除具有索引的断点 *arg* 在 `Breakpoint.bpbynumber` . 如果 *arg* 不是数字或超出范围，返回错误消息。`clear_all_file_breaks`(*filename*)删除中的所有断点 *filename* . 如果未设置，则返回错误消息。`clear_all_breaks`()删除所有现有断点。`get_bpbynumber`(*arg*)返回由给定数字指定的断点。如果 *arg* 是字符串，它将转换为数字。如果 *arg* 是非数字字符串，如果给定断点从未存在或已被删除，则为 [`ValueError`](https://www.osgeo.cn/cpython/library/exceptions.html#ValueError) 提高了。*3.2 新版功能.*`get_break`(*filename*, *lineno*)检查是否存在断点 *林诺* 属于 *filename* .`get_breaks`(*filename*, *lineno*)返回的所有断点 *林诺* 在里面 *filename* 或空列表（如果未设置）。`get_file_breaks`(*filename*)返回中的所有断点 *filename* 或空列表（如果未设置）。`get_all_breaks`()返回设置的所有断点。派生类和客户端可以调用以下方法来获取表示堆栈跟踪的数据结构。`get_stack`(*f*, *t*)获取一个帧和所有较高（调用）和较低帧的记录列表，以及较高部分的大小。`format_stack_entry`(*frame_lineno*, *lprefix=': '*)返回一个字符串，其中包含有关堆栈项的信息，由 `(frame, lineno)` 元组：包含框架的文件名的规范形式。函数名，或 `"<lambda>"` .输入参数。返回值。代码行（如果存在）。客户端可以调用以下两个方法来使用调试器调试 [statement](https://www.osgeo.cn/cpython/glossary.html#term-statement) ，作为字符串提供。`run`(*cmd*, *globals=None*, *locals=None*)调试通过 [`exec()`](https://www.osgeo.cn/cpython/library/functions.html#exec) 功能。 *globals* 默认为 `__main__.__dict__` ， *locals* 默认为 *globals* .`runeval`(*expr*, *globals=None*, *locals=None*)调试通过 [`eval()`](https://www.osgeo.cn/cpython/library/functions.html#eval) 功能。 *globals* 和 *locals* 与中的含义相同 [`run()`](https://www.osgeo.cn/cpython/library/bdb.html#bdb.Bdb.run) .`runctx`(*cmd*, *globals*, *locals*)为了向后兼容。调用 [`run()`](https://www.osgeo.cn/cpython/library/bdb.html#bdb.Bdb.run) 方法。`runcall`(*func*, */*, **args*, ***kwds*)调试单个函数调用，并返回其结果。
>
> 最后，模块定义了以下功能：
>
> - `bdb.``checkfuncname`(*b*, *frame*)
>
>     根据断点的方式，检查是否应在此处中断 *b* 被设定。如果是通过行号设置的，它会检查 `b.line` 与作为参数传递的框架中的相同。如果断点是通过函数名设置的，我们必须检查我们是否在正确的框架（正确的函数）中，以及是否在其第一个可执行行中。
>
> - `bdb.``effective`(*file*, *line*, *frame*)
>
>     确定此行代码是否存在有效（活动）断点。返回断点的元组和指示是否可以删除临时断点的布尔值。返回 `(None, None)` 如果没有匹配的断点。
>
> - `bdb.``set_trace`()
>
>     使用开始调试 [`Bdb`](https://www.osgeo.cn/cpython/library/bdb.html#bdb.Bdb) 来自调用方帧的实例。

### Bdb.run(*cmd*, *globals=None*, *locals=None*)

调试通过 [`exec()`](https://www.osgeo.cn/cpython/library/functions.html#exec) 功能。 *globals* 默认为 `__main__.__dict__` ， *locals* 默认为 *globals* .

#### 源码

```python
    def run(self, cmd, globals=None, locals=None):
        if globals is None:
            import __main__
            globals = __main__.__dict__
        if locals is None:
            locals = globals
        self.reset()  # 
        if isinstance(cmd, str):
            cmd = compile(cmd, "<string>", "exec") # 需要调试的代码
        sys.settrace(self.trace_dispatch)    # 开始调试，并设置调试的回调函数为 self.trace_dispatch 该处即为 bdb对 sys.settrace的进一步封装
        try:
            exec(cmd, globals, locals)  # 开始执行
        except BdbQuit:
            pass
        finally:
            self.quitting = True  
            sys.settrace(None)  # 调试结束
```



# 架构设计

## 设计概述

debug插件的架构设计为C/S(客户端，服务端)模式，客户端负责与用户进行信息交互，服务端负责代码调试功能。

此处插入架构设计图

## 客户端

 客户端通拿到用户给定的操作指令后，向服务端发送指令信息，服务端将本次指令的执行结果返回给客户端，结果信息中一般包括 运行至当前栈帧所在的行号、模块名、文件名
局部变量信息等。客户端可自定义将信息展示在信息面板中。例如常见的在已调试过的代码展示对应变量值，方法实参信息等。
 另一方面，为了方便开发人员调试代码，debug插件通常会提供一些在断点中止时基于当前栈帧环境执行代码功能，例如pycharm的watches功能。

### 服务端

 服务端主要负责根据客户端指令进行代码调试，并将执行结果返回给客户端。服务端的关键点在于对栈帧的处理，本质上在调试过程中对每一行代码处的栈帧都会解析信息，只不过我们只会把需要处理代码行处的栈帧信息返还给客户端。例如：例如当客户端发送debug开始指令时，我们一般会把第一个断点处的栈帧信息返回给客户端。
 debug插件大多采用c/s架构设计，另一主要目的是方便于远程调试。

