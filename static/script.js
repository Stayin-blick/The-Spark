// Get the buttons
const createPostBtn = document.querySelector(".btn-primary:nth-of-type(1)");
const topLikesBtn = document.querySelector(".btn-primary:nth-of-type(2)");
const topCommentsBtn = document.querySelector(".btn-primary:nth-of-type(3)");

// Get the blog post container
const blogPostContainer = document.querySelector(
    ".container-fluid.rounded-pill.text-center"
);

// Add event listeners to the buttons
createPostBtn.addEventListener("mouseenter", darkenButton);
createPostBtn.addEventListener("mouseleave", restoreButton);
createPostBtn.addEventListener("click", redirectToCreatePost);

topLikesBtn.addEventListener("mouseenter", darkenButton);
topLikesBtn.addEventListener("mouseleave", restoreButton);
topLikesBtn.addEventListener("click", sortPostsByLikes);

topCommentsBtn.addEventListener("mouseenter", darkenButton);
topCommentsBtn.addEventListener("mouseleave", restoreButton);
topCommentsBtn.addEventListener("click", sortPostsByComments);

// Function to darken the button
function darkenButton(event) {
    event.target.classList.add("darken");
}

// Function to restore the button to its original state
function restoreButton(event) {
    event.target.classList.remove("darken");
}

