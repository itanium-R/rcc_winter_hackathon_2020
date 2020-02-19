# -*- coding:utf-8 -*-

import numpy as np
import rwave


def cos_sim(v1, v2):
    ### -----*----- ベクトル間のコサイン類似度 -----*----- ##
    sim = []
    for i in range(len(v1)):
        sim.append(np.dot(v1[i], v2[i]) / (np.linalg.norm(v1[i]) * np.linalg.norm(v2[i])))

    return sum(sim) / len(sim)


rate = 8000
mfcc1 = rwave.to_mfcc('tmp/1.wav', rate)
mfcc2 = rwave.to_mfcc('tmp/2.wav', rate)

print(cos_sim(mfcc1, mfcc2))
