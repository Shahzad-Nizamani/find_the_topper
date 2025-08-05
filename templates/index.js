function validateForm(e) {
    const dept = document.getElementById("dept").value.trim();
    const semester = document.getElementById("semester").value.trim();
    const batch = document.getElementById("batch").value.trim();
    const subject = document.getElementById("subject").value.trim();

    if (!dept || !year || !semester || !batch || !subject) {
      alert("Please fill in all fields.");
      return false;
    }
e.preventDefault()
   

    if (semester < 1 || semester > 8) {
      alert("Semester must be between 1 and 8.");
      return false;
    }

    // All good
    return true;
  }
  
  function handleSubmit(e) {
    e.preventDefault(); // Stop actual form submission
    const btn = document.getElementById('submitBtn');
    
    // Change button state to loading
    btn.classList.add('loading');
    btn.disabled = true;

    // Simulate delay (e.g., sending request)
    setTimeout(() => {
      btn.classList.remove('loading');
      btn.disabled = false;
      btn.value = "Submitted"; // Optional
    }, 3000);

    return false;
  }
