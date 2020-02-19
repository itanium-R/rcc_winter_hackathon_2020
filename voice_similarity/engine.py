# -*- coding:utf-8 -*-

import numpy as np
from sklearn.metrics import r2_score
import rwave
import math
from lib.LPC import *


def similarity(v1, v2):
    ### -----*----- ベクトルの決定係数 -----*----- ##
    score = r2_score(v1, v2)
    if score < 0.0:
        score = 0.0

    return score


def cos_sim(v1, v2):
    ## -----*----- ベクトルのコサイン類似度 -----*----- ##
    if len(v1)==0 or len(v2)==0:
        return 0.0
    score = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))

    return score


def convert_wave(ori_file, to_file, fs, sec):
    ## -----*----- 音声ファイルのサンプリングレート・時間を変換 -----*----- ##
    # ori_file：変換対象のファイルパス
    # to_file ：変換後のファイルパス

    wave, rate = rwave.read_wave(ori_file)
    wave, _    = rwave.convert_fs(wave, rate, fs)
    wave, _    = rwave.convert_sec(wave, rate, sec)

    rwave.write_wave(to_file, wave, fs)


def comparison(file1, file2):
    ## -----*----- 類似度を算出 -----*----- ##
    score = {'mfcc': 0.0, 'lpc': 0.0}
    RATE = 8000

    # サンプリングレート・秒数をキャスト
    w1, fs = rwave.read_wave(file1)
    w2, _  = rwave.read_wave(file2)
    sec = len(w1) / fs # 秒数
    if len(w1) != len(w2):
        convert_wave(file1, file1, RATE, sec)
        convert_wave(file2, file2, RATE, sec)

    ## ===== MFCCで比較 ====================================
    # MFCCに変換
    mfcc1 = rwave.nomalize(rwave.to_mfcc(file1, RATE)).T
    mfcc2 = rwave.nomalize(rwave.to_mfcc(file2, RATE)).T

    scores = []
    score['mfcc'] = 1.0
    for i in range(len(mfcc1)-1):
        re_mfcc = np.roll(mfcc1, i)
        scores.append(similarity(re_mfcc.T, mfcc2.T))
    for i in range(len(mfcc1.T)-1):
        re_mfcc = np.roll(mfcc1.T, i)
        score['mfcc'] *= cos_sim(re_mfcc.flatten(), mfcc2.flatten())
    score['mfcc'] = (score['mfcc'] + max(scores)) / 2


    ## ===== LPC分析 ====================================
    extractor = Identifer()
    lpc1 = extractor.lpc_spectral_envelope(file1)
    lpc2 = extractor.lpc_spectral_envelope(file2)
    v1 = np.append(lpc1['max'], lpc1['argrelmax']),\
         np.append(lpc1['min'], lpc1['argrelmin'])
    v2 = np.append(lpc2['max'], lpc2['argrelmax']),\
         np.append(lpc2['min'], lpc2['argrelmin'])

    n_max = min(len(v1[0]), len(v2[0]))
    n_min = min(len(v1[1]), len(v2[1]))
    v1_max, v2_max = v1[0][:n_max], v2[0][:n_max]
    v1_min, v2_min = v1[1][:n_min], v2[1][:n_min]
    score['lpc'] = cos_sim(v1_max, v2_max) * cos_sim(v1_min, v2_min)
    score['lpc'] = score['lpc'] ** 5

    ret = (score['mfcc'] * score['lpc']) * 3
    ret = 1 / (1 + e**-ret)
    if ret > 0.75:
        ret += np.random.rand() / 10.0
    elif ret > 0.7:
        pass
    else:
        ret *= np.random.rand()

    return score, ret


if  __name__ == '__main__':
    # 決定係数
    score = comparison('audio/フリーザ.wav', 'tmp/source.wav')
    print(comparison('audio/フリーザ.wav', 'tmp/a.wav'))
    print(score)
