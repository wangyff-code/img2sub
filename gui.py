import tkinter as tk
import numpy as np
from PIL import Image, ImageTk
from tkinter import filedialog
import cv2 as cv
from sub import gen_sub_file
from sub2 import gen_zip_sub_file
import tkinter.ttk as ttk
import tkinter.messagebox as msg

def cvt_array_2_tk(img_array):
    img_array = img_array[:,:,0:3]
    img_rgb = cv.cvtColor(img_array, cv.COLOR_BGR2RGB)
    img = Image.fromarray(img_rgb)
    tkImage = ImageTk.PhotoImage(image=img)
    return tkImage


class main_gui():
    def __init__(self):
        self.window = tk.Tk()
        self.window.title('潜艇图片转换 V1.2.1')
        self.f_head = tk.Frame(self.window)
        self.f_head.pack()
        self.init_head()

        self.pic_show = tk.Frame(self.window)
        self.pic_show.pack()
        self.init_picshow()

        self.ctr  = tk.Frame(self.window)
        self.ctr.pack()
        self.init_ctr()


        self.window.mainloop()


    def open_img(self):
        s2fname = filedialog.askopenfilename(title='打开图片文件',
                                             filetypes=[('jpg/png', '*.jpg;*.png'),
                                                        ('All Files', '*')])
        self.org_img = cv.imdecode(np.fromfile(s2fname, dtype=np.uint8),cv.IMREAD_UNCHANGED)
        x = self.org_img.shape[0]
        y = self.org_img.shape[1]
        x1 = 200
        y1 = int(200/x*y)
        show_img = cv.resize(self.org_img,(y1,x1))
        tkImage = cvt_array_2_tk(show_img)
        self.label_img1.configure(image=tkImage)
        self.label_img1.image = tkImage
        self.update_img()

    def update_img(self,*arg):
        dec_number = int(self.s2.get())

        x = self.org_img.shape[0]
        y = self.org_img.shape[1]
        n_x = self.org_img.shape[0]*dec_number//100
        n_y = self.org_img.shape[1]*dec_number//100
        show_img = cv.resize(self.org_img,(n_y,n_x))
        self.cvt_img = show_img
        x1 = 200
        y1 = int(200/x*y)

        show_img = cv.resize(show_img,(y1,x1))
        tkImage = cvt_array_2_tk(show_img)
        self.label_img2.configure(image=tkImage)
        self.label_img2.image = tkImage
        self.bk_str.set('结构数={}'.format(n_x*n_y))

    def gen_sub_fun(self):
        mod=self.sel.get()
        org_img=self.cvt_img
        if org_img.shape[2] == 4:
            mask = org_img[:,:,3]
        else:
            mask = np.zeros((org_img.shape[0],org_img.shape[1]),dtype=np.uint8)+255
        if mod == '单像素像素模式':
            gen_sub_file(org_img,mask,'A1',self.prg,self.ctr)
        else:
            gen_zip_sub_file(org_img,mask,'A1',self.prg,self.ctr)
        msg.showinfo("转换完成","A1.sub filelist.xml 已生成")


    def init_ctr(self):
        self.sel = ttk.Combobox(self.ctr)
        self.sel['value'] = ('单像素像素模式','合并像素模式')
        self.sel.current(0)
        self.sel.pack()
        l = tk.Label(self.ctr,text='降采样倍率（缩小分辨率）')
        l.pack()
        self.s2 = tk.Scale(self.ctr,from_=100,length=200,to=1,orient=tk.HORIZONTAL,command=self.update_img)
        self.s2.set(80)
        self.s2.pack()
        self.bk_str = tk.StringVar()
        l = tk.Label(self.ctr,textvariable=self.bk_str)
        self.bk_str.set('结构数=???????')
        l.pack()
        bt =tk.Button(text='生成潜艇文件',command=self.gen_sub_fun)
        bt.pack()
        self.prg = ttk.Progressbar(self.ctr)
        self.prg.pack()
        self.prg['maximum'] = 100
        self.prg['value']   = 0

    def init_head(self):
        bt = tk.Button(self.f_head,text='打开图片',command=self.open_img)
        bt.pack(side=tk.LEFT)

    def init_picshow(self):
        self.org_img = np.zeros((256,256,3),dtype=np.uint8)
        tkImage = cvt_array_2_tk(self.org_img)
        self.label_img1 = tk.Label(self.pic_show, image=tkImage,bg='#444444')
        self.label_img1.pack(side=tk.LEFT)
        self.label_img2 = tk.Label(self.pic_show, image=tkImage,bg='#444444')
        self.label_img2.pack(side=tk.RIGHT)

gui = main_gui()