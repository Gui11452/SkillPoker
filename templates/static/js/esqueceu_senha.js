const loader = document.querySelector('.loader');
const submit = document.querySelector('.button-submit');

const email = document.querySelector('#email');

const spanEmail = document.querySelector('.email');

document.addEventListener('submit', e => {
    let validador = true;

    spanEmail.innerHTML = ''

    if(!email.value){
        e.preventDefault();
        spanEmail.innerHTML = 'O campo acima não pode ficar vazio!';
        validador = false;
    }

    if(validador){
        loader.classList.add('desocultar');
        submit.classList.add('ocultar');
    }
})