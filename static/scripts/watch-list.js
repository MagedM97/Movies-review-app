// check if watch-list is empty or not
function checkMovieList() {
  if (document.getElementById("movie-list").innerHTML == "") {
    document.getElementById("movies-to-watch").innerText =
      "No Movies selected yet";
  }
}

// get watchlist
document.addEventListener("DOMContentLoaded", function () {
  const id = document.getElementById("id-user").innerText;
  let movies = localStorage.getItem(id);
  if (movies) {
    movies = JSON.parse(movies);
    const movieList = document.getElementById("movie-list");
    // Create the list of movies
    movies.forEach(function (movie) {
      const listItem = document.createElement("li");
      listItem.textContent = movie;
      listItem.classList.add("movie-item");
      // Create delete button
      const deleteButton = document.createElement("button");
      deleteButton.textContent = "Delete";
      deleteButton.classList.add("delete-btn");
      deleteButton.addEventListener("click", function () {
        // Remove movie from local storage and update the list
        movies = movies.filter(function (item) {
          return item !== movie;
        });
        localStorage.setItem(id, JSON.stringify(movies));
        movieList.removeChild(listItem);
        // show "No movies selected" message if the user deleted all movies from watch list
        checkMovieList();
      });
      // Append delete button to list item
      listItem.appendChild(deleteButton);
      // Append list item to movie list
      movieList.appendChild(listItem);
    });
  }
  checkMovieList();
});
