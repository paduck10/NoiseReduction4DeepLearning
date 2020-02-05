# NoiseReduction4DeepLearning

NoiseReduction4DeepLearning - It automates the speech segment and noise reduction process mainly used for Deep Learning dataset


<br></br>



## WorkFlow 정리 :



### 0. 크롤링 작업 :

펭수 영상(90개), 양희은 라디오 음성(1000)개 크롤링. 파이썬 셀레니엄, 웹브라우저 모듈을 이용했습니다.

- Requirements(python modules, 3.8.1 기준 작업) : 

pip        19.2.3

pyperclip  1.7.0

selenium   3.141.0

setuptools 41.2.0

urllib3    1.25.7

*주의* : Window 환경(로컬)에서 pip 모듈을 다운 받으려면 프록시 설정을 수정해주어야 합니다! ESCORD PC-DOWNLOAD -> \[ 인터넷 보안 - 서울대연구소 / 프록시 (Proxy) \] - 프록시 설정 및 인증서 설치 가이드 -> 52페이지 
 

<br></br>

> Get it work!

코드는 엄청 crude합니다;;(세팅한 날 돌려놓고 퇴근) Window 환경에서 돌렸습니다. Linux 환경에서는 테스트 해보지 않았습니다!
위치 : /home/deokgyu.ahn/practice/Resource/Code/yt_crawl/

**펭수 유투브 영상 다운 : `python mp3window.py` 실행**

-> pengsu_youtube.txt에 저장된 유투브 링크들을 읽어서, 영상 한 개씩 음성 파일을 다운로드한다. (Window 환경)

-> `pengsu_youtube.txt`파일에 저장된 각 유투브 링크는 콤마(,)로, 혹은 `\r\n`으로 구별되어야 함!

-> 크롬 브라우저가 열릴 때, 10초 안에 `1회성 사용`버튼을 눌러주세요.

<br></br>

**양희은 유투브 라디오 파일 다운 : `python ppang_radio_down.py` 실행**

-> 팟빵에서 양희은 라디오 파일 링크들을 긁어와서, `yang_radio.txt`파일에 저장합니다. (Window환경)

-> /home/deokgyu.ahn/practice/Resource/Code/yt_crawl/ 폴더에 있는 `down_yang_mp3.py`파일을 돌리면 아까 얻은 링크들을 해당 링크들을 `yang_radio.txt` 파일에서 불러와서 라디오 음성파일들을 다운로드 합니다(`wget`이용) (Linux 환경)

-> `ppang_radio_down.py` 파일에는 `mp3Link` 라는 변수가 있습니다. 해당 변수를 팟빵닷컴에서 찾아 바꿔주기만 하면(예 : 양희은은 http://www.podbbang.com/ch/88 이고, 컬투쇼는 http://www.podbbang.com/ch/3866 입니다) 원하는 라디오 채널에서 음성파일을 다운로드 받을 수 있습니다.

-> 근데 링크가 달라지면 인덱스를 조정해 주어야 합니다.. `page_num`이라는 변수는, 해당 라디오 링크의 총 페이지 수를 의미합니다. 그래서 `page_num`이 100이면 100페이지까지 있는 음성파일들(총 1000개)은 안전하게 다운 가능하지만, 해당 라디오 진행자가 파일을 300개 정도만 올렸다고 한다면(예 : 총 336개 올림) `page_num`변수를 `336 // 10 = 33`으로 바꾸어 주어야 에러가 나지 않습니다.

<br></br>

> 현재 작업 상태 : \\10.114.72.73\hdd 에 옮겨 놓았습니다.

<br></br>
---


### 1. Spleeter : 음악 소리, 배경음악 제거 

배경음악 제거 작업은 [**spleeter** 라이브러리](https://github.com/deezer/spleeter) 이용(RNN Based).

테스트용으로, spleeter에서 제공하는 `pretrained_model`을 사용할 수 있고, 스크립트 작성은 매우 간단합니다. 다만 `pretrained_model`을 불러올때 SSL에러가 뜨는 경우가 있어 직접 `wget`으로 `pretrained_model`을 받아오는 게 더 편할 수 있습니다.

성능향상을 위해 [MusDB](https://sigsep.github.io/datasets/musdb.html)를 이용해 학습을 추가적으로 시킬 수도 있습니다.

새로 해당 라이브러리를 사용할 때, `pretrained_model`이 없다는 에러가 뜰텐데, 보안 이슈로 바로 데이터 셋을 받아올 수 없기에 `wget`으로 `pretrained_model`을 받아와야 합니다.


<br></br>


> Get it work!

1. 먼저, 환경 설정을 바꾸어줍니다. `conda activate spleeter`

2. /home/deokgyu.ahn/practice/Resource/Code/voice_separation/spleeter/ 폴더에 있는 `separate_pengsu.py` 파일을 실행시킵니다.

2-2. `separate_pengsu.py`파일의 argparse는 다음과 같습니다 :

- 자르고 싶은 mp3파일들이 위치한 디렉토리 : `-i`
```
parser.add_argument('-i', '--input_dir', default = '/home/deokgyu.ahn/practice/Resource/Code/speechseg/inaSpeechSegmenter/media/', help='Type the directory where original youtube files are')
```

- 음악/보컬 파일로 분리된 mp3파일들이 저장될 디렉토리 : `-o`
```
parser.add_argument('-o', '--output_dir', default = '/home/deokgyu.ahn/practice/Resource/Code/voice_separation/spleeter/pengsu_yt_output/', help='Type the output directory. Separated vocal and music files will be stored')
```

- 사용할 코덱 : `-c`, 기본은 `mp3`입니다.
```
parser.add_argument('-c', '--codec', default = 'mp3', help='Choose which codec to use : mp3    , wav, ogg, m4a, wma, flac')
```

- 예시 :

```
python separate_pengsu.py -i [mp3파일들이 위치한 디렉토리] -o [음악/보컬 파일들이 저장될 디렉토리] -c ['mp3', 'wav', 'm4a', 'ogg', 'wma', 'flac' 중 택1. 기본은 mp3코덱]
```

이때, mp3 파일 명에 공백(space)가 있을 경우, 에러가 납니다. 그래서 아래에 적어 놓은 `indexing.py`를 활용하여 1.mp3, 2.mp3 형식으로 바꾸어 주는 것이 안전합니다. 파일의 확장자는 .mp3 파일이어야 작업이 가능하게 만들어 놓았습니다. (다른 포맷도 받을 수 있게 코드 수정 가능함. 혹은 pydub으로 파일 확장자 mp3로 바꾸어주는 방법도...)

`separate_pengsu.py`파일을 실행시키면(argparse 인자 줘서), 각 파일별로 음악과 보컬이 분리가 됩니다(예 : 파일 명이 1.mp3이면 '1'이라는 폴더에, accompaniment.mp3(음악 파일)과 vocal.mp3(보컬 파일)이 생성되게 됩니다).

![image](https://user-images.githubusercontent.com/26838115/73428903-a4053880-437d-11ea-845c-265f7678d366.png)


- *참고* : /home/deokgyu.ahn/practice/Resource/Code/voice_separation/spleeter/ 폴더에 `mv_pengsu_vocal_files.py` 스크립트를 실행시키면, `-i` 인자에 위에서 작업한 vocal.mp3, accompaniment.mp3 파일들이 각 폴더별로 들어가 있는 상위 디렉토리를 넣으면, `-o` 인자에 넣은 디렉토리로 vocal.mp3 파일만 가져와서 이동시켜 줍니다(파일명 변경 자동).

**예시** :

```
python mv_pengsu_vocal_files.py -i [1, 2, 3... 폴더들이 위치한 디렉토리] -o [1, 2, 3... 폴더들에 담긴 vocal.mp3 파일들을 인덱싱해서 한꺼번에 모아 놓고 싶은 디렉토리]
```


- *참고* : .mp3 파일 이름을 간편하게 인덱싱하는 스크립트(1.mp3, 2.mp3... 등으로) : /home/deokgyu.ahn/practice/Resource/Code/voice_separation/spleeter/ 폴더에 `indexing.py`파일에 `-i`인자를 주면 해당 디렉토리 내의 .mp3 파일 이름들을 1.mp3, 2.mp3 ... 식으로 바꾸어 줍니다.

**예시** :

```
python indexing.py -i [유투브 영상들이 있는 디렉토리]
```


<br></br>

> 현재 작업 상태 : 일단 펭수 유투브에서 분리 작업 완료. 양희은 라디오 음성 파일은 1000개 파일 X 40분 가량 데이터 크롤링한 후, 배경음악 제거 작업 완료.


<br></br>
---


### 2. inaSpeechSegmenter : 스피치(남/여), 뮤직, 사일런스 분리

[**inaSpeechSegmenter**](https://github.com/ina-foss/inaSpeechSegmenter)는 SMN(Speech, Music, NoEnergy)로 음성 파일을 분리해낼 수 있습니다(CNN based). 이때, Speech는 다시 Male, Female화자로 구분해낼 수 있습니다.

inaSpeechSegmenter를 이용하면, 각 항목(Speech, Music, NoEnergy)들의 start, end time 값을 csv 파일로 저장할 수 있습니다. 위와 마찬가지로 간단한 코드 수정 및 스크립트 작성으로 각 파일별로 사람의 음성만 뽑아낼 수 있습니다. 일단 그냥 아무 영상만 넣으면 알아서 파일명을 인덱싱 한 다음, 다시 항목별(Male, Female, Music, NoEnergy)로 슬라이스 한 결과를 저장할 수 있는 스크립트를 만들어 놓았습니다.

결과 :

![image](https://user-images.githubusercontent.com/26838115/73429219-7240a180-437e-11ea-8aa1-f72d36507048.png)

내부 : 

![image](https://user-images.githubusercontent.com/26838115/73429162-56d59680-437e-11ea-9509-b1c8f8aab75a.png)

<br></br>

> Get it work!

1. 먼저 환경 설정을 바꾸어 줍니다. `conda activate speechseg`

2. /home/deokgyu.ahn/practice/Resource/Code/speechseg/inaSpeechSegmenter/scripts/ 폴더에 보면 `ina_speech_segmenter.py`라는 파일이 있습니다. 해당 파일을 실행시키면, 각 .mp3파일 별로 Label을 생성해줍니다

2-2. `ina_speech_segmenter.py`인자 설명 :

- 인풋 파일(almost obsolete) : `-i`, 인풋 파일(1개)를 넣으면, 해당 파일을 분석해 줍니다. 1개 짜리 쓸일이 없으니, 사실 거의 의미가 없습니다. 생략하시면 됩니다.

```
parser.add_argument('-i', '--input', nargs='+', help='Input media to analyse. May be a full path to a media (/home/david/test.mp3), a list of full paths (/home/david/test.mp3 /tmp/mymedia.avi), or a regex input pattern ("/home/david/myaudiobooks/*.mp3")', required=False)
```
- 인풋 디렉토리 : `-r`, 1에서 작업한 보컬 파일들이 사는 곳의 경로를 넣어 주시면 됩니다.
 ```
 parser.add_argument('-r', '--input_dir', default='/home/deokgyu.ahn/practice/Resource/Code/speechse    g/inaSpeechSegmenter/media', help='(Default : /home/deokgyu.ahn/practice/Resource/Code/speechseg/in    aSpeechSegmenter/media) Input media DIRECTORY where all the media files are in!')
 ```
 
 - 아웃풋 디렉토리 : `-o`, 분석을 완료한 csv 파일들이 저장될 위치입니다.
```
parser.add_argument('-o', '--output_directory', default='/home/deokgyu.ahn/practice/Resource/Code/speechseg/inaSpeechSegmenter/media/out', help='Directory used to store segmentations. Resulting segmentations have same base name as the corresponding input media, with csv extension. Ex: mymedia.MPG will result in mymedia.csv', required=False)
```

- 엔진 : `-d`, `sm`을 선택하면 화자와 음악만 분리를 하고, `smn`을 선택하면 남성/여성/음악으로 레이블을 분리합니다. 기본값은 `smn`입니다. 생략하셔도 됩니다.
```
parser.add_argument('-d', '--vad_engine', choices=['sm', 'smn'], default='smn', help="Voice activity detection (VAD) engine to be used (default: 'smn'). 'smn' split signal into 'speech', 'music' and 'noise' (better). 'sm' split signal into 'speech' and 'music' and do not take noise into account, which is either classified as music or speech. Results presented in ICASSP were obtained using 'sm' option")
```

- 성별 체크 : `-g`, 이것도 그냥 생략하셔도 됩니다.
```
parser.add_argument('-g', '--detect_gender', choices = ['true', 'false'], default='True', help="(default: 'true'). If set to 'true', segments detected as speech will be splitted into 'male' and 'female' segments. If set to 'false', segments corresponding to speech will be labelled as 'speech' (faster)")
```

- **예시** :

```
python ina_speech_segmenter.py -r [자르고 싶은 파일들이 위치한 디렉토리] -o [각 mp3 파일들의 레이블 분류 csv 데이터 파일들이 저장될 위치]
```

(엔진과 성별 체크는 생략해도 됩니다)

3. 위에서 생성한 csv 파일을 바탕으로, 실제 음성 파일을 잘라보겠습니다. /home/deokgyu.ahn/practice/Resource/Code/speechseg/inaSpeechSegmenter/scripts/ 폴더에 `csv_to_sliced.py`라는 파일을 이용하면, 다음과 같이 파일들을 잘라낼 수 있습니다.

![image](https://user-images.githubusercontent.com/26838115/73430351-30fdc100-4381-11ea-9f29-75dd25a75511.png)

3-2. `csv_to_sliced.py` 인자 설명 :

- slice 최소 시간 : `-m`, csv 파일에서 준 label에서, 잘라서 저장할 파일의 최소 시간을 조정할 수 있습니다. 기본값은 1.5초입니다.
```
parser.add_argument('-m', '--minsec', default="1.5", help='Minial second in terms of slicing the speech, used for training. It is float type value, but you can just type integer, e.g. "-m 1"', type=float, required=False)
```

- 자를 mp3 파일들 : `-i`, 자를 mp3 vocal 파일들이 들어 있는 디렉토리를 인풋으로 넣어줍니다.
```
parser.add_argument('-i', '--in_path', default='/home/deokgyu.ahn/practice/Resource/Code/speechseg/inaSpeechSegmenter/media/', help='Default : media folder! Path where the original mp3 files are!')
```

- 잘라진 아웃풋들이 저장될 위치 : `-o`
 ```
 parser.add_argument('-o', '--out_path', default='/home/deokgyu.ahn/practice/Resource/Code/speechseg/inaSpeechSegmenter/dataset_sliced/', help='Default : data_sliced folder. If you want to customize your output directory file, go ahead.')
 ```
 
 - 각 mp3 파일들(잘라질)의 이름과 동일한 파일명의 csv 파일들의 위치 : `-c`
```
parser.add_argument('-c' '--csv_path', default='/home/deokgyu.ahn/practice/Resource/Code/speechseg/inaSpeechSegmenter/dataset_sliced/out/', help='Directory where csv files are in!')
```

<br></br>

*참고* : 펭수 라디오 파일(pengsu_radio 폴더에 있는 음성파일들)은 성능이 매우 좋지 않음. [ffmpeg-normalize 라이브러리](https://github.com/slhck/ffmpeg-normalize/blob/master/README.md)를 사용해서 volume normalization을 하는 게 좋지 않을까? -> 이건 다른 dataset의 경우에도 universal하게 적용 가능!

<br></br>

> 현재 작업 상태 : 먼저 펭수 목소리 분리를 위해, 남성(Male)을 기준으로 음성을 잘랐다(pydub 라이브러리 이용). 이때, 발화의 최소 지속 시간(예: 1초, 1.5초, ...)은 사용자가 조정을 통해 어느 경우가 성능이 더 좋을지 비교해 볼 수 있을 것 같습니다(예 - 0.3초 가량 지속되는 유행어를 포함시키니 성능이 향상되었다 등등). <small>양희은 라디오 음성 음악제거한 파일을 다시 Female음성만 분리해서 저장해 놓았습니다.</small>

<br></br>
---


### 3. Noise Reduction : 잡음 제거 방법 연구(결론 - Low Pass Filtering or nothing)

먼저, 잡음 제거에 있어 *one ring to rule them all...* 같은 것은 없다는 것을 알 수 있었습니다. 그래도 시도해 본 결과를 간단히 언급하도록 하겠습니다.

#### 1. Audacity 방식 : SFX의 특징을 잡아내서 지워버리는 건 어떨까?

Audacity 방식의 경우 조금 더 구현체를 찾아보고 매칭만 잘 시키면 SFX효과를 삭제할 수 있지 않을까? 라는 생각을 해 보았으나, 시도해 본 결과 성능이 매우 좋지 않았습니다. 노이즈 소스를 미리 알고 있어야 하며, 해당 노이즈가 섞여 들어간 정확한 타이밍을 알아야 하기 때문입니다.

이론적으로는, FFT이후 이 값을 Numpy array 로 변환을 시킨 다음에, SFX의 Array 특징을 잡아내서 제거하는 코드를 짜볼 수도 있다고 생각해보기도 했습니다. 이론적으로는 노이즈 소스의 closest vector를 계산해서(FFT를 하면 orthonormal한 벡터들의 조합으로 표현되므로) 해당 vector 값만 제거할 수 있지 않을까? 라는 가정에서 한번 시도를 해 보았습니다. 다만 소리가 중첩될 경우, 해당하는 SFX효과의 Numpy array만 제거한다는 것이 행렬식에서 어떤 의미인지 잘 몰라 일단 넘어가기로 하였습니다.

#### 2. Low Pass Filtering : 특정 Frequency를 기준으로 attenuate(dB)

Low pass filtering 을 적용해 보았으나, 정성적으로는 효과가 좋지 않았습니다. 전체적으로 데시벨 크기가 줄어들고, 특정 잡음이 생기는 대역을 분리하는 것은 무리가 있다고 생각했으나...

5000Hz 기준으로 36dB의 롤백을 주고 2-3회 Pass를 시키면 스펙트로그램상으로는 *치지직...* 하는 잡음은 거의 제거할 수 있는 것 같습니다. 다만 학습시킬때 Normalization작업(증폭 등)이 필요할 것 같습니다. 이 부분은 실험을 통해 파악해야 할 것 같습니다.

<br></br>

> 현재는 가장 시도해볼 만한 가치가 있는 잡음 제거 방법입니다.

#### 3. Notch Filter

notch filter(특정 주파수 밴드만 통과시키는 방식의 필터링)을 이용하면 원하는 노이즈 패턴을 분석했을 때, 상대적으로 효과적으로 특정 피치의 잡음을 제거할 수 있었습니다(예: 6000Hz + Q인자<잘라낼 노치의 폭> 기준으로  6000Hz 근처의 음역대의 소리를 제거할 수 있음을 확인함). 하지만 어떤 음역대를 잘라야 해당 브금/노이즈를 제거할 수 있을지는 좀더 시도해 보아야 하며, 손이 굉장히 많이 가고, Frequency 기준점을 옮겨가며 같은 파일을 반복적으로 필터링해야 합니다. 위에서 설명한 Low Pass Filtering이 훨씬 효율적입니다.

<br></br>

> 저보다 지상님이 해 놓으신게 더 나을 것 같습니다..


<br></br>
---

### 4. 톤 분리 : Multispeaker Model 응용 -> 핵심은 Feature extraction!

기본적으로는 화난 톤/일반 톤으로 분리하고, 더 나아가서는 각 톤마다 클러스터링을 통해 감정표현을 할 수 있도록 하는 연구입니다. 펭수나 짱구 같은 캐릭터 연기의 경우 상당히 어려운 점이 있습니다. 톤이나 dB, 피치 등으로 구분하기가 쉽지 않기 때문입니다. 그래서 딥러닝을 이용한 [Feature extraction 방식](https://www.intechopen.com/books/from-natural-to-artificial-intelligence-algorithms-and-applications/some-commonly-used-speech-feature-extraction-algorithms)을 적용하기로 결정했습니다. 오픈소스 프로젝트는 구하지 못했으나 데이터셋은 구할 수 있어 간단히 구현해 보기로 하였습니다. (데이터셋 : [#1, ravdess, 영어](https://zenodo.org/record/1188976#.XjJiU2gzZhE) [#2, savee, 영어](https://www.kaggle.com/barelydedicated/savee-database) [#3, emo_DB, 독일어](http://emodb.bilderbar.info/download/) [#4, TESS, 영어](https://www.kaggle.com/ejlok1/toronto-emotional-speech-set-tess))

+ 시간이 허락되었다면 구현하고 싶었던 것 : [Automatic Speech Emotion Recognition Using Machine Learning](https://www.intechopen.com/online-first/automatic-speech-emotion-recognition-using-machine-learning)

<br></br>

> 밑바닥부터 시작하는 톤 분리 : 

먼저, 제일 crude한 모델로 시작합니다. 프로세스는 다음과 같습니다.

1. 먼저, 각 오디오 파일의 Feature를 extract합니다. Shape은 (180,)입니다.

2. 딥러닝 모델을 구축합니다. `sample.py`파일에서는, 가장 기초적인 [MLPClassifier모델](https://scikit-learn.org/stable/modules/neural_networks_supervised.html)을 활용했습니다([scikit-learn라이브러리 이용](https://github.com/scikit-learn/scikit-learn)) (MLPClassifier : Multi-layer Perceptron Classifier -> Use LBFGS or stochastic gradient descent as optimizer. -> feedforward ANN model)

3. 데이터셋을 넣고, 훈련을 시킵니다!

<br></br>

> 원리?

Feature extraction은 여러 가지가 있습니다(MFCC, LPC, LPCC, ...). 해당 모델에서는 MFCC를 사용했습니다. 알아야 할 개념은 크게 3가지 입니다.

1. MFCC :  Mel Frequency Cepstral Coefficient, represents the short-term power spectrum of a sound

-> MFCC는 사람의 청각 시스템을 모사합니다. 낮은 주파수 영역대는 Linear하게, 높은 주파수 영역대는 Logarithmic하게 처리해서, 대략 Mel Frequency 기준 1000Hz이하인 녀석들은 민감하게, 그 위의 녀석들은 덜 민감하게 받아들입니다.

-> 각자의 Feature extraction 방식마다 장단점이 있는데, MFCC는 노이즈에 예민합니다. 대신 노이즈가 거의 없는 환경일 경우 높은 성능을 보여줍니다.

![image](https://user-images.githubusercontent.com/26838115/73889819-d9e17a00-48b3-11ea-82c6-e42edb63de52.png)

2. Chroma : Pertains to the 12 different pitch classes

3. Mel : Mel Spectrogram Frequency

이 3가지 스텝을 밟으면 간단히 vector 포맷으로 오디오 파일을 변환할 수 있습니다. Feature extraction을 위한 함수는 librosa library에서 제공해주고 있으므로, 간단하게 구현할 수 있습니다.

그 다음으로는 그냥 classification을 딥러닝 모델을 통해 계속 돌리면 됩니다!

-> 참고 : 다른 Feature extraction 방식들의 장/단점 도표 정리

![image](https://user-images.githubusercontent.com/26838115/73889930-1e6d1580-48b4-11ea-8388-a3a6e1ea7cb0.png)

<br></br>

> How it works?

1. 먼저, 환경 설정을 바꾸어 줍니다 `conda activate emotion`

2. /home/deokgyu.ahn/practice/Resource/Code/emotion/duck_emotion/ 폴더로 이동하여, `duck_emotion.py` 파일을 실행시킵니다.

- 예시 :

-> `python duck_emotion.py` : MLP 모델 학습, Accuracy 약 97% (하이퍼 파라미터 조정을 통해 최적화 가능, 하지만 굳이 안 바꾸셔도...)

-> 위 명령어를 실행시키면, 

-> `python duck_emotion.py -k True` : RNN+LSTM 모델 학습([from Keras](https://machinelearningmastery.com/sequence-classification-lstm-recurrent-neural-networks-python-keras/)), Accuracy 약 80% (모델 Layer늘리기, 배치 정규화, Dropout 적용 등으로 성능 향상 가능)



<br></br>

> Improvements?

1. 데이터 셋 늘리기 (The more, the better!)

`sample.py`에서는 ravdess dataset을 활용하여 간단한 테스트를 진행했습니다. `duck_emotion.py`에서는 savee dataset과 emo_DB dataset을 추가한 custom dataset을 이용하여 훈련을 시킵니다. Clustering은 neutral와 anger 두 가지 케이스로 나누어 진행하였습니다.

-> 데이터셋을 늘린다고 해서 Accuracy가 무조건적으로 늘어나는 것은 아닙니다. 아래에 Anger, Neutral, Sadness 세 가지로 clustering 시 정확도 수치를 데이터셋 별로 정리해 놓았습니다.

<br></br>

- Anger, Neutral 두 가지로 clustering 시

**: ravdess + savee + emoDB -> Training set 481개, Testing set 161개, Accuracy 95\~97%**

: ravdess + savee -> Training set 351개, Testing set 117개, Accuracy 93\~96%

: ravdess -> Training set 216개, Testing set 72개, Accuracy 70\~89% (unstable, due to primal perceptron model)
 
<br></br>

- Anger, Nuetral, Sadness 세 가지로 clustering 시

**: ravdess + savee + emoDB -> Training set 714개, Testing set 238개, Accuracy 75\~80%**

: ravdess + savee -> Training set 540개, Testing set 180개, Accuracy 65\~75%

: ravdess -> Training set 216개, Testing set 72개, Accuracy 72\~87.5% (unstable, due to primal perceptron model)

2. 딥러닝 모델 개선

`sample.py`에서는 가장 원시적인 딥러닝 모델, 퍼셉트론을 활용했습니다. CNN 등 classification에 맞는 모델을 잘 적용하면 accuracy를 늘릴 수 있을 것입니다!

-> ~Tensorflow 모듈로 간단한 CNN 모델은 만들어 볼 수 있을 것 같습니다.~ : 실험 결과 성능이 더 떨어짐

-> MLPClassifier에서, hidden_layer_sizes를 늘리면 정확도가 향상되는 것을 확인했습니다. 다만 이것도 한계가 있어서, 500000개 정도를 Maximum으로 정해 놓고 돌렸습니다.


3. Things to note

-> 먼저, 딥러닝 모델을 개선함으로써 classification이 잘 작동하도록 만듭니다.

-> 그후, Anger, Neutral 수치가 있다고 하면 수치가 매우 높은 녀석들(예 - Anger:90, Neutral:10으로 분류된 녀석)을 다시 Training set으로 포함 시켜 학습을 시킵니다.(되먹임 회로 같은 원리)

-> 그런 식으로 데이터셋을 확장성 있게 늘려 나갈 수 있습니다!


<br></br>
---

### 5. 화자분리(Speaker 분리) : Voice Filter, Resemblyzer

##### <Resemblyzer : 보류>

화자를 분리하는 라이브러리 중, **resemblyzer**라는 좋은 패키지가 있다고 들어, 돌려보았으나...

별로 성능이 좋지 않아서, 사용하지 않을 예정입니다. 구체적으로는, 다음과 같은 문제가 있습니다.

<br></br>

1. 신뢰도의 문제점

-> 가장 근본적인 문제입니다. Resemblyzer는 먼저 깔끔한 캐릭터의 보이스를 일정 부분 인풋으로 받아서, embedding을 합니다(d-vector, length : 256). 그렇다면 깔끔한 캐릭터의 보이스를 다시 인풋으로 넣어서(간단히 말하자면 트레이닝 데이터로 훈련을 하는 느낌입니다) 지금 화자가 내가 voice를 embedding한 그 화자가 맞는지를 판단하면, 이론적으로는 confident한 수치가 계속 나와야 합니다(voice embedding을 한 화자가 말하고 있음이 확실한 경우를 confident, 애매한 경우를 uncertain이라고 분류하고 있습니다). 그러나 훈련 데이터를 돌려봤음에도 중간 중간 uncertain이 관측이 되며, A화자와 B화자가 순차적으로 대화하는 경우에서도 매우 낮은 성능을 보입니다. 실제로 그런 용도로는 사용할 수 없습니다.


-> 테스트셋(voice embedding을 하는 데 사용하지 않은 음성 파일)에 Resemblyzer를 적용하여 해당 화자가 말하고 있는지 아닌지를 체크할 때는 그 정도가 더 심각합니다.


2. 결국 수작업이 필요


-> Minor한 이슈이기는 합니다. 다만, voice embedding을 위해 일정 분량의 clean한 voice가 필요하다는 것이 단점이라면 단점입니다.


3. 그럼에도 불구하고

-> 의의는 있습니다. 신뢰도가 너무나도 낮은 파일의 경우는 걸러내는 것이 가능합니다. 예를 들어, 앞의 1번(spleeter)와 2번(inaSpeechSegmenter)작업을 거치면 `남성`화자 정도의 음악 slice들을 만들 수 있는데, Resemblyzer를 이용하면 '펭수가 전혀 아닐 가능성이 높은 일부 음악파일들' 정도는 제거할 수 있습니다.

-> 방법은 크게 두 가지 입니다. 그 중 좋은 방법은, Clean한 펭수 보이스를 이용한 embedding 벡터와 각 slice파일들의 embedding 벡터를 비교해서 유사도가 심각하게 떨어지는 녀석들을 삭제해 버리는 방식입니다.

-> 실험 및 테스트 : `conda activate resemblyzer` -> /home/deokgyu.ahn/practice/Resource/Code/speaker_separation/Resemblyzer/ 폴더에서 테스트


#### Voice Filter : Google, save us

[구글에서 2019년에 발표한 Voice Filter](https://google.github.io/speaker-id/publications/VoiceFilter/)를 복습해 보았습니다. 기본 방식은 Noise와 Voice가 Mixed된 파일에서 Noise를 마스킹하는 것이라면, VoiceFilter는 미리 학습된(임베딩된) 사용자의 d-Vector를 이용해 Mixed된 파일에서 Voice를 추출하는 방식입니다. 구글에서는 상당한 성능 향상을 보인다고 발표했습니다. 다만, 아직 변변한 구현체가 있는지는 잘 모르겠습니다. 찾아본 구현체들 : [#1](https://github.com/mindslab-ai/voicefilter) [#2](https://github.com/edwardyoon/voicefilter) [#3](https://github.com/funcwj/voice-filter)

그 중, [쓸만하다고 생각하는 구현체](https://github.com/mindslab-ai/voicefilter)가 있어 돌려보았습니다.


<br></br>

> Bugfix?

[위 링크](https://github.com/mindslab-ai/voicefilter)의 README를 따라가시면 됩니다! 다만, **Prepare dataset**부분에서, 4번 항목 *Preprodcess wav files* 의 경우, 아래와 같은 명령어를 입력해 주세요.

```
python generator.py -c ./config/config.yaml -d /home/deokgyu.ahn/practice/Resource/Code/speaker_separation/voicefilter/datasets/LibriSpeech -o /home/deokgyu.ahn/practice/Resource/Code/speaker_separation/voicefilter/datasets/normalized_dataset/ -p 16 >out.log &
```

이때, dev-clean 파일을 다운받지 않으면 test set 생성 과정에서 오류가 발생합니다. `wget http://www.openslr.org/resources/12/dev-clean.tar.gz` 필수! 이후 `tar -xvzf dev-clean.tar.gz`를 하면 자동으로 LibriSpeech 디렉토리 내부에 저장이 됩니다. -> 이거 해도 오류 발생할 경우, train 데이터셋에서 1000개정도 test 데이터셋으로 옮겨주면 됩니다. (현재 그렇게 돌려봄)

(`-o` 부분을 생략하면 `random.sample`에서 ValueError가 뜹니다. Librispeech 폴더의 디렉토리를 넣어 주시면 됩니다.)

(`-p`의 경우, cpu 갯수를 써 주시면 됩니다. `python; import multiprocessor as mp; mp.cpu_count()`로 갯수 확인.)

(./config/config.yaml 파일에서 batch size를 2로 낮춰야 약 10GB정도의 메모리를 잡아 먹으면서 겨우 돌아갑니다. - GTX2080Ti 기준)

(CUDA Runtime Execution Error 가 발생 -> `torch.backends.cudnn.enabled = False`를 넣어 해결)

(기타 모든 버그들 해결 완료된 상태입니다)


> How it work?

-> 테스트만 해보시길 원하신다면, 아래와 같은 형식으로 실행시키면 됩니다.

```
python inference.py -c [config yaml] -e [path of embedder pt file] --checkpoint_path [path of chkpt pt file] -m [path of mixed wav file] -r [path of reference wav file] -o [output directory]
```

-> 예시 : 

```
python inference.py -c ./config/config.yaml -e embedder.pt --checkpoint_path chkpt/first/chkpt_99000.pt -m test_jieun/jieun_duck_mixed.wav -r test_jieun/jieun_clean_merged.wav -o test_jieun/out_test/
```


> 현재 진행 상황 : 

-> 화자의 목소리가 Mixed 된 경우는 성능이 그리 좋지 못합니다. (test_jieun 폴더에서 jieun_duck_mixed.wav파일과 out_test/out_jieun_duck_mixed.wav파일 비교)

-> 화자 2명이 번갈아 가면서 말하는 경우는 생각보다 준수한 성능을 보입니다. (test_jieun 폴더에서 jieun_duck_alternate.wav파일과 out_test/out_jieun_duck_alternate.wav파일 비교)



<br></br>
---

### 6. 음성 파일에 맞는 스크립트 생성 : 

Speech-To-Text API 이용해서 스크립트 작성은 Azure SDK 사용한다고 들었는데, 직접 스크립트를 수정/레이블링하는 작업이 필요하다고 들어 대기중입니다.


<br></br>
---

### 7. 모델 학습 및 성능 향상 : 

데이터셋 생성 및 자동화 프로세스를 한 바퀴 돌고 나면, 본격적으로 모델을 학습시키며 Fine-Tuning 작업을 진행해 볼 수 있을 것 같습니다.

