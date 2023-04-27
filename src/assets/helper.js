let getCsrfToken = (csrf_ref) => {
    fetch('/api/v1/csrf-token')
        .then((response) => response.json())
        .then((data) => {
            csrf_ref.value = data.csrf_token;
        })
}


let getUserId = (curr_ref) => {
    fetch('/api/v1/authenticated')
    .then((response) => response.json())
    .then((data) => {
        curr_ref.value = data.current_user_id;
    })
}

let getJWTToken = (jwt_ref) => {
    fetch('/api/v1/jwt-token')
    .then((response) => response.json())
    .then((data) => {
        jwt_ref.value = data.jwt_token;
    })
}