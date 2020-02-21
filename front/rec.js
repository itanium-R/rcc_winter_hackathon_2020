// cf)https://qiita.com/optimisuke/items/f1434d4a46afd667adc6
// ブラウザで録音してwavで保存 by @optimisuke (2019年06月09日)
let isRecording = false;
let micIcon = document.querySelector("#micIcon");
let pBar = document.querySelector("#pBar");
let pBarInterb = null;
let pBarWidth = 0;

// for audio
let audio_sample_rate = null;
let scriptProcessor = null;
let audioContext = null;
let recTime = 2000;
let stream;

// audio data
let audioData = [];
let bufferSize = 1024;

let saveAudio = function () {
  isRecording = false;
  url = exportWAV(audioData);
  audioContext.close();

  if (micIcon) micIcon.src = "img/mic.png";
};

// export WAV from audio float data
let exportWAV = function (audioData) {
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
        output.setInt16(offset, s < 0 ? s * 0x8000 : s * 0x7fff, true);
      }
    };

    writeString(view, 0, "RIFF"); // RIFFヘッダ
    view.setUint32(4, 32 + samples.length * 2, true); // これ以降のファイルサイズ
    writeString(view, 8, "WAVE"); // WAVEヘッダ
    writeString(view, 12, "fmt "); // fmtチャンク
    view.setUint32(16, 16, true); // fmtチャンクのバイト数
    view.setUint16(20, 1, true); // フォーマットID
    view.setUint16(22, 1, true); // チャンネル数
    view.setUint32(24, sampleRate, true); // サンプリングレート
    view.setUint32(28, sampleRate * 2, true); // データ速度
    view.setUint16(32, 2, true); // ブロックサイズ
    view.setUint16(34, 16, true); // サンプルあたりのビット数
    writeString(view, 36, "data"); // dataチャンク
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

  let dataview = encodeWAV(mergeBuffers(audioData), audio_sample_rate);
  let audioBlob = new Blob([dataview], { type: "audio/wav" });
  console.log(dataview);
  console.log(audioBlob);
  // --------------------
  let fileReader = new FileReader();
  fileReader.onload = () => {
    let dataURI = fileReader.result;
    console.log(dataURI);
  }
  fileReader.readAsDataURL(audioBlob);
  // --------------------

  let myURL = window.URL || window.webkitURL;
  let url = myURL.createObjectURL(audioBlob);
  return url;
};

// save audio data
var onAudioProcess = function (e) {
  var input = e.inputBuffer.getChannelData(0);
  var bufferData = new Float32Array(bufferSize);
  for (var i = 0; i < bufferSize; i++) {
    bufferData[i] = input[i];
  }

  audioData.push(bufferData);
};

// getusermedia
function handleSuccess(s) {
  stream = s;
}

function startRec() {
  if (isRecording) return -1;
  try {
    audio_sample_rate = null;
    scriptProcessor = null;
    audioContext = null;
    audioData = [];

    audioContext = new AudioContext();
    audio_sample_rate = audioContext.sampleRate;
    console.log(audio_sample_rate);
    scriptProcessor = audioContext.createScriptProcessor(bufferSize, 1, 1);
    var mediastreamsource = audioContext.createMediaStreamSource(stream);
    mediastreamsource.connect(scriptProcessor);
    scriptProcessor.onaudioprocess = onAudioProcess;
    scriptProcessor.connect(audioContext.destination);

    if (micIcon) micIcon.src = "img/mic_active.png";

    // when time passed without pushing the stop button
    setTimeout(function () {
      if (isRecording) {
        saveAudio();
      }
    }, recTime);

    isRecording = true;
    animatePBar();
  } catch (e) {
    alert("Error (Web Audio API) \n" + e);
  }
}


try {
  navigator.mediaDevices
    .getUserMedia({ audio: true, video: false })
    .then(handleSuccess);
} catch (e) {
  alert("この環境は録音非対応です");
}

function animatePBar() {
  pBarWidth = 0;
  pBarInterb = setInterval(() => {
    pBar.style.width = pBarWidth + "%";
    pBarWidth += 1;
    if(pBarWidth > 100) clearInterval(pBarInterb);
  }, recTime / 100);
}

function initPBar(){
  pBarWidth = 0;
  pBar.style.width = pBarWidth + "%";
}