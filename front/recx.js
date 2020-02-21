// cf)https://qiita.com/optimisuke/items/f1434d4a46afd667adc6
// ブラウザで録音してwavで保存 by @optimisuke (2019年06月09日)
// cf2) https://cryptic-falls-47489.herokuapp.com/
let isRecording = false;
let micIcon = document.querySelector("#micIcon");
let pBar = document.querySelector("#pBar");
let pBarInterb = null;
let pBarWidth = 0;
function animatePBar() {
  if (micIcon) micIcon.src = "img/mic_active.png";
  pBarWidth = 0;
  pBarInterb = setInterval(() => {
    pBar.style.width = pBarWidth + "%";
    pBarWidth += 1;
    if (pBarWidth > 100) {
      clearInterval(pBarInterb);
      if (micIcon) micIcon.src = "img/mic.png";
      initPBar();
    }
  }, recTime / 100);
}

function initPBar() {
  pBarWidth = 0;
  pBar.style.width = pBarWidth + "%";
}

let recTime = 2000;
// ------------------------------------------------
let localMediaStream = null;
let localScriptProcessor = null;
let audioSampleRate = null;
let audioContext = null;
let bufferSize = 1024;
let audioData = []; // 録音データ

// 録音バッファ作成（録音中自動で繰り返し呼び出される）
function onAudioProcess(e) {
  if (!isRecording) return;
  console.log('onAudioProcess');

  // 音声のバッファを作成
  let input = e.inputBuffer.getChannelData(0);
  let bufferData = new Float32Array(bufferSize);
  for (let i = 0; i < bufferSize; i++) {
    bufferData[i] = input[i];
  }
  audioData.push(bufferData);
}

// 解析開始
function startRec(evt_stream) {
  if (isRecording) return -1;
  console.log('startRecording');
  isRecording = true;
  audioContext = null;
  localMediaStream = null;
  localScriptProcessor = null;
  audioData = [];

  // 取得されている音声ストリームの録音を開始
  localMediaStream = evt_stream;

  if (!navigator || !navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
    alert('Missing support for navigator.mediaDevices.getUserMedia') // temp: helps when testing for strange issues on ios/safari
    return
  }

  audioContext = new (window.AudioContext || window.webkitAudioContext)();
  // サンプルレートを保持しておく
  audioSampleRate = audioContext.sampleRate;

  let scriptProcessor = audioContext.createScriptProcessor(bufferSize, 1, 1);
  localScriptProcessor = scriptProcessor;

  if (audioContext.createMediaStreamDestination) {
    destinationNode = audioContext.createMediaStreamDestination();
  }
  else {
    destinationNode = audioContext.destination;
  }


  // safariで Web Audio APIを動かすため、先にaudioContextを生成し、UserMediaを生成する
  return navigator.mediaDevices.getUserMedia({ audio: true })
    .then((stream) => {
      this._startRecordingWithStream(stream, destinationNode, scriptProcessor);
      setTimeout(endRecording, recTime);
    })
    .catch((error) => {
      alert('Error with getUserMedia: \n' + error.message);
    });

}

function _startRecordingWithStream(stream, destinationNode, scriptProcessor) {
  // ループ処理のセット
  let mediastreamsource = audioContext.createMediaStreamSource(stream);
  mediastreamsource.connect(scriptProcessor);
  scriptProcessor.onaudioprocess = onAudioProcess;
  console.log('startRecording scriptProcessor.connect(audioContext.destination)');
  scriptProcessor.connect(destinationNode);
}

// 解析終了
function endRecording() {
  isRecording = false;

  // 録音できたので録音データをwavにしてinputに配置＆再生ボタンに登録
  let blob = exportWAV(audioData);

  // base64加工
  let reader = new FileReader();
  reader.readAsDataURL(blob);
  reader.onloadend = function () {
    base64data = reader.result;
    console.log(base64data);
  };

  let myURL = window.URL || window.webkitURL;
  let url = myURL.createObjectURL(blob);

  // audioタグに録音データをセット
  let player = document.getElementById('player');
  player.src = url;
  player.load();

  // audioDataをクリア
  localMediaStream = null;
  localScriptProcessor = null;
  audioContext.close()
  audioContext = null;
  audioData = []; // 録音データ
}

function exportWAV(audioData) {

  let encodeWAV = function (samples, sampleRate) {
    let buffer = new ArrayBuffer(44 + samples.length * 2);
    let view = new DataView(buffer);

    let writeString = function (view, offset, string) {
      for (let i = 0; i < string.length; i++) {
        view.setUint8(offset + i, string.charCodeAt(i));
      }
    };

    let floatTo16BitPCM = function (output, offset, input) {
      for (let i = 0; i < input.length; i++ , offset += 2) {
        let s = Math.max(-1, Math.min(1, input[i]));
        output.setInt16(offset, s < 0 ? s * 0x8000 : s * 0x7FFF, true);
      }
    };

    writeString(view, 0, 'RIFF');  // RIFFヘッダ
    view.setUint32(4, 32 + samples.length * 2, true); // これ以降のファイルサイズ
    writeString(view, 8, 'WAVE'); // WAVEヘッダ
    writeString(view, 12, 'fmt '); // fmtチャンク
    view.setUint32(16, 16, true); // fmtチャンクのバイト数
    view.setUint16(20, 1, true); // フォーマットID
    view.setUint16(22, 1, true); // チャンネル数
    view.setUint32(24, sampleRate, true); // サンプリングレート
    view.setUint32(28, sampleRate * 2, true); // データ速度
    view.setUint16(32, 2, true); // ブロックサイズ
    view.setUint16(34, 16, true); // サンプルあたりのビット数
    writeString(view, 36, 'data'); // dataチャンク
    view.setUint32(40, samples.length * 2, true); // 波形データのバイト数
    floatTo16BitPCM(view, 44, samples); // 波形データ

    return view;
  };

  let mergeBuffers = function (audioData) {
    let sampleLength = 0;
    for (let i = 0; i < audioData.length; i++) {
      sampleLength += audioData[i].length;
    }
    let samples = new Float32Array(sampleLength);
    let sampleIdx = 0;
    for (let i = 0; i < audioData.length; i++) {
      for (let j = 0; j < audioData[i].length; j++) {
        samples[sampleIdx] = audioData[i][j];
        sampleIdx++;
      }
    }
    return samples;
  };

  let dataview = encodeWAV(mergeBuffers(audioData), audioSampleRate);
  let audioBlob = new Blob([dataview], { type: 'audio/wav' });

  return audioBlob;
}
