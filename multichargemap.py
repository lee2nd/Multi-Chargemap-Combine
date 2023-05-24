import glob
import numpy as np
import matplotlib.pyplot as plt

def process_charge_file(map_source_path):
  
    file_path = map_source_path
    token = file_path.split('.')
    
    if token[-1][:2] == "f1" : 
      
        in_f100p_a = np.fromfile(file_path,np.uint8)
        len_aa=len(in_f100p_a)
        in_f100p_o = in_f100p_a[0::2]
        in_f100p_e = in_f100p_a[1::2]
        out_f100p_a = 256*in_f100p_o + 1*in_f100p_e
        data = out_f100p_a.copy()

        if len_aa >= 1656*312*2 and len_aa < 1656*313*2:  ##先用此界線分L6K 72*1656 或  L6B 312*1656 , 或許未來會再多幾種
          
            W=1656
            H=312
            if token[-1]=='f100p':
                C=0.24416883
            if token[-1]=='f10p':
                C=0.024416883
            if token[-1]=='f1p':
                C=0.0024416883
            if token[-1]=='f1000p':
                C=2.4416883
            data=data[5:516677]*C
            
        if len_aa >= 1440*270*2 and len_aa < 1440*271*2:  ##先用此界線分L6K 72*1656 或  L6B 312*1656 , 或許未來會再多幾種
          
            W=1440
            H=270
            if token[-1]=='f1000p':
                C=2.4417
            if token[-1]=='f100p':
                C=0.2442
            if token[-1]=='f10p':
                C=0.024416883
            if token[-1]=='f1p':
                C=0.0024416883
            data=data[4:388804]*C
            
        if len_aa >= 1656*72*2 and len_aa < 1656*73*2:   ##先用此界線分L6K 72*1656 或  L6B 312*1656 , 或許未來會再多幾種
          
            W=1656
            H=72
            if token[-1]=='f100p':
                C=0.2439715
            if token[-1]=='f10p':
                C=0.02439715
            if token[-1]=='f1p':
                C=0.002439715
            if token[-1]=='f1000p':
                C=2.439715
            data=data[5:119237]*C
        out_f100p_d=np.around(data,1)                 
        out_f100p_2d=np.reshape(data,(H,W))
        out_f100p_1d=np.array(data).flatten().tolist()
    
    return out_f100p_2d

chip_lst = ["970212",
            "970145",
            "9697B6",
            "9699L5",
            "9702H5",
            "970131",
            "970213",
            "9701A5"]

color_lst = ["Reds","Greens","Blues"]

step_lst = ["Step1_Step2",
            "Step3_Step4",
            "Step5_Step6",
            "Step7_Step8",
            "Step9_Step10",
            "Step11_Step12",
            "Step15_Step16"]

# 生成一個 2x4 的 subplot，figsize 可以調整整個圖的大小
fig, axs = plt.subplots(4, 2)

for step in step_lst:
    
    for color in color_lst:

        if color == "Reds":
            st = 0
        elif color == "Greens":
            st = 1
        elif color == "Blues":
            st = 2  

        for i, ax in enumerate(axs.flat):
            
            chip = chip_lst[i]

            try:
                file_path = glob.glob(f"/AMF/data/Target/SW_AT/{chip}/*{step}*p")

                output_2d = process_charge_file(file_path[0])
                output_2d = output_2d[:,st::3]

                ax.imshow(output_2d, cmap=color)
                ax.set_title(chip)
                ax.set_xticks([])
                ax.set_yticks([])        
                
            except:
                ax.set_title(chip)
                ax.set_xticks([])
                ax.set_yticks([])          
                continue   

        ax.set_aspect('equal')

        # 調整 subplot 之間的距離和邊界
        fig.tight_layout()
        
        print(f"plot_{step}_{color}")
        plt.savefig(f"plot_{step}_{color}.png") 
