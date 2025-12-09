document.addEventListener("DOMContentLoaded", () => {
  const fetchBtn = document.getElementById("fetchBtn");
  const recommendBtn = document.getElementById("recommendBtn");

  if (fetchBtn) {
    fetchBtn.addEventListener("click", async () => {
      const url = document.getElementById("urlInput").value.trim();
      const resultArea = document.getElementById("resultArea");

      if (!url) {
        alert("URL을 입력하세요.");
        return;
      }

      resultArea.textContent = "조리법 불러오는 중입니다...";

      try {
        const response = await fetch("/api/recipe", {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify({ url })
        });

        if (!response.ok) {
          resultArea.textContent = "레시피 요약 중 오류가 발생했습니다.";
          return;
        }

        const data = await response.json();
        const recipe = data.recipe ?? data;
        displayRecipe(recipe);
      } catch (error) {
        resultArea.textContent = "서버와 통신 중 문제가 발생했습니다.";
      }
    });
  }

  if (recommendBtn) {
    recommendBtn.addEventListener("click", () => {
      const input = document.getElementById("ingredientInput").value.trim();
      const target = document.getElementById("recommendResult");

      const ingredientsText = input ? input : "김치, 밥, 계란";

      const examples = [
        {
          name: "김치볶음밥",
          ingredients: "밥, 김치, 대파, 간장, 식용유, 계란",
          reason: "김치와 밥, 기본 양념만 있어도 만들 수 있는 대표 1인분 메뉴입니다."
        },
        {
          name: "계란야채볶음",
          ingredients: "계란, 양파, 파프리카, 소금, 후추",
          reason: "남아 있는 채소와 계란만 있으면 빠르게 만들 수 있는 간단 반찬입니다."
        },
        {
          name: "간장버터밥",
          ingredients: "밥, 버터, 간장, 김가루",
          reason: "시간이 없을 때 밥과 간단한 재료만으로 만드는 초간단 한 끼 메뉴입니다."
        }
      ];

      let html = "";
      html += `<p>입력한 재료 기준 예시 추천 결과입니다.</p>`;
      html += `<p><strong>입력 재료:</strong> ${ingredientsText}</p>`;
      html += `<div class="recommend-list">`;

      for (const ex of examples) {
        html += `<div class="recommend-item">`;
        html += `<div class="recommend-name">${ex.name}</div>`;
        html += `<div class="recommend-ingredients">필요 재료: ${ex.ingredients}</div>`;
        html += `<div class="recommend-reason">${ex.reason}</div>`;
        html += `</div>`;
      }

      html += `</div>`;

      target.innerHTML = html;
    });
  }
});

function displayRecipe(recipe) {
  const resultArea = document.getElementById("resultArea");

  if (!recipe || !recipe.recipeName) {
    resultArea.textContent = "요약 결과를 불러오지 못했습니다.";
    return;
  }

  let html = "";
  html += `<h2>${recipe.recipeName}</h2>`;
  html += "<h3>재료 목록</h3><ul>";
  for (const item of recipe.ingredients) {
    html += `<li>${item}</li>`;
  }
  html += "</ul>";
  html += "<h3>단계별 조리 순서</h3><ol>";
  for (const step of recipe.steps) {
    html += `<li>${step}</li>`;
  }
  html += "</ol>";
  html += `<p><strong>예상 조리 시간:</strong> ${recipe.cookingTime}</p>`;

  resultArea.innerHTML = html;
}
