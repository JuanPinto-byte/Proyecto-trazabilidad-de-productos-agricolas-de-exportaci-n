function login() {
    const usuario = document.getElementById("usuario").value;
    const password = document.getElementById("password").value;

    fetch("http://127.0.0.1:5000/auth/login", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            username: usuario,
            password: password
        })
    })
    .then(res => res.json())
    .then(data => {
        if (data.access_token) {
            // guardar token
            localStorage.setItem("token", data.access_token);

            // redirigir
            window.location.href = "/";
        } else {
            document.getElementById("mensaje").textContent = "Credenciales incorrectas";
        }
    })
    .catch(err => console.log(err));
}