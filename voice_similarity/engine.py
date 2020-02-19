# -*- coding:utf-8 -*-

import numpy as np
from sklearn.metrics import r2_score
import rwave
from lib.LPC import *


def similarity(v1, v2):
    ### -----*----- ベクトルの決定係数 -----*----- ##
    score = r2_score(v1, v2)
    if score < 0.0:
        score = 0.0

    return score ** 2


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
    RATE = 8000
    SEC  = 5

    # サンプリングレート・秒数をキャスト
    w1, w2 = rwave.read_wave(file1)[0], rwave.read_wave(file2)[0]
    if len(w1) != len(w2):
        convert_wave(file1, file1, RATE, SEC)
        convert_wave(file2, file2, RATE, SEC)

    # MFCCに変換
    mfcc1 = rwave.nomalize(rwave.to_mfcc(file1, RATE)).T
    mfcc2 = rwave.nomalize(rwave.to_mfcc(file2, RATE)).T

    scores = []
    for i in range(len(mfcc1)-1):
        re_mfcc = np.roll(mfcc1, i)
        scores.append(similarity(re_mfcc, mfcc2))
        #scores.append(cos_sim(re_mfcc.flatten(), mfcc2.flatten()))

    return max(scores)


if __name__ == '__main__':
    # 決定係数
    score = comparison('audio/孫悟空.wav', 'tmp/source.wav')
    print(score)

    # LPC分析
    extractor = Identifer()
    lpc1 = extractor.lpc_spectral_envelope('audio/フリーザ.wav')
    lpc2 = extractor.lpc_spectral_envelope('tmp/source.wav')
    v1 = lpc1['argrelmax']
    v2 = lpc2['argrelmax']
    n = min(len(v1), len(v2))
    v1, v2 = v1[:n], v2[:n]
    print(cos_sim(v1, v2))
