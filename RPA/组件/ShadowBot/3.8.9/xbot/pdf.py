from ._core import uidriver
import typing

def extract_text(path, from_page, to_page, *, password = None) -> str:
    '''
    提取pdf文件文本
    * @param path, pdf文件路径
    * @param from_page, 起始页码
    * @param to_page, 终止页码
    * @param password, 密码
    * @return `str`, 返回从pdf文件中提取的文本
    '''
    return uidriver.execute('Pdf.ExtractText', {
                'path' : path,
                'fromPage' : from_page,
                'toPage' : to_page,
                'password' : password
            })

def extract_images(path, from_page, to_page, save_to_dir, *, password = None, name_prefix = 'pdf_image') -> typing.List[str]:
    '''
    提取pdf文件图片
    * @param path, pdf文件路径
    * @param from_page, 起始页码
    * @param to_page, 终止页码
    * @param save_to_dir, 保存的文件夹路径
    * @param password, 密码
    * @param name_prefix, 导出的图片名称前缀
    * @return `List[str]`, 返回提取到本地的图片路径列表, 如['c:/work/image_0501101010_1.png', 'c:/work/image_0501101010_2.png']
    '''
    return uidriver.execute('Pdf.ExtractImages', {
                'path' : path,
                'fromPage' : from_page,
                'toPage' : to_page,
                'imagePrefix' : name_prefix,
                'saveToDir' : save_to_dir,
                'password' : password
            })

def extract_pages(path, from_page, to_page, save_to, *, password = None) -> str:
    '''
    导出pdf文件中的页
    * @param path, pdf文件路径
    * @param from_page, 起始页码
    * @param to_page, 终止页码
    * @param save_to, 保存的文件路径
    * @param password, 密码
    * @return `str`, 返回保存到本地的新文件路径
    '''
    return uidriver.execute('Pdf.ExtractPages', {
                'path' : path,
                'fromPage' : from_page,
                'toPage' : to_page,
                'saveTo' : save_to,
                'password' : password
            })
    
def merge_pdfs(paths, save_to, *, passwords = None) -> str:
    '''
    合并多个pdf文件
    * @param paths, pdf文件路径列表
    * @param save_to, 保存的文件路径
    * @param passwords, 密码列表
    * @return `str`, 返回保存到本地的新文件路径
    '''
    return uidriver.execute('Pdf.MergePdfs', {
                'paths' : paths,
                'saveTo' : save_to,
                'passwords' : passwords
            })