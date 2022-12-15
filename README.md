# P 개발자의 J되기 프로젝T

서비스 주소: https://pjt.vercel.app/ <br>
깃허브 프론트엔드: https://github.com/hvvany/pjt-frontend <br>
깃허브 백엔드 : https://github.com/kimdakyeom/PJT_backend

## 초보 개발자들을 위한 개발 일정 관리 서비스 🧐

![](https://velog.velcdn.com/images/hvvany/post/d4b22e67-6de4-4a05-a131-4b2e553d38b9/image.png)

> `PJT`라는 이름은 `MBTI`에서 영감을 받은 네이밍입니다. `즉흥적인 P 개발자`가 아닌 `계획적인 J개발자`가 될 수 있게 도와주는 서비스입니다 🙂

> PJT 사이트는 기존의 `복잡하고 사용이 어려운` 일정 관리 서비스들에 비하여 `좀 더 쉽고 직관적`이게 사용할 수 있게 제작하였습니다.

<br>

## 배포 주소

👉🏻 https://pjtpjt.tk/

<br>

# 팀 구성

@SeBin-Kwon
@kimdakyeom
@hvvany
@nevertheless0404
@tenedict
[![](https://velog.velcdn.com/images/hvvany/post/de8b26fe-1978-49e8-8235-3024c17400ca/image.png)](https://github.com/hvvany/pjt-frontend/graphs/contributors)

<br>

# 프로젝트 수행 도구

## 프론트엔드

![](https://img.shields.io/badge/Vue.js-35495E?style=for-the-badge&logo=vuedotjs&logoColor=4FC08D)![](https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white)![](https://img.shields.io/badge/Vercel-000000?style=for-the-badge&logo=vercel&logoColor=white)

## 백엔드

![](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=green)![](https://img.shields.io/badge/django%20rest-ff1709?style=for-the-badge&logo=django&logoColor=white)![](https://img.shields.io/badge/Amazon_AWS-232F3E?style=for-the-badge&logo=amazonaws&logoColor=white)![](https://img.shields.io/badge/Amazon_S3-569A31?style=for-the-badge&logo=amazons3&logoColor=white)![](https://img.shields.io/badge/Amazon_RDS-527FFF?style=for-the-badge&logo=amazonrds&logoColor=white)

## 데이터 베이스

![](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)![](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)

<br>

# 프로젝트 일정

11/25 ~ 11/28 : 서비스 기획

11/29 ~ 12/1 : vue & drf 학습

12/1 ~ 12/3 : CRUD 작성 및 기본 템플릿 작성

12/4 ~ 12/6 : 주요 기능 다 넣기, 부가 기능 하나씩 추가

12/7 : 백엔드 서버 배포

12/8 ~ 12/11 : 오류 해결

12/12 : 프론트엔드 서버 배포 및 백엔드와 연결

12/13 ~ 12/14 : 기능 마무리 & PPT 제작

12/15 : 프로젝트 발표

<br>


# 서비스 소개

## 주요 기능

- `프로젝트 CRUD`및 `캘린더` 반영
- `칸반보드`(드래그 & 드롭) 기능
- 팀원 추가 및 관리
- `마크다운` 코드 생성
- 댓글 및 댓글 `알림` 기능
- 프로젝트별 공지사항
- 인사이트 UI

<br>

## 개발 이슈

![](https://velog.velcdn.com/images/hvvany/post/d4191896-9da1-4eb4-beeb-1ab7d0738131/image.png)

---

### 1. 역참조 이슈

### ⁉️ 에러 메세지

projects.Todo.project: (fields.E304) Reverse accessor 'User.todo_set' for '
projects.Todo.project' clashes with reverse accessor for 'projects.Todo.user'.

HINT: Add or change a related_name argument to the definition for 'projects.Todo.project' or 'projects.Todo.user'.
projects.Todo.user: (fields.E304) Reverse accessor 'User.todo_set' for 'proprojectjects.Todo.user' clashes with reverse accessor for 'projects.Todo.project'.

HINT: Add or change a related_name argument to the definition for 'projects.Todo.user' or 'projects.Todo.project'.

### ⭕️ 해결 방법

1. 같은 class 내에서 여러개의 `ForeignKey`를 사용해야 할때는, `related_name`을 추가하여 역관계 충돌이 일어나지 않게 하기
2. 다른 class 내에서 같은 `ForeignKey.related_name`을 사용한다면, 이름을 별도로 지정하거나 %(class)를 추가하기

---

### 2. npm run serve 이슈

### 팀원의 프로젝트를 새로 클론 받은 후, 갑작스러운 npm run serve 에러

```bash
> pjt-frontend@0.1.0 serve
> vue-cli-service serve

sh: vue-cli-service: command not found
```

### macOS 기준

분명 node, npm, vue 잘 설치 되어 있는데 자꾸 명령어가 없다고 떴다.

> 깃허브에 푸쉬할 때, `node_modules` 폴더가 `.gitignore`에 걸러지면서 발생한 것 같다.

일단 뭐가 잘 안될 땐 모두가 삭제 및 재설치를 하라고 한다.

[[Mac] - node, npm 삭제 및 재설치](https://velog.io/@hrzo1617/Mac-node-npm-%EC%82%AD%EC%A0%9C-%EB%B0%8F-%EC%9E%AC%EC%84%A4%EC%B9%98)

- mac node/npm 설치
  - `brew install node`

### 그래도 안됬다.

보통 node를 install하면 node_modules 폴더와 package-lock.json 파일이 생겨야 하는데

아무리 통으로 삭제 및 재설치를 해도 생기지 않았다.

```bash
npm ERR! code ERESOLVE
npm ERR! ERESOLVE unable to resolve dependency tree
npm ERR!
npm ERR! While resolving: pjt-frontend@0.1.0
npm ERR! Found: eslint-plugin-vue@8.7.1
npm ERR! node_modules/eslint-plugin-vue
npm ERR!   dev eslint-plugin-vue@"^8.0.3" from the root project
npm ERR!
npm ERR! Could not resolve dependency:
npm ERR! peer eslint-plugin-vue@"^7.0.0" from @vue/eslint-config-standard@6.1.0
npm ERR! node_modules/@vue/eslint-config-standard
npm ERR!   dev @vue/eslint-config-standard@"^6.1.0" from the root project
npm ERR!
npm ERR! Fix the upstream dependency conflict, or retry
npm ERR! this command with --force, or --legacy-peer-deps
npm ERR! to accept an incorrect (and potentially broken) dependency resolution.
npm ERR!
npm ERR! See /Users/kwonsebin/.npm/eresolve-report.txt for a full report.

npm ERR! A complete log of this run can be found in:
npm ERR!     /Users/kwonsebin/.npm/_logs/2022-11-29T15_20_35_405Z-debug-0.log
```

### 해결 방법

[Fix the upstream dependency conflict installing NPM packages](https://stackoverflow.com/questions/64936044/fix-the-upstream-dependency-conflict-installing-npm-packages)

```bash
npm install --legacy-peer-deps
```

- 2년전 글인데도 불구하고 아직도 npm 최신 버전은 오류가 많은 것 같다.

---

### 3. 다양한 vue 에러사항

### new line required at end of the file

![](https://velog.velcdn.com/images/hvvany/post/ca5f5bec-0aec-46c7-97e7-705bfc937143/image.png)
vue는 마지막 줄에 엔터 한 번은 무조건 필요하다.

### semicolon

![](https://velog.velcdn.com/images/hvvany/post/f3e3b043-1a5f-4378-860b-baacaf036eeb/image.png)

vue에서는 세미콜론 쓰지 않기..?

### 문자열은 “ 말고 ’ 사용

![](https://velog.velcdn.com/images/hvvany/post/a01b8834-2875-46bd-ba6f-83d3d4a56c3f/image.png)

### 콤마, 스페이스

![](https://velog.velcdn.com/images/hvvany/post/7f7cb4c0-a74b-4d2c-bf35-11774e8a3e68/image.png)

쓸데 없는 마지막 콤마 삭제

함수이름 () 이거 사이에 공백 필수

### 원인

⇒ 코드 컨벤션 때문…!

프리티어 ⇒ 문법 추가?

[VSCode 저장시에 자동정렬 설정 (Prettier) - 적용 안됨 고치는법 포함](https://shoney.tistory.com/entry/VSCode-%EC%A0%80%EC%9E%A5%EC%8B%9C%EC%97%90-%EC%9E%90%EB%8F%99%EC%A0%95%EB%A0%AC-%EC%84%A4%EC%A0%95-Prettier-%EC%A0%81%EC%9A%A9-%EC%95%88%EB%90%A8-%EA%B3%A0%EC%B9%98%EB%8A%94%EB%B2%95-%ED%8F%AC%ED%95%A8#:~:text=Ctrl%20%2B%20S%20%EB%A5%BC%20%EB%88%8C%EB%A0%80%EC%9D%84%20%EB%95%8C,Prettier%EB%A5%BC%20%EB%8B%A4%EC%9A%B4%EB%B0%9B%EC%95%84%EC%A4%80%EB%8B%A4.&text=%EC%B2%B4%ED%81%AC%EB%B0%95%EC%8A%A4%EC%97%90%20%EC%B2%B4%ED%81%AC%EA%B0%80%20%EC%97%86%EC%9C%BC%EB%A9%B4%20%EC%9E%90%EB%8F%99%EC%A0%95%EB%A0%AC%20%EC%95%88%EB%90%9C%EB%8B%A4)

---

### 4. 400error ( json → querydict → parsing → json)

![](https://velog.velcdn.com/images/hvvany/post/ea5c9632-8e49-4a74-96eb-e1e3cc820b1f/image.png)

Vue 에서 post 로 json 넘김

⇒ django에서는 querydict로 데이터가 받아짐

⇒ json 파싱 필요 ⇒ json 변환

many = True 도 data 뒤에 존재하는 것을 제거하니 완전히 db로 잘 넘어가짐!!!!!!!

![](https://velog.velcdn.com/images/hvvany/post/5c2ca8c6-789a-4eaa-8e73-8e08291cc077/image.png)

---

### 5. class이름 이슈

class이름이랑 저장소이름을 똑같이 해버려서 에러 계속 떠서 어이없었는데 비모쌤와서 알려주고 완전 어이없어서 웃겼다. 앞으로 이런 실수 안해야겠다 ㅠㅠ

---

### 6. 소셜 로그인 이슈

![](https://velog.velcdn.com/images/hvvany/post/ebe95b0c-6ad4-411a-9a9d-2fc368c79062/image.png)

- 구글 소셜 로그인에 자꾸 리다이렉트 에러가 났다..

- admain 페이지에 들어가려고 했더니 Site matching query does not exist. 가 났다..
  - DB를 삭제하고 aullauth랑 연동? 하면서 Django가 DB에 갖고 있던 사이트 정보가 사라진 것이 원인이다.

![](https://velog.velcdn.com/images/hvvany/post/f78c8d6a-1167-40c4-9f93-485da0238286/image.png)

- shell 작업을 통해 Site 객체를 다시 DB에 입력

![](https://velog.velcdn.com/images/hvvany/post/0f467f09-f3a3-45ba-88bf-c702d6d5aa0b/image.png)

- site_id를 확인하고 해당 번호로 변경
- 구글 소셜 로그인까지 잘 된다. 갑자기 웨뒈..?

---

### 7. pk값이 객체가 아니여서 안들어감

![](https://velog.velcdn.com/images/hvvany/post/b1ad3c0a-240a-4c80-a95a-1113621521a3/image.png)

---

### 8. axios request 400 error

### vue form

```html
<form
  class="w-50 d-flex flex-column align-items-center"
  @submit.prevent="submitForm"
></form>
```

form 태그 사용 시 .prevent 로 새로고침 방지를 해야한다.

### src/api/index.js \_ axios 분리

```jsx
import axios from 'axios'

function registerUser(userData) {
  // 요청할 URL
  const url = 'http://127.0.0.1:8000/api/accounts/v1/registration/'
  console.log('userData :', userData)
  return axios.post(url, userData, {
    'Content-Type': 'application/json'
  })
}

// 함수 export
export { registerUser }
```

### headers 추가

{‘Content-Type’ : ‘application/json’}

### async, await 사용

```jsx
export default {
  data() {
    return {
      // form
      email: '',
      password1: '',
      password2: '',
      // log
      logMessage: ''
    }
  },
  methods: {
    async submitForm() {
      // API 요청시 전달할 userData 객체
      const userData = {
        email: this.email,
        password1: this.password1,
        password2: this.password2
      }
      const { data } = await registerUser(userData)

      this.logMessage = `${data.email} 님이 가입되었습니다.`

      // 가입 후 폼 초기화
      this.initForm()
    },
    initForm() {
      this.email = ''
      this.password1 = ''
      this.password2 = ''
    }
  }
}
```

---

### 9. 로그인 403 forbidden

로그인 한 후 local storage에 acces_token이 잘 저장되고, 홈 화면에서 토큰으로 로그인 유저 정보를 가져올 때 자꾸 403 forbidden error가 떴다…..

암걸리는줄………….

비모쌤이 drf에서 jwt 인증 허용이 안되있는거 아니냐고 하셨다….

```jsx
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'dj_rest_auth.jwt_auth.JWTCookieAuthentication',
    )
}
```

dj_restauth 공식문서 맨 밑에 박혀있던 \***\*JSON Web Token (JWT) Support (optional)\*\*** 에서 찾아와주셨다…

![](https://velog.velcdn.com/images/hvvany/post/13461eca-349d-4653-a614-2bf0bc46835a/image.png)

---

### 10. post 요청시 DB 저장 이슈

```jsx
<script>
import draggable from 'vuedraggable'
export default {
  components: { draggable },
  data() {
    return {
      newTask: [
        {
          title: '',
          content: '',
          start_at: '',
          end_at: ''
        }
      ],
      arrBacklog: [{ title: '', content: '', start_at: '', end_at: '' }],
      arrInProgress: [],
      arrDone: [],
      modalData: []
    }
  },
  setup() {},
  created() {},
  mounted() {},
  unmounted() {},
  methods: {
    showModal(element) {
      this.$refs['my-modal'].show()
      console.log('element: ', element)
      this.modalData = element
    },
    hideModal() {
      this.$refs['my-modal'].hide()
    },
    todoAdd() {
      if (this.newTask) {
        this.arrBacklog.push({
          title: this.newTask.title,
          content: this.newTask.content,
          start_at: this.newTask.start_at,
          end_at: this.newTask.end_at
        })
        console.log('이번 투두 :', this.arrBacklog)
        this.newTask.title = ''
        this.newTask.content = ''
        this.newTask.start_at = ''
        this.newTask.end_at = ''
        this.$refs['modal'].hide()
      }
    },
    add() {}
  },
  createModal() {}
}
</script>
```

### 이동근님이 해결해주심

클라우드여서 저장이 안됨 DB자체도 생성이 안되더라 ⇒ 클라우드에 수십개 데이터 쌓였을듯 ㅜㅜ

### 해결방법

.env

```bash
DEBUG = True
```

False로 되어있어서 안된거임

---

### 11. post 요청 시 DB 저장 이슈

서버 True False 설정 확인!!!

푸쉬 하고 풀 당기고 하다보니 누군가가 DEBUG = False 로 해놓으면 갑자기 로컬 서버가 아닌 배포 서버로 데이터가 간다. 항상 잘 확인하자..!

<br>
<br>

## 프로젝트 후기

- **김준환** : VUE와 DRF를 활용하여 처음으로 프론트/ 백 나누어 진행해보았다. 서로의 충돌을 최소화 하며 실제 현업의 경험을 할 수 있었다. 처음에 구현하고자 하는 기능들 중에서 핵심 기능 우선순위로 개발을 하였고 그 결과 모든 기능을 구현 성공하였다. 반응형도 고려하여 프로젝트 완성도를 높였다. 새로운 프레임워크를 사용하며 새로운 기술을 학습할 수 있어서 좋았다.
- **권세빈** : Vue를 이용해 백엔드와 데이터를 주고받으며 프론트 기능을 개발해보는 경험을 할 수 있어서 좋았습니다. 필수 기능을 위주로 개발하여 최대한 프로젝트 기획 의도와 맞췄고, 계속 디벨롭을 하며 완성도를 높여서 뿌듯했습니다. 이번 프로젝트는 특히 실무와 가깝다고 느껴지며 프론트 관련 학습을 더욱 진행해야겠다고 느꼈습니다.
- **김다겸** : 교육기간에 배운 django 내용을 활용하여 더 나아가 vue와 django rest framework를 통해 프로젝트를 진행하면서 익숙하지 않아 힘든 점이 많았지만 야생학습을 통해 새로운 기술을 학습해나가는 방법을 배울 수 있었다. 새로운 기술, 프레임워크 등을 학습하는 부분에 대해 자신감을 얻을 수 있던 프로젝트였다.
- **김유영** : Vue와 DRF를 야생학습으로 배우면서 프로젝트를 진행하니 어려운 점도 많았지만 그 만큼 어떻게 공부해야하는지 깨닫게 되었으며, 프론트와 백엔드를 확실히 나눠서 프로젝트를 진행하여 협업에 대해서 많이 배우게 되었던 프로젝트이다.
- **문재윤** : DRF를 처음 다뤄보는 프로젝트라 준비기간도 길었고 많이 낯설었다. 하지만 처음으로 스스로 공부를 했던만큼 앞으로 다른 것을 배울때 어떤식으로 배워야하는지 감이 잡혔고 매우 뿌듯했다. 결과물도 새로운 프레임워크로 시작을해서 확신이 없었지만 기대이상으로 잘 된것 같아서 자신감이 올라간 것 같다.
