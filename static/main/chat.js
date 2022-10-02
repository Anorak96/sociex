let form = document.getElementById("chatform")
form.addEventListener('submit', sendChat)
function sendChat(e) {
    e.preventDefault()
    let chatMess = document.getElementById("id_body").value
    const data = { body : chatMess };
    let url = "{% url 'chat:send_chat' active_user %}"
    fetch(url, {
        method: 'POST', // or 'PUT'
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify(data),
    })
    .then(response => response.json())
    .then(data => {
        console.log('Sent:', data);
        let chat_body = document.getElementById("chat_body")
        let chatBox = document.createElement("div")
        chatBox.classList.add("chat_sent")
        
        let chatImg = document.createElement("img");
        chatBox.appendChild(chatImg)
        
        let chatBody = document.createElement("p")
        chatBody.classList.add("ms-1")
        chatBox.appendChild(chatBody)
        
        chatBody.innerText = data
        chat_body.append(chatBox)
        document.getElementById("id_body").value = ""
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}

setInterval(receiverChat, 2000)
let counter = {{ num }}
function receiverChat(){
    let url = "{% url 'chat:receive_chat' active_user %}"
    fetch(url)
    .then(response => response.json())
    .then(data => {
        console.log('Success:', data);
        if (data.length == 0) {}
        
        else {
            let lastMsg = data[data.length - 1]
            
            if (counter == data.length) {
                console.log("there is no new chat")
            }
            else {
                let chat_body = document.getElementById("chat_body")
                let chatBox = document.createElement("div")
                chatBox.classList.add("chat_receive")
                
                let chatImg = document.createElement("img");
                chatBox.appendChild(chatImg)
                
                let chatBody = document.createElement("p")
                chatBody.classList.add("ms-1")
                chatBox.appendChild(chatBody)
                
                chatBox.innerText = lastMsg
                chat_body.appendChild(chatBox)
            }
        }
        counter = data.length
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}

setInterval(chatNotification, 1000)
function chatNotification(){
    let url = "{% url 'chat:notif_chat' %}"
    fetch(url)
    .then(res => res.json())
    .then(data => {
        console.log(data)
        let chatNotificationBtn = document.getElementById("msg_unread")
        for (let i = 0; i < data.length; i++) {
            chatNotificationBtn[i].innerText = data[i]
        }
    })
    .catch(error => console.log(error))
}