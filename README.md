# Evidence LLM Council

근거를 먼저 수집하고, 여러 관점의 검토를 거쳐 의사결정을 돕는 에이전트 스킬입니다. 사실(F), 해석(I), 미확인(U)을 구분하고 최종 주장과 출처를 연결합니다.

## 목적

전략 선택, 기술 설계, 프로젝트 회고에서 그럴듯한 의견과 확인 가능한 사실을 구분합니다. 자료 수집 → 중립 브리핑 → 다섯 관점 검토 → 익명 교차 검토 → 종합 판단 → 근거 검증 순서로 진행합니다.

## 기대효과

- 주장별 근거 ID와 출처를 남겨 검토와 후속 확인이 쉬워집니다.
- 반론, 실행 가능성, 이해관계자 관점을 함께 살펴 누락된 위험을 찾도록 돕습니다.
- 자료 부족과 상충하는 근거를 드러내 과도한 확신을 줄이도록 설계했습니다.
- 같은 형식으로 반복 평가하고, 판단이 바뀐 이유를 추적할 수 있습니다.

효과는 설계상 기대이며 정량적으로 검증된 성능 주장은 아닙니다. 다섯 개의 서로 다른 LLM을 자동 호출하는 프로그램이 아닙니다. 호스트가 지원하면 별도 에이전트를 활용하고, 그렇지 않으면 순차 검토임을 밝혀야 합니다. 동료 검토의 합의는 사실의 독립 검증이 아닙니다.

## 설치

Codex용 로컬 스킬 설치 예시입니다. Git과 검증용 Python 3이 필요합니다. Python 검증기는 표준 라이브러리만 사용합니다.

```sh
mkdir -p "$HOME/.agents/skills"
git clone https://github.com/probees1492/evidence-llm-council.git "$HOME/.agents/skills/evidence-llm-council"
```

같은 경로에 스킬이 있으면 덮어쓰지 말고 기존 내용을 먼저 확인하세요. 프로젝트 전용 설치는 프로젝트의 `.agents/skills/evidence-llm-council` 경로를 사용하세요. 인식되지 않으면 Codex를 다시 시작하세요. [공식 설치 경로 안내](https://learn.chatgpt.com/docs/build-skills)를 참고하세요.

ZIP으로 설치하려면 GitHub의 **Code → Download ZIP**을 선택하고 압축을 푼 폴더 이름을 `evidence-llm-council`로 바꾼 뒤 위 스킬 경로에 넣으세요. `SKILL.md`뿐 아니라 `scripts/`, `references/`, `examples/`도 함께 복사해야 합니다. 다른 호스트의 설치 위치와 지원 기능은 해당 제품 문서를 확인하세요.

## 활용법

설치 후 다음처럼 요청합니다.

```text
$evidence-llm-council
근거 기반 카운실 decision 모드로 이번 프로젝트의 두 아키텍처 대안을 평가해줘.
최근 2개월의 내가 제공한 문서와 접근 허용한 저장소만 사용해.
사실/해석/미확인을 구분하고, 근거 ID와 반론, 리스크, 다음 행동을 포함해줘.
```

| 모드 | 용도 |
| --- | --- |
| `decision` | 기본 모드. 대안 비교와 전체 교차 검토 |
| `fact-only` | 판단 없이 사실과 근거 정리 |
| `audit` | 출처 추적, 누락, 모순 점검 |
| `fast` | 핵심 사실과 간소화한 관점 검토. 검토 강도가 낮음을 표시 |

요청할 때 질문, 대안, 평가 기간, 허용 자료, 제약, 원하는 산출물을 함께 알려주세요. Jira·Confluence·Gmail 등의 접근 권한이나 연결 기능은 스킬 설치만으로 생기지 않습니다. 연결이 없으면 직접 제공한 자료로 진행합니다.

## 산출물과 검증

결과에는 요약, 자료 범위와 한계, 사실과 근거, 관점별 이견, 조건부 판단, 리스크, 다음 행동이 포함됩니다. 파일 생성 시 `evidence/ledger.json`과 `report/claims.json`을 작성합니다.

설치 폴더에서 예제를 검증할 수 있습니다.

```sh
python3 scripts/validate_report.py --ledger examples/ledger.json --claims examples/claims.json
```

예상 결과: `PASS: 1 evidence / 3 claims / 0 errors / 0 warnings`

실제 보고서는 해당 파일의 경로를 인수로 전달하세요. 검증기는 ID, 필수 필드, 근거 참조 같은 구조를 확인합니다. 인용 내용이 주장을 뒷받침하는지, 원문이 사실인지, 날짜와 수치가 맞는지는 사람이거나 에이전트가 별도로 확인해야 합니다. 예제는 가상 데이터이며 실제 문서가 있다는 뜻이 아닙니다.

## 구성

- `SKILL.md`: 에이전트 실행 절차
- `references/evidence-schema.md`: 근거 원장 형식
- `references/claims-schema.md`: 주장 형식
- `examples/`: 가상 예제 데이터
- `scripts/validate_report.py`: 구조 검증기
- `PUBLICATION_REVIEW.md`: 공개 전 점검 범위와 결과

## 개인정보와 보안

공개 저장소에는 실제 조사 자료나 생성 보고서를 넣지 마세요. 출처 발췌에는 비밀키·개인정보·고객 정보를 넣지 않고, 사내 자료를 외부 모델이나 서비스로 전송하려면 별도 권한을 확인해야 합니다. 검증 스크립트는 지정된 JSON 파일을 로컬에서 읽으며 네트워크 요청을 하지 않습니다.

## 출처와 라이선스 상태

이 스킬은 [aiwithremy/claude-skills-llm-council](https://github.com/aiwithremy/claude-skills-llm-council)의 다섯 관점 및 교차 검토 방식에서 출발해 근거 수집, 출처 추적, 사후 검증을 추가한 로컬 패키지입니다. 원본 README는 제작자를 Ole Lehmann으로 소개하고 Andrej Karpathy의 LLM Council 방법론을 출처로 명시합니다.

2026-10-28에 확인한 원본 커밋 `55ee36e89e0f3f780099ac50332fbb3ec8d14738`에는 LICENSE 파일이 없고 GitHub 라이선스 값도 null이었습니다. 이 패키지에도 기존 LICENSE 파일이 없어 MIT 등 별도 라이선스를 임의로 부여하지 않았습니다. 공개 열람이 포괄적인 사용·수정·재배포 허가를 뜻하지는 않습니다. 원본 유래 부분의 권리와 재배포 허가는 미확인 상태이며, 이 저장소는 라이선스 검토 완료 또는 오픈소스 라이선스 부여를 주장하지 않습니다.
