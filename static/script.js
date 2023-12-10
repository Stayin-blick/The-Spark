// interactive bar
// sorting script (Top Likes/Top Comments/Most Recent)

const sortLikesBtn = document.getElementById('sortLikesBtn');
const sortCommentsBtn = document.getElementById('sortCommentsBtn');

// Variables to track the current sorting state
let likesSortAscending = false;
let commentsSortAscending = false;

// assign event listener
sortLikesBtn.addEventListener('click', sortPostsByLikes);
sortCommentsBtn.addEventListener('click', sortPostsByComments);

// sort by likes function
function sortPostsByLikes() {
    const blogPosts = Array.from(document.querySelectorAll('.blog-post'));
    blogPosts.sort((a, b) => {
        const likesA = parseInt(a.dataset.likes);
        const likesB = parseInt(b.dataset.likes);
        if (likesSortAscending) {
            return likesA - likesB;
        } else {
            return likesB - likesA;
        }
    });
    likesSortAscending = !likesSortAscending;
    rearrangePosts(blogPosts);
}

// sort by comments function
function sortPostsByComments() {
    const blogPosts = Array.from(document.querySelectorAll('.blog-post'));
    blogPosts.sort((a, b) => {
        const commentsA = parseInt(a.dataset.comments);
        const commentsB = parseInt(b.dataset.comments);
        if (commentsSortAscending) {
            return commentsA - commentsB;
        } else {
            return commentsB - commentsA;
        }
    });
    commentsSortAscending = !commentsSortAscending;
    rearrangePosts(blogPosts);
}

function rearrangePosts(sortedPosts) {
    const container = document.getElementById('blog-post');
    sortedPosts.forEach(post => container.appendChild(post));
}

// tag search bar
document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('search-form');
    const input = document.getElementById('tag-input');
    const blogPosts = document.getElementsByClassName('blog-post');

    form.addEventListener('submit', function (event) {
        event.preventDefault();
        const searchValue = input.value.toLowerCase();

        for (let i = 0; i < blogPosts.length; i++) {
            const post = blogPosts[i];
            const tags = post.dataset.tags.toLowerCase();

            if (searchValue === '' || tags.includes(searchValue)) {
                post.style.display = 'block';
            } else {
                post.style.display = 'none';
            }
        }
    });

    input.addEventListener('input', function () {
        const searchValue = input.value.toLowerCase();

        for (let i = 0; i < blogPosts.length; i++) {
            const post = blogPosts[i];
            const tags = post.dataset.tags.toLowerCase();

            if (searchValue === '' || tags.includes(searchValue)) {
                post.style.display = 'block';
            } else {
                post.style.display = 'none';
            }
        }
    });
});

document.addEventListener('DOMContentLoaded', function() {
    setTimeout(function() {
        const alertElement = document.querySelector(".alert");
        if (alertElement) {
            alertElement.classList.remove('show');
        }
    }, 5000);
});
