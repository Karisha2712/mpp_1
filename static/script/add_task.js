let addTask = document.querySelector("#add-task");
let form = document.querySelector("#form");

addTask.addEventListener('click', () => {
    form.classList.remove("d-none");
    addTask.classList.add("d-none");
})

const actualBtn = document.getElementById('fileInput');
const fileChosen = document.getElementById('file-upload-label');

actualBtn.addEventListener('change', function () {
    fileChosen.innerText = this.files[0].name;
})