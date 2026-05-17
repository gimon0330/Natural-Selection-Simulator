# Natural Selection Simulator

Pygame으로 구현한 자연선택 시뮬레이터입니다.

부산일과학고등학교 생명과학II 프로젝트로 제작했던 코드를 기반으로, 포식자와 피식자의 상호작용을 통해 세대가 지나며 피식자의 형질이 어떻게 달라질 수 있는지 시각적으로 관찰할 수 있도록 다시 정리했습니다.

## Concept

이 프로젝트는 복잡한 생태계를 정확히 재현하기보다, 자연선택의 핵심 아이디어를 간단한 rule-based simulation으로 보여주는 것을 목표로 합니다.

시뮬레이션의 기본 가정은 다음과 같습니다.

- 검은 원은 prey입니다.
- 붉은 원은 predator입니다.
- 낮 동안 predator와 prey는 공간을 움직입니다.
- predator와 prey가 충돌하면 prey가 제거됩니다.
- 하루가 끝나면 살아남은 prey가 번식합니다.
- offspring은 parent의 speed와 size를 물려받되, 작은 mutation이 발생합니다.
- 생존에 유리한 trait은 다음 세대에 더 많이 남을 가능성이 커집니다.

즉, 이 시뮬레이터는 `selection pressure → survival → reproduction → mutation → population change`의 흐름을 직관적으로 보여주기 위한 프로젝트입니다.

## What Changed

기존 코드는 실험용 script에 가까웠고, 여러 파일에 비슷한 predator/prey logic이 반복되어 있었습니다.

이번 정리에서는 결과물의 의도는 유지하되, `main.py`를 거의 새로 작성했습니다.

### 개선한 점

- `SimulationConfig`, `Stats`, `Creature`, `Prey`, `Predator`, `Simulation`으로 역할 분리
- day/night cycle을 명확하게 분리
- prey의 `speed`, `radius` trait이 reproduction 과정에서 mutation되도록 구조화
- predator가 prey를 추적하고, prey는 가까운 predator로부터 도망가도록 개선
- population history graph 추가
- pause/reset/quit control 추가
- magic number를 config로 이동
- 실행 방법과 프로젝트 의도 문서화

## Repository Structure

```text
.
├── main.py                  # Refactored simulator
├── prey_and_pred_reflect.py # Original experiment file
├── prey_and_pred_size.py    # Original experiment file
├── requirements.txt
└── README.md
```

## Installation

```bash
pip install -r requirements.txt
```

## Run

```bash
python main.py
```

## Controls

```text
SPACE  pause / resume
R      reset simulation
ESC    quit
```

## Simulation Model

### Prey

Prey has two major traits.

```text
speed
radius
```

- Faster prey can escape predators more easily.
- Larger prey may be easier to collide with and consumes more simulated energy.
- Offspring inherit the parent traits with random mutation.

### Predator

Predator moves toward the nearest prey and eats prey on collision.

At the end of the day:

- Predators that eat enough prey survive.
- Predators that fail to eat enough prey disappear.
- Predators may reproduce if enough prey were eaten.

### Selection

At the end of each day, surviving prey reproduce. Since prey that are caught do not reproduce, the trait distribution of the population gradually changes.

This is a simplified natural selection model, not a biologically exact simulation.

## Project Note

이 프로젝트는 생명과학 개념을 코드로 직접 실험해보려는 시도였습니다.

처음 만들 당시에는 코드 구조가 많이 복잡했고, predator와 prey의 움직임, 충돌, 번식, mutation이 한 파일 안에 뒤섞인 spaghetti code에 가까웠습니다. 하지만 그만큼 “생명과학에서 배운 개념을 눈에 보이는 simulation으로 만들 수 있다”는 경험이 컸습니다.

이번 refactoring을 통해 같은 아이디어를 더 읽기 쉬운 구조로 다시 구성했습니다.

## Known Limitations

- 실제 생태계와 달리 환경, 자원, 성별, 유전형/표현형 구분은 단순화되어 있습니다.
- trait은 `speed`와 `radius`만 사용합니다.
- predator/prey movement는 rule-based입니다.
- 통계 분석보다는 시각적 이해를 우선한 simulation입니다.

## Future Ideas

- trait distribution histogram 추가
- predator trait mutation 추가
- food/resource system 추가
- 여러 환경 구역 추가
- CSV export 기능 추가
- experiment preset 기능 추가
