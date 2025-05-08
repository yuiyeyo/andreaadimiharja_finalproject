

document.addEventListener("DOMContentLoaded", function () {
    fetch("/data/articles.csv")
        .then(response => response.text())
        .then(csvData => {
            Papa.parse(csvData, {
                header: true, 
                skipEmptyLines: true,  
                complete: function (results) {
                    let articlesContainer = document.getElementById("articlesContainer");
                    if (!articlesContainer) return;

                    articlesContainer.innerHTML = "";  
                    
                    results.data.forEach(article => {
                        let articleHTML = `
                            <article>
                                <img src="${article.image_url}" alt="${article.headline}">
                                <h2><a href="/articles/${article.id}">${article.headline}</a></h2>
                                <p>${article.description || article.content.substring(0, 100) + "..."}</p>
                            </article>
                        `;
                        articlesContainer.innerHTML += articleHTML;
                    });
                }
            });
        })
        .catch(error => console.error("Error loading CSV:", error));
});

document.addEventListener("DOMContentLoaded", function () {
    const searchInput = document.getElementById("searchInput");
    const articlesContainer = document.getElementById("articlesContainer");

    searchInput.addEventListener("input", function () {
        let query = searchInput.value.toLowerCase();
        let articles = articlesContainer.getElementsByTagName("article");

        for (let article of articles) {
            let title = article.getElementsByTagName("h2")[0].innerText.toLowerCase();
            if (title.includes(query)) {
                article.style.display = "block";
            } else {
                article.style.display = "none";
            }
        }
    });
});

document.getElementById("comment-form").addEventListener("submit", function(event) {
    event.preventDefault();
    let commentName = document.getElementById("comment-name").value;
    let commentText = document.getElementById("comment-text").value;

    fetch("{% url 'add_comment' article.article_id %}", {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: new URLSearchParams({ "name": commentName, "text": commentText })
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            let commentList = document.getElementById("comment-list");
            let newComment = document.createElement("p");
            newComment.innerHTML = `<strong>${data.name}</strong> (${data.created_at}): ${data.text}`;
            commentList.appendChild(newComment);
            document.getElementById("comment-name").value = "";
            document.getElementById("comment-text").value = "";
        }
    });
});

document.addEventListener("DOMContentLoaded", function () {
    const likeBtn = document.getElementById("like-btn");

    likeBtn.addEventListener("click", function () {
        const articleId = likeBtn.getAttribute("data-article-id");

        fetch(`/like/${articleId}/`, { method: "POST" })
            .then(response => response.json())
            .then(data => {
                document.getElementById("like-count").textContent = data.likes;
            })
            .catch(error => console.error("Error:", error));
    });
});