## GenAI Evaluation Service and Prompt Optimizer

## 실습 준비

#### 상단 검색 메뉴에서 'workbench' 를 입력하여 'Workbench' 메뉴를 클릭합니다.
![image](https://raw.githubusercontent.com/jk1333/handson/main/images/6/1.png)

#### 2. 'Open Jupyterlab' 버튼을 눌러 환경에 접속합니다.
![image](https://raw.githubusercontent.com/cheeunlim/agent-engine-lab/main/images/workbench_open.png)

실행된 Jupyterlab 환경에서 Terminal에 진입 후 아래 명령어를 실행해 실습자료를 다운로드 받습니다.

```
pip install google-adk
pip install --force-reinstall google-cloud-aiplatform==1.162.0 google-genai==2.14.0
pip install --upgrade scikit-learn
git clone https://github.com/jk1333/genai_evaluation
```

---

## Module 1: Evaluation UI 를 이용한 평가 (Single turn only)

실습 노트북: text_multiturn_api_eval.ipynb

노트북 전체를 실행하면 생성되는 'single_reference.jsonl' 과 'single_response_free.jsonl' 을 로컬 PC에 다운로드 받습니다.

상단 검색 메뉴에서 'agent platform' 을 검색해 메뉴로 진입합니다.

진입 후 Overview -> Evaluation 메뉴를 클릭합니다.

![image](https://raw.githubusercontent.com/jk1333/handson/main/images/8/1.png)

Upload 버튼을 눌러 'single_reference.jsonl' 을 업로드 합니다.

![image](https://raw.githubusercontent.com/jk1333/handson/main/images/8/2.png)

아래 그림과 같이 예제 데이터셋에서 데이터를 선택해 평가할 내용을 준비합니다.

![image](https://raw.githubusercontent.com/jk1333/handson/main/images/8/3.png)

+Add Metric 을 클릭하여 'General Quality' 를 선택 후 저장합니다.

아래 그림과 같이 준비가 되면 하단의 'Evaluate' 버튼을 클릭합니다.

![image](https://raw.githubusercontent.com/jk1333/handson/main/images/8/4.png)

아래 그림과 같이 결과가 나오면 평가 결과 셀을 클릭하여 결과를 확인합니다.

![image](https://raw.githubusercontent.com/jk1333/handson/main/images/8/5.png)

![image](https://raw.githubusercontent.com/jk1333/handson/main/images/8/6.png)

다시 메인 메뉴로 돌아가서 Upload 버튼을 눌러 'single_response_free.jsonl' 을 업로드 합니다.

이번에는 아래 그림과 같이 Response 는 'gemini-3.7-flash' 로 동적 생생 후 결과를 살펴봅니다.

![image](https://raw.githubusercontent.com/jk1333/handson/main/images/8/7.png)

---

---

## Module 2: Evaluation API 를 이용한 평가 (Multi turn)

실습 노트북
```
text_multiturn_api_eval.ipynb
```

---

---

## Module 3: Agent 평가 (Whitebox, Blackbox by Agent Runtime)

실습 노트북
```
agent_eval.ipynb
```

---

---

## Module 4: Agent trajectory 평가

실습 노트북
```
trajectory_eval.ipynb
```

---

---

## Module 5: Translation 평가

실습 노트북
```
translation_eval.ipynb
```

---

---

## Module 6: Image / Video generation 평가

실습 노트북
```
image_video_api_eval.ipynb
```

---

---

## Module 7: Prompt Optimizer

실습 노트북
```
custom_metric_optimizer.ipynb
```

---