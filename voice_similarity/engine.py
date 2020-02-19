# -*- coding:utf-8 -*-

import numpy as np
from sklearn.metrics import r2_score
import rwave


def similarity(v1, v2):
    ### -----*----- ベクトルの類似度 -----*----- ##
    score = r2_score(v1, v2)
    if score < 0.0:
        score = 0.0

    return score ** 2


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
