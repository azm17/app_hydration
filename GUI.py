# -*- coding: utf-8 -*-
"""
Created on Mon May 27 22:44:20 2019

@author: Azumi Mamiya
"""
import tkinter as tk
import tkinter.ttk as ttk
import my_function as my_func
import datetime

status=False # ログインしていれば，True,していなければ，False
login_id =''
login_pass =''
server_host='192.168.0.32'
server_port=3306
database_name='hydration_db'

#login_message = tk.StringVar()
id_entry = None
pass_entry = None
sub_win = None

def center(toplevel):
    toplevel.update_idletasks()
    w = toplevel.winfo_screenwidth()
    h = toplevel.winfo_screenheight()
    size = tuple(int(_) for _ in toplevel.geometry().split('+')[0].split('x'))
    x = w/2 - size[0]/2
    y = h/2 - size[1]/2
    toplevel.geometry("%dx%d+%d+%d" % (size + (x, y)))

def sub_window():
    global sub_win
    global id_entry
    global pass_entry
    global sub_win

    #サブウィンドウ生成
    sub_win = tk.Toplevel()
    #サブウィンドウの画面サイズ
    sub_win.geometry("300x200")
    center(sub_win)

    # ラベル
    #global login_message
    login_message = tk.StringVar()
    login_message.set('IDとPASSを入力してください')
    login_label = tk.Label(sub_win,textvariable=login_message,font=("",10),height=2)
    login_label.pack(fill="x")

    # エントリー
    id_frame = tk.Frame(sub_win,pady=10)
    id_frame.pack()
    id_label = tk.Label(id_frame,font=("",10),text="  ID   ")
    id_label.pack(side="left")
    id_entry = tk.Entry(id_frame,font=("",10),justify="center",width=15)
    id_entry.pack(side="left")
    
    pass_frame = tk.Frame(sub_win,pady=10)
    pass_frame.pack()
    pass_label = tk.Label(pass_frame,font=("",10),text="PASS")
    pass_label.pack(side="left")
    pass_entry = tk.Entry(pass_frame,font=("",10),justify="center",width=15, show='*')
    pass_entry.pack(side="left")

    # ログインボタン
    login_button = tk.Button(sub_win,bg="gray",text="ログイン",font=("",10),width=7,command=login)
    login_button.pack()

    '''
    #Button生成
    button = tk.Button(\
            sub_win,\
            bg="gray",\
            text = '閉じる',\
            width = str('閉じる'),\
            command = sub_win.destroy\
            )
    button.pack()
    '''

def login():
    global status
    global login_id
    global id_entry
    global pass_entry
    global sub_win

    login_id = id_entry.get()
    login_pass = pass_entry.get()
    try:
        if my_func.kakunin(login_id,login_pass,server_port,server_host,database_name)==True:
            sub_win.destroy()
            home_message.set(login_id+'さん、こんにちは。ログイン中です。')
            status=True
            tree_insert()
        else:
            status=False
            login_message.set('IDまたはPASSが違います')
            tree.delete(*tree.get_children())#リストを消す
    except:
        print('error')
        status=False
        login_message.set('IDまたはPASSが違います')
        tree.delete(*tree.get_children())#リストを消す
    tree_insert()

def send_data():#データをサーバーに送信する
    global status
    if status:
        try:
            wb=float(entry1_1.get())
            wa=float(entry1_2.get())
            text=entry1_3.get()
            time=float(entry1_4.get())
            amount=float(entry1_5.get())
            shitsudo=float(entry1_shitsudo.get())
            tenki=int(flg1.get())
            
            
            if wb==0 or wa ==0 or time ==0 or amount==0 or tenki==int(5):
                raise ValueError("error!")
            else:
                entry1_1.delete(0, tk.END)
                entry1_2.delete(0, tk.END)
                entry1_3.delete(0, tk.END)
                entry1_4.delete(0, tk.END)
                entry1_5.delete(0, tk.END)
                entry1_shitsudo.delete(0, tk.END)
                flg1.set('5')#ボタン初期化
            
            input_message.set('** 結果を送信しました **')
            my_func.sql_data_send(wb,wa,text,time,amount,tenki,shitsudo)
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
    data_tuple_list=my_func.sql_data_get(login_id)
    
    for i in data_tuple_list[::-1]:#(date0,before1,after2,training3,minute4,water5,tenki6,shitsudo7)
        dassui_ristu=my_func.dassui_ritu(i[1],i[2])
        dassui_ryo=round(i[1]-i[2],2)
        if i[6]==0:#天気
            text='晴れ'
        elif i[6]==1:
            text='曇り'
        elif i[6]==2:
            text='雨'
        else:
            text='エラー'
        
        reformed_tuple_list.append((i[0],text,i[7],i[3],i[1],i[2],dassui_ryo,dassui_ristu,i[5],i[4]))
    
    return reformed_tuple_list

if __name__ == "__main__":
    # rootフレームの設定
    root = tk.Tk()
    root.title("デスクトップアプリ")
    root.geometry("800x400")
    center(root)
    
    # ノートブック
    nb = ttk.Notebook(width=400, height=400)
    
    # タブの作成
    home_tab = tk.Frame(nb)
    tab1 = tk.Frame(nb)
    result_tab = tk.Frame(nb)
    tab3 = tk.Frame(nb)
    
    
    nb.add(home_tab, text='ホーム', padding=3)
    nb.add(tab1, text='入力', padding=3)
    nb.add(result_tab, text='表示', padding=3)
    nb.add(tab3, text='コメント', padding=3)
    nb.pack(expand=1, fill='both')

    #home_tab
    home_message = tk.StringVar()
    home_message.set('ようこそ\nログインしてください')
    home_label = tk.Label(home_tab,textvariable=home_message,font=("",10),height=2)
    home_label.pack(fill="x")

    '''
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
    '''
    
    login_button = tk.Button(home_tab,text="ログイン",font=("",10),width=7,bg="gray",command=sub_window)
    login_button.pack()
    
    # input_tab
    # 入力画面ラベルの設定
    input_message = tk.StringVar()
    input_message.set('以下を入力してください。')
    label1_1 = tk.Label(tab1,textvariable=input_message,font=("",15),height=2)
    label1_1.pack(fill="x")
    
    
    # 運動後体重のラベルとエントリーの設定
    frame1_3 = tk.Frame(tab1,pady=10)
    frame1_3.pack()
    label1_4 = tk.Label(frame1_3,font=("",10),text="トレーニング内容   ")
    label1_4.pack(side="left")
    entry1_3 = tk.Entry(frame1_3,font=("",10),justify="center",width=15)
    entry1_3.pack(side="left")
    
    # 天気設定
    flg1 = tk.StringVar()
    flg1.set('5')#ボタン初期値
    frame1_tenki = tk.Frame(tab1,pady=10)
    frame1_tenki.pack()
    label1_tenki = tk.Label(frame1_tenki,font=("",10),text="　　　　　　天気　　　   ")
    label1_tenki.pack(side="left")
    #entry1_tenki = tk.Entry(frame1_tenki,font=("",10),justify="center",width=15)
    bt_tenki0 =tk.Radiobutton(frame1_tenki,text='晴れ',value=0,variable=flg1)
    bt_tenki0.pack(side="left")
    bt_tenki1 =tk.Radiobutton(frame1_tenki,text='くもり',value=1,variable=flg1)
    bt_tenki1.pack(side="left")
    bt_tenki2 =tk.Radiobutton(frame1_tenki,text='雨',value=2,variable=flg1)
    bt_tenki2.pack(side="left")
    
    # 湿度の設定
    frame1_shitsudo = tk.Frame(tab1,pady=10)
    frame1_shitsudo.pack()
    label1_shitsudo = tk.Label(frame1_shitsudo,font=("",10),text="　　 湿度　　　  　　")
    label1_shitsudo.pack(side="left")
    entry1_shitsudo = tk.Entry(frame1_shitsudo,font=("",10),justify="center",width=15)
    entry1_shitsudo.pack(side="left")
    
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
    
    # 運動時間のラベルとエントリーの設定
    frame1_4 = tk.Frame(tab1,pady=10)
    frame1_4.pack()
    label1_5 = tk.Label(frame1_4,font=("",10),text="運動時間（h）  　　")
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
    tree["columns"] = (1,2,3,4,5,6,7,8,9,10)
    tree["show"] = "headings"
    
    tree.column(1,width=75)
    tree.column(2,width=50)
    tree.column(3,width=50)
    tree.column(4,width=90)
    tree.column(5,width=90)
    tree.column(6,width=90)
    tree.column(7,width=70)
    tree.column(8,width=70)
    tree.column(9,width=70)
    tree.column(10,width=70)
    
    # 各列のヘッダー設定(インデックス,テキスト)
    tree.heading(1,text="日付")
    tree.heading(2,text="天気")
    tree.heading(3,text="湿度")
    tree.heading(4,text="トレーニング内容")
    tree.heading(5,text="運動前体重(kg)")
    tree.heading(6,text="運動後体重(kg)")
    tree.heading(7,text="脱水量(L)")
    tree.heading(8,text="脱水率(%)")
    tree.heading(9,text="水分摂取量")
    tree.heading(10,text="運動時間(h)")
    
    scroll2_1 = tk.Scrollbar(result_frame, orient = 'v', command = tree.yview)
    
    # スクロールの設定
    tree.configure(yscrollcommand = scroll2_1.set)
    
    # gridで配置
    tree.grid(row = 1, column = 0, sticky = 'ns')
    scroll2_1.grid(row = 1, column = 1, sticky = 'ns')
    # ツリービューの配置
    
    
    # メインループ
    root.mainloop()
