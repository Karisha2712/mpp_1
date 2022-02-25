let addTask = document.querySelector("#add-task");
let form = document.querySelector("#form");

addTask.addEventListener('click', () => {
    form.classList.remove("d-none");
    addTask.classList.add("d-none");
})

