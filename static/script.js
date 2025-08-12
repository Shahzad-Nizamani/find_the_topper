document.addEventListener('DOMContentLoaded', function() {
  // Get DOM elements
  const form = document.getElementById('topperForm');
  const loadingOverlay = document.querySelector('.loading-overlay');
  const submitButton = document.querySelector('input[type="submit"]');
  
  // Initially hide the loading overlay
  loadingOverlay.style.display = 'none';

  // Check if we're showing results or error
  const resultsTable = document.querySelector('table');
  const errorMessage = document.querySelector('.error');
  const hasResults = resultsTable?.querySelector('tr');
  
  if (hasResults || errorMessage?.textContent) {
      loadingOverlay.style.display = 'none';
      form.classList.remove('loading');
  }

  function showLoading() {
      loadingOverlay.style.display = 'flex';
      form.classList.add('loading');
      if (submitButton) {
          submitButton.disabled = true;
      }
  }

  function validateForm() {
      const requiredFields = ['dept', 'exam-year', 'semester', 'batch', 'subject'];
      
      for (const fieldId of requiredFields) {
          const field = document.getElementById(fieldId);
          if (!field || !field.value.trim()) {
              alert('Please fill in all fields');
              return false;
          }
      }
      return true;
  }

  // Handle form submission
  form.addEventListener('submit', function(e) {
      if (!validateForm()) {
          e.preventDefault();
          return;
      }
      showLoading();
  });

  // Handle back button and page refresh
  window.addEventListener('pageshow', function(event) {
      if (event.persisted || window.performance?.navigation.type === 1) {
          loadingOverlay.style.display = 'none';
          form.classList.remove('loading');
          if (submitButton) {
              submitButton.disabled = false;
          }
      }
  });
});
