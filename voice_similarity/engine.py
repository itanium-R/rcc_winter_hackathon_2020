# -*- coding:utf-8 -*-

import numpy as np
from sklearn.metrics import r2_score
import rwave


def similarity(v1, v2):
    ### -----*----- ベクトルの類似度 -----*----- ##
    return r2_score(v1, v2)


def convert_wave(ori_file, to_file, fs, sec):
    ## -----*----- 音声ファイルのサンプリングレート・時間を変換 -----*----- ##
    # ori_file：変換対象のファイルパス
    # to_file ：変換後のファイルパス

    wave, rate = rwave.read_wave(ori_file)
    wave, _    = rwave.convert_fs(wave, rate, fs)
    wave, _    = rwave.convert_sec(wave, rate, sec)

    rwave.write_wave(to_file, wave, fs)


RATE = 8000
SEC  = 5

# サンプリングレート・秒数をキャスト
convert_wave('tmp/1.wav', 'tmp/1.wav', RATE, SEC)
convert_wave('tmp/2.wav', 'tmp/2.wav', RATE, SEC)
# MFCCに変換
mfcc1 = rwave.to_mfcc('tmp/1.wav', RATE)
mfcc2 = rwave.to_mfcc('tmp/2.wav', RATE)

print(similarity(mfcc1, mfcc2))
