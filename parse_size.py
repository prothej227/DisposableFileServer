def ParseSize(size):
    count=0
    size_list=["B","KB","MB","GB","TB","PB","EB","ZB","YB"]
    while size>1024:
        size=size/1024
        count=count+1   
    parseSize=size/(1024**count)+(size%1024)
    return str(round(parseSize,2))+" "+size_list[count]
