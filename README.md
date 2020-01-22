# NoiseReduction4DeepLearning
NoiseReduction4DeepLearning - It automates the speech segment and noise reduction process mainly used for Deep Learning dataset

## WorkFlow 정리 :

### 0. 크롤링 작업 :

펭수 영상(90개), 양희은 라디오 음성(1000)개 크롤링. 파이썬 셀레니엄, 웹브라우저 모듈을 이용했습니다.


---


### 1. Spleeter : 음악 소리, 배경음악 제거 

배경음악 제거 작업은 [**spleeter** 라이브러리](https://github.com/deezer/spleeter) 이용(RNN Based).

테스트용으로, spleeter에서 제공하는 `pretrained_model`을 사용할 수 있고, 스크립트 작성은 매우 간단합니다. 다만 `pretrained_model`을 불러올때 SSL에러가 뜨는 경우가 있어 직접 `wget`으로 `pretrained_model`을 받아오는 게 더 편할 수 있습니다.

성능향상을 위해 [MusDB](https://sigsep.github.io/datasets/musdb.html)를 이용해 학습을 추가적으로 시킬 수도 있습니다.

> 현재 작업 상태 : 일단 펭수 유투브에서 분리 작업 완료. 양희은 라디오 음성 파일은 1000개 파일 X 40분 가량 데이터 크롤링한 후, 배경음악 제거 작업 완료.


---


### 2. inaSpeechSegmenter : 스피치(남/여), 뮤직, 사일런스 분리

[**inaSpeechSegmenter**](https://github.com/ina-foss/inaSpeechSegmenter)는 SMN(Speech, Music, NoEnergy)로 음성 파일을 분리해낼 수 있습니다(CNN based). 이때, Speech는 다시 Male, Female화자로 구분해낼 수 있습니다.

inaSpeechSegmenter를 이용하면, 각 항목(Speech, Music, NoEnergy)들의 start, end time 값을 csv 파일로 저장할 수 있습니다. 위와 마찬가지로 간단한 코드 수정 및 스크립트 작성으로 각 파일별로 사람의 음성만 뽑아낼 수 있습니다. 일단 그냥 아무 영상만 넣으면 알아서 파일명을 인덱싱 한 다음, 다시 항목별(Male, Female, Music, NoEnergy)로 슬라이스 한 결과를 저장할 수 있는 스크립트를 만들어 놓았습니다.

> 현재 작업 상태 : 먼저 펭수 목소리 분리를 위해, 남성(Male)을 기준으로 음성을 잘랐다(pydub 라이브러리 이용). 이때, 발화의 최소 지속 시간(예: 1초, 1.5초, ...)은 사용자가 조정을 통해 어느 경우가 성능이 더 좋을지 비교해 볼 수 있을 것 같습니다(예 - 0.3초 가량 지속되는 유행어를 포함시키니 성능이 향상되었다 등등). <small>양희은 라디오 음성 음악제거한 파일을 다시 Female음성만 분리해서 저장해 놓았습니다.</small>


---


### 3. Noise Reduction : 잡음 제거 방법 연구

먼저, 잡음 제거에 있어 *one ring to rule them all...* 같은 것은 없다는 것을 알 수 있었습니다. 그래도 시도해 본 결과를 간단히 언급하도록 하겠습니다.

#### 3. Audacity 방식으로 효과음 제거하기? 혹은 SFX의 특징을 잡아내서 지워버리는 건 어떨까? : 

Numpy array 로 변환을 시킨 다음에, SFX의 Array 특징을 잡아내서 제거하는 코드를 짜볼 수도 있음. 그런데 소리가 중첩될 경우, 해당하는 SFX효과의 Numpy array만 제거한다는 것이 어떤 의미인지 조금 연구를 해봐야 함.

Audacity 방식의 경우 조금 더 구현체를 찾아보고 매칭만 잘 시키면 SFX효과를 삭제할 수 있지 않을까? -> 이것도 리서치를 해 봐야 한다!

-> Audacity 방식을 시도해 보았으나 성능이 매우 좋지 않다. 또한 노이즈 소스를 미리 알고 있어야 하며, 해당 노이즈가 섞여 들어간 정확한 타이밍을 알아야 한다.

-> Low pass filtering 을 적용해 보았으나, 정성적으로는 효과가 좋지 않다. 전체적으로 데시벨 크기가 줄어들고, 특정 잡음이 생기는 대역을 분리하는 것은 무리가 있다

-> notch filter(특정 주파수 밴드만 통과시키는 방식의 필터링) : 이걸 적용하면 원하는 노이즈 패턴을 분석했을 때, 상대적으로 효과적으로 특정 피치의 잡음을 제거할 수 있다! (예: 6000Hz + Q인자<잘라낼 노치의 폭> 기준으로  6000Hz 근처의 음역대의 소리를 제거할 수 있음을 확인했다. : 하지만 어떤 음역대를 잘라야 해당 브금/노이즈를 제거할 수 있을지는 좀더 시도해 보아야 한다. 수작업이 필요할 수도?
-> 이거 이해하려면 DSP 공부해야.
-> 아니 근데 Notch 돌려도 별 효과가 없는 듯? 결국 각 브금마다 frequency band를 다르게 설정해야 하잖아?

---

4. csv_to_sliced.py : 이 파일을 돌리면, 일단 media 폴더에 들어있는 원본으로부터 펭수 목소리를 대강 잘라서 다시 dataset_sliced 폴더에 넣어준다! : pydub 라이브러리를 사용했다.

---

5. 화자분리(Speaker 분리) :
일단 resemblyzer라는 좋은 패키지가 있어서 사용해 보기. -> 아직 여기까지 안 갔다.

---

6. 음성 파일에 맞는 스크립트 생성 : 
 Speech-To-Text API 이용해서 스크립트 작성 -> 마이크로소프트 SDK 사용해서 데이터셋 만들기
