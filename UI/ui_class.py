import sys
import tkinter as tk
from function.config import source_urls

class ConfigUi:
    def __init__(self):
        self.selected_urls = [] # 选定的直播源地址
        self.is_match_template = False # 是否匹配模板给定频道
        self.is_response_test = False  # 是否对直播地址测试响应时间
        self.is_dump_remove = True # 是否对采集到的地址进行去重
        self.response_time = 300  # 设置筛选直播源url的响应时间，单位毫秒
        self.save_name = None # 保存文件名
        self.v6_or_v4 = 6

    def main_win(self):
        root = tk.Tk()
        root.geometry('302x340')
        root.resizable(False,False)
        root.title('参数配置')
        lb = tk.Label(root, text='', width=21).grid(row=0,column=0)
        lb = tk.Label(root, text='', width=21).grid(row=0,column=1)
        lb1 = tk.Label(root, text=f'共收集直播源  {len(source_urls)}  条', width=18).grid(row=1, column=0, sticky='ew')
        self.lb2 = tk.Label(root, text=f'已选择____条')
        self.lb2.grid(row=1, column=1, sticky='ew')
        bt1 = tk.Button(root, text='选源', command=self.sources_select).grid(row=2, columnspan=2,sticky='ew')
        lb3 = tk.Label(root, text='-' * 80, width=40).grid(row=3, columnspan=2)
        def update_radios():
            if vars_ckbox[2].get():
                radio1.grid(row=7, column=0, sticky='ew')
                radio2.grid(row=7, column=1, sticky='ew')
                entry_response_time.grid(row=8, column=1)
                lb4.grid(row=8, column=0)
            else:
                radio1.grid_remove()
                radio2.grid_remove()
                entry_response_time.grid_remove()
                lb4.grid_remove()
        vars_ckbox = []
        var = tk.IntVar()
        var.set(1)
        vars_ckbox.append(var)
        ck_box1 = tk.Checkbutton(root, text='是否对urls去重',variable=var).grid(row=4, sticky='w')
        var = tk.IntVar()
        vars_ckbox.append(var)
        ck_box2 = tk.Checkbutton(root, text='是否匹配给定频道', variable=var).grid(row=5, sticky='w')
        var = tk.IntVar()
        vars_ckbox.append(var)
        ck_box3 = tk.Checkbutton(root, text='是否进行响应检测', variable=var, command=update_radios).grid(row=6, sticky='w')

        var_r = tk.IntVar()  # 排序优先级
        var_r.set(6)
        radio1 = tk.Radiobutton(root, text='IPV6排先', variable=var_r, value=6)
        radio2 = tk.Radiobutton(root, text='IPV4排先', variable=var_r, value=4)

        lb4 = tk.Label(root,text='响应时间阈值(ms)：')
        entry_response_time = tk.Entry(root)

        lb5 = tk.Label(root, text='保存的文件名：').grid(row=9, column=0)
        entry_save_name = tk.Entry(root)
        entry_save_name.grid(row=9, column=1)
        def confirm():
            self.is_dump_remove = vars_ckbox[0].get()
            self.is_match_template = vars_ckbox[1].get()
            self.is_response_test = vars_ckbox[2].get()
            self.v6_or_v4 = var_r.get()
            self.response_time = int(entry_response_time.get()) if entry_response_time.get() else None
            self.save_name = entry_save_name.get() if entry_save_name.get() else 'live'
            root.destroy()
        bt2 = tk.Button(root, text='Start', command=confirm).grid(row=10, column=0, sticky='ew')
        bt3 = tk.Button(root, text='Cancel', command=lambda :sys.exit()).grid(row=10, column=1, sticky='ew')


        root.protocol('WM_DELETE_WINDOW',lambda:sys.exit())
        root.mainloop()

    def sources_select(self):
        root = tk.Toplevel()
        root.title('直播源选择')
        vars_u = []
        is_selected = True
        row = 1
        for url in source_urls:
            var_u = tk.IntVar()
            ck_box = tk.Checkbutton(root, text=url, variable=var_u).grid(row=row, sticky='w')
            vars_u.append(var_u)
            row += 1
        def select_all():
            nonlocal is_selected
            if is_selected:
                for var in vars_u:
                    var.set(1)
                    bt_select.config(text='全不选')
            else:
                for var in vars_u:
                    var.set(0)
                    bt_select.config(text='全选')
            is_selected = not is_selected
        def click_ok():
            self.selected_urls = [source_urls[i] for i, v in enumerate(vars_u) if v.get()]
            print(f'已选urls:{self.selected_urls}')
            self.lb2.config(text=f'已选择  {len(self.selected_urls)}  条')
            root.destroy()
        bt_ok = tk.Button(root, text='OK', command=click_ok).grid(row=row,column=1)
        bt_select = tk.Button(root, text='全选', command=select_all)
        bt_select.grid(row=row,column=0)



if __name__ == '__main__':
    cfg = ConfigUi()
    cfg.main_win()
    print(cfg.selected_urls)
    print(cfg.is_dump_remove)
    print(cfg.is_match_template)
    print(cfg.is_response_test)
    print(cfg.v6_or_v4)
    print(cfg.response_time)
    print(cfg.save_name)