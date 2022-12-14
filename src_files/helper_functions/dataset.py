"""
car type classification dataset
"""
#from ast import main
import os
#import pdb
#from tkinter.tix import MAIN
from PIL import Image
from torch.utils.data import Dataset
import torchvision.transforms as transforms


image_path = {}
image_label = {}


def get_transform(resize, phase='train'):
    if phase == 'train':
        return transforms.Compose([
            transforms.Resize(size=(int(resize[0] / 0.875), int(resize[1] / 0.875))),
            transforms.RandomCrop(resize),
            transforms.RandomHorizontalFlip(0.5),
            transforms.ColorJitter(brightness=0.126, saturation=0.5),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])
    else:
        return transforms.Compose([
            transforms.Resize(size=(int(resize[0] / 0.875), int(resize[1] / 0.875))),
            transforms.CenterCrop(resize),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])


class CarTypeDataset(Dataset):
    def __init__(self, phase='train', resize=500):
        assert phase in ['train', 'val', 'test']
        self.phase = phase
        self.resize = resize
        self.image_id = []
        self.num_classes = 9
        if self.phase in ['train', 'val']:
            self.data_path = './CarType_train'
        else:
            self.data_path = './CarType_test'

        # get image path from images.txt
        with open(os.path.join(self.data_path, 'images.txt')) as f:
            for line in f.readlines():
                id, path = line.strip().split(' ')
                image_path[id] = path

        # get image label from image_class_labels.txt
        with open(os.path.join(self.data_path, 'image_class_labels.txt')) as f:
            for line in f.readlines():
                id, label = line.strip().split(' ')
                image_label[id] = int(label)

        # get train/test image id from train_test_split.txt
        with open(os.path.join(self.data_path, 'train_test_split.txt')) as f:
            for line in f.readlines():
                image_id, is_training_image = line.strip().split(' ')
                is_training_image = int(is_training_image)

                if self.phase == 'train' and is_training_image:
                    self.image_id.append(image_id)
                if self.phase in ('val', 'test') and not is_training_image:
                    self.image_id.append(image_id)

        # transform
        self.transform = get_transform(self.resize, self.phase)

    def __getitem__(self, item):
        # get image id
        image_id = self.image_id[item]

        # image
        image = Image.open(os.path.join(self.data_path, 'images', image_path[image_id])).convert('RGB') # (C, H, W)
        image = self.transform(image) # ????????????

        # return image and label
        return image, image_label[image_id] # count begin from 0

    def __len__(self):
        return len(self.image_id)

    def get_all_image_path(self):
        all_image_path = []
        for i in range(len(self.image_id)):
            all_image_path.append(image_path[self.image_id[i]])
        return all_image_path


if __name__ == '__main__':
    cartype_dataset = CarTypeDataset('train', (448, 448))
    print(len(cartype_dataset))
    for i in range(0, 10):
        image, label = cartype_dataset[i]
        print(image.shape, label)