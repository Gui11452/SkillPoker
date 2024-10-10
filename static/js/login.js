const loader = document.querySelector('.loader');
const submit = document.querySelector('.button-submit');

const senha = document.querySelector('#senha');
const email = document.querySelector('#email');

const spanSenha = document.querySelector('.senha');
const spanEmail = document.querySelector('.email');

document.addEventListener('submit', e => {
    let validador = true;

    spanSenha.innerHTML = ''
    spanEmail.innerHTML = ''

    if(!senha.value){
        e.preventDefault();
        spanSenha.innerHTML = 'O campo acima não pode ficar vazio!';
        validador = false;
    }
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