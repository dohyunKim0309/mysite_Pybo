// 페이징처리를 위한 script.
// <a class="page-link" ...>...</a>의 data-page 속성값을 읽어
const page_elements = document.getElementsByClassName("page-link");
Array.from(page_elements).forEach(function(element) {
    element.addEventListener('click', function() {
        // 이해안감 ㅠㅠ
        document.getElementById('page').value = this.dataset.page;
        // searchForm 요청
        document.getElementById('searchForm').submit();
    });
});
// 검색버튼 처리를 위한 script.
// 검색버튼을 클릭하면 검색어 텍스트창의 값을 searchForm의 kw에 저장한 다음 searchForm을 요청하도록 함
const btn_search = document.getElementById("btn_search");
btn_search.addEventListener('click', function() {
    document.getElementById('kw').value = document.getElementById('search_kw').value;
    document.getElementById('page').value = 1;  // 검색버튼을 클릭할 경우 1페이지부터 조회한다.
    // searchForm 요청
    document.getElementById('searchForm').submit();
});
