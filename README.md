# NoiseReduction4DeepLearning

NoiseReduction4DeepLearning - It automates the speech segment and noise reduction process mainly used for Deep Learning dataset


<br></br>



## WorkFlow 정리 :



### 0. 크롤링 작업 :

펭수 영상(90개), 양희은 라디오 음성(1000)개 크롤링. 파이썬 셀레니엄, 웹브라우저 모듈을 이용했습니다.

> 현재 작업 상태 : \\10.114.72.73\hdd 에 옮겨 놓았습니다.

코드는 엄청 crude합니다;;(세팅한 날 돌려놓고 퇴근) Window 환경에서 돌렸습니다. Linux 환경에서는 테스트 해보지 않았습니다!
위치 : /home/deokgyu.ahn/practice/Resource/Code/yt_crawl/

**펭수 유투브 영상 다운 : `python mp3window.py` 실행**

-> pengsu_youtube.txt에 저장된 유투브 링크들을 읽어서, 영상 한 개씩 음성 파일을 다운로드한다. (Window 환경)

-> `pengsu_youtube.txt`파일에 저장된 각 유투브 링크는 콤마(,)로, 혹은 `\r\n`으로 구별되어야 함!

**양희은 유투브 라디오 파일 다운 : `python ppang_radio_down.py` 실행**

-> 팟빵에서 양희은 라디오 파일 링크들을 긁어와서, `yang_radio.txt`파일에 저장합니다. (Window환경)

-> /home/deokgyu.ahn/practice/Resource/Code/yt_crawl/ 폴더에 있는 `down_yang_mp3.py`파일을 돌리면 아까 얻은 링크들을 해당 링크들을 `yang_radio.txt` 파일에서 불러와서 라디오 음성파일들을 다운로드 합니다(`wget`이용) (Linux 환경)

-> `ppang_radio_down.py` 파일에는 `mp3Link` 라는 변수가 있습니다. 해당 변수를 팟빵닷컴에서 찾아 바꿔주기만 하면(예 : 양희은은 http://www.podbbang.com/ch/88 이고, 컬투쇼는 http://www.podbbang.com/ch/3866 입니다) 원하는 라디오 채널에서 음성파일을 다운로드 받을 수 있습니다.

<br></br>
---


### 1. Spleeter : 음악 소리, 배경음악 제거 

배경음악 제거 작업은 [**spleeter** 라이브러리](https://github.com/deezer/spleeter) 이용(RNN Based).

테스트용으로, spleeter에서 제공하는 `pretrained_model`을 사용할 수 있고, 스크립트 작성은 매우 간단합니다. 다만 `pretrained_model`을 불러올때 SSL에러가 뜨는 경우가 있어 직접 `wget`으로 `pretrained_model`을 받아오는 게 더 편할 수 있습니다.

성능향상을 위해 [MusDB](https://sigsep.github.io/datasets/musdb.html)를 이용해 학습을 추가적으로 시킬 수도 있습니다.

> Get it work!





> 현재 작업 상태 : 일단 펭수 유투브에서 분리 작업 완료. 양희은 라디오 음성 파일은 1000개 파일 X 40분 가량 데이터 크롤링한 후, 배경음악 제거 작업 완료.


<br></br>
---


### 2. inaSpeechSegmenter : 스피치(남/여), 뮤직, 사일런스 분리

[**inaSpeechSegmenter**](https://github.com/ina-foss/inaSpeechSegmenter)는 SMN(Speech, Music, NoEnergy)로 음성 파일을 분리해낼 수 있습니다(CNN based). 이때, Speech는 다시 Male, Female화자로 구분해낼 수 있습니다.

inaSpeechSegmenter를 이용하면, 각 항목(Speech, Music, NoEnergy)들의 start, end time 값을 csv 파일로 저장할 수 있습니다. 위와 마찬가지로 간단한 코드 수정 및 스크립트 작성으로 각 파일별로 사람의 음성만 뽑아낼 수 있습니다. 일단 그냥 아무 영상만 넣으면 알아서 파일명을 인덱싱 한 다음, 다시 항목별(Male, Female, Music, NoEnergy)로 슬라이스 한 결과를 저장할 수 있는 스크립트를 만들어 놓았습니다.

> 현재 작업 상태 : 먼저 펭수 목소리 분리를 위해, 남성(Male)을 기준으로 음성을 잘랐다(pydub 라이브러리 이용). 이때, 발화의 최소 지속 시간(예: 1초, 1.5초, ...)은 사용자가 조정을 통해 어느 경우가 성능이 더 좋을지 비교해 볼 수 있을 것 같습니다(예 - 0.3초 가량 지속되는 유행어를 포함시키니 성능이 향상되었다 등등). <small>양희은 라디오 음성 음악제거한 파일을 다시 Female음성만 분리해서 저장해 놓았습니다.</small>


<br></br>
---


### 3. Noise Reduction : 잡음 제거 방법 연구(결론 - Low Pass Filtering)

먼저, 잡음 제거에 있어 *one ring to rule them all...* 같은 것은 없다는 것을 알 수 있었습니다. 그래도 시도해 본 결과를 간단히 언급하도록 하겠습니다.

#### 1. Audacity 방식 : SFX의 특징을 잡아내서 지워버리는 건 어떨까?

Audacity 방식의 경우 조금 더 구현체를 찾아보고 매칭만 잘 시키면 SFX효과를 삭제할 수 있지 않을까? 라는 생각을 해 보았으나, 시도해 본 결과 성능이 매우 좋지 않았습니다. 노이즈 소스를 미리 알고 있어야 하며, 해당 노이즈가 섞여 들어간 정확한 타이밍을 알아야 하기 때문입니다.

이론적으로는, FFT이후 이 값을 Numpy array 로 변환을 시킨 다음에, SFX의 Array 특징을 잡아내서 제거하는 코드를 짜볼 수도 있다고 생각해보기도 했습니다. 이론적으로는 노이즈 소스의 closest vector를 계산해서(FFT를 하면 orthonormal한 벡터들의 조합으로 표현되므로) 해당 vector 값만 제거할 수 있지 않을까? 라는 가정에서 한번 시도를 해 보았습니다. 다만 소리가 중첩될 경우, 해당하는 SFX효과의 Numpy array만 제거한다는 것이 행렬식에서 어떤 의미인지 잘 몰라 일단 넘어가기로 하였습니다.

#### 2. Low Pass Filtering : 특정 Frequency를 기준으로 attenuate(dB)

Low pass filtering 을 적용해 보았으나, 정성적으로는 효과가 좋지 않았습니다. 전체적으로 데시벨 크기가 줄어들고, 특정 잡음이 생기는 대역을 분리하는 것은 무리가 있다고 생각했으나...

5000Hz 기준으로 36dB의 롤백을 주고 2-3회 Pass를 시키면 스펙트로그램상으로는 *치지직...* 하는 잡음은 거의 제거할 수 있는 것 같습니다. 다만 학습시킬때 Normalization작업(증폭 등)이 필요할 것 같습니다. 이 부분은 실험을 통해 파악해야 할 것 같습니다.

> 현재는 가장 시도해볼 만한 가치가 있는 잡음 제거 방법입니다.

#### 3. Notch Filter

notch filter(특정 주파수 밴드만 통과시키는 방식의 필터링)을 이용하면 원하는 노이즈 패턴을 분석했을 때, 상대적으로 효과적으로 특정 피치의 잡음을 제거할 수 있었습니다(예: 6000Hz + Q인자<잘라낼 노치의 폭> 기준으로  6000Hz 근처의 음역대의 소리를 제거할 수 있음을 확인함). 하지만 어떤 음역대를 잘라야 해당 브금/노이즈를 제거할 수 있을지는 좀더 시도해 보아야 하며, 손이 굉장히 많이 가고, Frequency 기준점을 옮겨가며 같은 파일을 반복적으로 필터링해야 합니다. 위에서 설명한 Low Pass Filtering이 훨씬 효율적입니다.



<br></br>
---

### 4. 톤 분리 : Multispeaker Model 응용

기본적으로는 화난 톤/일반 톤으로 분리하고, 더 나아가서는 각 톤마다 클러스터링을 통해 감정표현을 할 수 있도록 하는 연구입니다. 펭수나 짱구 같은 캐릭터 연기의 경우 상당히 어려운 점이 있습니다. 톤이나 dB, 피치 등으로 구분하기가 쉽지 않기 때문입니다.



<br></br>
---

### 5. 화자분리(Speaker 분리) : Voice Filter, Resemblyzer

먼저 [구글에서 2019년에 발표한 Voice Filter](https://google.github.io/speaker-id/publications/VoiceFilter/)를 복습해 보았습니다. 기본 방식은 Noise와 Voice가 Mixed된 파일에서 Noise를 마스킹하는 것이라면, VoiceFilter는 미리 학습된(임베딩된) 사용자의 d-Vector를 이용해 Mixed된 파일에서 Voice를 추출하는 방식입니다. 구글에서는 상당한 성능 향상을 보인다고 발표했습니다. 다만, 아직 변변한 구현체가 있는지는 잘 모르겠습니다. 찾아본 구현체들 : [#1](https://github.com/mindslab-ai/voicefilter) [#2](https://github.com/edwardyoon/voicefilter) [#3](https://github.com/funcwj/voice-filter)

화자를 분리하는 라이브러리 중, **resemblyzer**라는 좋은 패키지가 있다고 들었는데, 아직 돌려보지는 않았습니다.


<br></br>
---

### 6. 음성 파일에 맞는 스크립트 생성 : 

Speech-To-Text API 이용해서 스크립트 작성은 Azure SDK 사용한다고 들었는데, 직접 스크립트를 수정/레이블링하는 작업이 필요하다고 들어 대기중입니다.


<br></br>
---

### 7. 모델 학습 및 성능 향상 : 

데이터셋 생성 및 자동화 프로세스를 한 바퀴 돌고 나면, 본격적으로 모델을 학습시키며 Fine-Tuning 작업을 진행해 볼 수 있을 것 같습니다.

