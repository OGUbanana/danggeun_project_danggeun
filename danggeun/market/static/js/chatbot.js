function getCurrentTimeString() {
    const now = new Date();
    const hours = now.getHours().toString().padStart(2, '0');
    const minutes = now.getMinutes().toString().padStart(2, '0');
    const ampm = hours >= 12 ? '오후' : '오전';
    return `${ampm} ${hours % 12 || 12}:${minutes}`;
}

window.onload = function() {
    const chatbox = document.getElementById("chatbox");
    const currentTimeString = getCurrentTimeString();
    chatbox.innerHTML += `<div class="message-box from-you"><div class="message-text">안녕하세요 무엇을 도와드릴까요?<br>상품에 대한 추천을 받으시려면 !"키워드"로 메세지를 보내주세요<br>(예시 : !컴퓨터)</div><p class="s-text">${currentTimeString}</p></div>`;
}

document.getElementById("message").addEventListener("keydown", function(event) {
    if (event.key === "Enter") {
        event.preventDefault();  // 줄바꿈 동작 방지
        sendMessage();          // 메시지 전송 함수 호출
    }
});



let loadingInterval;

async function sendMessage() {
    const message = document.getElementById("message").value;
    
    if (message.trim() === "") return;

    const chatbox = document.getElementById("chatbox");
    const currentTimeString = getCurrentTimeString();
    chatbox.innerHTML += `
        <div class="message-box from-me">
            <div class="message-text">${message}</div>
            <p class="s-text">${currentTimeString}</p>
        </div>
    `;
    chatbox.scrollTop = chatbox.scrollHeight;

    // 로딩 애니메이션 시작
    const loadingIndicator = document.getElementById("loading");
    loadingIndicator.style.display = "block";
    let dotsCount = 1;
    loadingInterval = setInterval(() => {
        dotsCount = (dotsCount % 3) + 1;
        loadingIndicator.textContent = '.'.repeat(dotsCount);
    }, 500);

    const response = await fetch(`/chatai?message=${encodeURIComponent(message)}`);
    const data = await response.json();

    // 로딩 애니메이션 종료
    clearInterval(loadingInterval);
    loadingIndicator.style.display = "none";

    if (data.type === 'text') {
        chatbox.innerHTML += `<div class="message-box from-you"><div class="message-text">${data.data}</div><p class="s-text">${currentTimeString}</p></div>`;
    }
    else if (data.type === 'product_recommendation') {
        let productHTML = `<div class="message-box from-you"><div class="message-text">${data.data.message}<br>`;
    
        // 추천된 상품 목록을 HTML 변수에 추가
        data.data.products.forEach(product => {
            productHTML += `
            <div class="goods-box flex-box between">
                <div class="flex-box">
                    <div class="selected-thumbnail-box">
                        <img src="${product.image_url}" alt="${product.title}">
                    </div>
                    <div class="goods-info-box">
                        <a href="/trade_post/${product.product_id}">
                            <p>${product.title}</p>
                        </a>
                        <p class="bold">${product.price}</p>
                    </div>
                </div>
            </div>
            `;
        });
    
        productHTML += `</div><p class="s-text">${currentTimeString}</p></div>`;
    
        chatbox.innerHTML += productHTML;
    }

    document.getElementById("message").value = "";
    setTimeout(() => {
        chatbox.scrollTop = chatbox.scrollHeight;
    }, 0);
}


