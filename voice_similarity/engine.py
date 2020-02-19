# -*- coding:utf-8 -*-

import numpy as np
import rwave


def cos_sim(v1, v2):
    ### -----*----- ベクトル間のコサイン類似度 -----*----- ##
    v1 = v1.flatten()
    v2 = v2.flatten()

    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))


def convert_wave(ori_file, to_file, fs, sec):
    ## -----*----- 音声ファイルのサンプリングレート・時間を変換 -----*----- ##
    # ori_file：変換対象のファイルパス
    # to_file ：変換後のファイルパス

    wave, rate = rwave.read_wave(ori_file)
    wave, _    = rwave.convert_fs(wave, rate, fs)
    wave, _    = rwave.convert_sec(wave, rate, sec)

    rwave.write_wave(to_file, wave, fs)


rate = 8000
mfcc1 = rwave.to_mfcc('tmp/1.wav', rate)
mfcc2 = rwave.to_mfcc('tmp/2.wav', rate)

print(cos_sim(mfcc1, mfcc2))
