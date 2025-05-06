from mongoengine import Document, StringField, IntField

class Character(Document):
    name = StringField(required=True) #필수값
    age = IntField() #선택값, 기본 0살
    role = StringField() # 주인공, 조연
    gender = StringField() # 성별
    description = StringField() # 캐릭터 설명

 # 🧾 메타데이터
    meta = {
        'collection': 'characters',     # MongoDB 컬렉션 이름
        'ordering': ['-id'],            # 정렬 순서: 최근 생성순 (id 내림차순)
        'strict': False                 # 정의하지 않은 필드도 저장 허용
    }