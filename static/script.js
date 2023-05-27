// interactive bar
// Get the buttons
const sortLikesBtn = document.getElementById('sortLikesBtn');
const sortCommentsBtn = document.getElementById('sortCommentsBtn');

//assigned event listener
sortLikesBtn.addEventListener('click', sortPostsByLikes);
sortCommentsBtn.addEventListener('click', sortPostsByComments);

function sortPostsByLikes() {
    const blogPosts = Array.from(document.querySelectorAll('.blog-post'));
    blogPosts.sort((a, b) => {
        const likesA = parseInt(a.dataset.likes);
        const likesB = parseInt(b.dataset.likes);
        return likesB - likesA;
    });
    rearrangePosts(blogPosts);
}

function sortPostsByComments() {
    const blogPosts = Array.from(document.querySelectorAll('.blog-post'));
    blogPosts.sort((a, b) => {
        const commentsA = parseInt(a.dataset.comments);
        const commentsB = parseInt(b.dataset.comments);
        return commentsB - commentsA;
    });
    rearrangePosts(blogPosts);
}

function rearrangePosts(sortedPosts) {
    const container = document.getElementById('postsContainer');
    sortedPosts.forEach(post => container.appendChild(post));
}

// search functionality
// Get the form and input elements
document.getElementById("search-form").addEventListener("submit", function (event) {
    event.preventDefault(); // Prevent form submission

    var searchTerm = document.getElementById("tag-input").value.toLowerCase();
    var blogPosts = document.getElementsByClassName("blog-post");

    for (var i = 0; i < blogPosts.length; i++) {
        var tags = blogPosts[i].getAttribute("data-tags").split(",");
        var shouldDisplay = tags.some(function (tag) {
            return tag.trim().toLowerCase() === searchTerm;
        });

        blogPosts[i].style.display = shouldDisplay ? "block" : "none";
    }
});
