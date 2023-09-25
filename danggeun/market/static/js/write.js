document.querySelector(".submit-button").addEventListener("click", function(event){
  let imageField = document.getElementById("productImage");

  if(!imageField.value){
      alert("이미지를 넣어주세요!");
      event.preventDefault();
  }
});

function previewImage(event) {
  let reader = new FileReader();
  reader.onload = function () {
    let output = document.getElementById("imagePreview");
    output.src = reader.result;
    output.classList.add("img-upload-fit");
  };
  reader.readAsDataURL(event.target.files[0]);
}

