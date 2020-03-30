# django-restapi-squaremall
React와 연동하기 위하여 구현한 Django Rest Framework(DRF)를 이용한 REST API

> 쇼핑몰을 주제로한 웹 앱 구현에 front-end는 ``React``를, back-end는 ``Django``를 사용하여 구현하기로 결정하고 back-end 부분을 맡아서 진행

![image](https://user-images.githubusercontent.com/46367323/77907260-4c734280-72c4-11ea-9f19-193e32af9f71.png)
**[🔗squaremall](https://squre-mall.github.io/square-front/)**

## Features
pythonanywhere 사이트에서 서버 생성하여 해당 앱 업로드 후 서버 실행

![image](https://user-images.githubusercontent.com/46367323/77908393-63b32f80-72c6-11ea-8593-66d82e826438.png)
![image](https://user-images.githubusercontent.com/46367323/77908531-a07f2680-72c6-11ea-9e17-46c632fa79ad.png)

*테스트를 위해 상품에 대한 데이터는 [무신사스토어](https://store.musinsa.com/app/items/lists/001) 사이트로부터 크롤링하여 DB에 저장*

### Models.py
> Cloth 라는 의류 공통 테이블을 두고 의류의 상세 정보는 사이트마다 상이하기 때문에 사이트별로 테이블 새로 생성
- 의류 테이블 
    - 제품 번호, 브랜드명, 제품명, 의류 이미지 suffix, 가격, 카테고리, 생성시간, 수정시간
```py
class Cloth(models.Model):
    # id = models.IntegerField(primary_key=True)
    productNo = models.CharField(max_length=200)
    brand = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    clothImgSuffix = models.CharField(max_length=300)
    price = JSONField(default=dict)
    category = models.CharField(max_length=100)
    created = models.DateTimeField(editable=False)
    modified = models.DateTimeField(editable=False)
```
- 의류 상세 무신사 테이블(의류 테이블과 One-to-One 관계)
    - 설명, 시즌, 성별, 1개월 인기도, 추가정보(색상, 수입여부, ...)
```py
class Cloth_Detail_Musinsa(models.Model):
    cloth = models.OneToOneField(
        Cloth,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    description = models.TextField(blank=True, null=True)
    season = models.CharField(max_length=100)
    gender = models.CharField(max_length=100)
    monthlyPopularity = models.CharField(max_length=100)
    color = models.CharField(max_length=100)
    importation = models.CharField(max_length=100)
    manufacturingYM = models.CharField(max_length=100)
    material = models.CharField(max_length=100)
    sizeNweight = models.CharField(max_length=100)
    manufacturer = models.CharField(max_length=100)
    manufactured = models.CharField(max_length=100)
    asdirector = models.CharField(max_length=100)
    precautions = models.CharField(max_length=500)
    warrantyBasis = models.CharField(max_length=200)
```
### views.py
> ``Generic API View``를 이용하여 HTTP 요청 처리
```py
class ListCloth(generics.ListCreateAPIView):
    queryset = Cloth.objects.all()
    serializer_class = ClothSerializer
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [a for a in ClothSerializer.Meta.fields if a != 'price']
    search_fields = [a for a in ClothSerializer.Meta.fields if a != 'price']
    ordering_fields = [a for a in ClothSerializer.Meta.fields if a != 'price']

    pagination_class = ClothPageNumberPagination

class DetailCloth(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cloth.objects.all()
    serializer_class = ClothSerializer
```

### serializers.py
> ``ModelSerializer``를 통해 JSON 형식으로 데이터 직렬화
```py
class ClothSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id',) + tuple(a.name for a in Cloth._meta.get_fields())
        model = Cloth
```

### Filtering, Pagination, JSON Field
> 1. 각 테이블의 컬럼에 대한 필터링 구현
> 2. 성능 개선을 위해 페이징 처리 구현
> 3. JSON Field를 사용하여 한 컬럼에 여러 데이터 저장

![image](https://user-images.githubusercontent.com/46367323/77909203-e5578d00-72c7-11ea-8115-534a77b058d5.png)

## Issue
### Crawling
지정한 사이트로부터 데이터를 가져와서 파싱 후에 DB에 저장하는 것까지 구현하였으나   
pythonanywhere 서버에서는 해당 코드 실행 불가
> pythonanywhere 내에서 관리하는 white list에 추가되어야 해당 사이트로부터 request 가능

    → 로컬에서 실행한 후에 DB에 저장된 데이터를 txt로 저장하여 pythonanywhere 서버에 업로드하는 방식으로 진행

