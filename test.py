import torch
import cv2
import matplotlib
import matplotlib.pyplot as plt
from src.Models import Unet
import json

matplotlib.rcParams['font.family'] = 'Malgun Gothic'
matplotlib.rcParams['font.size'] = 15
matplotlib.rcParams['axes.unicode_minus'] = False

def run(n):
    labels = ['긁힌 영역', '이격된 영역', '찌그러진 영역', '파손된 영역']
    models = []

    n_classes = 2
    device = 'cuda' if torch.cuda.is_available() else 'cpu'

    for label in labels:
        model_path = f'models/[{label}]Unet.pt'

        model = Unet(encoder='resnet34', pre_weight='imagenet', num_classes=n_classes).to(device)
        model.model.load_state_dict(torch.load(model_path, map_location=torch.device(device)))
        model.eval()

        models.append(model)

    img_path = 'static/images/original.png'

    outputs = []

    for i, model in enumerate(models):

        img_path = 'static/images/original.png'

        img = cv2.imread(img_path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, (256, 256))

        img_input = img / 255.
        img_input = img_input.transpose([2, 0, 1])
        img_input = torch.tensor(img_input).float().to(device)
        img_input = img_input.unsqueeze(0)

        output = model(img_input)

        img_output = torch.argmax(output, dim=1).detach().cpu().numpy()
        img_output = img_output.transpose([1, 2, 0])

        outputs.append(img_output)

        plt.imshow(img.astype('uint8'), alpha=0.5)
        plt.imshow(img_output, cmap='jet', alpha=0.5)
        plt.gca().axes.xaxis.set_visible(False)
        plt.gca().axes.yaxis.set_visible(False)
        plt.savefig(f'static/images/{i}_image.png', transparent = True, bbox_inches = 'tight', pad_inches = 0)
        plt.clf()

    price_table = [
        100, # 긁힘
        120, # 이격
        220, # 찌그러짐
        200, # 파손
    ]

    line = n
    if line == 0:
        for i in range(4):
            price_table[i] -= 20
    elif line == 1:
        for i in range(4):
            price_table[i] -= 10
    elif line == 2:
        pass
    elif line == 3:
        for i in range(4):
            price_table[i] += 20
    
    total = 0
    total_price = 0

    all_price = dict()

    scratch = dict()
    seperation = dict()
    crush = dict()
    damage = dict()

    for i, price in enumerate(price_table):

        if labels[i] == '긁힌 영역':
            area = outputs[i].sum()
            total = 0
            total += area * price
            total_price += total

            scratch["area"] = str(area)
            scratch["price"] = str(total)
            all_price["scratched"] = scratch
            
        elif labels[i] == '이격된 영역':
            area = outputs[i].sum()
            total = 0
            total += area * price
            total_price += total

            seperation["area"] = str(area)
            seperation["price"] = str(total)
            all_price["seperationed"] = seperation

        elif labels[i] == '찌그러진 영역':
            area = outputs[i].sum()
            total = 0
            total += area * price
            total_price += total

            crush["area"] = str(area)
            crush["price"] = str(total)
            all_price["crushed"] = crush

        elif labels[i] == '파손된 영역':
            area = outputs[i].sum()
            total = 0
            total += area * price
            total_price += total

            damage["area"] = str(area)
            damage["price"] = str(total)
            all_price["damaged"] = damage
        
    all_price["total_price"] = str(total_price)
    
    with open('static/images/printed.json', 'w', encoding='utf-8') as make_file:
        json.dump(all_price, make_file, indent='\t')