import cv2 as cv
import numpy as np
import gzip

#mb2 = '''<Structure name="标签 箭头 垂直 B" identifier="labelsarroverticalb" ID="{}" rect="{},{},{},{}" MaxHealth="100" CrushDepth="0" SpriteColor="{},{},{},255" UseDropShadow="False" DropShadowOffset="0,0" Scale="0.1" TextureScale="2.5999997,4.799998" TextureOffset="-12,-90" NoAITarget="False" DisallowedUpgrades="" SpriteDepth="0.85" HiddenInGame="False" />\n'''

mb2='''<Structure name="混凝土墙" identifier="Concrete_Wall_1" ID="{}" rect="{},{},{},{}" MaxHealth="100" CrushDepth="0" SpriteColor="{},{},{},255" UseDropShadow="False" DropShadowOffset="0,0" Scale="1" TextureScale="0.5,0.5" TextureOffset="0,0" NoAITarget="False" DisallowedUpgrades="" SpriteDepth="0.98" HiddenInGame="False" />'''


body='''
<Submarine description="" checkval="418639220" price="1000" tier="1" initialsuppliesspawned="false" noitems="false" lowfuel="true" type="Player" ismanuallyoutfitted="false" class="Undefined" tags="0" gameversion="1.0.8.0" dimensions="0,0" cargocapacity="0" recommendedcrewsizemin="1" recommendedcrewsizemax="2" recommendedcrewexperience="CrewExperienceLow" requiredcontentpackages="" name="{}">
{}
</Submarine>
'''

flist='''
<?xml version="1.0" encoding="utf-8"?>
<contentpackage name="A2" modversion="1.0.0" corepackage="False" gameversion="1.0.8.0">
  <Submarine file="%ModDir%/A2.sub" />
</contentpackage>
'''

def cal_same_pix(img,x,y,th):
    s = np.zeros((3),dtype=np.int32)
    for i in [-1,0,1]:
        for k in [-1,0,1]:
            s += img[x+i][y+k]
    avg = s/9
    dist = 0
    for i in [-1,0,1]:
        for k in [-1,0,1]:
            dist += sum(abs(img[x+i][y+k] - avg))/3
    if dist >= th:
        return False
    else:
        return True




def cal_same(mask_one_pix,org_img):
    for x in range(1,mask_one_pix.shape[0]-1):
        for y in range(1,mask_one_pix.shape[1]-1):
            b_mark = 0
            for i in [-1,0,1]:
                if b_mark == 1:
                    break
                for k in [-1,0,1]:
                    if mask_one_pix[x+i][y+k] == 0:
                        b_mark = 1
                        break
            if b_mark != 1:
                is_same=cal_same_pix(org_img,x,y,20)
                if is_same :
                    for i in [-1,0,1]:
                        for k in [-1,0,1]:
                            mask_one_pix[x+i][y+k] = 0
                    mask_one_pix[x][y]  = 2






def gen_zip_sub_file(img,mask,file_name,progress_calback,root):
    img = img [:,:,:3]
    ret,mask_one_pix =cv.threshold(mask,128,1,cv.THRESH_BINARY)
    cal_same(mask_one_pix,img)
    mask = mask_one_pix
    txt = ''
    id_cnt = 1
    for i in range(0,img.shape[0]):
        for k in range(0,img.shape[1]):
            c = img[i][k]
            alph = mask[i][k]
            if alph == 1:
              txt += mb2.format(id_cnt,k*16-8,-i*16+8,16,16,c[2],c[1],c[0])
              id_cnt += 1
            elif alph == 2:
                txt += mb2.format(id_cnt,k*16-8*3,-i*16+8*3,16*3,16*3,c[2],c[1],c[0])
                id_cnt += 1
            
        progress_calback['value'] = int(100*i/img.shape[0])
        root.update()

# def gen_sub_file(img,mask,file_name):
#     txt = ''
#     id_cnt = 1
#     for i in range(0,img.shape[0]):
#         for k in range(0,img.shape[1]):
#             c = img[i][k]
#             alph = mask[i][k]
#             if alph == 1:
#               txt += mb2.format(id_cnt,k,-i,1,1,c[2],c[1],c[0])
#               id_cnt += 1
#             elif alph == 2:
#                 txt += mb2.format(id_cnt,k-1,-i+1,3,3,c[2],c[1],c[0])
#                 id_cnt += 1
            

    f = open('o.html','w',encoding='utf-8')
    f.write(body.format(file_name,txt))
    f.close()

    f = open('o.html','rb')
    data =f.read()
    f.close()
    f_g = gzip.GzipFile('{}.sub'.format(file_name),'wb')
    f_g.write(data)
    f_g.close()
    
    f = open('filelist.xml','w')
    f.write(flist)
    f.close()


# org_img = cv.imdecode(np.fromfile('3.png', dtype=np.uint8),cv.IMREAD_UNCHANGED)
# x = org_img.shape[0]
# y = org_img.shape[1]
# n_x = org_img.shape[0]//5
# n_y = org_img.shape[1]//5
# org_img = cv.resize(org_img,(n_y,n_x))



# if org_img.shape[2] == 4:
#     mask = org_img[:,:,3]
# else:
#     mask = np.zeros((org_img.shape[0],org_img.shape[1]),dtype=np.uint8)+255

# org_img = org_img[:,:,0:3]
# ret,mask_one_pix =cv.threshold(mask,128,1,cv.THRESH_BINARY)




# cal_same(mask_one_pix,org_img)


# gen_sub_file(org_img,mask_one_pix,'A1')

# cv.imshow('0',mask*128)
# cv.imshow('1',mask_one_pix*128)
# cv.waitKey(0)