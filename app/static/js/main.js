window.onload = () => {
    let followBtn = document.querySelector('#follow-btn');
    followBtn.addEventListener('click', () => {
        if(followBtn.classList.contains('btn-register')){
            followBtn.classList.remove('btn-register')
            followBtn.classList.add('btn-login')
            followBtn.textContent = 'Follow'
        } else{
            followBtn.classList.remove('btn-login')
            followBtn.classList.add('btn-register')
            followBtn.textContent = 'Following'
        }
        console.log('click')
    })
}