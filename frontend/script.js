const form = document.getElementById('predictForm');
const experienceEl = document.getElementById('experience');
const skillsEl = document.getElementById('skills');
const btn = document.getElementById('predictBtn');
const messageEl = document.getElementById('message');
const resultEl = document.getElementById('result');

function setLoading(isLoading) {
  if (isLoading) {
    btn.classList.add('loading');
    btn.setAttribute('disabled', 'true');
    messageEl.classList.remove('error');
    messageEl.textContent = 'Predicting...';
  } else {
    btn.classList.remove('loading');
    btn.removeAttribute('disabled');
  }
}

function showError(msg) {
  messageEl.classList.add('error');
  messageEl.textContent = msg;
}

function clearStatus() {
  messageEl.classList.remove('error');
  messageEl.textContent = '';
}

function formatMoney(n) {
  try {
    return new Intl.NumberFormat(undefined, {
      style: 'currency',
      currency: 'USD',
      maximumFractionDigits: 0,
    }).format(n);
  } catch {
    return `$${Math.round(n).toLocaleString()}`;
  }
}

function validateInputs(experience, skills) {
  if (!Number.isFinite(experience) || experience < 0) return 'Experience must be 0 or greater.';
  if (!Number.isFinite(skills) || !Number.isInteger(skills) || skills < 1 || skills > 10)
    return 'Skills rating must be a whole number between 1 and 10.';
  return null;
}

form.addEventListener('submit', async (e) => {
  e.preventDefault();

  resultEl.textContent = '';
  clearStatus();

  const experience = Number(experienceEl.value);
  const skills = Number(skillsEl.value);

  const validationError = validateInputs(experience, skills);
  if (validationError) {
    showError(validationError);
    return;
  }

  setLoading(true);

  try {
    const res = await fetch('/predict', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        experience,
        skills,
      }),
    });

    const data = await res.json().catch(() => null);

    if (!res.ok) {
      const msg = data && data.error ? data.error : 'Request failed.';
      showError(msg);
      return;
    }

    const salary = data && typeof data.predicted_salary === 'number' ? data.predicted_salary : NaN;
    if (!Number.isFinite(salary)) {
      showError('Invalid prediction response from server.');
      return;
    }

    messageEl.classList.remove('error');
    messageEl.textContent = 'Done.';
    resultEl.textContent = `Estimated salary: ${formatMoney(salary)}`;
  } catch (err) {
    showError('Could not connect to the server. Is the backend running?');
  } finally {
    setLoading(false);
  }
});
