import datetime
#神经网络
from torch.utils.data import DataLoader
import torchvision
import torchvision.transforms as transforms
import torch
import torch.optim as optim
import torch.nn.functional as F
from torch.autograd import Variable

#from cv2 import cv2
from PIL import Image

import net.MobileNetV2 as net
import numpy as np

transform = transforms.Compose([
transforms.Resize([224,224], interpolation=2),
transforms.ToTensor(),
transforms.Normalize((0.56719673,0.5293289,0.48351972),(0.20874391,0.21455203,0.22451781))
])

idx_to_class = ["有害垃圾","厨余垃圾","其他垃圾","可回收垃圾"]

def print_time():
    now = datetime.datetime.now()
    print ("当前系统日期和时间是: ")
    print (now.strftime("%Y-%m-%d %H:%M:%S"))


def classify():
    print('\nStarting to classify garbage!')
    print_time()
    print("\n")
    data = Image.open("photo.jpg")
    data_in = transform(data).unsqueeze(0)
    """
    #print(data.shape)
    data =np.transpose(data, (2, 0, 1))
    #print(data.shape)
    data = data[np.newaxis,:,:,:]
    #print(data.shape)
    data_in = torch.from_numpy(data).float()
    #print(data_in.shape)
    """

    #model = torch.load('model.pkl')
    model = torch.load('mobile_net_v2_4_v1_83_n3.pkl', map_location='cpu')
    model.eval()
    #print(model)
    

    out = model(data_in)                                                    #log概率：out               类型tensor
    out_p = torch.exp(out)                                                  #概率：out_p                类型tensor
    #print(out_p)
    top_p, top_class = out_p.topk(1, dim=1)                                 #最大分数：top_p            类型tensor #最大可能类别：top_class 类型tensor
    Prediction = idx_to_class[int(top_class.detach().numpy()[0][0])]        #最大可能类别：Prediction   类型numpy
    score = top_p.detach().numpy()[0][0]                                    #最大分数：score            类型numpy
    print("Prediction : ", Prediction,"Score: ", score )
    #pre = out.argmax(dim=1)
    #print(top_p)
    print('\nClassification complete!')
    print_time()
    return (top_class.numpy()[0][0],Prediction,score)
    

if __name__ == '__main__':
    classify()