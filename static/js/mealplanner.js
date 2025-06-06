// mealplanner.js

export async function fetchMealPlan(systemPrompt, userPrompt) {
  const res = await fetch('/api/meal-plan', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Accept': 'application/json'
    },
    body: JSON.stringify({
      system_prompt: systemPrompt,
      user_prompt: userPrompt
    })
  });
  if (!res.ok) throw new Error('Failed to generate meal plan');
  return await res.json();
}

export function renderCalendar(mealsForDays) {
  const container = document.getElementById("calendar-container");
  if (!mealsForDays?.length) {
    container.innerHTML = "<em>No meal plan found.</em>";
    return;
  }

  let html = `<table><thead><tr><th>Day</th><th>Breakfast</th><th>Lunch</th><th>Dinner</th></tr></thead><tbody>`;
  mealsForDays.forEach((dayObj) => {
    html += `<tr><td class="meal-title">${dayObj.day}</td>`;
    ["breakfast", "lunch", "dinner"].forEach((type) => {
      const meal = dayObj[type];
      if (meal?.name) {
        html += `<td><span class="meal-link" onclick='showMealDetails(${JSON.stringify(meal).replace(/'/g, "&#39;")})'>${meal.name}</span></td>`;
      } else {
        html += "<td>-</td>";
      }
    });
    html += "</tr>";
  });
  html += "</tbody></table>";
  document.getElementById("calendar-container").innerHTML = html;
}

export function showMealDetails(meal) {
  const modal = document.getElementById("meal-modal");
  const content = document.getElementById("modal-content");
  content.innerHTML = `
    <h2>${meal.name}</h2>
    <strong>Ingredients:</strong>
    <ul>${(meal.ingredients || []).map(i => `<li>${i}</li>`).join('')}</ul>
    <strong>Instructions:</strong>
    <p>${meal.instructions || ''}</p>
    ${meal.dietary_restrictions ? `<strong>Dietary:</strong> ${meal.dietary_restrictions}` : ''}
  `;
  modal.style.display = "flex";
  document.getElementById("close-modal").onclick = () => modal.style.display = "none";
  modal.onclick = (e) => { if (e.target === modal) modal.style.display = "none"; };
}

// DOM Hook
export function setupMealForm() {
  document.getElementById("meal-form").addEventListener("submit", async function (e) {
    e.preventDefault();
    const systemPrompt = document.getElementById("system-prompt").value;
    const userPrompt = document.getElementById("user-prompt").value;
    document.getElementById("calendar-container").innerHTML = "<em>Generating meal plan...</em>";
    document.getElementById("notes").style.display = "none";

    try {
      const data = await fetchMealPlan(systemPrompt, userPrompt);
      renderCalendar(data.meals);
      if (data.additional_notes) {
        document.getElementById("notes").textContent = data.additional_notes;
        document.getElementById("notes").style.display = "block";
      }
    } catch (err) {
      document.getElementById("calendar-container").innerHTML = `<span style="color:red">Error: ${err.message}</span>`;
    }
  });
}

// Initialize on DOMContentLoaded
window.addEventListener("DOMContentLoaded", setupMealForm);
