import sys, fitz
import os
import matplotlib.pyplot as plt
from matplotlib.pyplot import MultipleLocator
# import tecplot
import pandas as pd
import numpy as np

def get_dir(path):
    if os.path.isdir(path):
        path = path
    elif os.path.isfile(path):
        path = os.path.split(path)[0]
    else:
        path = os.getcwd()
    return path

def mcr(path, nums, scale):
    for i in nums:
        num = str(i)
        num = num.zfill(3)

        mcr = r'''#!MC 1410
$!VarSet |MFBD| = ''' + "'" + path + "'" + r'''
$!READDATASET  '"|MFBD|\field''' + num + r'''.dat" "|MFBD|\front''' + num + r'''.dat" '
  READDATAOPTION = NEW
  RESETSTYLE = YES
  VARLOADMODE = BYNAME
  ASSIGNSTRANDIDS = YES
  VARNAMELIST = '"X" "Y" "U" "V" "F" "P" "temp"'
$!GLOBALRGB REDCHANNELVAR = 3
$!GLOBALRGB GREENCHANNELVAR = 3
$!GLOBALRGB BLUECHANNELVAR = 3

$!ALTERDATA 
  EQUATION = '{uv}=sqrt({u}**2+{v}**2)'

$!SETCONTOURVAR 
  VAR = 7
  CONTOURGROUP = 1
  LEVELINITMODE = RESETTONICE

$!CONTOURLEVELS NEW
  CONTOURGROUP = 1
  RAWDATA
'''
        mcr += str(scale.shape[0]) + '\n'
        for j in scale:
            mcr += str(j) + '\n'
        mcr += '''
$!TWODAXIS YDETAIL{SHOWAXIS = NO}
$!TWODAXIS XDETAIL{SHOWAXIS = NO}

$!FIELDLAYERS SHOWCONTOUR = YES
$!FIELDMAP [1]  CONTOUR{CONTOURTYPE = FLOOD}

$!FIELDLAYERS SHOWMESH = YES
$!FIELDMAP [1]  MESH{SHOW = NO}
$!FIELDMAP [2]  MESH{COLOR = WHITE}
$!FIELDMAP [2]  MESH{LINETHICKNESS = 0.40000000000000001}

$!GLOBALTWODVECTOR UVAR = 3
$!GLOBALTWODVECTOR VVAR = 4
$!RESETVECTORLENGTH 
$!FIELDLAYERS SHOWVECTOR = YES
$!FIELDMAP [1]  VECTOR{COLOR = BLACK}
$!FIELDMAP [1]  VECTOR{LINETHICKNESS = 0.40000000000000001}
$!FIELDMAP [1]  POINTS{IJKSKIP{I = 5}}
$!FIELDMAP [1]  POINTS{IJKSKIP{J = 10}}

$!GLOBALCONTOUR 1  LEGEND{BOX{BOXTYPE = NONE}}
$!GLOBALCONTOUR 1  LEGEND{NUMBERTEXTSHAPE{FONTFAMILY = 'Times New Roman'}}
$!GLOBALCONTOUR 1  LEGEND{HEADERTEXTSHAPE{FONTFAMILY = 'Times New Roman'}}
$!GLOBALCONTOUR 1  LABELS{NUMFORMAT{FORMATTING = FIXEDFLOAT}}
$!GLOBALCONTOUR 1  LABELS{NUMFORMAT{PRECISION = 2}}
$!GLOBALCONTOUR 1  LABELS{NUMFORMAT{TIMEDATEFORMAT = ''}}
$!GLOBALCONTOUR 1  LABELS{NUMFORMAT{POSITIVEPREFIX = ''}}
$!GLOBALCONTOUR 1  LABELS{NUMFORMAT{POSITIVESUFFIX = ''}}
$!GLOBALCONTOUR 1  LABELS{NUMFORMAT{ZEROPREFIX = ''}}
$!GLOBALCONTOUR 1  LABELS{NUMFORMAT{ZEROSUFFIX = ''}}
$!GLOBALCONTOUR 1  LABELS{NUMFORMAT{NEGATIVEPREFIX = ''}}
$!GLOBALCONTOUR 1  LABELS{NUMFORMAT{NEGATIVESUFFIX = ''}}
$!GLOBALCONTOUR 1  LABELS{AUTOLEVELSKIP = 2}

$!PRINT 
$!RemoveVar |MFBD|
'''
        with open("temp.mcr", 'w') as f:
            f.write(mcr)
        os.system("tec360.exe -b -p temp.mcr")

def PDF_fitz(Path):
    # filepath, fullflname = os.path.split(pdfPath)
    # fname, ext = os.path.splitext(fullflname)
    # pdfDoc = fitz.open(pdfPath)

    for root, dirs, pdffiles in os.walk(Path):
        for i in pdffiles:
            pdfPath = os.path.join(Path, i)
            pdfDoc = fitz.open(pdfPath)
            # pdfDoc.save(filepath + '/' + fname + '_backup.pdf')
            for pg in range(pdfDoc.pageCount):
                page = pdfDoc[pg]
                zoom = 20
                rotate = int(0); zoom_x = zoom; zoom_y = zoom
                mat = fitz.Matrix(zoom_x, zoom_y).preRotate(rotate)
                rect = page.rect
                h = rect.br[1] - rect.tl[1]
                w = rect.br[0] - rect.tl[0]
                clip = fitz.Rect(0.195*w, 0.14*h, 0.48*w, 0.87*h)                 # fig
                # clip = fitz.Rect(155, 86, 379, 532)  # fig
                pix = page.getPixmap(matrix=mat, alpha=False, clip=clip)
                # if not os.path.exists(filepath):
                #     os.makedirs(filepath)
                fname, ext = os.path.splitext(i)
                pix.writeImage(Path + '/' + str(fname) + '.png', output="png")

def get_data(file, column1, column2):
    x, y = [],[]
    # with open(file,'r') as f:
    #     lines = f.readlines()
    #     for line in lines:
    #         value = [float(s) for s in line.split()]
    #         x.append(value[column1])
    #         y.append(value[column2])
    #     print("data import succeed")

    # cvs_data = pd.read_csv(file)
    # print(cvs_data.shape)

    data = np.loadtxt(file)
    x = data[:,column1]
    y = data[:,column2]
    print("data import succeed")
    return x, y

def plot(x, y):

    plt.rcParams['xtick.direction'] = 'in'
    plt.rcParams['ytick.direction'] = 'in'
    plt.rcParams["font.family"] = "Times New Roman"
    plt.rcParams['font.size'] = '14'

    #fig, ax = plt.subplots(figsize=(12, 6))

    x_major_locator = MultipleLocator(10)
    y_major_locator = MultipleLocator(0.1)
    bwith = 2  # 边框宽度设置为2
    ax = plt.gca()
    # ax.spines['top'].set_color('black')
    # ax.spines['right'].set_color('black')
    ax.spines['bottom'].set_linewidth(bwith)
    ax.spines['left'].set_linewidth(bwith)
    ax.spines['top'].set_linewidth(bwith)
    ax.spines['right'].set_linewidth(bwith)
    ax.xaxis.set_major_locator(x_major_locator)
    ax.yaxis.set_major_locator(y_major_locator)

    # plt.title('title')
    plt.xlabel('$\omega*$')
    plt.ylabel('$v*$')
    plt.xlim(0, 30)
    plt.ylim(0.01, 0.3)                        # plt.axis([0,10,0,100])
    plt.minorticks_on()
    plt.tick_params(which='major', width=2, length=3)

    # plt.xticks([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    # # 第一个参数是点的位置，第二个参数是点的文字提示。
    # plt.yticks([0, 20, 60, 80, 100],
    #            [r'$really\ bad$', r'$bad$', r'$normal$', r'$good$', r'$readly\ good$'])
    # # $表示特殊的字体，这边如果后期有需要可以上网查，空格需要转译，数学alpha可以用\来实现

    plt.plot(x, y, '.', linewidth=2)
    plt.show()

    print("plot finish")

if __name__ == '__main__':
    path = get_dir(r"E:\Study\Focus\paper\sinT\sinInit\verity")
    mcr(path, [1, 21, 41, 61, 81, 101], np.arange(-80, 80, 4))
    PDF_fitz(r"E:\Desktop\sciplot.py\pdf")

    # x, y = get_data(os.path.join(path,"stats_front.dat"), 1, 2)
    # plot(x, y)












# def tecplot_data(data_dir, file):
#
#     tecplot.session.connect()
#     examples_dir = tecplot.session.tecplot_examples_directory()
#     datafile = os.path.join(examples_dir, data_dir, file)
#     dataset = tecplot.data.load_tecplot(datafile)
#
#     frame = tecplot.active_frame()
#     frame.plot_type = tecplot.constant.PlotType.Cartesian2D
#     frame.plot().show_contour = True
