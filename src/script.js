// 1. 요약 레시피에 사용할 예시 JSON 데이터 (외부 API 응답 가정)
const dummyResponse = {
  recipeName: "김치볶음밥",
  ingredients: [
    "밥 2공기",
    "김치 1컵 (잘게 자름)",
    "대파 1/2대 (송송 썬 것)",
    "식용유 2큰술",
    "간장 1큰술",
    "참기름 1큰술",
    "계란 1개"
  ],
  steps: [
    "팬을 중불로 달군 후 식용유를 두른다.",
    "잘게 썬 대파와 김치를 팬에서 2-3분간 볶는다.",
    "밥을 넣고 간장을 뿌려 함께 볶는다.",
    "참기름을 넣어 섞은 후 불을 끈다.",
    "그릇에 담고 계란 프라이를 올려 완성한다."
  ],
  cookingTime: "약 15분"
};

// DOM 요소 가져오기
const urlInput = document.getElementById("urlInput");
const fetchBtn = document.getElementById("fetchBtn");
const outputDiv = document.getElementById("output");

// JSON 데이터를 받아 화면에 표시하는 함수
function displayRecipe(data) {
  // 요리명 (h2) 및 재료, 순서, 시간 등의 HTML 생성
  let html = `<h2>요리명: ${data.recipeName}</h2>`;
  html += "<h3>재료 목록:</h3><ul>";
  for (const item of data.ingredients) {
    html += `<li>${item}</li>`;
  }
  html += "</ul>";
  html += "<h3>단계별 조리 순서:</h3><ol>";
  for (const step of data.steps) {
    html += `<li>${step}</li>`;
  }
  html += "</ol>";
  html += `<p><strong>예상 조리 시간:</strong> ${data.cookingTime}</p>`;

  // 생성한 HTML을 출력 영역에 넣기
  outputDiv.innerHTML = html;
}

// 버튼 클릭 시 이벤트 처리
fetchBtn.addEventListener("click", () => {
  const url = urlInput.value.trim();
  if (!url) {
    alert("URL을 입력하세요.");  // URL이 비어있으면 알림 표시
    return;
  }

  // 로딩 중 메시지 표시
  outputDiv.textContent = "요약 불러오는 중...";

  // 2. API 호출 시뮬레이션 (1초 지연 후 dummyResponse 사용)
  fetchBtn.disabled = true;  // (선택 사항) 중복 클릭 방지 위해 버튼 잠시 비활성화
  setTimeout(() => {
    // 실제 구현 시, 여기에 fetch를 사용하여 API로부터 데이터를 가져옵니다.
    // 예: fetch('API_ENDPOINT', { method: 'POST', body: JSON.stringify({ url }) }).then(res => res.json()).then(displayRecipe);
    displayRecipe(dummyResponse);   // dummy 데이터로 결과 표시
    fetchBtn.disabled = false;
  }, 1000);
});
