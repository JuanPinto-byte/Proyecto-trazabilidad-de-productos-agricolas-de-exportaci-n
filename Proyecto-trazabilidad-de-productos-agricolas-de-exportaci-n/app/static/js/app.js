function probarAPI() {
    fetch("http://127.0.0.1:5000/")
        .then(res => res.json())
        .then(data => {
            document.getElementById("resultado").textContent =
                JSON.stringify(data, null, 2);
        })
        .catch(err => console.log(err));
}