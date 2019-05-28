# -*- coding: utf-8 -*-
"""
Created on Mon May 27 22:44:20 2019

@author: Azumi Mamiya
"""

# -*- coding: utf-8 -*-
"""
Created on Mon May 27 22:43:09 2019

@author: Azumi Mamiya
"""

import tkinter as tk
import tkinter.ttk as ttk
import my_function as my_func
import datetime

status=False # ログインしていれば，True,していなければ，False
login_id =''
login_pass =''
server_host='192.168.0.31'
server_port=3306
database_name='db_test0518'



def login():
    global status
    login_id = id_entry.get()
    login_pass = pass_entry.get()
    try:
        if my_func.kakunin(login_id,login_pass,server_port,server_host,database_name)==True:
            login_message.set(login_id+'さん、こんにちは。ログイン中です。')
            status=True
            tree_insert()
        else:
            status=False
            login_message.set('IDまたはPASSが違います')
            tree.delete(*tree.get_children())#リストを消す
    except:
        status=False
        login_message.set('IDまたはPASSが違います')
        tree.delete(*tree.get_children())#リストを消す

def send_data():#データをサーバーに送信する
    global status
    if status:
        try:
            wb=float(entry1_1.get())
            wa=float(entry1_2.get())
            text=entry1_3.get()
            time=int(entry1_4.get())
            amount=float(entry1_5.get())
            input_message.set('** 結果を送信しました **')
            my_func.sql_data_send(wb,wa,text,time,amount)
            tree_insert()
        except:
            input_message.set('結果を送信できませんでした。\n情報を正しく入力してください。')
    else:
        input_message.set('ログインしてください')

def tree_insert():#データを結果に表示
    tree.delete(*tree.get_children())
    data_list=data_reform()
    for data in data_list:
        tree.insert("","end",values=data)

def data_reform():#SQLからのデータをタプルに変換
    reformed_tuple_list=[]
    #data_tuple_list=[(datetime.date(2019, 5, 28), 60.0, 59.0, 'run', 60.0, 1.0),
    #                 (datetime.date(2019, 5, 28), 60.0, 59.0, 'run', 60.0, 1.0)]
    data_tuple_list=my_func.sql_data_get()
    
    for i in data_tuple_list[::-1]:
        reformed_tuple_list.append((i[0],i[1],i[2],i[4],i[5],i[3]))
    
    return reformed_tuple_list

if __name__ == "__main__":
    # rootフレームの設定
    root = tk.Tk()
    root.title("デスクトップアプリ")
    root.geometry("600x400")
    
    # ノートブック
    nb = ttk.Notebook(width=400, height=400)
    
    # タブの作成
    login_tab = tk.Frame(nb)
    tab1 = tk.Frame(nb)
    result_tab = tk.Frame(nb)
    tab3 = tk.Frame(nb)
    
    
    nb.add(login_tab, text='ログイン', padding=3)
    nb.add(tab1, text='入力', padding=3)
    nb.add(result_tab, text='表示', padding=3)
    nb.add(tab3, text='コメント', padding=3)
    nb.pack(expand=1, fill='both')

    #login_tab
    login_message = tk.StringVar()
    login_message.set('IDとPASSを入力してください')
    login_label = tk.Label(login_tab,textvariable=login_message,font=("",10),height=2)
    login_label.pack(fill="x")
    
    id_frame = tk.Frame(login_tab,pady=10)
    id_frame.pack()
    id_label = tk.Label(id_frame,font=("",10),text="  ID   ")
    id_label.pack(side="left")
    id_entry = tk.Entry(id_frame,font=("",10),justify="center",width=15)
    id_entry.pack(side="left")
    
    pass_frame = tk.Frame(login_tab,pady=10)
    pass_frame.pack()
    pass_label = tk.Label(pass_frame,font=("",10),text="PASS")
    pass_label.pack(side="left")
    pass_entry = tk.Entry(pass_frame,font=("",10),justify="center",width=15, show='*')
    pass_entry.pack(side="left")
    
    login_button = tk.Button(login_tab,text="ログイン",font=("",10),width=7,bg="gray",command=login)
    login_button.pack()
    
    # input_tab
    # 入力画面ラベルの設定
    input_message = tk.StringVar()
    input_message.set('以下を入力してください。')
    label1_1 = tk.Label(tab1,textvariable=input_message,font=("",15),height=2)
    label1_1.pack(fill="x")
    
    
    # 水分摂取量とエントリーの設定
    frame1_1 = tk.Frame(tab1,pady=10)
    frame1_1.pack()
    label1_2 = tk.Label(frame1_1,font=("",10),text="運動前の体重（kg）")
    label1_2.pack(side="left")
    entry1_1 = tk.Entry(frame1_1,font=("",10),justify="center",width=15)
    entry1_1.pack(side="left")
    
    # 運動前の体重のラベルとエントリーの設定
    frame1_2 = tk.Frame(tab1,pady=10)
    frame1_2.pack()
    label1_3 = tk.Label(frame1_2,font=("",10),text="運動後の体重（kg）")
    label1_3.pack(side="left")
    entry1_2 = tk.Entry(frame1_2,font=("",10),justify="center",width=15)
    entry1_2.pack(side="left")
    
    # 運動後体重のラベルとエントリーの設定
    frame1_3 = tk.Frame(tab1,pady=10)
    frame1_3.pack()
    label1_4 = tk.Label(frame1_3,font=("",10),text="トレーニング内容   ")
    label1_4.pack(side="left")
    entry1_3 = tk.Entry(frame1_3,font=("",10),justify="center",width=15)
    entry1_3.pack(side="left")
    
    # 運動時間のラベルとエントリーの設定
    frame1_4 = tk.Frame(tab1,pady=10)
    frame1_4.pack()
    label1_5 = tk.Label(frame1_4,font=("",10),text="運動時間（分）  　　")
    label1_5.pack(side="left")
    entry1_4 = tk.Entry(frame1_4,font=("",10),justify="center",width=15)
    entry1_4.pack(side="left")
    
    # 運動時間のラベルとエントリーの設定
    frame1_5 = tk.Frame(tab1,pady=10)
    frame1_5.pack()
    label1_6 = tk.Label(frame1_5,font=("",10),text="水分摂取量（L） 　　")
    label1_6.pack(side="left")
    entry1_5 = tk.Entry(frame1_5,font=("",10),justify="center",width=15)
    entry1_5.pack(side="left")
    
    # 登録ボタンの設定
    button1_5 = tk.Button(tab1,text="送信",font=("",10),width=5,bg="gray",command=send_data)
    button1_5.pack()
    
    ## タブ2
    # 入力画面ラベルの設定
    result_frame = tk.Frame(result_tab,pady=10)
    result_frame.pack()
    tree = ttk.Treeview(result_frame, height=16) # to change height of treeview
    tree["columns"] = (1,2,3,4,5,6)
    tree["show"] = "headings"
    
    tree.column(1,width=75)
    tree.column(2,width=70)
    tree.column(3,width=70)
    tree.column(4,width=70)
    tree.column(5,width=70)
    tree.column(6,width=70)
    # 各列のヘッダー設定(インデックス,テキスト)
    tree.heading(1,text="日付")
    tree.heading(2,text="運動前体重")
    tree.heading(3,text="運動後体重")
    tree.heading(4,text="運動時間")
    tree.heading(5,text="水分摂取量")
    tree.heading(6,text="トレーニング内容")
    
    
    
    scroll2_1 = tk.Scrollbar(result_frame, orient = 'v', command = tree.yview)
    
    # スクロールの設定
    tree.configure(yscrollcommand = scroll2_1.set)
    
    # gridで配置
    tree.grid(row = 1, column = 0, sticky = 'ns')
    scroll2_1.grid(row = 1, column = 1, sticky = 'ns')
    # ツリービューの配置
    
    
    # メインループ
    root.mainloop()
