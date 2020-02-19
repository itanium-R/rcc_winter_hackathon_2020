# -*- coding:utf-8 -*-
import wave
import numpy as np
import scipy.io.wavfile
import scipy.signal
import pylab as P
from levinson_durbin import autocorr, LevinsonDurbin


class Identifer(object):
    def __init__(self):
        ## ----*----- コンストラクタ -----*----- ##
        self.rate = 8000


    def read_wavfile(self, file):
        ## -----*----- 音声ファイル読み込み -----*----- ##
        wf = wave.open(file, 'r')
        fs = wf.getframerate()
        x = wf.readframes(wf.getnframes())
        x = np.frombuffer(x, dtype="int16") / 32768.0  # (-1, 1)に正規化
        wf.close()
        return x, float(fs)


    def preEmphasis(self, signal, p):
        ## -----*----- プリエンファシスィルタ -----*----- ##
        # 係数 (0.97, -p) のFIRフィルタを作成
        return scipy.signal.lfilter([1.0, -p], 1, signal)

    def spectrum(self, s, a, e, fs, file):
        ## -----*----- LPC係数の振幅スペクトルを求める -----*----- ##
        fscale = np.fft.fftfreq(self.rate, d=1.0 / fs)[:self.rate // 2]
        # オリジナル信号の対数スペクトル
        spec = np.abs(np.fft.fft(s, self.rate))
        logspec = 20 * np.log10(spec)

        # LPC対数スペクトル
        w, h = scipy.signal.freqz(np.sqrt(e), a, self.rate, "whole")
        lpcspec = np.abs(h)
        loglpcspec = 20 * np.log10(lpcspec)

        # 2000~8000[Hz]のバンドパスフィルタ
        loglpcspec = loglpcspec[2000:8000]

        ret = {
            'argrelmax': scipy.signal.argrelmax(loglpcspec),
            'argrelmin': scipy.signal.argrelmin(loglpcspec),
            'max': np.amax(loglpcspec)
        }

        return ret


    def lpc_spectral_envelope(self, file):
        ## -----*----- 音声をロード -----*----- ##
        wav, fs = self.read_wavfile(file)
        t = np.arange(0.0, len(wav) / fs, 1 / fs)
        # 音声波形の中心部分を切り出す
        center = len(wav) / 2  # 中心のサンプル番号
        cuttime = 0.04  # 切り出す長さ [s]
        s = wav[int(center - cuttime / 2 * fs): int(center + cuttime / 2 * fs)]
        # プリエンファシスフィルタをかける
        p = 0.97  # プリエンファシス係数
        s = self.preEmphasis(s, p)
        # ハミング窓をかける
        hammingWindow = np.hamming(len(s))
        s = s * hammingWindow
        # LPC係数を求める
        #    lpcOrder = 12
        lpcOrder = 32
        r = autocorr(s, lpcOrder + 1)
        a, e = LevinsonDurbin(r, lpcOrder)
        return self.spectrum(s, a, e, fs, file)


if __name__ == "__main__":
    obj = Identifer()
    print(obj.lpc_spectral_envelope('tmp/source.wav'))
    print(obj.lpc_spectral_envelope('audio/フリーザ.wav'))
    exit(0)
