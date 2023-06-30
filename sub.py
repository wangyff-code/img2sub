import gzip




mb2 = '''<Structure name="标签 箭头 垂直 B" identifier="labelsarroverticalb" ID="{}" rect="{},{},4,4" MaxHealth="100" CrushDepth="0" SpriteColor="{},{},{},255" UseDropShadow="False" DropShadowOffset="0,0" Scale="0.1" TextureScale="2.5999997,4.799998" TextureOffset="-12,-90" NoAITarget="False" DisallowedUpgrades="" SpriteDepth="0.85" HiddenInGame="False" />\n'''


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


def gen_sub_file(img,mask,file_name,progress_calback,root):
    txt = ''
    id_cnt = 1
    for i in range(0,img.shape[0]):
        for k in range(0,img.shape[1]):
            c = img[i][k]
            alph = mask[i][k]
            if alph > 128:
              txt += mb2.format(id_cnt,k*1,-i*1,c[2],c[1],c[0])
              id_cnt += 1
            progress_calback['value'] = int(100*i/img.shape[0])
            root.update()

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

