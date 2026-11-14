function getCSRFToken() {
    const name = 'csrftoken';
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
        cookie = cookie.trim();
        if (cookie.startsWith(name + '=')) {
            return decodeURIComponent(cookie.slice(name.length + 1));
        }
    }
    return '';
}

function toggleInteraction(ele, recipeId, type) {
    fetch(`/interact/${type}/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCSRFToken()
        },
        body: JSON.stringify({ recipe_id: recipeId })
    })
        .then(res => res.json())
        .then(data => {
            console.log(data);

            // Sets the button image based on the interaction status
            if (data[`is_${type}`]) {
                ele.innerHTML = `<img src="/static/images/${type}Active.ico" alt="${type}" width="20" height="20" />`;
            } else {
                ele.innerHTML = `<img src="/static/images/${type}.ico" alt="${type}" width="20" height="20" />`;
            }

            if(type === "like" && document.getElementById("likeCount")) {
                document.getElementById("likeCount").innerText = data.like_count;
            }
        })
        .catch(err => console.error("Error:", err));
}