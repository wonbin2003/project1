// API 호출 시 실제 백엔드 요청으로 변경
fetchBtn.addEventListener("click", async () => {
  const url = document.getElementById("urlInput").value.trim();
  const resultArea = document.getElementById("resultArea");

  if (!url) {
    alert("URL을 입력하세요.");
    return;
  }

  // 로딩 중 메시지 표시
  resultArea.textContent = "조리법 불러오는 중...";

  try {
    const response = await fetch("http://127.0.0.1:8000/api/recipe", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ url }),
    });

    if (!response.ok) {
      throw new Error("API 호출 실패");
    }

    const data = await response.json();
    displayRecipe(data.recipe);  // 실제 API 응답으로 데이터 처리

  } catch (error) {
    resultArea.textContent = `❌ 오류 발생: ${error.message}`;
  } finally {
    fetchBtn.disabled = false;  // 버튼 활성화
  }
});

// JSON 데이터를 받아 화면에 표시하는 함수
function displayRecipe(data) {
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

  resultArea.innerHTML = html;
}
