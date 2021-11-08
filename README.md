# 튜링 과제
## Models
### `Board`
```python
class Board(models.Model):
    password = models.CharField(max_length=50, null=False)
    title = models.CharField(max_length=50, null=False)
    content = models.TextField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```
- `id`: 게시판 id
- `title`: 게시판 제목
- `content`: 게시판 내용
- `created_at`: 게시판 생성일시
- `updated_at`: 최근 게시판 변경일시
- `password`: 게시판 암호

### `Comment`
```python
class Comment(models.Model):
    password = models.CharField(max_length=50, null=False)
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField(null=False)
```
- `id`: 댓글 id
- `board`: 댓글이 달린 `board` 외래키
- `content`: 댓글 내용
- `password`: 댓글 암호
## API
### Base URL
- https://0qnhnw8vm2.execute-api.ap-northeast-2.amazonaws.com/dev
### `게시물 생성`
#### Request
```
method: POST
path: /api/board/
Content-type: json
data: {
    title: "게시판 제목", # CharField, 최대 50자
    content: "게시판 내용입니다.", # TextField
    password: "password1234", # 게시판 암호, 수정/삭제시 사용
}
```
#### Response
```
code: 201
Content-type: json
data: {
    id: 1,
    title: "게시판 제못",
    content: "게시판 내용입니다.",
    created_at: "2021-11-08T12:00:00.123456",
    updated_at: "2021-11-08T12:00:00.123456",
    comments: []
}
```
### `게시판 조회`
#### Request
```
method: GET
path: /api/board/
```
#### Response
```
code: 200
Content-type: json
data: {
    count: 98, # 게시물 수
    next: "http://-/api/board/?page=~", 다음 페이지
    previous: "http://-/api/board/?page=~", 이전 페이지
    result: [
        {
            id: 1,
            title: "게시판 제목",
            created_at: "2021-11-08T12:00:00.123456",
            updated_at: "2021-11-08T12:00:00.123456",
        },
        ...
    ]
}
```
### `게시물 조회`
#### Request
```
method: GET
path: /api/board/{id}/   # id: 해당 게시물 id
```
#### Response
```
code: 200
Content-type: json
data: {
    id: 1,
    title: "게시판 제못",
    content: "게시판 내용입니다.",
    created_at: "2021-11-08T12:00:00.123456",
    updated_at: "2021-11-08T12:00:00.123456",
    comments: {
        id: 1,
        board: 1,
        content: "댓글입니다."
    },  # 댓글이 없는 경우 null
    ...
}
```
### `게시물 변경`
#### Request
```
method: PATCH
path: /api/board/{id}/   # id: 해당 게시물 id
Content-type: json
header: {
    password: "password1234"  # 게시물의 암호
}
data: {
    "title": "변경한 제목",
    "content": "변경한 내용입니다."
}
```
#### Response
```
code: 200
Content-type: json
data: {
    id: 2,
    title: "변경한 제목",
    content: "변경한 내용입니다.",
    created_at: "2021-11-08T12:00:00.123456",
    updated_at: "2021-11-08T13:12:01.123456",
    comments: []  # 있는 경우 위와 같이 표현됩니다.
}
```
### `게시물 삭제`
#### Request
```
method: DELETE
path: /api/board/{id}/   # id: 해당 게시물 id
header: {
    "password": "password1234"  # 게시물의 암호
}
```
#### Response
```
code: 204
```
### `댓글 생성`
#### Requeset
```
method: POST
path: /api/comment/
Content-type: json
data: {
    board: 1,  # 댓글이 달리는 Board id
    content: "댓글 내용입니다."
    password: "password1234"
}
```
#### Response
```
code: 201
Content-type: json
data: {
    id: 1,
    board: 1,
    content: "댓글 내용입니다."
}
```
### `댓글 변경`
#### Request
```
method: PATCH
path: /api/comment/{id}/  # id: 댓글 id
Content-type: json
header: {
    password: "password1234"  # 댓글 암호
}
data: {
    content: "변경한 내용입니다."
}
```
#### Response
```
code: 200
Content-type: json
data: {
    id: 1,
    board: 1,
    content: "변경한 내용입니다."
}
```
### `댓글 삭제`
#### Request
```
method: DELETE
path: /api/comment/{id}/  # id: 댓글 id
header: {
    password: "password1234"  # 댓글 암호
}
```
#### Response
```
code: 204
```
