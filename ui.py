import tkinter as tk
import tkinter.ttk as ttk

class ToolTip(object):
    def __init__(self, widget, text):
        self.widget = widget
        self.tipwindow = None
        self.id = None
        self.x = self.y = 0
        self.text=text
        widget.bind('<Enter>', self.enter)
        widget.bind('<Leave>', self.leave)
    def enter(self,event):
        self.showtip(self.text)
    def leave(self,event):
        self.hidetip()
    #当光标移动指定控件是显示消息
    def showtip(self, text):
        "Display text in tooltip window"
        self.text = text
        if self.tipwindow or not self.text:
            return
        x, y, cx, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx()+30
        y = y + cy + self.widget.winfo_rooty()+30
        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry("+%d+%d" % (x, y))
        label = tk.Label(tw, text=self.text,justify=tk.LEFT,
                      background="white", relief=tk.SOLID, borderwidth=1,
                      font=("仿宋", "10"))
        label.pack(side=tk.BOTTOM)
    #当光标移开时提示消息隐藏
    def hidetip(self):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()

class ScrolledFrame(tk.Canvas):
    def __init__(self,parent,width=200,height=None,bg=None):
        self.parent=parent
        self.width=width
        self.height=height
        self.frame=tk.Frame(self.parent,width=self.width,height=self.height)
        self.scrollbar=tk.Scrollbar(self.frame)
        tk.Canvas.__init__(self,self.frame,bg=bg,yscrollcommand=self.scrollbar.set,width=self.width,height=self.frame['height'])
        self.scrollbar.pack(side=tk.RIGHT,fill=tk.Y)
        self.pack(fill=tk.BOTH)
        self.scrollbar.config(command=self.yview)
    def frame_pack(self,**kwargs):
        self.frame.pack(**kwargs)
    def place(self,**kwargs):
        self.frame.place(**kwargs)
    def grid(self,**kwargs):
        self.frame.grid(**kwargs)

class LogList(ScrolledFrame):
    def __init__(self,parent,initial_list=[],width=200,height=None):
        self.parent=parent
        self.width=width
        self.height=height
        self.txtlst=[]
        self.tooltiplst=[]
        ScrolledFrame.__init__(self,self.parent,width=self.width,height=self.height)
    def insert(self,index,content,bg='#ffffff',fg='#000000',font=None):
        for i in self.txtlst:
            i.pack_forget()
        if index==tk.END:
            self.txtlst.append(tk.Label(self,text=content,bg=bg,fg=fg,font=font,anchor='w'))
            self.tooltiplst.append(ToolTip(self.txtlst[len(self.txtlst)-1],content))
        else:
            self.txtlst.insert(index,tk.Label(self,text=content,bg=bg,fg=fg,font=font,anchor='w'))
            self.tooltiplst.insert(index,ToolTip(self.txtlst[index],content))
        for i in self.txtlst:
            i.pack(fill=tk.X,expand=True)
    def remove(self,index):
        for i in self.txtlst:
            i.pack_forget()
        if index==tk.END:
            self.txtlst.remove(len(self.txtlst-1))
        else:
            self.txtlst.remove(index)
        for i in self.txtlst:
            i.pack(fill=tk.X,expand=True)
