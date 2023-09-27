document.addEventListener("DOMContentLoaded", () => {
  if (
    window.location.pathname.includes("trade") ||
    window.location.pathname.includes("write") ||
    window.location.pathname.includes("edit")
  ) {
    document.getElementById("trade-button").classList.toggle("orange-text");
  } else if (window.location.pathname == "/location/") {
    document.getElementById("location-button").classList.toggle("orange-text");
  }else if (window.location.pathname == "/my_list/") {
    document.getElementById("trade_list").classList.toggle("orange-text");
  }else if (window.location.pathname == "/mypage/") {
    document.getElementById("mydangguen").classList.toggle("orange-text");
  }else if (window.location.pathname == "/buy_list/") {
    document.getElementById("buy_list").classList.toggle("orange-text");
  }else if (window.location.pathname == "/wish_list/") {
    document.getElementById("wish_list").classList.toggle("orange-text");
  }

  document.querySelector('.user').addEventListener('click', function() {
    var menu = document.getElementById('menu-container');
    
    // Menu 표시 상태 토글
    if (menu.style.display === 'none' || menu.style.display === '') {
        menu.style.display = 'block';
    } else {
        menu.style.display = 'none';
    }

    this.classList.toggle('selected');
    var arrow = document.querySelector('.arrow-down');
    if (arrow) {
        arrow.classList.toggle('flip');
    }
});

document.getElementById('menu-container').addEventListener('click', function(event) {
    event.stopPropagation();
});

});


