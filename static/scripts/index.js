// Function to add a movie to the watch-list in localStorage, associated with a user ID
function addToWatchList(movieName, user) {
  const movies = JSON.parse(localStorage.getItem(user)) || [];
  if (!movies.includes(movieName)) {
    movies.push(movieName);
    localStorage.setItem(user, JSON.stringify(movies));
  }
}

// Get the rate and review form elements
const rateForm = document.getElementById("rateform");
const reviewForm = document.getElementById("reviewform");

function openPopup(movieid) {
  document.getElementById("popupContainer").style.display = "block";
  const movie = document.getElementById("lastrate");
  if (movie) {
    // Remove the last movie ID that was selected to add the new ID of the current selection
    rateForm.removeChild(rateForm.lastElementChild);
  }
  // Add the movie ID to the form for the current selection
  rateForm.innerHTML += `<input type="hidden" id="lastrate"  name="movieId" value="${movieid}" >`;
}

function closePopup() {
  document.getElementById("popupContainer").style.display = "none";
}

// Add event listener for every star on the rating form to submit the form
rateForm.addEventListener("click", function (event) {
  if (event.target.matches('.rate-review input[name="rate"]')) {
    rateForm.submit();
  }
});

function openReviewPopup(movieid) {
  document.getElementById("reviewPopupContainer").style.display = "block";
  const lastReview = document.getElementById("lastreview");
  if (lastReview) {
    // Remove the last movie ID that was selected to add the new ID of the current selection
    reviewForm.removeChild(reviewForm.lastElementChild);
  }
  // Add event listener for every star on the rating form to submit the form
  reviewForm.innerHTML += `<input type="hidden" id="lastreview"  name="movieId" value="${movieid}" >`;
}

function closeReviewPopup() {
  document.getElementById("reviewPopupContainer").style.display = "none";
}
