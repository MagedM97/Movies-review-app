// display flash message for 10 sec.
document.addEventListener("DOMContentLoaded", function () {
  const messageDiv = document.getElementById("message");
  if (messageDiv) {
    if (messageDiv.innerText.trim() !== "") {
      messageDiv.style.display = "block";
      setTimeout(function () {
        messageDiv.style.display = "none";
      }, 10000); 
    }
  }
});
