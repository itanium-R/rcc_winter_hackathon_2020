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
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))


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
    convert_wave(file1, file1, RATE, SEC)
    convert_wave(file2, file2, RATE, SEC)
    # MFCCに変換
    mfcc1 = rwave.to_mfcc(file1, RATE)
    mfcc2 = rwave.to_mfcc(file2, RATE)

    return similarity(mfcc1, mfcc2)


if __name__ == '__main__':
    # 決定係数
    #score = comparison('audio/孫悟空.wav', 'tmp/source.wav')
    #print(score)

    # LPC分析
    extractor = Identifer()
    lpc1 = extractor.lpc_spectral_envelope('audio/フリーザ.wav')
    lpc2 = extractor.lpc_spectral_envelope('tmp/source.wav')
    v1 = lpc1['lpc']
    v2 = lpc2['lpc']
    n = min(len(v1), len(v2))
    v1, v2 = v1[:n], v2[:n]
    print(v1)
    print(v2)
    print(similarity(v1, v2))
