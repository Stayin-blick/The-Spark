// interative bar
// Get the buttons
const topLikesBtn = document.querySelector(".btn-primary:nth-of-type(2)");
const topCommentsBtn = document.querySelector(".btn-primary:nth-of-type(3)");

// Get the blog post container
const blogPostContainer = document.querySelector(
    ".container-fluid.rounded-pill.text-center"
);

// Add event listeners to the buttons

topLikesBtn.addEventListener("click", sortPostsByLikes);

topCommentsBtn.addEventListener("click", sortPostsByComments);

