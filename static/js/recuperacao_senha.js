const loader = document.querySelector('.loader');
const submit = document.querySelector('.button-submit');

const senha1 = document.querySelector('#senha1');
const senha2 = document.querySelector('#senha2');

const spanSenha1 = document.querySelector('.senha1');
const spanSenha2 = document.querySelector('.senha2');

document.addEventListener('submit', e => {
    let validador = true;

    spanSenha1.innerHTML = ''
    spanSenha2.innerHTML = ''

    if(!senha1.value){
        e.preventDefault();
        spanSenha1.innerHTML = 'O campo acima não pode ficar vazio!';
        validador = false;
    }
    if(!senha2.value){
        e.preventDefault();
        spanSenha2.innerHTML = 'O campo acima não pode ficar vazio!';
        validador = false;
    }

    if(senha1.value != senha2.value && senha2.value && senha1.value){
        e.preventDefault();
        spanSenha1.innerHTML = 'As senhas precisam ser iguais!';
        validador = false;
    }

    if(senha1.value.length < 8 && senha2.value && senha1.value){
        e.preventDefault();
        spanSenha1.innerHTML = 'O campo senha não pode ter menos de 8 caracteres!';
        validador = false;
    }

    if(validador){
        loader.classList.add('desocultar');
        submit.classList.add('ocultar');
    }
})