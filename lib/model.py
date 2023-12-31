import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.distributions.normal import Normal
import math

def huber_loss(y_true, y_pred):
    return F.huber_loss(y_pred,y_true)

def make_one_hot(vol, mask):
    lens = len(mask)
    shape = np.array(vol.shape)
    shape[1] = lens
    shape = tuple(shape)
    result = torch.zeros(shape)

    for idx, label in enumerate(mask):
        tmp = vol == label
        result[:,idx] = tmp

    return result
def euclidean(y_true, y_pred):
    sim = np.sqrt(np.sum(np.square(y_true - y_pred)))
    return sim

def class2_diceloss(y_true, y_pred, smooth=1e-5):
    #print(y_true.shape)
    N = y_true.shape[1]
    #print(N)
    y_pred_flat = y_pred.view(N,-1)
    #print(y_pred_flat.shape)
    y_true_flat = y_true.view(N,-1)
    #print(y_true_flat.shape)
    intersection = y_pred_flat * y_true_flat
    #print(intersection.shape)
    loss = 2 * (intersection.sum() + smooth) / (y_pred_flat.sum() + y_true_flat.sum() + smooth)
    loss = 1 - loss.sum()
    return 1-loss 

def diceLoss(y_true, y_pred):
    top = 2 * torch.sum(torch.mul(y_true,y_pred), dtype=float)
    bottom = torch.sum(y_true, dtype=float) + torch.sum(y_pred, dtype=float)
    bottom = torch.max(bottom,(torch.ones_like(bottom, dtype=float) * 1e-5))
    dice = torch.mean(top / bottom)
    return 1-dice

def dice_coefficient(y_true, y_pred, smooth=1e-5):
    y_true_d = np.sum(y_true*y_true)
    y_pred_d = np.sum(y_pred*y_pred)
    intersection = np.sum(y_true * y_pred)
    return (2. * intersection + smooth) / (y_true_d + y_pred_d + smooth)

#def dice_loss(vol1, vol2):
#    top = 2 * torch.sum(torch.mul(vol1, vol2), dtype=float)
#    bottom = torch.sum(vol1, dtype=float) + torch.sum(vol2, dtype=float)
#   bottom = torch.max(bottom, (torch.ones_like(bottom, dtype=float) * 1e-5))  # add epsilon.
#    loss = -1 * (top / bottom)
#    return loss

def diceLoss1(y_true, y_pred):
    top = 2 * torch.sum(torch.mul(y_true,y_pred), dtype=float)
    bottom = torch.sum(y_true, dtype=float) + torch.sum(y_pred, dtype=float)
    bottom = torch.max(bottom, (torch.ones_like(bottom, dtype=float) * 1e-5))
    dice = torch.mean(top / bottom)
    return 1-dice

def muldiceloss_1(y_true,y_pre):
    shape = y_true.shape
    print('y_true  shape',shape)
    total_loss = 0
    for i in range(shape[1]):
        dice_loss = class2_diceloss(y_true[:,i,:,:,:],y_pre[:,i,:,:,:])
        total_loss += dice_loss

    return total_loss

def dist_loss(y_true, y_pred, smooth=1e-5):
    loss = (y_true - y_pred) * (y_true - y_pred)/(y_true.shape[0] *y_true.shape[1] *y_true.shape[2] * y_true.shape[3]  * y_true.shape[4])
    return loss.sum()

def dist_loss_mul(y_true, y_pred):
    shape = y_true.shape

    # print(shape)

    total_loss = 0
    for i in range(shape[1]):
        # print (i)
        # print(y_true.shape)
        # ll = y_true[:, 1, :, :, :]
        loss = (y_true[:,i,:,:,:] - y_pred[:,i,:,:,:]) * (y_true[:,i,:,:,:] - y_pred[:,i,:,:,:])
        total_loss += loss.sum()
    total_loss = total_loss/(y_true.shape[0] *y_true.shape[1] *y_true.shape[2] * y_true.shape[3]  * y_true.shape[4])
   
    return total_loss

def color_loss(y_true,y_pred,y):
    similarity = torch.cosine_similarity(y_true, y_pred, dim=1)
    similarity[y==0]=1
    similarity=1-similarity
    return torch.sum(similarity)/(y_true.shape[0]  *y_true.shape[2] * y_true.shape[3]  * y_true.shape[4])
    #return torch.sum(similarity)/count
