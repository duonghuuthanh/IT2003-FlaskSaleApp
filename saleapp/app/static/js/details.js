function spinner(flag="block") {
    let s = document.getElementsByClassName('my-spinner');
    for (let i = 0; i < s.length; i++)
        s[i].style.display=flag;
}

function loadComments(productId) {
    fetch(`/products/${productId}/comments`).then(res => res.json()).then(data => {
        console.info(data)
        let re = ""
        data.forEach(v => {
            re += `
            <li class="list-group-item">
                <div class="row">
                    <div class="col-md-1 col-sm-4 text-center">
                        <img  src="${v.user.avatar}" alt="${v.user.name}" class="rounded-circle" width="100%" />
                        <p></p>
                    </div>
                    <div class="col-md-11 col-sm-8">
                        <p>${v.content}</p>
                        <hr>
                        <small>Bình luận <span class="text-primary">${moment(v.created_date).locale('vi').fromNow()}</span> bởi <span class="text-info">${v.user.name}</span></small>
                    </div>
                </div>
            </li>
            `
        })

        let e = document.getElementById('comments')
        e.innerHTML = re

        spinner("none")
    })
}

function addComment(productId) {
    spinner("block")
    fetch(`/products/${productId}/comments`, {
        method: "post",
        body: JSON.stringify({
            "content": document.getElementById("comment-content").value
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(function(res) { return res.json() }).then(function(data) {
        spinner("none")
        if (data.status === 204) {
            let v = data.comment
            let h = `
            <li class="list-group-item">
                <div class="row">
                    <div class="col-md-1 col-sm-4 text-center">
                        <img  src="${v.user.avatar}" alt="${v.user.name}" class="rounded-circle" width="100%" />
                        <p></p>
                    </div>
                    <div class="col-md-11 col-sm-8">
                        <p>${v.content}</p>
                        <hr>
                        <small>Bình luận <span class="text-primary">${moment(v.created_date).locale('vi').fromNow()}</span> bởi <span class="text-info">${v.user.name}</span></small>
                    </div>
                </div>
            </li>
            `
            let e = document.getElementById('comments')
            e.innerHTML = h + e.innerHTML
        } else
            alert("Hệ thống đang bị lỗi!")
    })
}