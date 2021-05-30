# Big data

### 🚀️ 유튜브 댓글 수집

##### 👍 작업순서

**1. 유튜브 댓글 데이터 가져오기**

1. Selenium으로 전체를 가져올 경우 로딩 시간으로 인해 너무 느림.
2. Youtube API를 사용해서 가져오는 방법 선택.
3. 각각을 필요한 상황에 맞게 사용함.

**2. 수집 데이터 Pandas DataFrame으로 변환하기**

**3. 데이터 분석**

1. 유해 댓글 찾기가 목적이었으나..
2. 유튜브 인기동영상들의 평균 댓글 수를 시각화.
3. 인기동영상 카테고리마다 100개씩 댓글뽑아서 유해 댓글 존재 체크, 어떤 카테고리에서 가장 많이보이는 지 시각화.
4. 쁘걸 동영상에서 댓글 키워드 분석 워드클라우드 시각화, 감정분석 시도. (패스😄)

**4. 스팸 댓글 분류**

1. 스팸메일을 구분하는 방법을 적용. 데이터를 직접 생성해야 함.
2. 차단 댓글에 등록하거나 사용자를 차단하는 것을 Selenium으로 자동화해볼 예정. (진행중😄 )

**5. 앞으로 진행 예정**

1. 프로그램 화 진행
2. 더 많은 스팸 댓글 데이터 필요.

##### 👍 참고 URL

1. [Selenium공부](<https://www.youtube.com/watch?v=yQ20jZwDjTE](https://)>)

2. [Youtube API 이용 & CSV, JSON변환(유료, API이용법만 참고)](https://www.youtube.com/watch?v=Mzj3_FjuDuI)

3. [CNN 스팸 메일 분류 -> 유튜브 댓글 분류](https://www.youtube.com/watch?v=QejZQ0Dh5x8&list=PL7ZVZgsnLwEEoHQAElEPg7l7T6nt25I3N&index=11)
