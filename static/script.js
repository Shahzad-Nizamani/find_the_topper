document.addEventListener('DOMContentLoaded', function() {
  // Get DOM elements
  const form = document.getElementById('topperForm');
  const loadingOverlay = document.querySelector('.loading-overlay');
  const submitButton = document.querySelector('input[type="submit"]');
  const instructionsContainer = document.getElementById('instructions-container');
  const checkNewResultBtn = document.getElementById('checkNewResult');
  const resultsContainer = document.getElementById('results-container');
  const errorMessage = document.querySelector('.error');

  // Initially hide the loading overlay
  if (loadingOverlay) {
      loadingOverlay.style.display = 'none';
  }

  // Function to show the form and hide results
  function showForm() {
      console.log('Showing form...');
      if (form) {
          form.style.display = 'block';
          form.reset();
      }
      if (instructionsContainer) {
          instructionsContainer.style.display = 'block';
      }
      if (checkNewResultBtn) {
          checkNewResultBtn.style.display = 'none';
      }
      if (resultsContainer) {
          resultsContainer.style.display = 'none';
      }
      if (errorMessage) {
          errorMessage.textContent = '';
      }
  }

  // Function to show results and hide form
  function showResults() {
      console.log('Showing results...');
      if (form) {
          form.style.display = 'none';
      }
      if (instructionsContainer) {
          instructionsContainer.style.display = 'none';
      }
      if (checkNewResultBtn) {
          checkNewResultBtn.style.display = 'block';
      }
      if (resultsContainer) {
          resultsContainer.style.display = 'block';
      }
  }

  // Check if we have results
  const hasResults = resultsContainer && resultsContainer.querySelector('table tr');
  console.log('Has results:', !!hasResults);

  // Set initial page state
  if (hasResults) {
      showResults();
  } else {
      showForm();
  }

  // Add click handler for the Check New Result button
  if (checkNewResultBtn) {
      console.log('Adding click handler to button');
      checkNewResultBtn.onclick = function(e) {
          e.preventDefault();
          console.log('Button clicked');
          showForm();
      };
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
