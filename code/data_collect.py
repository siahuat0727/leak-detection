#lists=["1-0.log","1-20.log","1-40.log","1-60.log","1-80.log","2-20.log","2-40.log","2-60.log","2-80.log","3-20.log","3-40.log","3-60.log","4-20.log","4-40.log","4-60.log","5-20.log","5-40.log","5-60.log","5-80.log","6-20.log","6-40.log","6-60.log","7-20.log","7-40.log","7-60.log","open_close.log"]
lists=["1-20.log","1-40.log","1-60.log","1-80.log","3-20.log","3-40.log","3-60.log"]
count=0
def file_lines_count(filename):
    global total
    total=0
    file_open=open(filename,'r')
    for text in file_open:
        total=total+1;
    file_open.close()
    
for i in lists:
    file_open=open(i,'r')
    filename=i[0:i.index(".")]+"_new.log"
    file_lines_count(i)
    global file_wirte
    file_wirte=open(filename,'w')
    print(total)
    count=0
    while True:
        text=file_open.readline()
        count=count+1
        if text=="":
            break
        if count>100:
            if count!=total:
                text=text.strip('\n')
                file_wirte.write(text)
                file_wirte.write(" ")
    file_open.close()
    file_wirte.close()

    
