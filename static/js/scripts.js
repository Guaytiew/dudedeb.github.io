// this JavaScripts make AJAX requests to the Flask API to retrieve and display data dynamically
document.getElementById('commentForm').addEventListener('submit', function(e) {
    e.preventDefault();
    let content = document.getElementById('commentContent').value;
    let rating = document.getElementById('commentRating').value;

    fetch('/api/task/{{ task.id }}/comments', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ content: content, rating: rating }),
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        location.reload();
    });
});
