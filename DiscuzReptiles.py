import os
import time
import random
import requests
from selenium import webdriver
from ua_info import ua_list
from selenium.webdriver.common.by import By
#设置加载策略为eager
options = webdriver.EdgeOptions()
options.page_load_strategy = 'eager'
options.add_argument("headless")
options.add_experimental_option("detach",True)
#该函数用于打开页面
def startStage(url):
    while(1):
        try:
            edge.get(url)
            time.sleep(1)
            #判断是否正确加载
            break
        except Exception:
            continue
#实例化浏览器对象并指定驱动路径
#edge=webdriver.Edge(executable_path='msedgedriver.exe',capabilities=options.to_capabilities())#旧版本
edge=webdriver.Edge(options=options)
url = 'https://XXXXX'   #网站基础url
start = input('enter a start:')  #起始页
end=input('enter a end:')       #结束页(不包括)
search=""   #可搜索特定内容下载
findXPATH='/html/body/div[7]/div/div[7]/table/tbody[2]/tr/td[2]/h3/a'  #要查找的XPATH路径，用于找到每一个帖子
imageXPATH=[                                                           #帖子内的图片XPATH
            '/html/body/div[5]/div[7]/table/tbody/tr[1]/th[2]/div[5]/div[2]/img',
            '/html/body/div[6]/div[7]/table/tbody/tr[1]/th[2]/div[5]/div[2]/img',
            '/html/body/div[7]/div/form/div/table/tbody/tr[1]/th[2]/div[6]/div[2]/img',
            '/html/body/div[6]/div[7]/table/tbody/tr[1]/th[2]/div[5]/div[2]/sub/img',
            ]
for i in range(int(start),int(end)):
    # 根据页码生成对应的链接
    if i==1: urlString=url+'XXXXXX?fid=21'
    else: urlString=url+"XXXXXX?fid=21&page="+str(i)
    # 打开对应网页
    startStage(urlString)
    print("当前为第",i,"页")
    # 创建空的用于标志进行到过第几页
    if not os.path.exists('Search/'):
        os.makedirs('Search/')
    #获取页面对应的链接信息
    titlelists = edge.find_elements(By.XPATH,findXPATH)
    #循环打开对应的详情页面
    for title in titlelists:
        #################################此处用于查找特定文本的帖子,如需要则取消注释
        # titleName=title.text
        # if not search in titleName:#不包含对应字符串则进行下次循环
        #     continue

        titleName=titleName.replace('+','').replace('.','').replace(':','').replace('?','').replace('/','')
        titleUrl=title.get_attribute("href")
        #不存在则创建，存在则跳过
        if not os.path.exists("Search/" + titleName):
            os.makedirs("Search/" + titleName)
        else:
            print("已下载: ", titleName, titleUrl)
            continue
        print("开始下载: ", titleName, titleUrl)
        title.click()#打开详情页面
        edge.switch_to.window(edge.window_handles[1])#切换到最后一个标签页

        #获取图片路径
        imgList=edge.find_elements(By.XPATH,imageXPATH[0])
        while(len(imgList)==0):#如果图片地址列表为空，则刷新页面
            edge.refresh()
            time.sleep(1)
            #路径1请求,若仍未空,则请求路径2
            for imgpath in imageXPATH:
                imgList = edge.find_elements(By.XPATH, imgpath)
                if (len(imgList)!=0):break

        count=0
        for img in imgList:
            imageUrl=img.get_attribute("src")
            image=None
            while(image==None):
                try:
                    #time.sleep(1)
                    #设置超时时间为5 如果请求超过了这个时间还没有得到响应，则会抛出Timeou错误。
                    image = requests.get(url=imageUrl, headers={'User-Agent': random.choice(ua_list)},timeout=5).content
                except Exception:
                    continue
            count = count + 1
            imagePath = "Search/" + titleName + '/' +str(count)+ '.jpeg'
            with open(imagePath,'wb') as fp:
                fp.write(image)
                print("第"+str(i)+"页 "+titleName+" 内 图片 "+str(count)+" 下载完成 图片链接 "+imageUrl)

        edge.close()
        edge.switch_to.window(edge.window_handles[0])  # 切换回原来的tab页
edge.quit()
