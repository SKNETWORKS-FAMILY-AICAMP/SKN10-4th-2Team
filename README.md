# SKN10-4th-2Team

**개발 기간** : 2025.05.09 ~ 2025.05.12

<table align=center>
  <tbody>
    <tr>
    <br>
      <td align=center><b>문승기</b></td>
      <td align=center><b>배민경</b></td>
      <td align=center><b>신민주</b></td>
      <td align=center><b>좌민서</b></td>
      <td align=center><b>홍승표</b></td>
    </tr>
    <tr>
      <td align="center">
         <img src="https://github.com/user-attachments/assets/9edf699b-3f3d-4847-a7da-c5278c65394c" width="200px;" alt="문승기"/>
      </td>
      <td align="center">
          <img src="https://github.com/user-attachments/assets/90e304e9-f8ae-4ee5-9ac4-e635dc83d066" width="200px;" alt="배민경"/>
      </td>
      <td align="center">
          <img src="https://github.com/user-attachments/assets/28f92593-63d0-4915-a837-205732ea7517" width="200px;" alt="신민주"/>
      </td>
      <td align="center">
          <img src="https://github.com/user-attachments/assets/5d24e79a-1a8a-42e7-9131-785511c671bc" width="200px;" alt="좌민서"/>
      </td>
       <td align="center">
          <img src="https://github.com/user-attachments/assets/b56ec8b6-050f-45f0-a2ab-2befcc876604" width="200px;" alt="홍승표"/>
      </td>
    </tr>
    <tr>
      <td><a href="https://www.wine21.com/13_search/wine_view.html?Idx=162135"><div align=center>칸티 모스카토 다스티</div></a></td>
      <td><a href="https://www.wine21.com/13_search/wine_view.html?Idx=171671"><div align=center>프로세코 로제</div></a></td>
      <td><a href="https://www.wine21.com/13_search/wine_view.html?Idx=149632"><div align=center>G7 레세르바 샤르도네</div></a></td>
      <td><a href="https://www.wine21.com/13_search/wine_view.html?Idx=156782"><div align=center>스크리밍 이글</div></a></td>
      <td><a href="https://www.wine21.com/13_search/wine_view.html?Idx=142964"><div align=center>드라이 셰리</div></a></td>
    </tr>
  </tbody>
</table>

<br>

## VINO - **와인 입문 가이드 챗봇**

![Image](https://github.com/user-attachments/assets/bc165d75-9bcf-4e68-8044-b87e811f8aea)

<br>

## 1. 서비스 개요

**와인 초보 입문 가이드 챗봇**은 와인에 대한 지식이 부족한 초보자를 위해 음식 페어링, 와인 용어 해석, 입문용 추천 정보를 **AI 기반의 정교한 다단계 평가 방식**으로 제공하는 **와인 입문 가이드 챗봇 서비스**입니다.

<br>

## 2. 서비스 기획 배경

-   복잡한 와인 정보 구조
    → 라벨, 품종, 빈티지 등 비정형 정보가 많아 입문자에게 큰 장벽

-   실생활에 맞는 음식 페어링 정보 부족
    → 한식, 매운 음식 등 일상 속 음식과의 궁합 정보 미흡

-   대화형 와 추천 수요 증가
    → 홈술 트렌드 확인산 및 입문자 증가로 대화 기반 정보 탐색 니즈 상승

<br>

## 3. 세부 기능 및 사용자 흐름

### 사용자 권한 및 보안 정책

#### 권한 비교

| 기능 항목                             | 일반 사용자 | 관리자 (`is_staff` / `is_superuser`) |
| ------------------------------------- | ----------- | ------------------------------------ |
| 챗봇 기능 이용                        | O           | O                                    |
| 챗봇 인터페이스 접속 (대화 화면 접근) | O           | O                                    |
| 관리자 페이지(Django Admin) 접속      | X           | O                                    |
| 사용자 목록 조회/생성/수정/삭제       | X           | O                                    |
| 회원 정보 상세 관리                   | X           | O (`/admin/user/customuser/`)        |

> 챗봇 기능은 웹 인터페이스를 통해 제공되며, 일반 사용자도 자유롭게 이용할 수 있습니다.  
> 관리자 권한을 가진 사용자는 Django Admin을 통해 추가적인 기능을 수행할 수 있습니다.

#### 보안 정책

-   `admin` 계정은 어떤 사용자도 삭제할 수 없습니다.
-   관리자 계정 생성 시, 강력한 비밀번호 보안 정책이 적용됩니다.
-   관리자 가입 시, SweetAlert를 통해 인증 코드(예: `777`)를 입력해야 가입이 완료됩니다.

### 사용자 입력 단계

-   질문 예시
    -   “스테이크에 어울리는 와인 뭐가 있어요?”
    -   “까쇼 블렌딩이 뭔 뜻이에요?”
    -   “2 ~ 3만원대 입문용 레드 추천해줘요”

### 챗봇 응답 프로세스

```
1. 사용자 로그인 및 회원가입
2. 사용자 로그인 여부 확인
3. 사용자 질문 입력
4. sLLM이 1차 응답 A 생성
5. GPT-4o-mini가 응답 A의 적절성 평가
6. 불충분 시 → FAISS 기반 RAG로 내부 문서 검색 → 응답 B 생성
7. GPT-4o-mini가 응답 B의 적절성 평가
8. 여전히 불충분하면 → Tavily API를 통해 외부 콘텐츠 검색 및 요약 → 응답 C 생성
9. A~C 중 가장 신뢰도 높은 응답을 사용자에게 제공
```

<br>

## 4. 기술 구성 요소

### LLM 및 평가 모델

-   1차 응답 생성: Fine-tuned sLLM (와인 용어·페어링 문체 학습)
-   응답 평가: GPT-4o-mini (OpenAI API 기반, 응답 적절성 평가)

### 검색 기반 QA (RAG)

-   GPT 판단 후 부정확한 경우 → FAISS 기반 내부 문서 벡터 검색
-   관련 콘텐츠를 sLLM에 프롬프트로 주입해 응답 재생성
-   최종 보완 필요 시 → Tavily 웹 검색으로 요약 보완

### 시스템 구성

-   백엔드: Django (Python)
-   프론트엔드: HTML, CSS, Django Template 기반 UI
-   모듈 흐름: 사용자 입력 → sLLM → 응답 GPT-4o-mini 평가 → RAG 검색 → 응답 GPT-4o-mini 평가 → Tavily 보완

<br>

## 5. 데이터 소스

### 1. Fine-Tuning - 유튜브 자막 기반

-   [**세상의 모든 와인 All that wine**](https://www.youtube.com/@allthatwine/playlists)의 재생목록

    -   와인 테이스팅의 모든 것
    -   [중급 강의]30분만에 끝나는 '와인 이제 좀 안다!' 클래스
    -   [초급 강의]30분만에 끝나는 와인 인생초보 탈출
    -   와인추천
    -   와인 지역별 비교
    -   와인 품종별 비교
    -   와인기초상식

-   [**와푸밸 Wine Food Balance**](https://www.youtube.com/@winefoodbalance1143/playlists)의 재생목록
    -   [와인 추천]
    -   [와인 상식, 와인 꿀팁]
    -   [음식과 와인 조합]

→ 해당 재생목록 영상들의 자막 데이터를 통해 와인에 대한 지식, 와인 추천 등에 대한 정보를 추출하여 모델을 학습시킨다.

### 2. RAG

-   [**WINE21.COM**](https://www.wine21.com/13_search/wine_list.html)

→ 해당 사이트에서 필요한 정보를 `request`, `BeautifulSoup`, `Selenium`을 통해 추출하여 사용하였다.

<br>

## 5-1. 데이터셋 생성

### 1. 데이터 수집

`yt-dlp` 라이브러리를 사용하여 유튜브 영상의 자막 데이터를 추출한다.

### 2. 전처리 과정

-   자막 내 불필요한 요소(특수문자, 이모티콘 등) 제거
-   와인과 직접적인 관련이 없는 단어 또는 문장 제거
-   음성 인식 오류로 잘못 표기된 단어 수정

### 3. 질문-답변 데이터셋 생성

전처리된 자막 데이터를 기반으로 `gpt-4o-mini` 모델을 사용하여 요리 과정을 중심으로 한 질문-답변 데이터셋을 생성한다.

<br>

## 6. 사용자 케이스별 활용 예시

| 케이스 유형 | 설명                                                   | 챗봇 기능                             |
| ----------- | ------------------------------------------------------ | ------------------------------------- |
| 용어 설명   | 까쇼, 블렌딩, 빈티지 등 용어 설명                      | 와인 용어 설명 및 관련 와인 예시 제공 |
| 구매 가이드 | 입문자용 와인 가격대, 인기 품종 추천                   | 가격대별 추천 와인 및 선택 팁 제공    |
| 음식 페어링 | 삼겹살, 매운탕, 치즈 등 일상 음식과 어울리는 와인 추천 | 추천 와인 및 페어링 이유 제공         |

<br>

## 7. 확장 가능성 및 고도화 아이디어

| 기능             | 설명                                     |
| ---------------- | ---------------------------------------- |
| 쇼핑몰 연동      | 추천된 와인의 구매 링크 제공             |
| 라벨 이미지 인식 | 와인 라벨 이미지에서 텍스트 추출 후 해석 |

<br>

## 8. 요약 및 기대 효과

-   와인 입문자의 학습과 실용적인 소비를 지원
-   사용자 질문 기반의 정확한 추천 및 해설로 신뢰성 있는 콘텐츠 제공
-   와인 문화 확산 및 커머스 연계 가능성 확보

<br>

## 9. 응답 생성 및 서비스 동작 프로세스

![Image](https://github.com/user-attachments/assets/0baed123-e378-4c5f-b8f8-ad2c2262a3c3)

<br>

## 10. 설치 및 실행 방법

**와인 입문 가이드 챗봇 서비스**를 실행하기 위해서는 아래의 단계를 따라야 한다.

### 1. 프로젝트 클론

```bash
git clone https://github.com/SKNETWORKS-FAMILY-AICAMP/SKN10-4th-2Team.git
```

### 2. 가상환경 생성 및 라이브러리 설치

```bash
uv venv .venv -p [파이썬 버전 ex) 3.13]
.\.venv\Scripts\activate
uv pip install -r requirements.txt
```

### 3. Ollama 모델 설치

Hugging Face에 등록된 모델을 사용하기 위해 `.gguf` 파일을 다운로드하여 Ollama에 설치한다.<br/>
자세한 설치 방법은 **11번 항목**을 참고한다.

### 4. 환경 변수 설정 (.env 파일 생성)

`.env` 파일을 프로젝트 루트 디렉터리에 생성하고, 다음 내용을 추가해야 한다:

```env
GROQ_API_KEY=[groq_api_key]
OPENAI_API_KEY=[openai_api_key]
HF_TOKEN=[huggingface_token_api_key]

SECRET_KEY=[django_secret_key]
DEBUG=[True_or_False]

MYSQL_DB=[mysql_db_name]
MYSQL_USER=[mysql_username]
MYSQL_PWD=[mysql_password]
MYSQL_HOST=[mysql_host]
MYSQL_PORT=[mysql_port]
```

### 5. 실행

Django를 사용하는 경우:

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

<br>

## 11. Ollama 모델 설치

### 1. `.gguf` 파일 다운로드

[**Hugging Face 모델**](https://huggingface.co/Minkyeong2/gemma3-Wine-Guide-gguf) 페이지에서 `.gguf` 확장자를 가진 파일을 다운로드한다.

<img src='https://github.com/user-attachments/assets/842ba5bd-f867-48e1-b2b2-a98668d6b45c' width=800>

### 2. Modelfile을 통한 모델 설치

#### 2-1. 파일 위치 지정

Hugging Face에서 다운로드한 `.gguf` 파일과 `Modelfile`을 동일한 디렉토리에 위치시킨다.

<img src='https://github.com/user-attachments/assets/f9c2c01d-e959-431b-818f-461e151c6090' width=600>

#### 2-2. Modelfile 수정

Modelfile 내 `FROM` 구문을 다운로드한 `.gguf` 파일 이름으로 수정한다.

```dockerfile
FROM gemma3-Wine-Guid.Q8_0.gguf

TEMPLATE """{{- if .System }}
<s>{{ .System }}</s>
{{- end }}
<s>Human:
{{ .Prompt }}</s>
<s>Assistant:
"""

SYSTEM """A chat between a curious user and an artificial intelligence assistant. The assistant gives helpful, detailed, and polite answers to the user's questions."""

PARAMETER temperature 0
PARAMETER num_predict 3000
PARAMETER num_ctx 4096
PARAMETER stop <s>
PARAMETER stop </s>
```

#### 2-3. Powershell을 통한 모델 추가

다음 명령어를 통해 Local 환경에 모델을 설치한다.

```shell
cd [.gguf 및 Modelfile 위치]
ollama create gemma3-wine -f Modelfile
```

설치가 완료되면 `ollama list` 명령어로 모델이 추가된 것을 확인할 수 있다.

<img src='https://github.com/user-attachments/assets/4ac8d91f-8546-41d1-b57e-6e86f4d4f520' width=600>

<br>

## 12. 이슈 및 해결방법

### 1. AWS

![Image](https://github.com/user-attachments/assets/79e49e71-3a67-4847-a0dc-7da61436c053)

#### 원인

-   컨테이너 이미지를 pull하거나 layer를 추출하는 과정에서 **작업 노드의 디스크 용량 부족**으로 인해 실패함.

#### 해결 방법

-   결국 CICD를 구축하는 것은 완성하지 못했으나, 찾아본 방법으로는 EC2 컨테이너에 파인튜닝된 모델을 업로드 하여, CICD 파이프라인에 연결한다면, 문제 없이 구축될 가능성을 확인했다.

<br>

### 2. Django Admin

#### 원인

-   CustomUserAdmin에서 슈퍼유저 권한에 대한 메서드를 설정하지 않아, 슈퍼유저임에도 Admin 화면에서 추가·수정·삭제·조회 기능이 제한됨.
    특히 has_delete_permission만 커스터마이즈하면서 다른 권한 메서드를 건드리지 않아, 슈퍼유저도 일부 권한이 비활성화되는 상황 발생

#### 해결 방법

-   슈퍼유저가 모든 기능을 사용할 수 있도록 메서드들을 오버라이드하고, 로그인한 사용자가 superuser일 때 관리자로서 권한을 사용할 수 있도록 설정.

<br>

## 13. 회고

### 문승기

-   팀장으로서 첫 프로젝트이다 보니, 부담과 압박감이 심했던 것 같습니다다. 하지만, 팀원들이 자기주도적으로 열심히 참여하려는 모습에 감사했고, 마지막까지 최선을 다할 수 있었던 동기부여가 되었습니다.

### 배민경

-   열정적인 팀장님 덕분에 좋은 프로젝트를 즐겁게 완료할 수 있어서 너무 좋은 시간이었습니다. 팀원들도 서로 격려와 응원으로 개발 위기를 잘 넘겼습니다. AWS가 결국 안되서 너무 아쉽고 조금 더 시간이 있었더라면 더 좋은 결과가 나올 수 있을 것 같아서 아쉽습니다.

### 신민주

-   실력이 많이 부족해서 간단한 기능 구현도 시간이 오래 걸리고 많이 헤맸는데 다들 많이 도와주시고, 특히 팀장이 참고 사이트부터 요령도 알려주셔서 많은 도움이 되었습니다. 이제까지 단위 프로젝트를 진행한 경험으로 최종 프로젝트도 열심히 참여하겠습니다.

### 좌민서

-   이번이 마지막 단위 프로젝트였던 만큼 더 잘해보고 싶었는데 저의 실력 부족으로 생각만큼 잘 해내지 못한 것 같아서 아쉬웠습니다. 전반적으로는 잘 진행되었지만, 마지막 AWS 배포 단계에서 계속 오류가 발생해서 속상했습니다. 비록 이번에는 배포에 성공하지 못했지만, 오류를 검색하고 해결해 나가는 과정에서 AWS에 대해서 많이 배울 수 있었습니다. 다음에 기회가 또 있다면 그때는 꼭 배포에 성공해 보고 싶습니다. 마지막으로 함께 고생해준 팀원들 너무 잘해주셨고 수고 많으셨습니다.

### 홍승표

-   프로젝트를 진행하면서 막히는 부분이 많았다. 생각치도 못한 곳에서 오류가 발생했고 오류 코드가 없는 오류가 발생하기도했다. 그래도 어떻게든 주변 사람들과 gpt의 도움을 받아서 잘해결했다. 마지막 단위 프로젝트를 무사히 끝내서 다행이고, 고생해준 팀원들에게 감사하다.

<br>
