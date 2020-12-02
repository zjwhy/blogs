# -*- coding:utf-8 -*-
from ftplib import FTP
import os
from ubpa.ilog import ILog
from ubpa.encrypt import decrypt
logger = ILog(__file__)


class IFtp(object):

    def __init__(self, ip, port=21, encoding="utf-8"):
        '''
           ip: ftp connection address
           port: Port number
           user: user Name
           psw: password
           encoding:  # encoding = "utf-8" ,# encoding = "GB18030"
        '''
        try:
            self.ftp = FTP()
            self.ftp.encoding = encoding
            self.ip = ip
            self.port = port
        except Exception as e:
            raise (e)

    def ftp_login(self, user, psw):
        '''
        function: Ftp connection and login
        param:
            user: user Name
            psw: password
        '''
        try:
            self.connect = self.ftp.connect(self.ip, self.port)
            self.login = self.ftp.login(user, decrypt(psw))
        except Exception as e:
            raise e


    def ftp_upload(self, src_path, dst_path, mode='binary'):

        '''
             function: ftp upload by two modes, mode binary or mode line
             param:  src_path:you can upload a file or a folder to ftp server
                     r'd://xlss//xlsss1.xlsx,
                     d://xlss//xlsss2.xlsx',
                     r'd://xlss//conf'
                     dst_path: the address which you need upload folder to ftp; r'home//test'
                     or you can build new folder on ftp;r'home//test//conf1//conf2'
             return:  True
        '''
        logger.debug('start ftp_upload the file or folder')

        try:
            if src_path.find(".") == -1:

                src_path_list = [file.strip().rstrip() for file in src_path.split(',')]
                for index_src_path in src_path_list:

                    self.get_to_distpath(index_src_path,dst_path)
                    self.ftp_upload_folder(index_src_path, mode)
            else:
                self.ftp_upload_singlefile(src_path, dst_path, mode)

            self.back_file()
            logger.debug('end ftp_upload the file or folder')
            return True
        except Exception as e:
            raise (e)

    def upload(self, src_path, mode):
        try:
            fp = open(src_path, 'rb')

            if "binary" == mode:
                self.ftp.storbinary('STOR ' + os.path.basename(src_path), fp)
            elif "line" == mode:
                self.ftp.storlines('STOR ' + os.path.basename(src_path), fp)

            fp.close()
        except Exception as e:
            raise (e)

    def ftp_upload_singlefile(self, src_path, dst_path, mode):
        '''upload single_file'''
        try:
            self.back_file()
            self.ftp.cwd(dst_path)
            local_files_list = [file.strip().rstrip() for file in src_path.split(',')]

            for local_file in local_files_list:

                self.upload(local_file, mode)
        except Exception as e:
            raise (e)

    def get_to_distpath(self, index_src_path, dst_path):

        try:
            folder_name = os.path.basename(index_src_path)

            self.back_file()
            dst_path_list = self.get_list(dst_path)

            if len(dst_path_list) > 0:
                for index1 in dst_path_list:
                    try:

                        self.ftp.cwd(index1)
                    except Exception as e:

                        self.ftp.mkd(index1)
                        self.ftp.cwd(index1)
            else:
                try:

                    self.ftp.cwd(dst_path)
                except Exception as e:

                    self.ftp.mkd(dst_path)
                    self.ftp.cwd(dst_path)

            self.ftp.mkd(folder_name)
            self.ftp.cwd(folder_name)
        except Exception as e:
            self.ftp.cwd(folder_name)


    def ftp_upload_folder(self, src_path, mode):
        '''upload folder to ftp'''
        try:
            files = os.listdir(src_path)
            os.chdir(src_path)
            for f in files:
                if os.path.isfile(src_path + r'\{}'.format(f)):

                    self.upload(f, mode)
                elif os.path.isdir(src_path + r'\{}'.format(f)):
                    try:
                        self.ftp.mkd(f)
                        self.ftp.cwd(f)
                        self.ftp_upload_folder(src_path + r'\{}'.format(f), mode)
                    except Exception as e:

                        self.ftp.cwd(f)
                        self.ftp_upload_folder(src_path + r'\{}'.format(f), mode)

            self.ftp.cwd('..')
            os.chdir('..')
        except Exception as e:
            raise (e)


    def ftp_download(self, src_path, dst_path, mode='binary'):
        '''

            :function: ftp download by two modes, mode binary or mode line
           :param：src_path:  the local address which you need download ;
                              r'd://xlss'
                   dst_path: you can download signle-file or folder
                             r'home//isa', r'usr//local//test.txt'
           :return:
        '''

        logger.debug('start ftp_download the file or folder')
        try:
            if dst_path.find(".") == -1:

                dst_path_list = [file.strip().rstrip() for file in dst_path.split(',')]
                for index_dst_path in dst_path_list:
                    self.back_file()
                    p = self.get_list(index_dst_path)

                    new_src_path = src_path + os.sep + p[len(p)-1]
                    try:
                        os.mkdir(new_src_path)
                    except Exception as e:
                        pass

                    self.ftp_download_folder(new_src_path, index_dst_path, mode)
            else:
                self.ftp_download_singlefile(src_path, dst_path, mode)

            self.back_file()
            logger.debug('end ftp_download the file or folder')
            return True
        except Exception as e:
            raise (e)

    def download(self, src_path, dst_path, mode):
        '''ftp download'''
        try:
            if "binary" == mode:
                fp = open(src_path, 'wb')
                self.ftp.retrbinary('RETR ' + dst_path, fp.write)
            elif "line" == mode:
                fp = open(src_path, 'wt')
                self.ftp.retrlines('RETR ' + dst_path, fp.write)

            fp.close()
        except Exception as e:
            raise (e)

    def ftp_download_singlefile(self, src_path, dst_path, mode):
        '''download single_file'''
        try:
            local_files_list = [file.strip().rstrip() for file in dst_path.split(',')]

            for local_file in local_files_list:

                file_path = self.get_current(local_file)
                if "/" in src_path:
                    new_src_path = src_path + "/" + file_path
                if "\\" in src_path:
                    new_src_path = src_path + "\\" + file_path

                self.download(new_src_path, file_path, mode)
        except Exception as e:
            raise (e)


    def ftp_download_folder(self, src_path, dst_path, mode):
        '''download when download folder on ftp'''
        try:
            if not os.path.exists(src_path):
                os.makedirs(src_path)

            self.get_current1(dst_path)

            dst_names = self.ftp.nlst()
            for file in dst_names:

                local_path = os.path.join(src_path, file)
                if file.find(".") == -1:

                    if not os.path.exists(local_path):

                        os.makedirs(local_path)
                    self.ftp_download_folder(local_path, file, mode)
                else:

                    self.download(local_path, file, mode)

            self.ftp.cwd("..")
            return
        except Exception as e:
            raise (e)

    def get_current(self, dst_path):
        '''get current file path'''
        try:
            dst_path_list = self.get_list(dst_path)

            self.back_file()

            if len(dst_path_list) > 0:

                if dst_path.find(".") == -1:
                    dp_list = dst_path_list
                else:
                    dp_list = dst_path_list[:-1]

                for j in range(len(dp_list)):
                    if 0 == j:
                        self.ftp.cwd("..")

                    self.ftp.cwd(dp_list[j])

                return dst_path_list[len(dst_path_list)-1]
            else:
                self.ftp.cwd("..")
                return dst_path
        except Exception as e:
            raise (e)


    def get_current1(self, dst_path):
        '''get current file path'''
        try:
            dst_path_list = self.get_list(dst_path)

            if len(dst_path_list) > 0:

                if dst_path.find(".") == -1:
                    dp_list = dst_path_list
                else:
                    dp_list = dst_path_list[:-1]

                for j in range(len(dp_list)):
                    if 0 == j:
                        self.ftp.cwd("..")
                    self.ftp.cwd(dp_list[j])

                return dst_path_list[len(dst_path_list)-1]
            else:
                self.ftp.cwd(dst_path)
                return dst_path
        except Exception as e:
            raise (e)


    def ftp_close(self):
        '''close ftp'''
        try:
            self.ftp.close()
        except Exception as e:
            raise (e)


    def back_file(self):
        ''' back to the top catalog '''
        try:
            ab_filepath = self.ftp.pwd()

            ab_file_list = self.get_list(ab_filepath)

            for index in ab_file_list:
                if '' != index:
                    self.ftp.cwd("..")
        except Exception as e:
            raise (e)

    def get_list(self, path):
        ab_file_list = []

        if "/" in path:
            ab_file_list = path.split("/")
        if "\\" in path:
            ab_file_list = path.split("\\")

        return ab_file_list



# def ftp_upload(src_path, dst_path, ip, port, user, psw, encoding,mode):
#     try:
#         ftp = IFtp(ip, user, psw, encoding, port)
#         res = ftp.ftp_upload(src_path, dst_path, mode)
#         ftp.ftp_close()
#         return res
#     except Exception as e:
#         raise e
#
#
# def ftp_download(src_path, dst_path, ip, port, user, psw, encoding,mode):
#     try:
#         ftp = IFtp(ip, user, psw, encoding, port)
#         res = ftp.ftp_download(src_path, dst_path, mode)
#         ftp.ftp_close()
#         return res
#     except Exception as e:
#         raise e



# if __name__ == '__main__':
#     ftp = IFtp("192.168.0.213", "root", "s0rtec1o2o", "GB18030", 21)
#     ftp = IFtp("192.168.0.93", 2121, "isearch", "is1arch-u1ba")
    # ftp = IFtp("192.168.0.168", "ftpuser", "ftp!o@o", 21)

    # ftp.ftp_upload(r'D:\aaa.ipkg', r'home/ftpuser/liuhan', "line")

    # ftp.ftp_upload(r'C:\Users\tanbinbin\Desktop\aa.txt', r'home/test', "line")
    # ftp.ftp_upload(r'C:\Users\tanbinbin\Desktop\保额计算_20181120101404.xlsx,C:\Users\tanbinbin\Desktop\aa.txt', r'home/test', "line")
    # ftp.ftp_upload(r'D:\xlss\RPA Activites DesignBook你好.xlsx,'
    #                r'D:\xlss\RPA DesignBook他好.docx', r'root/test/哈哈')
    # ftp.test()
    #
    # ftp.ftp_upload(r'd:/xlss/conf新建文件', r'home/test')
    # ftp.ftp_upload(r'd:/xlss/conf新建文件,D:\xlss\session', r'root/test')
    # ftp.ftp_download(r'd:/xlss', r'home/test/conf新建文件,home/test/session')
    # ftp.ftp_download(r'd:/xlss', r'home/test/寿险查询数据.txt', "line")
    # ftp.ftp_close()




